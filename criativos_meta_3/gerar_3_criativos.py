"""Gera os três MP4 completos e valida os resultados em uma única execução."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,json,subprocess,shutil,importlib
from PIL import Image
from scripts.comum import ler_config,preparar_assets,Contexto,ease
from scripts.audio import criar_audio

ROOT=Path(__file__).resolve().parent
def renderizar(root,cfg,key,layout):
    ctx=Contexto(root,cfg,key,layout);mod=importlib.import_module('scripts.criativo_'+key.lower())
    durations=cfg['criativos'][key]['duracoes'];fps=cfg['visual']['fps'];w=cfg['visual']['width'];h=cfg['visual']['height']
    if sum(durations)!=15 or (w,h,fps)!=(1080,1920,30):raise ValueError('Cada configuração deve manter 15 segundos,1080×1920,30fps.')
    scenes=[mod.construir(ctx,i) for i in range(len(durations))];raw=root/'output'/f'.{key}_sem_audio.mp4';ff=shutil.which(cfg.get('ffmpeg','ffmpeg'))
    audio,cues=criar_audio(root,cfg,key)
    cmd=[ff,'-v','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset',cfg['visual']['preset'],'-crf',str(cfg['visual']['crf']),'-threads','2','-pix_fmt','yuv420p','-frames:v','450',str(raw)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE);previous=None
    try:
        for i,(fn,seconds) in enumerate(zip(scenes,durations)):
            n=round(seconds*fps);start=previous
            for frame in range(n):
                t=frame/fps;image=fn(t)
                if i>0 and t<.13:image=Image.blend(start.convert('RGBA'),image,ease(t/.13))
                rgb=image.convert('RGB');process.stdin.write(rgb.tobytes());previous=image
            print(key,'cena',i+1,'/',len(scenes),'renderizada',flush=True)
    finally:process.stdin.close()
    if process.wait()!=0:raise RuntimeError('Falha no FFmpeg durante '+key)
    output=root/'output'/cfg['criativos'][key]['arquivo']
    subprocess.run([ff,'-v','error','-y','-i',str(raw),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','15','-movflags','+faststart',str(output)],check=True);raw.unlink()
    (root/'output/qa'/f'{key}_voz.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return output

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--sem-voz',action='store_true');ap.add_argument('--somente',choices=['C3','C4','C5']);args=ap.parse_args()
    root=ROOT;cfg=ler_config(root)
    for name in ['ffmpeg','ffprobe']:
        if not shutil.which(cfg.get(name,name)):raise RuntimeError(f'{name} não encontrado. Instale FFmpeg conforme README.md e reabra o terminal.')
    if args.sem_voz:cfg['audio']['usar_voz']=False
    (root/'output/qa').mkdir(parents=True,exist_ok=True);preparar_assets(root,cfg)
    keys=[args.somente] if args.somente else ['C3','C4','C5'];layout=[]
    with ThreadPoolExecutor(max_workers=cfg['visual']['paralelismo']) as pool:
        results=list(pool.map(lambda key:renderizar(root,cfg,key,layout),keys))
    (root/'output/qa/layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Arquivos produzidos:',*[str(p) for p in results],sep='\n')
    if not args.somente:
        from scripts.validar import validar_todos
        validar_todos(root)
        print('Três vídeos efetivamente renderizados e aprovados nos testes executados.')
if __name__=='__main__':main()
