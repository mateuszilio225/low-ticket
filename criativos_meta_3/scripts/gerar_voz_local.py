"""Opcional: refaz os WAV com Kokoro local. O projeto já entrega WAV prontos."""
from pathlib import Path
import argparse,json

CUES={
'C3':[(.10,1.93,'Una actividad para disfrutar juntos.'),(2.10,4.90,'Así de fácil es empezar.'),(5.10,7.90,'Memoria, palabras y atención.'),(8.10,10.92,'Trescientas veinte actividades en ocho cuadernos.'),(11.10,14.80,'Conoce Momentos para Compartir. Descubre el kit digital.')],
'C4':[(.10,2.90,'A veces, lo más sencillo es compartir.'),(3.10,5.90,'Una idea para hoy: una comida querida.'),(6.10,8.90,'Elegid una hoja. Conversad y disfrutad.'),(9.10,11.90,'Con un calendario para elegir a vuestro ritmo.'),(12.10,14.85,'Descubre las trescientas veinte actividades en PDF.')],
'C5':[(.10,1.90,'¿Qué incluye este kit digital?'),(2.10,4.90,'Ocho cuadernos. Trescientas veinte actividades en PDF.'),(5.10,7.90,'Memoria, atención, lógica y palabras.'),(8.10,10.90,'Calendario de noventa días y solucionario.'),(11.10,14.85,'Consulta la oferta y descubre todo lo que incluye.')]
}
def main():
    import onnxruntime as rt
    import soundfile as sf
    from kokoro_onnx import Kokoro
    ap=argparse.ArgumentParser();ap.add_argument('--model-dir',type=Path,required=True);args=ap.parse_args()
    root=Path(__file__).resolve().parents[1];out=root/'assets/voz';out.mkdir(exist_ok=True)
    cfg=json.loads((root/'config/projeto.json').read_text(encoding='utf-8'))
    opts=rt.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
    session=rt.InferenceSession(str(args.model_dir/'kokoro-v1.0.onnx'),sess_options=opts,providers=['CPUExecutionProvider']);k=Kokoro.from_session(session,str(args.model_dir/'voices-v1.0.bin'))
    for key,cues in CUES.items():
        entries=[]
        for n,(start,end,words) in enumerate(cues):
            durations=cfg['criativos'][key]['duracoes'];last=len(durations)-1 if n==len(cues)-1 else n
            end_margin=.15 if n==len(cues)-1 else .1
            start=sum(durations[:n])+.1;end=sum(durations[:last+1])-end_margin
            speed={'C3':1.07,'C4':1.02,'C5':1.08}[key];samples,sr=k.create(words,voice='ef_dora',speed=speed,lang='es')
            available=end-start-.035;length=len(samples)/sr
            if length>available*1.18:
                samples,sr=k.create(words,voice='ef_dora',speed=min(1.45,speed*length/available),lang='es');length=len(samples)/sr
            name=f'{key}_{n}.wav';sf.write(out/name,samples,sr)
            entries.append(dict(inicio=start,fim=end,texto=words,arquivo=name,duracao_original=length,cena_inicial=n,cena_final=last,offset_inicio=.1,offset_fim=end_margin))
            print(key,n,round(length,3),words,flush=True)
        (out/f'{key}.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
