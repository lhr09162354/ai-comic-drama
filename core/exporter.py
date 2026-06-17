"""导出模块 v4 - EPUB格式、阅读器HTML"""

import os
import io
import zipfile
import tempfile
from PIL import Image
import config

def export_pages_as_images(pages, title, output_dir=None):
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, pg in enumerate(pages):
        path = os.path.join(out_dir, f"page_{i+1:03d}.png")
        pg.save(path, "PNG")
        paths.append(path)
    return paths

def export_as_pdf(pages, title, output_dir=None):
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
        os.makedirs(out_dir, exist_ok=True)
        pdf_path = os.path.join(out_dir, f"{title}.pdf")
        c = None
        for i, pg in enumerate(pages):
            tmp = os.path.join(out_dir, f"_tmp_{i}.png")
            pg.save(tmp, "PNG")
            if c is None:
                c = rl_canvas.Canvas(pdf_path, pagesize=(pg.width, pg.height))
            c.drawImage(tmp, 0, 0, width=pg.width, height=pg.height)
            c.showPage()
            try: os.remove(tmp)
            except: pass
        if c: c.save()
        return pdf_path
    except ImportError:
        return _pdf_pillow(pages, title, output_dir)

def _pdf_pillow(pages, title, output_dir=None):
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{title}.pdf")
    if not pages: return path
    rgbs = [p.convert("RGB") for p in pages]
    rgbs[0].save(path, "PDF", save_all=True, append_images=rgbs[1:])
    return path

def export_long_strip(pages, title, output_dir=None):
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    if not pages: return ""
    mw = max(p.width for p in pages)
    th = sum(p.height for p in pages) + 10*(len(pages)-1)
    strip = Image.new("RGB", (mw, th), "white")
    yo = 0
    for pg in pages: strip.paste(pg, (0, yo)); yo += pg.height + 10
    path = os.path.join(out_dir, f"{title}_长条.png")
    strip.save(path, "PNG")
    return path

def export_as_cbz(pages, title, output_dir=None):
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{title}.cbz")
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for i, pg in enumerate(pages):
            buf = io.BytesIO(); pg.save(buf, "PNG")
            zf.writestr(f"{i+1:03d}.png", buf.getvalue())
    return path

def export_all_formats(pages, title, output_dir=None):
    results = {}
    for fmt, fn in [("images", export_pages_as_images), ("pdf", export_as_pdf),
                     ("long_strip", export_long_strip), ("cbz", export_as_cbz)]:
        try: results[fmt] = fn(pages, title, output_dir)
        except Exception as e: results[fmt] = f"失败: {e}"
    return results

# ============ EPUB 导出 ============

def export_as_epub(pages, title, author="AI漫剧生成器", output_dir=None) -> str:
    """导出为EPUB电子书格式"""
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    epub_path = os.path.join(out_dir, f"{title}.epub")
    
    # EPUB本质是ZIP，包含特定结构
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype（必须第一个，不压缩）
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        
        # META-INF/container.xml
        container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''
        zf.writestr("META-INF/container.xml", container_xml)
        
        # 生成页面图片
        page_ids = []
        for i, pg in enumerate(pages):
            img_buf = io.BytesIO()
            pg.save(img_buf, "PNG")
            zf.writestr(f"OEBPS/images/page_{i+1:03d}.png", img_buf.getvalue())
            page_ids.append(f"page_{i+1}")
        
        # content.opf
        manifest_items = '\n'.join(
            f'<item id="{pid}" href="images/{pid}.png" media-type="image/png"/>'
            for pid in page_ids
        )
        spine_items = '\n'.join(f'<itemref idref="{pid}"/>' for pid in page_ids)
        
        # XHTML页面
        xhtml_items = ''
        for i, pid in enumerate(page_ids):
            xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Page {i+1}</title></head>
<body style="margin:0;padding:0;text-align:center;">
<img src="images/{pid}.png" style="max-width:100%;height:auto;"/>
</body></html>'''
            zf.writestr(f"OEBPS/{pid}.xhtml", xhtml)
            xhtml_items += f'<item id="{pid}_html" href="{pid}.xhtml" media-type="application/xhtml+xml"/>\n'
        
        spine_xhtml = '\n'.join(f'<itemref idref="{pid}_html"/>' for pid in page_ids)
        
        opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">urn:uuid:ai-comic-{hash(title)}</dc:identifier>
    <dc:title>{title}</dc:title>
    <dc:creator>{author}</dc:creator>
    <dc:language>zh</dc:language>
    <meta property="dcterms:modified">2024-01-01T00:00:00Z</meta>
  </metadata>
  <manifest>
    {xhtml_items}
    {manifest_items}
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine>{spine_xhtml}</spine>
</package>'''
        zf.writestr("OEBPS/content.opf", opf)
        
        # nav.xhtml
        nav = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>目录</title></head>
<body>
<nav epub:type="toc"><h1>目录</h1><ol>
{''.join(f'<li><a href="{pid}.xhtml">第{i+1}页</a></li>' for i, pid in enumerate(page_ids))}
</ol></nav>
</body></html>'''
        zf.writestr("OEBPS/nav.xhtml", nav)
    
    return epub_path

# ============ 漫画阅读器HTML ============

def export_as_reader_html(pages, title, output_dir=None) -> str:
    """生成交互式漫画阅读器HTML页面"""
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    
    # 将所有页面转为base64
    import base64
    page_b64 = []
    for pg in pages:
        buf = io.BytesIO()
        pg.save(buf, "PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        page_b64.append(b64)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{title} - 漫画阅读器</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#1a1a2e; color:white; font-family:system-ui,-apple-system,sans-serif;
        touch-action:pan-y; -webkit-overflow-scrolling:touch; overflow-x:hidden; }}
.header {{ position:fixed; top:0; left:0; right:0; z-index:100;
           background:rgba(26,26,46,0.95); padding:12px 16px; text-align:center;
           backdrop-filter:blur(10px); border-bottom:1px solid rgba(255,255,255,0.1); }}
.header h1 {{ font-size:16px; font-weight:500; }}
.page-counter {{ font-size:12px; color:#888; margin-top:4px; }}
.reader {{ padding-top:56px; }}
.page-img {{ width:100%; display:block; border-bottom:4px solid #111; }}
.controls {{ position:fixed; bottom:0; left:0; right:0; z-index:100;
             background:rgba(26,26,46,0.95); padding:12px; display:flex;
             justify-content:space-around; backdrop-filter:blur(10px);
             border-top:1px solid rgba(255,255,255,0.1); }}
.controls button {{ background:none; border:1px solid rgba(255,255,255,0.2);
                    color:white; padding:8px 16px; border-radius:8px; font-size:14px;
                    cursor:pointer; }}
.controls button:active {{ background:rgba(255,255,255,0.1); }}
.mode-btn {{ display:none; }} /* 横排模式按钮 */
</style>
</head>
<body>
<div class="header">
  <h1>{title}</h1>
  <div class="page-counter" id="counter">1 / {len(pages)}</div>
</div>
<div class="reader" id="reader">
  {"".join(f'<img class="page-img" src="data:image/png;base64,{b64}" loading="lazy">' for b64 in page_b64)}
</div>
<div class="controls">
  <button onclick="scrollToPage(-1)">⬅ 上一页</button>
  <button onclick="toggleMode()">📖 模式</button>
  <button onclick="scrollToPage(1)">下一页 ➡</button>
</div>
<script>
let currentMode = 'vertical'; // vertical | single
let currentPage = 0;
const totalPages = {len(pages)};
const reader = document.getElementById('reader');
const counter = document.getElementById('counter');
const imgs = document.querySelectorAll('.page-img');

// 监听滚动更新页码
const observer = new IntersectionObserver((entries) => {{
  entries.forEach(e => {{
    if (e.isIntersecting) {{
      const idx = Array.from(imgs).indexOf(e.target);
      if (idx >= 0) {{ currentPage = idx; counter.textContent = (idx+1) + ' / ' + totalPages; }}
    }}
  }});
}}, {{ threshold: 0.5 }});
imgs.forEach(img => observer.observe(img));

function scrollToPage(dir) {{
  currentPage = Math.max(0, Math.min(totalPages-1, currentPage + dir));
  imgs[currentPage].scrollIntoView({{ behavior:'smooth', block:'start' }});
}}

let singleMode = false;
function toggleMode() {{
  singleMode = !singleMode;
  if (singleMode) {{
    // 单页模式：只显示当前页
    imgs.forEach((img, i) => {{ img.style.display = i === currentPage ? 'block' : 'none'; }});
  }} else {{
    // 竖排模式：全部显示
    imgs.forEach(img => {{ img.style.display = 'block'; }});
  }}
}}

// 触摸翻页（左右滑动）
let touchStartX = 0;
document.addEventListener('touchstart', e => {{ touchStartX = e.touches[0].clientX; }});
document.addEventListener('touchend', e => {{
  if (!singleMode) return;
  const dx = e.changedTouches[0].clientX - touchStartX;
  if (Math.abs(dx) > 60) scrollToPage(dx > 0 ? -1 : 1);
}});
</script>
</body></html>'''
    
    html_path = os.path.join(out_dir, f"{title}_阅读器.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_path

# ============ 内存下载 ============

def pages_to_zip_bytes(pages, title):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for i, pg in enumerate(pages):
            ib = io.BytesIO(); pg.save(ib, "PNG")
            zf.writestr(f"{title}/page_{i+1:03d}.png", ib.getvalue())
    buf.seek(0); return buf.getvalue()

def page_to_png_bytes(page):
    buf = io.BytesIO(); page.save(buf, "PNG"); buf.seek(0); return buf.getvalue()

def pages_to_pdf_bytes(pages):
    buf = io.BytesIO()
    if not pages: return buf.getvalue()
    rgbs = [p.convert("RGB") for p in pages]
    rgbs[0].save(buf, "PDF", save_all=True, append_images=rgbs[1:])
    buf.seek(0); return buf.getvalue()

def pages_to_cbz_bytes(pages):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for i, pg in enumerate(pages):
            ib = io.BytesIO(); pg.save(ib, "PNG")
            zf.writestr(f"{i+1:03d}.png", ib.getvalue())
    buf.seek(0); return buf.getvalue()

def pages_to_epub_bytes(pages, title, author="AI漫剧生成器"):
    """EPUB字节数据"""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp:
        tmp_path = tmp.name
    export_as_epub(pages, title, author, os.path.dirname(tmp_path))
    # 重命名为正确路径
    real_path = export_as_epub(pages, title, author)
    with open(real_path, "rb") as f:
        data = f.read()
    return data

def reader_html_bytes(pages, title):
    """阅读器HTML字节数据"""
    import tempfile
    path = export_as_reader_html(pages, title)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().encode("utf-8")
