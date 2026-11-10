"""Controle de qualidade portátil dos três criativos.

Executar na raiz do projeto: python scripts/validar.py
Ou chamar validar_todos(root) ao final da renderização. Falhas são registradas
em output/qa/verificacao.json antes de gerar uma exceção e um exit code != 0.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VIDEOS = {
    "C3": "MOMENTOS_C3_DEMONSTRACAO_15S.mp4",
    "C4": "MOMENTOS_C4_FAMILIA_15S.mp4",
    "C5": "MOMENTOS_C5_OFERTA_15S.mp4",
}


def _read_config(root: Path) -> dict[str, Any]:
    path = root / "config" / "projeto.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _binary(name: str, config: dict[str, Any], root: Path) -> str:
    value = config.get(name) or config.get("tools", {}).get(name) or name
    if not isinstance(value, str):
        raise ValueError(f"config.{name} deve ser um nome de comando ou caminho.")
    located = shutil.which(value)
    if located:
        return located
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    if candidate.is_file():
        return str(candidate.resolve())
    raise FileNotFoundError(
        f"{name} não encontrado. Instale FFmpeg e reabra o terminal, "
        f"ou configure {name} em config/projeto.json."
    )


def _run(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Comando falhou (exit {result.returncode}): {Path(args[0]).name}\n"
            + stderr[-5000:]
        )
    return result


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _caption_font(root: Path) -> ImageFont.ImageFont:
    for name in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"):
        file = root / "assets" / "fonts" / name
        if file.is_file():
            return ImageFont.truetype(str(file), 20)
    try:
        return ImageFont.load_default(size=20)
    except TypeError:
        return ImageFont.load_default()


def _contact_sheet(video: Path, cid: str, qa: Path, ffmpeg: str, root: Path) -> Path:
    """Seleciona os quadros 15, 45, ..., 435: 0,5 a 14,5 s em 30 FPS."""
    destination = qa / f"{video.stem}_contato.jpg"
    with TemporaryDirectory(prefix=f"quadros-{cid}-", dir=str(qa)) as tmp:
        pattern = str(Path(tmp) / "frame-%02d.jpg")
        _run([
            ffmpeg, "-hide_banner", "-nostats", "-v", "error", "-y",
            "-i", str(video), "-map", "0:v:0", "-an",
            "-vf", "select='eq(mod(n,30),15)',scale=360:640",
            "-fps_mode", "passthrough", "-frames:v", "15", "-start_number", "0",
            "-q:v", "2", pattern,
        ])
        frames = [Path(tmp) / f"frame-{i:02}.jpg" for i in range(15)]
        if not all(frame.is_file() for frame in frames):
            raise RuntimeError(f"{cid}: não foram extraídos os 15 quadros atuais.")
        # A legenda fica fora da imagem: não encobre conteúdo a ser inspecionado.
        margin, fw, fh, caption, columns = 16, 360, 640, 36, 5
        sheet = Image.new(
            "RGB", (margin + columns * (fw + margin), margin + 3 * (fh + caption + margin)),
            "#E8EDF2",
        )
        draw = ImageDraw.Draw(sheet)
        caption_font = _caption_font(root)
        for i, file in enumerate(frames):
            x = margin + i % columns * (fw + margin)
            y = margin + i // columns * (fh + caption + margin)
            draw.text((x + 6, y + 3), f"{cid} | {i + 0.5:.1f} s", fill="#172F4D", font=caption_font)
            with Image.open(file) as image:
                if image.size != (fw, fh):
                    raise RuntimeError(f"Quadro de contato com tamanho inesperado: {image.size}")
                sheet.paste(image.convert("RGB"), (x, y + caption))
        sheet.save(destination, quality=93, subsampling=0)
    return destination


def _audio_stats(video: Path, ffmpeg: str) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    detected = _run([
        ffmpeg, "-hide_banner", "-nostats", "-v", "info", "-xerror",
        "-i", str(video), "-map", "0:a:0", "-vn", "-sn", "-dn",
        "-af", "volumedetect", "-f", "null", "-",
    ])
    log = detected.stderr.decode("utf-8", errors="replace")
    peak = re.search(r"max_volume:\s*(-?(?:\d+(?:\.\d+)?|inf))\s*dB", log)
    mean = re.search(r"mean_volume:\s*(-?(?:\d+(?:\.\d+)?|inf))\s*dB", log)
    if not peak or not mean:
        raise RuntimeError("FFmpeg não retornou as medições de volume esperadas.")
    peak_db = float(peak[1])
    mean_db = float(mean[1])
    if not math.isfinite(peak_db) or not math.isfinite(mean_db):
        errors.append("A faixa de áudio está silenciosa ou não possui amostras úteis.")
    elif peak_db >= -0.1:
        errors.append(f"Pico de áudio sem margem contra clipping: {peak_db:.2f} dBFS.")
    pcm = _run([
        ffmpeg, "-hide_banner", "-nostats", "-v", "error", "-xerror",
        "-i", str(video), "-map", "0:a:0", "-vn", "-sn", "-dn",
        "-ar", "16000", "-ac", "1", "-f", "f32le", "pipe:1",
    ]).stdout
    samples = np.frombuffer(pcm, dtype="<f4")
    if samples.size < 16000 or not np.isfinite(samples).all():
        errors.append("Áudio vazio, muito curto ou com amostras não finitas.")
    if samples.size:
        rms = float(np.sqrt(np.mean(np.square(samples.astype(np.float64)))))
        tail = samples[-800:]  # 50 ms: identifica término ainda muito energizado.
        before = samples[-4000:-800]
        tail_rms = float(np.sqrt(np.mean(np.square(tail.astype(np.float64)))))
        before_rms = float(np.sqrt(np.mean(np.square(before.astype(np.float64))))) if before.size else 0
        if rms < 1e-6:
            errors.append("Áudio detectado sem energia útil.")
        # Sinaliza uma provável interrupção brusca, não a presença normal de música.
        smooth_end = tail_rms <= max(0.008, before_rms * 0.45)
        if not smooth_end:
            errors.append(
                "Final de áudio ainda energizado: conferir e aplicar fade sem cortar a narração "
                f"(RMS últimos 50 ms={tail_rms:.5f}; anterior={before_rms:.5f})."
            )
    else:
        rms, tail_rms, before_rms, smooth_end = 0.0, 0.0, 0.0, False
    return {
        "pico_dBFS": peak_db if math.isfinite(peak_db) else None,
        "volume_medio_dBFS": mean_db if math.isfinite(mean_db) else None,
        "amostras_mono_16000_Hz": int(samples.size),
        "rms": rms, "rms_ultimos_50ms": tail_rms,
        "rms_200ms_anteriores": before_rms, "termino_suave_no_teste": smooth_end,
        "decodificacao_integral": "OK",
    }, errors


def validar_video(
    path: Path, cid: str, qa: Path, ffmpeg: str, ffprobe: str, root: Path,
) -> dict[str, Any]:
    result: dict[str, Any] = {"criativo": cid, "arquivo": path.name, "aprovado": False, "erros": [], "avisos": []}
    errors = result["erros"]
    if not path.is_file():
        errors.append(f"Arquivo ainda não existe: {path.name}")
        return result
    try:
        result.update(bytes=path.stat().st_size, sha256=_hash(path))
        probe = json.loads(_run([
            ffprobe, "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(path),
        ]).stdout)
        streams = probe.get("streams", [])
        video = next((s for s in streams if s.get("codec_type") == "video"), None)
        if video is None:
            raise RuntimeError("O arquivo não possui faixa de vídeo.")
        audio = [s for s in streams if s.get("codec_type") == "audio"]
        duration = float(probe.get("format", {}).get("duration", 0))
        fps = float(Fraction(video.get("r_frame_rate", "0/1")))
        average_fps = float(Fraction(video.get("avg_frame_rate", "0/1")))
        count = int(video.get("nb_read_frames", 0))
        result["video"] = {
            "duracao_s": duration, "largura": video.get("width"), "altura": video.get("height"),
            "fps": fps, "fps_medio": average_fps, "quadros_decodificados": count,
            "codec": video.get("codec_name"), "pixel_format": video.get("pix_fmt"),
        }
        if abs(duration - 15.0) > 0.02:
            errors.append(f"Duração {duration:.6f} s; esperado 15,000 s (tolerância 0,02 s).")
        if (video.get("width"), video.get("height")) != (1080, 1920):
            errors.append("Resolução diferente de 1080 × 1920.")
        if abs(fps - 30) > 0.001 or abs(average_fps - 30) > 0.001:
            errors.append(f"FPS inesperado: declarado {fps}, médio {average_fps}.")
        if count != 450:
            errors.append(f"Foram decodificados {count} quadros; esperado 450.")
        if video.get("codec_name") != "h264":
            errors.append("Codec de vídeo diferente de H.264.")
        decoded = _run([
            ffmpeg, "-hide_banner", "-nostats", "-v", "info", "-xerror",
            "-i", str(path), "-map", "0:v:0", "-an", "-sn", "-dn",
            "-vf", "blackdetect=d=0.02:pix_th=0.04:pic_th=0.98", "-f", "null", "-",
        ])
        log = decoded.stderr.decode("utf-8", errors="replace")
        blacks = [dict(inicio=float(m[0]), fim=float(m[1]), duracao=float(m[2])) for m in re.findall(
            r"black_start:([\d.]+)\s+black_end:([\d.]+)\s+black_duration:([\d.]+)", log,
        )]
        result["video"]["decodificacao_integral"] = "OK"
        result["video"]["intervalos_pretos_detectados"] = blacks
        if blacks or "black_start:" in log:
            errors.append("Quadro/intervalo preto indevido detectado pelo FFmpeg.")
        if audio:
            if any(s.get("codec_name") != "aac" for s in audio):
                errors.append("Há faixa de áudio com codec diferente de AAC.")
            for stream in audio:
                if int(stream.get("nb_read_frames", 0)) == 0:
                    errors.append("Uma faixa de áudio não possui quadros decodificados.")
            audio_info, audio_errors = _audio_stats(path, ffmpeg)
            audio_info.update(codec=audio[0].get("codec_name"), canais=audio[0].get("channels"), sample_rate=audio[0].get("sample_rate"))
            result["audio"] = audio_info
            errors.extend(audio_errors)
        else:
            result["audio"] = None
            result["avisos"].append("Vídeo sem áudio; a compreensão deve depender dos textos visuais.")
        contact = _contact_sheet(path, cid, qa, ffmpeg, root)
        result["folha_contato"] = str(contact.relative_to(root)).replace("\\", "/")
        result["contato_tempos_s"] = [i + 0.5 for i in range(15)]
    except (OSError, ValueError, RuntimeError, KeyError, ZeroDivisionError) as exc:
        errors.append(str(exc))
    result["aprovado"] = not errors
    return result


def _layout(root: Path) -> dict[str, Any]:
    path = root / "output" / "qa" / "layout.json"
    errors: list[str] = []
    seen: set[str] = set()
    if not path.is_file():
        return {"aprovado": False, "erros": ["Falta output/qa/layout.json produzido pela renderização."]}
    try:
        items = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(items, list) or not items:
            raise ValueError("layout.json deve conter uma lista não vazia de textos diagramados.")
        for i, item in enumerate(items):
            cid = item.get("criativo", "?")
            seen.add(cid)
            bounds = item.get("bbox", [])
            if len(bounds) != 4 or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in bounds):
                errors.append(f"Texto {i}/{cid}: caixa inválida.")
                continue
            x0, y0, x1, y1 = bounds
            if not (70 <= x0 < x1 <= 980 and 150 <= y0 < y1 <= 1600):
                errors.append(f"{cid}: texto fora da área segura {bounds}: {item.get('texto', '')!r}")
            if item.get("essencial") and (not isinstance(item.get("font_size"), (int, float)) or item["font_size"] < 42):
                errors.append(f"{cid}: texto essencial abaixo de 42 px: {item.get('texto', '')!r}")
        if not set(VIDEOS).issubset(seen):
            errors.append("O registro de layout não cobre os três criativos.")
    except (OSError, ValueError, TypeError) as exc:
        errors.append(str(exc))
    return {"aprovado": not errors, "arquivo": "output/qa/layout.json", "criativos": sorted(seen), "erros": errors}


def validar_todos(root: str | Path | None = None) -> dict[str, Any]:
    root = Path(root).resolve() if root is not None else ROOT
    qa = root / "output" / "qa"
    qa.mkdir(parents=True, exist_ok=True)
    config = _read_config(root)
    ffmpeg, ffprobe = _binary("ffmpeg", config, root), _binary("ffprobe", config, root)
    results = [validar_video(root / "output" / name, cid, qa, ffmpeg, ffprobe, root) for cid, name in VIDEOS.items()]
    layout = _layout(root)
    integrity_errors: list[str] = []
    hashes = [video["sha256"] for video in results if video.get("sha256")]
    if len(hashes) == 3 and len(set(hashes)) != 3:
        integrity_errors.append("Há arquivos MP4 idênticos: os três criativos devem ser independentes.")
    result = {
        "aprovado": all(v["aprovado"] for v in results) and layout["aprovado"] and not integrity_errors,
        "videos": results, "layout": layout,
        "integridade_entre_criativos": {"hashes_distintos": len(set(hashes)), "erros": integrity_errors},
        "metodo": "FFprobe, decodificação completa FFmpeg, blackdetect, volumedetect, PCM e contato de 15 quadros atuais por vídeo.",
        "limites": "Os testes automatizados não substituem a inspeção visual/escuta nem validam conversões, preço vigente ou configuração de uma campanha.",
    }
    (qa / "verificacao.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    for video in results:
        print(f"{video['criativo']}: {'OK' if video['aprovado'] else 'FALHOU'} — {video['arquivo']}")
        for error in video["erros"]:
            print("  " + error)
    for error in layout["erros"]:
        print("LAYOUT: " + error)
    for error in integrity_errors:
        print("INTEGRIDADE: " + error)
    if not result["aprovado"]:
        raise RuntimeError("Controle de qualidade reprovou. Consulte output/qa/verificacao.json antes de entregar.")
    print("QA automatizado aprovado. Contatos em output/qa/; a inspeção visual deve ser documentada separadamente.")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do projeto, sem depender do diretório atual.")
    arguments = parser.parse_args()
    validar_todos(arguments.root)
