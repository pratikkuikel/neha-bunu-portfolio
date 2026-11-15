"""Render dist/book.html, the no-JavaScript complete text edition, from dist/manuscript.json.
Usage: python scripts/render-book.py   (also run by extract-manuscript.py)
"""
from pathlib import Path
import json, html

root = Path(__file__).resolve().parent.parent
items = json.loads((root / 'dist/manuscript.json').read_text())

def label(text):
    return {'AUTHOR NOTE': 'Author’s note'}.get(text, text)

front, body, contents = [], [], []
seen_heading = False
for i, item in enumerate(items):
    text = html.escape(item['text'])
    if item['heading']:
        seen_heading = True
        anchor = f's{len(contents) + 1}'
        contents.append(f'<li><a href="#{anchor}">{html.escape(label(item["text"]))}</a></li>')
        body.append(f'<h2 class="reveal" id="{anchor}">{html.escape(label(item["text"]))}</h2>')
    elif not seen_heading:
        front.append(f'<p>{text}</p>')
    else:
        body.append(f'<p>{text}</p>')

style = '''
body.text-page{background:var(--bg);color:var(--text)}
.text-page{font:20px/1.7 Literary,Georgia,serif}
.text-page .top{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:28px var(--m)}
.text-page .wordmark{font:var(--f-lead)/1 Literary,Georgia,serif;white-space:nowrap}.text-page .top nav a{white-space:nowrap}
.text-page .top nav{display:flex;gap:32px;font:var(--f-small)/1 Sans,Arial,sans-serif}
.text-page .top nav a{padding:10px 0;text-decoration:underline;text-decoration-color:transparent;text-underline-offset:6px;transition:text-decoration-color .2s}
.text-page .top nav a:hover{text-decoration-color:currentColor}
.book-head{padding:clamp(40px,6vw,96px) var(--m) 0;display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;align-items:center}.book-head .intro{grid-column:1/8}.book-head .cover{grid-column:9/13;justify-self:end;width:100%;max-width:360px;height:auto;display:block}
.book-head h1{font-size:var(--f-display);line-height:1;letter-spacing:-.035em;margin:0;text-wrap:balance}
.book-head .sub{font:var(--f-lead)/1.35 Literary,Georgia,serif;margin:32px 0 0}
.book-head .actions{display:flex;flex-wrap:wrap;align-items:center;gap:28px;margin-top:40px;font:var(--f-small)/1.4 Sans,Arial,sans-serif;color:var(--soft)}
.contents{margin:clamp(96px,10vw,160px) var(--m) 0;display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px}
.contents h2{grid-column:1/-1;margin-bottom:32px!important;font-size:var(--f-head);line-height:1.04;letter-spacing:-.02em;margin:0}
.contents ol{grid-column:1/8;list-style:none;margin:0;padding:0;columns:2 200px;column-gap:24px;font:var(--f-lead)/1.6 Literary,Georgia,serif}
.contents a{display:inline-block;transition:transform .3s var(--ease),color .2s}
.contents a:hover,.contents a:focus-visible{transform:translateX(8px)}
.contents figure,.closing figure{margin:0}.contents figure{grid-column:9/13;align-self:start}.contents img{display:block;width:100%;height:auto;aspect-ratio:1;object-fit:cover}figcaption{margin-top:14px;font:var(--f-small)/1.5 Sans,Arial,sans-serif;color:var(--soft)}
.closing{position:relative;display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;min-height:max(90svh,620px);margin-top:clamp(120px,14vw,200px);padding:0 var(--m);overflow:hidden}.closing img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.62)}.closing-text{position:relative;grid-column:8/13;align-self:end;padding-bottom:12svh}.closing h2{font-size:var(--f-head);line-height:1.04;letter-spacing:-.02em;margin:0 0 24px}.closing p{margin:0 0 24px;max-width:40ch}.closing .links{display:flex;flex-wrap:wrap;gap:16px 28px;align-items:center;font:var(--f-body)/1.4 Sans,Arial,sans-serif}.closing .links a:not(.btn){text-decoration:underline;text-underline-offset:6px}
.band{margin:clamp(120px,14vw,200px) var(--m) 0}.band img{display:block;width:100%;height:min(80svh,760px);object-fit:cover;filter:brightness(.85) contrast(1.05)}
.text{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;padding:0 var(--m)}
.text>*{grid-column:4/10}
.front{margin-top:clamp(96px,10vw,160px);color:var(--soft);font:var(--f-small)/1.7 Sans,Arial,sans-serif}
.front p{margin:0}
.text h2{font-size:var(--f-head);line-height:1.04;letter-spacing:-.02em;margin:clamp(96px,10vw,160px) 0 40px;scroll-margin-top:32px}
.text p{margin:0 0 18px}
.text-page .foot{padding:clamp(120px,14vw,200px) var(--m) 32px;font:var(--f-small)/1.6 Sans,Arial,sans-serif;color:var(--soft);display:grid;grid-template-columns:1fr auto 1fr;gap:24px;align-items:baseline}
.text-page .foot nav{display:flex;gap:24px}.text-page .foot a{color:var(--text)}.text-page .foot a:hover{text-decoration:underline;text-underline-offset:5px}
.text-page .foot>span:last-of-type{text-align:right}.text-page .foot .credits{grid-column:1/-1;margin:16px 0 0;max-width:75ch}.text-page .foot .credits a{text-decoration:underline;text-underline-offset:3px}
@media(max-width:1024px){.text>*{grid-column:2/12}.contents h2{grid-column:1/-1;margin-bottom:24px}.contents ol{grid-column:1/-1}.contents figure{grid-column:1/-1;margin-top:48px!important;width:70%}}
@media(max-width:640px){.text-page .top nav a.hide-sm{display:none}.book-head .intro{grid-column:1/-1;order:2;margin-top:40px}.book-head .cover{grid-column:1/-1;justify-self:center;max-width:62%}.book-head .actions .btn{width:100%}.text>*{grid-column:1/-1}.contents ol{columns:2;font-size:var(--f-body)}.band img{height:56svh}.closing{display:block;min-height:0;padding:0;margin-top:96px}.closing img{position:relative;height:60svh}.closing-text{padding:40px var(--m) 0}.text-page .foot{grid-template-columns:1fr;gap:8px}.text-page .foot>span:last-of-type{text-align:left}}
.progress{position:fixed;left:0;right:0;top:0;height:4px;background:var(--accent);transform:scaleX(0);transform-origin:left;z-index:5}
html.js .reveal{opacity:0;transform:translateY(24px);transition:opacity .8s var(--ease) var(--d,0ms),transform .9s var(--ease) var(--d,0ms)}html.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition-duration:0s!important}html.js .reveal{opacity:1;transform:none}}
'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#0d060b"><meta name="description" content="The complete text of The Sky She Left Me, the debut novel by Neha Kharel, on one page."><title>The Sky She Left Me — Complete text edition</title><script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__reveal)document.documentElement.classList.remove('js')}},3000)</script><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><style>{style}</style></head>
<body class="text-page"><div class="progress" aria-hidden="true"></div><a class="skip" href="#text">Skip to the text</a>
<header class="top"><a class="wordmark" href="./">Neha Kharel</a><nav aria-label="Main navigation"><a class="hide-sm" href="./">Author website</a><a class="hide-sm" href="#contents">Contents</a><a href="./#read">Page-turning edition</a></nav></header>
<main>
<section class="book-head" aria-labelledby="title"><div class="intro"><h1 id="title" class="reveal">The Sky She Left Me</h1><p class="sub reveal">The complete novel by Neha Kharel, as plain text on one page.</p><p class="actions reveal"><a class="btn" href="#s2">Begin with Chapter 1</a><span>230 pages in print, published October 2025</span></p></div><img class="cover reveal" src="assets/title-page.png" alt="The title page of The Sky She Left Me, hand-lettered by Neha Kharel" width="893" height="1364"></section>
<nav class="contents" id="contents" aria-labelledby="contents-title"><h2 id="contents-title">Contents</h2><ol>{"".join(contents)}</ol><figure class="reveal"><img src="assets/sky-stars.webp" alt="A dark blue night sky full of stars" width="1024" height="768" loading="lazy" decoding="async"><figcaption>The sky Ishan and Anya watched from her rooftop.</figcaption></figure></nav>
<figure class="band reveal"><img src="assets/sky-tilicho.jpg" alt="The Milky Way above snow peaks and a lodge at Tilicho, Nepal" width="1920" height="1280" loading="lazy" decoding="async"><figcaption>“You exist in my every tomorrow.” From the Epilogue.</figcaption></figure>
<article class="text" id="text" aria-label="The Sky She Left Me"><div class="front">{"".join(front)}</div>{"".join(body)}</article>
<section class="closing" aria-labelledby="end-title"><img src="assets/rooftop-dusk.jpg" alt="A rooftop at dusk, the sun setting behind a curved roof edge over the city" width="1600" height="900" decoding="async"><div class="closing-text"><h2 id="end-title" class="reveal">The end, for now</h2><p class="reveal">If the story stayed with you, share your favourite line and tag Neha, as she asks in her note.</p><p class="links reveal"><a class="btn" href="./">Back to Neha’s website</a><a href="#contents">Contents</a></p></div></section>
</main>
<footer class="foot"><span>Neha Kharel, author</span><nav aria-label="Footer"><a href="./">Author website</a><a href="./#read">Page-turning edition</a><a href="#">Back to top</a></nav><span>© 2025 Neha Kharel · ISBN 978-9937-1-9286-6</span><p class="credits">Photographs: <a href="https://commons.wikimedia.org/wiki/File:Milky_Way_as_seen_from_Tilicho.jpg">Milky Way as seen from Tilicho</a> by Yugesh Pandey, CC BY-SA 4.0, via Wikimedia Commons; <a href="https://www.rawpixel.com/image/6031865/starry-night-sky-free-public-domain-cc0-image">Starry night sky</a>, CC0, via rawpixel; <a href="https://wordpress.org/photos/photo/844668d30b/">rooftop at sunset</a> by PRABIN M, CC0, via WordPress Photo Directory.</p></footer>
<script>(function(){{window.__reveal=true;var bar=document.querySelector(".progress"),ticking=false;function upd(){{var h=document.documentElement,max=h.scrollHeight-innerHeight;bar.style.transform="scaleX("+(max>0?Math.min(1,scrollY/max):0)+")";ticking=false}}addEventListener("scroll",function(){{if(!ticking){{ticking=true;requestAnimationFrame(upd)}}}},{{passive:true}});upd();var els=[].slice.call(document.querySelectorAll(".reveal"));els.slice(0,4).forEach(function(el,i){{el.style.setProperty("--d",i*80+"ms")}});if(!("IntersectionObserver" in window)){{els.forEach(function(el){{el.classList.add("in")}});return}}var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add("in");io.unobserve(e.target)}}}})}},{{threshold:.1}});els.forEach(function(el){{io.observe(el)}})}})();</script>
</body></html>
'''
(root / 'dist/book.html').write_text(page)
print('wrote dist/book.html', len(contents), 'sections')
