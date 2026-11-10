from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np
import fitz,json,math,re,shutil

W,H=1080,1920
def ease(t):
    t=max(0,min(1,t));return t*t*(3-2*t)
def ler_config(root):
    return json.loads((Path(root)/'config/projeto.json').read_text(encoding='utf-8'))
def _perspectiva(im,quad,size):
    src=[(0,0),(im.width,0),(im.width,im.height),(0,im.height)];a=[];b=[]
    for (x,y),(u,v) in zip(quad,src):
        a.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);b.extend([u,v])
    coeff=np.linalg.solve(np.array(a),np.array(b))
    return im.convert('RGBA').transform(size,Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC)

def preparar_assets(root,cfg):
    root=Path(root);dest=root/'assets/pages';dest.mkdir(exist_ok=True)
    doc=fitz.open(root/cfg['recursos']['pdf']);mapping={}
    for i,p in enumerate(doc):
        m=re.search(r'\b(C[1-8]-\d{2})\s*/\s*Nivel',p.get_text())
        if m:mapping[m[1]]=i
    assert len(mapping)==320,'O PDF de entrada deve conter as 320 folhas reais.'
    codes=set(cfg['paginas']['C3']['variedade']+[cfg['paginas']['C3']['demonstracao'],cfg['paginas']['C4']['conversa'],cfg['paginas']['C4']['alternativa']]+list(cfg['paginas']['C5'].values()))
    for code in sorted(codes):
        p=doc[mapping[code]]
        for suffix,clip,scale in [('',None,1.4),('_prompt',fitz.Rect(45,110,550,315),2.2)]:
            p.get_pixmap(matrix=fitz.Matrix(scale,scale),clip=clip,alpha=False).save(dest/f'{code}{suffix}.png')
    demo=cfg['paginas']['C3'];p=doc[mapping[demo['demonstracao']]]
    words=demo['palavras'];boxes=[p.search_for(word)[-1] for word in words]
    # Close real das duas palavras, ampliado sem fabricar uma página.
    clip=fitz.Rect(min(b.x0 for b in boxes)-25,boxes[0].y0-16,max(b.x1 for b in boxes)+30,boxes[-1].y1+14)
    p.get_pixmap(matrix=fitz.Matrix(6,6),clip=clip,alpha=False).save(dest/'demonstracao.png')
    normboxes=[[(b.x0-clip.x0)/clip.width,(b.y0-clip.y0)/clip.height,(b.x1-clip.x0)/clip.width,(b.y1-clip.y0)/clip.height] for b in boxes]
    if words!=['LAGO','LADO']:raise ValueError('Confira a resposta e adapte a demonstração ao alterar as palavras de C3.')
    titles=[]
    for level,title,page in doc.get_toc():
        if level==1 and re.match(r'Cuaderno [1-8]:',title):titles.append((title,page-1))
    assert len(titles)==8
    for i,(_,n) in enumerate(titles,1):doc[n].get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False).save(dest/f'cuaderno-{i}.png')
    cal=next((i for l,t,i in doc.get_toc() if l==1 and 'calendario' in t.lower()),None)
    sol=next(i for l,t,i in doc.get_toc() if l==1 and t=='Solucionario')
    day=f'Día {cfg["paginas"]["C4"]["dia_calendario"]:02}'
    found=None
    for i in range(cal-1,len(doc)):
        hit=doc[i].search_for(day)
        if hit:found=(i,hit[0]);break
    assert found,'Dia do calendário não encontrado.'
    pi,rect=found;p=doc[pi];clip=fitz.Rect(42,max(60,rect.y0-18),550,min(p.rect.height-60,rect.y1+60))
    p.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(dest/'calendario.png')
    p.get_pixmap(matrix=fitz.Matrix(3,3),clip=clip,alpha=False).save(dest/'calendario_detalhe.png')
    code=cfg['paginas']['C4']['conversa'];hit=p.search_for(code);assert hit,'O dia escolhido deve conter a atividade de conversa.'
    target=next(x for x in hit if clip.intersects(x))
    calbox=[(target.x0-clip.x0)/clip.width,(target.y0-clip.y0)/clip.height,(target.x1-clip.x0)/clip.width,(target.y1-clip.y0)/clip.height]
    doc[sol-1].get_pixmap(matrix=fitz.Matrix(1.8,1.8),clip=fitz.Rect(40,65,555,490),alpha=False).save(dest/'solucionario.png')
    info={'paginas':mapping,'demo_boxes':normboxes,'cal_box':calbox,'capas':titles,'dia':day,'fontes_reais':sorted(codes)}
    (dest/'metadados.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    # Inserir uma folha autêntica na página branca da cena familiar.
    raw=Image.open(root/cfg['recursos']['familia']).convert('RGBA');scale=max(W/raw.width,H/raw.height);ox=(raw.width*scale-W)/2;oy=(raw.height*scale-H)/2
    photo=ImageOps.fit(raw,(W,H),Image.Resampling.LANCZOS)
    quad=[(x*raw.width*scale-ox,y*raw.height*scale-oy) for x,y in [(.314,.752),(.657,.747),(.804,.951),(.264,.956)]]
    paper=Image.open(dest/f'{code}.png');warped=_perspectiva(paper,quad,(W,H));photo.alpha_composite(warped)
    photo.convert('RGB').save(root/'assets/familia_com_pagina.png')
    doc.close();return info

class Contexto:
    def __init__(self,root,cfg,key,layout):
        self.root=Path(root);self.cfg=cfg;self.key=key;self.cc=cfg['criativos'][key];self.layout=layout;self._imgs={}
        self.v=cfg['visual'];self.navy=self.v['navy'];self.cream=self.v['cream'];self.gold=self.v['gold'];self.meta=json.loads((self.root/'assets/pages/metadados.json').read_text(encoding='utf-8'))
    def font(self,size,bold=False,serif=False):
        path=self.v['font_serif'] if serif else self.v['font_bold' if bold else 'font_regular'];return ImageFont.truetype(str(self.root/path),size)
    def image(self,name):
        path=name if str(name).startswith('assets/') else 'assets/pages/'+str(name)
        if path not in self._imgs:self._imgs[path]=Image.open(self.root/path).convert('RGBA')
        return self._imgs[path]
    def bg(self,family=False):return self.image('assets/familia_com_pagina.png').copy() if family else Image.new('RGBA',(W,H),self.cream)
    def text(self,im,s,xy,size=54,bold=False,color=None,width=850,essential=True,serif=False):
        d=ImageDraw.Draw(im);f=self.font(size,bold,serif);lines=[]
        for raw in s.split('\n'):
            line=''
            for word in raw.split():
                new=(line+' '+word).strip()
                if line and d.textlength(new,font=f)>width:lines.append(line);line=word
                else:line=new
            lines.append(line)
        value='\n'.join(lines);spacing=round(size*.22);box=d.multiline_textbbox(xy,value,font=f,spacing=spacing)
        x0,y0,x1,y1=box
        if not(70<=x0<x1<=980 and 150<=y0<y1<=1600):raise ValueError(f'{self.key}: texto fora da área segura: {value} {box}')
        if essential and size<42:raise ValueError('Texto essencial deve ter ao menos 42 px.')
        d.multiline_text(xy,value,font=f,spacing=spacing,fill=color or self.navy)
        self.layout.append({'criativo':self.key,'texto':value,'bbox':list(box),'essencial':essential,'font_size':size})
        return box
    def header(self,scene,title_size=62,family=False):
        layer=Image.new('RGBA',(W,H))
        if family:
            arr=np.zeros((H,W,4),np.uint8);arr[:,:,:3]=(252,250,244);arr[:,:,3]=np.clip(245*(1-np.arange(H)[:,None]/680),0,245).astype(np.uint8);layer.alpha_composite(Image.fromarray(arr))
        self.text(layer,self.cfg['produto']['nome'].upper(),(90,170),size=27,bold=True,essential=False)
        self.text(layer,self.cfg['produto']['formato'],(90,220),size=43,bold=True)
        title=self.cc['titulos'][scene]
        if title:self.text(layer,title,(90,315),size=title_size,bold=True)
        secondary=self.cc['secundarios'][scene]
        if secondary:self.text(layer,secondary,(90,1470),size=43,bold=True)
        return layer
    def overlay(self,base,over):
        base.alpha_composite(over);return base
    def card(self,img,size,angle=0):
        image=ImageOps.contain(img.copy(),size,Image.Resampling.LANCZOS)
        card=Image.new('RGBA',(image.width+40,image.height+40));shadow=Image.new('RGBA',card.size)
        ImageDraw.Draw(shadow).rounded_rectangle((12,17,12+image.width,17+image.height),radius=9,fill=(23,47,77,50));card.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(9)));card.alpha_composite(image,(20,12))
        return card.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True) if angle else card
    def paste(self,bg,im,xy):bg.alpha_composite(im,(round(xy[0]),round(xy[1])))
    def zoom(self,im,amount):
        grown=im.resize((round(im.width*amount),round(im.height*amount)),Image.Resampling.BICUBIC)
        x=(grown.width-W)//2;y=(grown.height-H)//2
        return grown.crop((x,y,x+W,y+H))
    def covers(self,size=(200,282)):
        return [self.card(self.image(f'cuaderno-{i}.png'),size) for i in range(1,9)]
    def cover(self,size=(420,600)):return self.card(self.image(self.cfg['recursos']['capa']),size)
    def detail(self,code,size=(880,470)):return self.card(self.image(code+'_prompt.png'),size)
    def label(self,im,s,xy,size=48,color=None):return self.text(im,s,xy,size=size,bold=True,color=color)
