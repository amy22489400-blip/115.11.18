from pathlib import Path
import re

page = Path(__file__).resolve().parents[1] / "index.html"
html = page.read_text(encoding="utf-8")

html, photo_count = re.subn(
    r'<div class="item-art">.*?</div><div><div class="item-name">',
    '${x.sourceNo?`<button class="item-art photo" data-photo="${x.sourceNo}" aria-label="查看教材照片"><img src="./assets/photos/item-${String(x.sourceNo).padStart(2,\'0\')}.jpg" alt=""></button>`:`<div class="item-art">＋</div>`}<div><div class="item-name">',
    html,
    count=1,
)
if photo_count != 1:
    raise SystemExit("Could not find the material thumbnail in the item renderer")

html, modal_count = re.subn(
    r'(<dialog id="loan-dialog".*?</form></dialog>)',
    r'\1\n<dialog id="photo-dialog" class="photo-dialog"><div class="modal-head"><h2 id="photo-title">教具照片</h2><button class="icon-btn" id="close-photo" aria-label="關閉">✕</button></div><img id="photo-large" class="photo-large" alt="教材照片"><div id="photo-caption" class="photo-caption"></div></dialog>',
    html,
    count=1,
    flags=re.S,
)
if modal_count != 1:
    raise SystemExit("Could not add the photo preview dialog")

old = "document.addEventListener('click',e=>{const b=e.target.closest('[data-edit],[data-loan],[data-return],[data-delete]');if(!b)return;"
new = "document.addEventListener('click',e=>{const b=e.target.closest('[data-edit],[data-loan],[data-return],[data-delete],[data-photo]');if(!b)return;if(b.dataset.photo){const n=Number(b.dataset.photo),x=items.find(a=>Number(a.sourceNo)===n);$('photo-title').textContent=x?.name||`教具項次 ${n}`;$('photo-caption').textContent=`臨床技能中心教具清冊 · PDF 項次 ${String(n).padStart(2,'0')}　｜　${x?.model||''}`;$('photo-large').src=`./assets/photos/item-${String(n).padStart(2,'0')}.jpg`;$('photo-large').alt=x?.name||`教具項次 ${n}`;$('photo-dialog').showModal()}"
if old not in html:
    raise SystemExit("Could not find the item action handler")
html = html.replace(old, new, 1)

old = "$('close-loan').onclick=$('cancel-loan').onclick=()=>$('loan-dialog').close();"
new = old + "$('close-photo').onclick=()=>$('photo-dialog').close();"
if old not in html:
    raise SystemExit("Could not find the modal close handlers")
html = html.replace(old, new, 1)

html = html.replace(".bottom-mobile{display:none}", ".bottom-mobile{display:none}.item-art.photo{width:54px;height:46px;border:0;padding:2px;background:#f3f5f2;overflow:hidden;cursor:zoom-in}.item-art.photo img{width:100%;height:100%;object-fit:contain}.photo-dialog{width:min(760px,calc(100% - 28px))}.photo-large{display:block;width:100%;height:min(68vh,650px);object-fit:contain;background:#f7f8f6}.photo-caption{padding:12px 20px;color:#66766c;font-size:12px}", 1)

page.write_text(html, encoding="utf-8")
print("Photo thumbnails and enlarged preview wired into the material list")
