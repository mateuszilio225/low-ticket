from PIL import Image,ImageDraw
import math
from .comum import ease,W,H

def construir(ctx,scene):
    family=ctx.bg(True);duration=ctx.cc['duracoes'][scene];header=ctx.header(scene,family=scene==0,title_size=58 if scene==0 else 62)
    code=ctx.cfg['paginas']['C4']['conversa']
    if scene==0:
        def frame(t):
            im=ctx.zoom(family,1+.025*ease(t/duration));im.alpha_composite(header);return im
        return frame
    if scene==1:
        page=ctx.detail(code,(900,470));quote=Image.new('RGBA',(W,H))
        ctx.text(quote,'«Nombre una comida\nque le guste.»',(90,1130),size=55,bold=True)
        def frame(t):
            im=ctx.bg();ctx.paste(im,page,(70,650-14*ease(t/duration)));im.alpha_composite(quote);im.alpha_composite(header);return im
        return frame
    if scene==2:
        other=ctx.cfg['paginas']['C4']['alternativa'];small=[ctx.detail(c,(405,240)) for c in [code,other]];chosen=ctx.detail(code,(880,410))
        portrait=ctx.card(family.crop((20,430,W-20,1450)),(900,730))
        phases=[]
        for n,word in enumerate(['1. Elegid una hoja','2. Conversad','3. Compartid una idea']):
            layer=Image.new('RGBA',(W,H));ctx.text(layer,word,(90,1310 if n==1 else 1250),size=49,bold=True);phases.append(layer)
        def frame(t):
            k=min(2,int(t/(duration/3)));u=(t%(duration/3))/(duration/3);im=ctx.bg()
            if k==0:
                ctx.paste(im,small[0],(70,720-25*ease(u)));ctx.paste(im,small[1],(580,755))
                ImageDraw.Draw(im).line((100,1050,460,1050),fill=ctx.gold,width=7)
            elif k==1:
                ctx.paste(im,portrait,((W-portrait.width)//2,540))
            else:
                ctx.paste(im,chosen,(80,670));ctx.text(im,'Ejemplo de respuesta',(90,1080),size=30,bold=True,essential=False);ctx.text(im,'«Tortilla, con mi familia.»',(90,1140),size=49,bold=True)
            im.alpha_composite(phases[k]);im.alpha_composite(header);return im
        return frame
    if scene==3:
        full=ctx.card(ctx.image('calendario.png'),(340,485));detail=ctx.card(ctx.image('calendario_detalhe.png'),(880,300));box=ctx.meta['cal_box']
        def frame(t):
            im=ctx.bg();ctx.paste(im,full,(355,600));xy=(80,1130);ctx.paste(im,detail,xy)
            d=ImageDraw.Draw(im);x0=xy[0]+20+box[0]*(detail.width-40);y0=xy[1]+12+box[1]*(detail.height-40);x1=xy[0]+20+box[2]*(detail.width-40);y1=xy[1]+12+box[3]*(detail.height-40)
            if t>.5:d.rounded_rectangle((x0-5,y0-5,x1+5,y1+5),radius=6,outline=ctx.gold,width=5)
            im.alpha_composite(header);return im
        return frame
    cover=ctx.cover((380,540))
    portrait=ctx.card(family.crop((20,430,W-20,1450)),(420,490))
    extra=Image.new('RGBA',(W,H));ctx.text(extra,'PDF para consultar o imprimir',(90,1315),size=47,bold=True)
    def frame(t):
        im=ctx.bg();u=ease(t/duration);ctx.paste(im,portrait,(70,700-10*u));ctx.paste(im,cover,(560,640-12*u));im.alpha_composite(extra);im.alpha_composite(header);return im
    return frame
