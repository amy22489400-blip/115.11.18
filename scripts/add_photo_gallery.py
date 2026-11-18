from pathlib import Path

page = Path(__file__).resolve().parents[1] / "index.html"
html = page.read_text(encoding="utf-8")

old = '</div><div class="tools">'
new = '</div><div class="view-toggle"><button id="photo-view" class="view-btn active" type="button">照片清單</button><button id="table-view" class="view-btn" type="button">表格</button></div><div class="tools">'
if old not in html:
    raise SystemExit("Panel header insertion point not found")
html = html.replace(old, new, 1)

old = '<div class="table-wrap"><table>'
new = '<div id="photo-grid" class="photo-grid"></div><div id="table-wrap" class="table-wrap" hidden><table>'
if old not in html:
    raise SystemExit("Table insertion point not found")
html = html.replace(old, new, 1)

styles = """
    .view-toggle{display:flex;gap:4px;flex-shrink:0;background:#f7e9ee;border-radius:9px;padding:3px}
    .view-btn{border:0;border-radius:7px;background:transparent;color:#8d6877;padding:7px 10px;font-size:11px;font-weight:600;white-space:nowrap}
    .view-btn.active{background:#fff;color:#a94f70;box-shadow:0 1px 4px #5a344411}
    .photo-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px;padding:0 20px 20px}
    .material-card{min-width:0;border:1px solid var(--line);border-radius:13px;overflow:hidden;background:#fff;box-shadow:0 3px 12px #16352505;display:flex;flex-direction:column}
    .card-photo{height:158px;width:100%;border:0;padding:10px;background:#fbf7f9;display:grid;place-items:center;cursor:zoom-in}
    .card-photo img{width:100%;height:100%;object-fit:contain}
    .card-photo:disabled{cursor:default;color:#b45f7b;font-size:32px}
    .material-card-body{padding:12px 13px;display:grid;gap:8px;flex:1}
    .card-name{font-size:12px;font-weight:700;line-height:1.5;color:#30423a}
    .card-model{font-size:10px;color:#89948d;min-height:15px;overflow-wrap:anywhere}
    .card-footer{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:auto;padding-top:3px}
    .card-qty{font-size:11px;font-weight:700;color:#59665f;white-space:nowrap}
    .photo-grid[hidden],#table-wrap[hidden]{display:none!important}
    @media(max-width:720px){.photo-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;padding:0 12px 14px}.card-photo{height:125px}.material-card-body{padding:10px}.view-btn{padding:7px 8px}}
"""
pos = html.rfind("</style>")
if pos < 0:
    raise SystemExit("Stylesheet closing tag not found")
html = html[:pos] + styles + html[pos:]

card_renderer = '''$('photo-grid').innerHTML=shown.map(x=>`<article class="material-card"><button class="card-photo" data-photo="${x.sourceNo||''}" aria-label="查看教材照片" ${x.sourceNo?'':'disabled'}>${x.sourceNo?`<img src="./assets/photos/item-${String(x.sourceNo).padStart(2,'0')}.jpg" alt="${esc(x.name)}">`:'＋'}</button><div class="material-card-body"><div class="card-name">${esc(x.name)}${x.review?' <span style="color:#bd7942;font-size:9px;font-weight:500">待核對</span>':''}</div><div class="card-model">${esc(x.model||'—')}</div><div class="card-footer"><span class="status ${x.status==='在庫'?'ready':x.status==='借出中'?'borrowed':'service'}">${esc(x.status)}</span><span class="card-qty">${x.quantity} 件</span></div>${x.sourceNo?`<div class="item-sub">PDF 清冊・項次 ${String(x.sourceNo).padStart(2,'0')}</div>`:''}</div></article>`).join('');'''
needle = "$('rows').innerHTML=shown.map"
if html.count(needle) != 1:
    raise SystemExit("Material renderer insertion point not found")
html = html.replace(needle, card_renderer + needle, 1)

views = "$('photo-view').onclick=()=>{$('photo-grid').hidden=false;$('table-wrap').hidden=true;$('photo-view').classList.add('active');$('table-view').classList.remove('active')};$('table-view').onclick=()=>{$('photo-grid').hidden=true;$('table-wrap').hidden=false;$('table-view').classList.add('active');$('photo-view').classList.remove('active')};"
needle = "['search','category-filter','status-filter'].forEach"
if html.count(needle) != 1:
    raise SystemExit("View toggle handler insertion point not found")
html = html.replace(needle, views + needle, 1)

page.write_text(html, encoding="utf-8")
print("Default photo list added with a table view toggle")
