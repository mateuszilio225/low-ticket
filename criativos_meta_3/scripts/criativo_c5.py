from PIL import Image,ImageDraw
import math
from .comum import ease,W,H

def construir(ctx,scene):
    duration=ctx.cc['duracoes'][scene];header=ctx.header(scene);cover=ctx.cover((405,575))
    if scene==0:
        pages=[ctx.detail(c,(400,210)) for c in list(ctx.cfg['paginas']['C5'].values())[:2]]
        def frame(t):
            im=ctx.bg();u=ease(t/duration);ctx.paste(im,pages[0],(70-15*u,750));ctx.paste(im,pages[1],(580+15*u,920));ctx.paste(im,cover,(330,630-15*u));im.alpha_composite(header);return im
        return frame
    if scene==1:
        books=ctx.covers((185,262))
        def frame(t):
            im=ctx.bg()
            for i,page in enumerate(books):
                u=ease((t-i*.05)/.4);x=72+(i%4)*235;y=670+(i//4)*350+40*(1-u);ctx.paste(im,page,(x,y))
            im.alpha_composite(header);return im
        return frame
    if scene==2:
        pairs=list(ctx.cfg['paginas']['C5'].items());items=[ctx.detail(code,(850,340)) for label,code in pairs]
        def frame(t):
            im=ctx.bg();pair=0 if t<duration/2 else 2;u=(t%(duration/2))/(duration/2)
            for j in range(2):ctx.paste(im,items[pair+j],(95,610+j*390-10*ease(u)))
            im.alpha_composite(header);return im
        return frame
    if scene==3:
        docs=[ctx.card(ctx.image('calendario.png'),(470,665)),ctx.card(ctx.image('solucionario.png'),(850,700))]
        def frame(t):
            im=ctx.bg();idx=0 if t<duration/2 else 1;page=docs[idx];ctx.paste(im,page,((W-page.width)//2,630-10*ease((t%(duration/2))/(duration/2))));im.alpha_composite(header);return im
        return frame
    if scene==4:
        price=Image.new('RGBA',(W,H));p=ctx.cfg['produto']
        miniature=ctx.cover((240,340))
        if p['mostrar_preco']:
            ctx.text(price,p['preco_prefixo'],(90,645),size=57,bold=True)
            ctx.text(price,p['preco'],(90,750),size=132,bold=True)
            ctx.text(price,p['impostos'],(90,955),size=53,bold=True)
        else:ctx.text(price,'Consulta la oferta\nen el checkout',(90,740),size=72,bold=True)
        def frame(t):
            im=ctx.bg();ctx.paste(im,miniature,(655,345));im.alpha_composite(price);im.alpha_composite(header);return im
        return frame
    def frame(t):
        im=ctx.bg();ctx.paste(im,cover,(330,640-12*ease(t/duration)));ImageDraw.Draw(im).line((90,1420,940,1420),fill=ctx.gold,width=4);im.alpha_composite(header);return im
    return frame
