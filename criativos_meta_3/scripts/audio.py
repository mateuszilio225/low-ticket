from pathlib import Path
import numpy as np
import subprocess,json,math,shutil

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
def criar_audio(root,cfg,key):
    root=Path(root);sr=48000;count=sr*15;voice=np.zeros(count,np.float32);music=np.zeros(count,np.float32);fx=np.zeros(count,np.float32)
    ff=shutil.which(cfg.get('ffmpeg','ffmpeg'))
    if not ff:raise RuntimeError('FFmpeg não encontrado. Consulte README.md.')
    ac=cfg['audio'];manifest=root/'assets/voz'/f'{key}.json';cues=[]
    if ac['usar_voz'] and manifest.exists():
        for item in json.loads(manifest.read_text(encoding='utf-8')):
            item=dict(item)
            if 'cena_inicial' in item:
                ds=cfg['criativos'][key]['duracoes']
                item['inicio']=sum(ds[:item['cena_inicial']])+item['offset_inicio']
                item['fim']=sum(ds[:item['cena_final']+1])-item['offset_fim']
            rate=max(.9,item['duracao_original']/(item['fim']-item['inicio']-.02))
            # A fala nunca é truncada para caber no corte.
            if rate>1.25:raise RuntimeError(f'Locução {key} longa demais: {item["texto"]}')
            pcm=subprocess.check_output([ff,'-v','error','-i',str(root/'assets/voz'/item['arquivo']),'-af',f'atempo={rate:.8f}','-ar',str(sr),'-ac','1','-f','f32le','pipe:1'])
            audio=np.frombuffer(pcm,np.float32).copy();start=round(item['inicio']*sr);end=start+len(audio)
            if end>count or end>round(item['fim']*sr)+200:raise RuntimeError('Locução ultrapassou o tempo reservado.')
            fade=min(220,len(audio)//4);audio[:fade]*=np.linspace(0,1,fade);audio[-fade:]*=np.linspace(1,0,fade);voice[start:end]+=audio
            cues.append(dict(inicio=item['inicio'],fim=end/sr,texto=item['texto']))
    voice/=max(1,float(np.max(np.abs(voice)))/.7)
    bpm={'C3':110,'C4':86,'C5':100}[key];period=60/bpm
    chords={'C3':[[261.63,329.63,392,523.25],[220,261.63,329.63,440]],'C4':[[174.61,220,261.63,329.63],[196,246.94,293.66,392]],'C5':[[196,246.94,293.66,392],[220,277.18,329.63,440]]}[key]
    for beat in range(math.ceil(15/period)):
        start=round(beat*period*sr);t=np.arange(int(.8*sr))/sr;f=chords[(beat//8)%2][beat%4]
        sustain=4.8 if key=='C4' else 8
        note=(np.sin(2*np.pi*f*t)+.14*np.sin(4*np.pi*f*t))*np.exp(-sustain*t)*(1-np.exp(-80*t))*ac['volume_musica']
        end=min(start+len(note),count);music[start:end]+=note[:end-start]
    # Efeito original de página/ênfase; nenhuma gravação ou música de terceiros.
    rng=np.random.default_rng({'C3':3,'C4':4,'C5':5}[key]);times=np.cumsum(cfg['criativos'][key]['duracoes'])[:-1]
    for at in times:
        start=round(at*sr);t=np.arange(int(.10*sr))/sr;noise=rng.normal(0,1,len(t));noise=np.convolve(noise,np.ones(9)/9,mode='same')
        sound=noise*np.sin(np.linspace(0,np.pi,len(t)))**2*ac['volume_efeitos'];fx[start:start+len(sound)]+=sound
    ramp=np.clip(np.arange(count)/sr/.25,0,1)*np.clip((15-np.arange(count)/sr)/.50,0,1);music*=ramp;fx*=ramp
    left=voice*ac['volume_voz']+music+fx;right=voice*ac['volume_voz']+music*.92+fx*.9
    mix=np.column_stack([left,right]).astype('<f4');dest=root/'output'/f'{key}_audio.wav'
    subprocess.run([ff,'-v','error','-y','-f','f32le','-ar',str(sr),'-ac','2','-i','pipe:0','-af',f'loudnorm=I={ac["lufs_alvo"]}:TP={ac["true_peak_alvo"]}:LRA=9','-ar',str(sr),str(dest)],input=mix.tobytes(),check=True)
    (root/'output'/f'{key}_legendas.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["inicio"])} --> {stamp(c["fim"])}\n{c["texto"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    return dest,cues
