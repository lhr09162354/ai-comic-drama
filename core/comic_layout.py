"""漫画排版引擎 v6 - 面板特效、打印模式、分享卡片"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont
import config

def _get_font(size=20):
    if config.FONT_PATH and os.path.exists(config.FONT_PATH):
        return ImageFont.truetype(config.FONT_PATH, size)
    for p in [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\simhei.ttf",
    ]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    try: return ImageFont.truetype("DejaVuSans.ttf", size)
    except: return ImageFont.load_default()

# ============ 角色配色 ============
CHARACTER_COLORS = ["#4A90D9","#E74C3C","#2ECC71","#F39C12","#9B59B6","#1ABC9C","#E91E63","#795548"]

def get_character_color_map(characters):
    return { (c["name"] if isinstance(c, dict) else c): CHARACTER_COLORS[i % len(CHARACTER_COLORS)]
             for i, c in enumerate(characters) }

# ============ 气泡样式 ============
BUBBLE_STYLES = {"normal":"普通","thought":"思考","shout":"呐喊","whisper":"耳语","burst":"爆发"}

def _detect_bubble_style(text, speaker):
    if speaker in ("旁白","narrator","narration"): return "narration"
    if text.count("！")>=2 or text.count("!")>=2: return "shout"
    if "……" in text or "..." in text or "？" in text: return "thought"
    if "（" in text or "（" in text or "悄悄" in text or "低声" in text: return "whisper"
    return "normal"

# ============ 布局模板 ============
LAYOUT_TEMPLATES = {
    "auto":"自动适配","2-row":"上下两格","2-col":"左右两格",
    "3-top1-bot2":"上大下两小","3-left1-right2":"左大右两小",
    "2x2":"田字格(4格)","3-top2-bot1":"上两小下大",
    "5-comic":"漫画经典5格","3x2":"6格网格","8-action":"动作场景8格",
}

def _cl(n,pw,ph,m,g):
    if n<=2:return _cl2r(n,pw,ph,m,g)
    elif n==3:return _cl3t1b2(n,pw,ph,m,g)
    elif n==4:return _cl2x2(n,pw,ph,m,g)
    elif n==5:return _cl5c(n,pw,ph,m,g)
    else:return _cl3x2(min(n,6),pw,ph,m,g)
def _cl2r(n,pw,ph,m,g):
    uw,uh=pw-2*m,ph-2*m;h=(uh-g)//2;return[(m,m,uw,h),(m,m+h+g,uw,h)][:n]
def _cl2c(n,pw,ph,m,g):
    uw,uh=pw-2*m,ph-2*m;w=(uw-g)//2;return[(m,m,w,uh),(m+w+g,m,uw-w-g,uh)][:n]
def _cl3t1b2(n,pw,ph,m,g):
    uw,uh=pw-2*m,ph-2*m;th=int(uh*.55);bh=uh-th-g;hw=(uw-g)//2
    return[(m,m,uw,th),(m,m+th+g,hw,bh),(m+hw+g,m+th+g,uw-hw-g,bh)][:n]
def _cl3l1r2(n,pw,ph,m,g):
    uw,uh=pw-2*m,ph-2*m;lw=int(uw*.55);rw=uw-lw-g;hh=(uh-g)//2
    return[(m,m,lw,uh),(m+lw+g,m,rw,hh),(m+lw+g,m+hh+g,rw,uh-hh-g)][:n]
def _cl2x2(n,pw,ph,m,g):
    uw,uh=pw-2*m,ph-2*m;hw,hh=(uw-g)//2,(uh-g)//2
    return[(m,m,hw,hh),(m+hw+g,m,uw-hw-g,hh),(m,m+hh+g,hw,uh-hh-g),(m+hw+g,m+hh+g,uw-hw-g,uh-hh-g)][:n]
def _cl3t2b1(n,pw,ph,m,g):
    uw,uh=pw-2*m,ph-2*m;th=int(uh*.45);bh=uh-th-g;hw=(uw-g)//2
    return[(m,m,hw,th),(m+hw+g,m,uw-hw-g,th),(m,m+th+g,uw,bh)][:n]
def _cl5c(n,pw,ph,m,g):
    uw,uh=pw-2*m,ph-2*m;th=int(uh*.5);bh=uh-th-g;tw=(uw-2*g)//3;hw=(uw-g)//2
    return[(m,m,tw,th),(m+tw+g,m,tw,th),(m+2*(tw+g),m,uw-2*(tw+g),th),(m,m+th+g,hw,bh),(m+hw+g,m+th+g,uw-hw-g,bh)][:n]
def _cl3x2(n,pw,ph,m,g):
    uw,uh=pw-2*m,ph-2*m;tw=(uw-2*g)//3;hh=(uh-g)//2;ls=[]
    for r in range(2):
        for c in range(3):
            x=m+c*(tw+g);y=m+r*(hh+g);w=tw if c<2 else uw-2*(tw+g);h=hh if r<1 else uh-hh-g;ls.append((x,y,w,h))
    return ls[:n]
_LC={"auto":_cl,"2-row":_cl2r,"2-col":_cl2c,"3-top1-bot2":_cl3t1b2,"3-left1-right2":_cl3l1r2,"2x2":_cl2x2,"3-top2-bot1":_cl3t2b1,"5-comic":_cl5c,"3x2":_cl3x2,"8-action":_cl3x2}

def _calc_layout(panels,pw,ph,m,g,tmpl="auto"):
    return _LC.get(tmpl,_cl)(len(panels),pw,ph,m,g)

# ============ 绘图工具 ============
def _wrap_text(text,font,mw):
    ls,cur=[],""
    for ch in text:
        t=cur+ch
        try:w=font.getbbox(t)[2]-font.getbbox(t)[0]
        except:w=len(t)*font.size
        if w>mw and cur:ls.append(cur);cur=ch
        else:cur=t
    if cur:ls.append(cur)
    return ls or [text]

def _fit_image(img,tw,th):
    tr,ir=tw/th,img.width/img.height
    if ir>tr:nw=int(img.height*tr);l=(img.width-nw)//2;img=img.crop((l,0,l+nw,img.height))
    else:nh=int(img.width/tr);t=(img.height-nh)//2;img=img.crop((0,t,img.width,t+nh))
    return img.resize((tw,th),Image.LANCZOS)

def _draw_bubble(draw,x,y,text,font,max_width,style="normal",border_color="#222222",fill_color="white"):
    lines=_wrap_text(text,font,max_width-24);lh=font.size+6;th=len(lines)*lh;pad=12
    bw=min(max_width,max(font.size*max(len(l) for l in lines)+pad*2,60));bh=th+pad*2
    
    if style=="narration":
        draw.rectangle([x,y,x+bw,y+bh],fill="#FFFDE7",outline=border_color,width=2)
        for i,l in enumerate(lines):draw.text((x+pad,y+pad+i*lh),l,font=font,fill="#333333")
    elif style=="thought":
        draw.ellipse([x+4,y+4,x+bw-4,y+bh-4],fill=fill_color,outline=border_color,width=2)
        draw.ellipse([x+8,y+bh+2,x+18,y+bh+10],fill=fill_color,outline=border_color,width=1)
        draw.ellipse([x+2,y+bh+8,x+8,y+bh+14],fill=fill_color,outline=border_color,width=1)
        for i,l in enumerate(lines):draw.text((x+pad,y+pad+i*lh),l,font=font,fill="#555555")
    elif style=="shout":
        cx2,cy2=x+bw//2,y+bh//2;pts=[]
        for i in range(32):
            a=math.pi*2*i/32;r=max(bw,bh)//2+(8 if i%2==0 else -4)
            pts.append((cx2+r*math.cos(a),cy2+r*math.sin(a)))
        draw.polygon(pts,fill=fill_color,outline=border_color)
        for i,l in enumerate(lines):draw.text((x+pad,y+pad+i*lh),l,font=font,fill="#CC0000")
    elif style=="whisper":
        draw.rectangle([x,y,x+bw,y+bh],fill="#F8F8F8")
        dl=5
        for ex in range(x,x+bw,dl*2):
            draw.line([(ex,y),(min(ex+dl,x+bw),y)],fill=border_color,width=1)
            draw.line([(ex,y+bh),(min(ex+dl,x+bw),y+bh)],fill=border_color,width=1)
        for ey in range(y,y+bh,dl*2):
            draw.line([(x,ey),(x,min(ey+dl,y+bh))],fill=border_color,width=1)
            draw.line([(x+bw,ey),(x+bw,min(ey+dl,y+bh))],fill=border_color,width=1)
        for i,l in enumerate(lines):draw.text((x+pad,y+pad+i*lh),l,font=font,fill="#777777")
    elif style=="burst":
        cx2,cy2=x+bw//2,y+bh//2;pts=[]
        for i in range(24):
            a=math.pi*2*i/24-math.pi/2;r=max(bw,bh)//2+(15 if i%2==0 else -10)
            pts.append((cx2+r*math.cos(a),cy2+r*math.sin(a)))
        draw.polygon(pts,fill="#FFFF00",outline=border_color)
        for i,l in enumerate(lines):draw.text((x+pad,y+pad+i*lh),l,font=font,fill="#CC0000")
    else:
        draw.rounded_rectangle([x,y,x+bw,y+bh],radius=12,fill=fill_color,outline=border_color,width=2)
        tx,ty=x+bw//2-6,y+bh;draw.polygon([(tx,ty),(tx+12,ty),(tx+6,ty+10)],fill=fill_color,outline=border_color)
        for i,l in enumerate(lines):draw.text((x+pad,y+pad+i*lh),l,font=font,fill="#111111")
    return bh+10

def _draw_sound_effect(draw,x,y,text,font):
    bf=_get_font(font.size+10);draw.text((x,y),text,font=bf,fill="#FF1744",stroke_width=2,stroke_fill="#FFFFFF")

# ============ 面板特效 ============
PANEL_EFFECTS = {"none":"无特效","speed_lines":"速度线","impact_lines":"冲击线","focus_lines":"集中线","speed_horizontal":"横向速度线"}

def add_speed_lines(img,direction="radial",intensity=15,line_color=(0,0,0),alpha=80):
    w,h=img.size;overlay=Image.new("RGBA",(w,h),(0,0,0,0));draw=ImageDraw.Draw(overlay)
    cx,cy=w//2,h//2;rng=random.Random(42)
    if direction=="radial":
        for _ in range(intensity*3):
            a=rng.uniform(0,2*math.pi);r1=rng.uniform(max(w,h)*.15,max(w,h)*.35);r2=rng.uniform(max(w,h)*.5,max(w,h)*.8)
            draw.line([(int(cx+r1*math.cos(a)),int(cy+r1*math.sin(a))),(int(cx+r2*math.cos(a)),int(cy+r2*math.sin(a)))],
                      fill=(*line_color,rng.randint(30,alpha)),width=rng.randint(1,3))
    elif direction=="horizontal":
        for _ in range(intensity*2):
            yp=rng.randint(0,h);x1=rng.randint(0,w//4);x2=rng.randint(w*3//4,w)
            draw.line([(x1,yp),(x2,yp)],fill=(*line_color,rng.randint(20,alpha)),width=rng.choice([1,1,2]))
    elif direction=="impact":
        fx,fy=rng.randint(w//3,2*w//3),rng.randint(h//3,2*h//3)
        for _ in range(intensity*4):
            a=rng.uniform(0,2*math.pi);r1=rng.uniform(10,40);r2=rng.uniform(max(w,h)*.4,max(w,h)*.9)
            draw.line([(int(fx+r1*math.cos(a)),int(fy+r1*math.sin(a))),(int(fx+r2*math.cos(a)),int(fy+r2*math.sin(a)))],
                      fill=(*line_color,rng.randint(40,alpha)),width=rng.choice([1,2,2,3]))
    elif direction=="focus":
        for _ in range(intensity*3):
            a=rng.uniform(0,2*math.pi);r1=rng.uniform(max(w,h)*.55,max(w,h)*.85);r2=max(w,h)*.2
            draw.line([(int(cx+r1*math.cos(a)),int(cy+r1*math.sin(a))),(int(cx+r2*math.cos(a)),int(cy+r2*math.sin(a)))],
                      fill=(*line_color,rng.randint(30,alpha)),width=rng.randint(1,2))
    return Image.alpha_composite(img.convert("RGBA"),overlay).convert("RGB")

def auto_detect_effect(emotion):
    return {"紧张":("radial",12),"愤怒":("impact",18),"惊讶":("focus",10),
            "搞笑":("impact",8),"热血":("radial",15),"恐惧":("focus",12)}.get(emotion,("none",0))

# ============ 水印 ============
def add_watermark(page,text="AI漫剧",position="bottom_right",opacity=60):
    if not text:return page
    w,h=page.size;overlay=Image.new("RGBA",(w,h),(0,0,0,0));draw=ImageDraw.Draw(overlay)
    font=_get_font(16)
    pos={"bottom_right":(w-20,h-20),"bottom_left":(20,h-20),"top_right":(w-20,20),"top_left":(20,20),"center":(w//2,h//2)}
    anc={"bottom_right":"rb","bottom_left":"lb","top_right":"rt","top_left":"lt","center":"mm"}
    p=pos.get(position,pos["bottom_right"]);a=anc.get(position,"rb")
    draw.text(p,text,font=font,fill=(180,180,180,opacity),anchor=a)
    return Image.alpha_composite(page.convert("RGBA"),overlay).convert("RGB")

# ============ 封面 ============
COVER_TEMPLATES={"classic":"经典漫画风","minimal":"极简风","magazine":"杂志风"}

def compose_cover(title,synopsis="",cover_image_path=None,style_key="manga",genre="热血冒险",cover_template="classic"):
    pw,ph=config.PAGE_WIDTH,config.PAGE_HEIGHT
    if cover_template=="minimal":return _cover_minimal(pw,ph,title,synopsis,genre)
    elif cover_template=="magazine":return _cover_magazine(pw,ph,title,synopsis,genre,cover_image_path)
    else:return _cover_classic(pw,ph,title,synopsis,genre,cover_image_path)

def _cover_classic(pw,ph,title,synopsis,genre,cp=None):
    c=Image.new("RGB",(pw,ph),"black");d=ImageDraw.Draw(c)
    if cp and os.path.exists(cp):i=Image.open(cp);i=_fit_image(i,pw,ph);c.paste(i,(0,0));o=Image.new("RGBA",(pw,ph),(0,0,0,130));c=Image.alpha_composite(c.convert("RGBA"),o).convert("RGB");d=ImageDraw.Draw(c)
    else:
        for y in range(ph):r=int(20+30*(y/ph));g=int(10+15*(y/ph));b=int(40+60*(y/ph));d.line([(0,y),(pw,y)],fill=(r,g,b))
    tf=_get_font(min(64,max(32,pw//15)));d.text((pw//2+3,ph//3+3),title,font=tf,fill="#000000",anchor="mm");d.text((pw//2,ph//3),title,font=tf,fill="#FFFFFF",anchor="mm")
    if synopsis:
        sf=_get_font(20)
        for i,l in enumerate(_wrap_text(synopsis,sf,pw-100)[:3]):d.text((pw//2,ph//3+60+i*28),l,font=sf,fill="#CCCCCC",anchor="mm")
    d.text((pw//2,ph-30),f"AI漫剧 | {genre}",font=_get_font(14),fill="#888888",anchor="mm");return c

def _cover_minimal(pw,ph,title,synopsis,genre):
    c=Image.new("RGB",(pw,ph),"#FAFAFA");d=ImageDraw.Draw(c)
    d.line([(pw//2-100,ph//3-40),(pw//2+100,ph//3-40)],fill="#333333",width=2)
    d.text((pw//2,ph//3),title,font=_get_font(min(48,max(28,pw//18))),fill="#1a1a1a",anchor="mm")
    d.line([(pw//2-60,ph//3+35),(pw//2+60,ph//3+35)],fill="#CCCCCC",width=1)
    if synopsis:
        for i,l in enumerate(_wrap_text(synopsis,_get_font(16),pw-200)[:2]):d.text((pw//2,ph//3+60+i*24),l,font=_get_font(16),fill="#888888",anchor="mm")
    d.text((pw//2,ph-40),f"AI漫剧 | {genre}",font=_get_font(12),fill="#BBBBBB",anchor="mm");return c

def _cover_magazine(pw,ph,title,synopsis,genre,cp=None):
    c=Image.new("RGB",(pw,ph),"#111111");d=ImageDraw.Draw(c)
    if cp and os.path.exists(cp):i=Image.open(cp);i=_fit_image(i,pw,int(ph*.7));c.paste(i,(0,0))
    else:
        colors={"热血冒险":"#E74C3C","恋爱日常":"#E91E63","悬疑推理":"#34495E","奇幻魔法":"#8E44AD","科幻未来":"#2980B9","恐怖惊悚":"#1C1C1C","搞笑日常":"#F39C12","古风仙侠":"#D35400"}
        for y in range(int(ph*.7)):d.line([(0,y),(pw,y)],fill=colors.get(genre,"#E74C3C"))
    for y in range(int(ph*.7),ph):f=(y-ph*.7)/(ph*.3);g=int(30-20*f);d.line([(0,y),(pw,y)],fill=(g,g,g))
    d.rectangle([20,20,20+len(genre)*18+10,42],fill="#FF4444");d.text((25,20),genre,font=_get_font(16),fill="white")
    for dx in range(4):d.text((pw//2+dx,int(ph*.78)+dx),title,font=_get_font(min(56,max(30,pw//16))),fill="#000000",anchor="mm")
    d.text((pw//2,int(ph*.78)),title,font=_get_font(min(56,max(30,pw//16))),fill="#FFFFFF",anchor="mm")
    if synopsis:
        for i,l in enumerate(_wrap_text(synopsis,_get_font(14),pw-120)[:2]):d.text((pw//2,int(ph*.86)+i*20),l,font=_get_font(14),fill="#AAAAAA",anchor="mm")
    d.rectangle([0,ph-35,pw,ph],fill="#FF4444");d.text((pw//2,ph-18),"AI COMIC GENERATOR",font=_get_font(12),fill="white",anchor="mm");return c

# ============ 章节页 ============
def compose_chapter_page(chapter_title,chapter_subtitle="",chapter_number=1,style_key="manga"):
    pw,ph=config.PAGE_WIDTH,config.PAGE_HEIGHT;page=Image.new("RGB",(pw,ph),"#1a1a2e");draw=ImageDraw.Draw(page)
    draw.text((pw//2,ph//3),f"{chapter_number:02d}",font=_get_font(80),fill="#FFFFFF33",anchor="mm")
    draw.line([(pw//2-150,ph//2-30),(pw//2+150,ph//2-30)],fill="#FFFFFF44",width=1)
    draw.text((pw//2,ph//2),chapter_title,font=_get_font(40),fill="white",anchor="mm")
    if chapter_subtitle:draw.text((pw//2,ph//2+50),chapter_subtitle,font=_get_font(18),fill="#FFFFFFAA",anchor="mm")
    draw.line([(pw//2-100,ph//2+80),(pw//2+100,ph//2+80)],fill="#FFFFFF44",width=1);return page

# ============ 打印就绪 ============
def compose_print_page(page_img,dpi=300,bleed_mm=3,crop_marks=True):
    bleed_px=int(bleed_mm*dpi/25.4);scale=dpi/72
    nw,nh=int(page_img.width*scale),int(page_img.height*scale)
    page_hires=page_img.resize((nw,nh),Image.LANCZOS)
    tw,th=nw+2*bleed_px,nh+2*bleed_px
    pp=Image.new("RGB",(tw,th),"white");pp.paste(page_hires,(bleed_px,bleed_px))
    if crop_marks:
        d=ImageDraw.Draw(pp);ml=int(15*scale);mo=int(5*scale);lw=max(1,int(scale))
        corners=[
            [(mo,bleed_px-mo),(mo+ml,bleed_px-mo)],[(bleed_px-mo,mo),(bleed_px-mo,mo+ml)],
            [(tw-mo-ml,bleed_px-mo),(tw-mo,bleed_px-mo)],[(tw-bleed_px+mo,mo),(tw-bleed_px+mo,mo+ml)],
            [(mo,th-bleed_px+mo),(mo+ml,th-bleed_px+mo)],[(bleed_px-mo,th-mo-ml),(bleed_px-mo,th-mo)],
            [(tw-mo-ml,th-bleed_px+mo),(tw-mo,th-bleed_px+mo)],[(tw-bleed_px+mo,th-mo-ml),(tw-bleed_px+mo,th-mo)],
        ]
        mid=[
            [(tw//2-ml//2,bleed_px-mo),(tw//2+ml//2,bleed_px-mo)],
            [(tw//2-ml//2,th-bleed_px+mo),(tw//2+ml//2,th-bleed_px+mo)],
            [(bleed_px-mo,th//2-ml//2),(bleed_px-mo,th//2+ml//2)],
            [(tw-bleed_px+mo,th//2-ml//2),(tw-bleed_px+mo,th//2+ml//2)],
        ]
        for l in corners+mid:d.line(l,fill="black",width=lw)
    return pp

# ============ 社交分享卡片 ============
def compose_share_card(page_img,title,genre="",style_key="manga"):
    cw,ch=800,1000;card=Image.new("RGB",(cw,ch),"#1a1a2e");draw=ImageDraw.Draw(card)
    draw.rectangle([0,0,cw,8],fill="#FF6B6B")
    preview=page_img.resize((cw-40,600),Image.LANCZOS);card.paste(preview,(20,60))
    draw.text((cw//2,700),title,font=_get_font(32),fill="white",anchor="mm")
    if genre:
        tf=_get_font(16);tw=tf.getbbox(genre)[2]-tf.getbbox(genre)[0]+16
        draw.rounded_rectangle([cw//2-tw//2,730,cw//2+tw//2,756],radius=8,fill="#FF6B6B")
        draw.text((cw//2,743),genre,font=tf,fill="white",anchor="mm")
    draw.text((cw//2,920),"AI漫剧自动生成器",font=_get_font(14),fill="#888888",anchor="mm")
    draw.text((cw//2,945),"🎭 创意 → 剧本 → 画面 → 漫画",font=_get_font(14),fill="#666666",anchor="mm")
    draw.rectangle([0,ch-8,cw,ch],fill="#FF6B6B");return card

# ============ 内容页 ============
def compose_page(panels_data,page_width=None,page_height=None,layout_template="auto",
                 page_number=None,title="",show_page_number=True,character_colors=None,
                 watermark_text="",watermark_position="bottom_right",auto_bubble_style=True,
                 panel_effect="auto"):
    pw=page_width or config.PAGE_WIDTH;ph=page_height or config.PAGE_HEIGHT
    margin=config.MARGIN;gap=config.PANEL_GAP
    page=Image.new("RGB",(pw,ph),"white");draw=ImageDraw.Draw(page)
    if title:draw.text((pw//2,10),title,font=_get_font(12),fill="#999999",anchor="mt")
    if show_page_number and page_number is not None:draw.text((pw//2,ph-15),f"- {page_number} -",font=_get_font(12),fill="#999999",anchor="mm")
    top_off=25 if title else margin;bot_off=ph-20 if show_page_number and page_number else ph-margin
    layouts=_calc_layout(panels_data,pw,bot_off-top_off,margin,gap,layout_template)
    layouts=[(x,y+top_off,w,h) for x,y,w,h in layouts]
    font=_get_font(18);small_font=_get_font(14);name_font=_get_font(12)
    
    for i,panel in enumerate(panels_data):
        if i>=len(layouts):break
        x,y,w,h=layouts[i]
        draw.rectangle([x,y,x+w,y+h],fill="#F5F5F5",outline="black",width=config.BORDER_WIDTH)
        if panel.get("image_path") and os.path.exists(panel["image_path"]):
            img=Image.open(panel["image_path"]);img=_fit_image(img,w-2,h-2);page.paste(img,(x+1,y+1))
        else:
            desc=panel.get("scene_description","画面生成中...")
            for j,line in enumerate(_wrap_text(desc,small_font,w-20)[:6]):draw.text((x+10,y+10+j*22),line,font=small_font,fill="#666666")
        by=y+10
        for dialogue in panel.get("dialogues",[]):
            speaker=dialogue.get("speaker","");text=dialogue.get("text","")
            if auto_bubble_style:style=_detect_bubble_style(text,speaker)
            else:style="normal"
            is_n=style=="narration";char_color=character_colors.get(speaker,"#222222") if character_colors else "#222222"
            if not is_n:
                nb=name_font.getbbox(speaker);nw=nb[2]-nb[0]+8
                draw.rectangle([x+10,by-2,x+10+nw,by+14],fill=char_color);draw.text((x+14,by),speaker,font=name_font,fill="white");by+=16
            bh=_draw_bubble(draw,x+8,by,text,font,max_width=w-16,style=style,border_color=char_color if not is_n else "#333333")
            by+=bh+5
            if by>y+h-30:break
        sx,sy=x+w-80,y+h-50
        for sfx in panel.get("sound_effects",[]):_draw_sound_effect(draw,sx,sy,sfx,font);sy-=40
        
        # 面板特效
        if panel_effect=="auto":
            emotion=panel.get("scene_description","") # 从pages_data可能拿不到emotion，先跳过
        elif panel_effect!="none":
            effect_map={"speed_lines":"radial","impact_lines":"impact","focus_lines":"focus","speed_horizontal":"horizontal"}
            d=effect_map.get(panel_effect,"radial")
            panel_region=page.crop((x+1,y+1,x+w-1,y+h-1))
            panel_region=add_speed_lines(panel_region,d,10)
            page.paste(panel_region,(x+1,y+1))
    
    if watermark_text:page=add_watermark(page,watermark_text,watermark_position)
    return page

# ============ v9 新增：章节页面 ============

def compose_chapter_title_page(chapter_number: int, chapter_title: str, 
                               chapter_synopsis: str = "", style_key: str = "manga") -> Image:
    """生成章节标题页（用于多章节漫画）
    
    Args:
        chapter_number: 章节号
        chapter_title: 章节标题
        chapter_synopsis: 章节简介
        style_key: 画风key
    
    Returns:
        PIL Image
    """
    w, h = config.PAGE_WIDTH, config.PAGE_HEIGHT
    page = Image.new("RGB", (w, h), "#FAFAFA")
    draw = ImageDraw.Draw(page)
    
    font_title = _get_font(72)
    font_synopsis = _get_font(28)
    font_number = _get_font(24)
    
    # 章节号
    number_text = f"CHAPTER {chapter_number}"
    nb = draw.textbbox((0, 0), number_text, font=font_number)
    draw.text(((w - (nb[2] - nb[0])) // 2, 200), number_text, font=font_number, fill="#999999")
    
    # 章节标题
    tb = draw.textbbox((0, 0), chapter_title, font=font_title)
    draw.text(((w - (tb[2] - tb[0])) // 2, 300), chapter_title, font=font_title, fill="#333333")
    
    # 分割线
    line_y = 450
    draw.line([(w//4, line_y), (w*3//4, line_y)], fill="#CCCCCC", width=2)
    
    # 章节简介
    if chapter_synopsis:
        synopsis_lines = _wrap_text(chapter_synopsis, font_synopsis, w - 200)
        y = 500
        for line in synopsis_lines[:4]:
            lb = draw.textbbox((0, 0), line, font=font_synopsis)
            draw.text(((w - (lb[2] - lb[0])) // 2, y), line, font=font_synopsis, fill="#666666")
            y += 40
    
    return page

def compose_series_cover(title: str, synopsis: str, total_chapters: int,
                         genre: str = "", style_key: str = "manga") -> Image:
    """生成系列封面（多章节漫画封面）
    
    Args:
        title: 作品标题
        synopsis: 简介
        total_chapters: 总章节数
        genre: 类型
        style_key: 画风
    
    Returns:
        PIL Image
    """
    w, h = config.PAGE_WIDTH, config.PAGE_HEIGHT
    page = Image.new("RGB", (w, h), "#1A1A2E")
    draw = ImageDraw.Draw(page)
    
    font_title = _get_font(80)
    font_subtitle = _get_font(32)
    font_meta = _get_font(24)
    
    # 类型标签
    if genre:
        gb = draw.textbbox((0, 0), genre, font=font_meta)
        genre_w = gb[2] - gb[0]
        draw.rectangle([(w//2 - genre_w//2 - 20, 80), (w//2 + genre_w//2 + 20, 130)], fill="#E74C3C")
        draw.text(((w - genre_w) // 2, 90), genre, font=font_meta, fill="white")
    
    # 主标题
    tb = draw.textbbox((0, 0), title, font=font_title)
    draw.text(((w - (tb[2] - tb[0])) // 2, 250), title, font=font_title, fill="white")
    
    # 分割线
    line_y = 400
    draw.line([(w//4, line_y), (w*3//4, line_y)], fill="#4A90D9", width=3)
    
    # 简介
    syn_lines = _wrap_text(synopsis, font_subtitle, w - 300)
    y = 450
    for line in syn_lines[:5]:
        lb = draw.textbbox((0, 0), line, font=font_subtitle)
        draw.text(((w - (lb[2] - lb[0])) // 2, y), line, font=font_subtitle, fill="#AAAAAA")
        y += 45
    
    # 章节信息
    ch_info = f"共 {total_chapters} 章"
    cb = draw.textbbox((0, 0), ch_info, font=font_meta)
    ch_w = cb[2] - cb[0]
    draw.text(((w - ch_w) // 2, h - 150), ch_info, font=font_meta, fill="#666666")
    
    # 底部装饰
    draw.line([(w//4, h-100), (w*3//4, h-100)], fill="#333355", width=2)
    
    return page
