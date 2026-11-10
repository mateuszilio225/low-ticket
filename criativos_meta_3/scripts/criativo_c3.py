from PIL import Image,ImageDraw
import math
from .comum import ease,W,H

def construir(ctx,scene):
    header=ctx.header(scene);duration=ctx.cc['duracoes'][scene]
    if scene in [0,1]:
        detail=ctx.image('demonstracao.png');detail=detail.resize((650,round(650*detail.height/detail.width)),Image.Resampling.LANCZOS)
        panel=ctx.card(detail,(650,700));base=ctx.bg();xy=(195,660)
        boxes=ctx.meta['demo_boxes']
        solution=Image.new('RGBA',(W,H));ctx.text(solution,'LAGO → LADO',(90,1360),size=60,bold=True)
        def frame(t):
            im=base.copy();shift=10*(1-ease(t/duration))
            if scene==0:
                scale=1+.035*ease(t/duration);grown=panel.resize((round(panel.width*scale),round(panel.height*scale)),Image.Resampling.BICUBIC)
                ctx.paste(im,grown,(xy[0]-(grown.width-panel.width)/2,xy[1]+shift-(grown.height-panel.height)/2))
            else:ctx.paste(im,panel,(xy[0],xy[1]+shift))
            if scene==1:
                d=ImageDraw.Draw(im);progress=ease((t-.25)/1.2)
                for b in boxes:
                    x0=xy[0]+20+b[0]*detail.width;y=xy[1]+12+b[3]*detail.height+shift+10;x1=xy[0]+20+b[2]*detail.width
                    d.line((x0,y,x0+(x1-x0)*progress,y),fill=ctx.gold,width=9)
                if t>.9:
                    fade=solution.copy();fade.putalpha(fade.getchannel('A').point(lambda a:round(a*ease((t-.9)/.3))));im.alpha_composite(fade)
            im.alpha_composite(header);return im
        return frame
    if scene==2:
        cards=[ctx.detail(code,(880,400)) for code in ctx.cfg['paginas']['C3']['variedade']]
        captions=[]
        for word in ['Una canción','Tres ejemplos de frutas']:
            lay=Image.new('RGBA',(W,H));ctx.text(lay,word,(90,1240),size=52,bold=True);captions.append(lay)
        def frame(t):
            idx=0 if t<duration/2 else 1;u=(t%(duration/2))/(duration/2);im=ctx.bg();ctx.paste(im,cards[idx],(80,720-18*ease(u)));im.alpha_composite(captions[idx]);im.alpha_composite(header);return im
        return frame
    if scene==3:
        cover=ctx.cover((390,555));pages=ctx.covers((195,275))
        def frame(t):
            im=ctx.bg();u=ease(t/duration)
            for i,page in enumerate(pages):
                x=90+i*105;y=710+abs(i-3.5)*35+14*(1-u);ctx.paste(im,page,(x,y))
            ctx.paste(im,cover,(325,835-12*u));im.alpha_composite(header);return im
        return frame
    cover=ctx.cover((470,665));label=Image.new('RGBA',(W,H));ctx.text(label,'PDF · 8 cuadernos',(90,1305),size=48,bold=True)
    def frame(t):
        im=ctx.bg();ctx.paste(im,cover,(285,590-12*ease(t/duration)));ImageDraw.Draw(im).line((90,1410,940,1410),fill=ctx.gold,width=4);im.alpha_composite(label);im.alpha_composite(header);return im
    return frame
