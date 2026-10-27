"""Сборка сайта «Сеть своих» v2: python3 _src/build.py [--artifact DIR]

Без пакетов, только Python 3. Пишет *.html в корень website-v2.
С --artifact дополнительно собирает копию для превью на claude.ai (главная без <html>/<head>).
"""
import html, json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa: F401,F403

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
FONTS = "https://fonts.googleapis.com/css2?family=Forum&family=IBM+Plex+Mono:wght@400;500&family=Spectral:ital,wght@0,300;0,400;0,600;1,400&display=swap"

# ---------- знаки ----------

def tri(cx, cy, r):
    pts = [(cx, cy - r), (cx - r * math.sin(math.radians(60)), cy + r / 2), (cx + r * math.sin(math.radians(60)), cy + r / 2)]
    return pts

LOGO = '''<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="18.5" fill="none" stroke="var(--brass)" stroke-width="1"/><circle cx="20" cy="20" r="15" fill="none" stroke="var(--brass)" stroke-width=".5" stroke-dasharray="1 2"/><path d="M20 10.5 11.8 24.8h16.4Z" fill="none" stroke="var(--paper)" stroke-width="1.2" stroke-linejoin="round"/><circle cx="20" cy="10.5" r="2.6" fill="var(--seal-hi)"/><circle cx="11.8" cy="24.8" r="2.3" fill="var(--brass)"/><circle cx="28.2" cy="24.8" r="2.3" fill="var(--brass)"/></svg>'''


def seal(big=True):
    a, b, c = tri(200, 214, 92)
    ticks = "".join(
        f'<line x1="{200 + 178 * math.cos(math.radians(i * 5)):.1f}" y1="{200 + 178 * math.sin(math.radians(i * 5)):.1f}" '
        f'x2="{200 + (170 if i % 6 else 164) * math.cos(math.radians(i * 5)):.1f}" y2="{200 + (170 if i % 6 else 164) * math.sin(math.radians(i * 5)):.1f}"/>'
        for i in range(72))
    ring = "СЛОВО ВМЕСТО ЗАЛОГА · ВХОД ПО ПРИГЛАШЕНИЮ · СВОИ ПОМОГАЮТ СВОИМ · "
    return f'''<svg class="seal" viewBox="0 0 400 400" role="img" aria-label="Печать сети: три точки в круге и девиз «Слово вместо залога»">
<defs><path id="rt" d="M200,200 m-148,0 a148,148 0 1,1 296,0 a148,148 0 1,1 -296,0"/>
<radialGradient id="sg" cx="50%" cy="40%" r="60%"><stop offset="0" stop-color="var(--brass-hi)" stop-opacity=".16"/><stop offset="1" stop-color="var(--brass)" stop-opacity="0"/></radialGradient></defs>
<circle cx="200" cy="200" r="190" fill="url(#sg)"/>
<circle class="draw" cx="200" cy="200" r="190" fill="none" stroke="var(--brass)" stroke-width="1.2"/>
<g stroke="var(--brass)" stroke-width="1" opacity=".55">{ticks}</g>
<circle class="draw d2" cx="200" cy="200" r="128" fill="none" stroke="var(--brass)" stroke-width=".8"/>
<g class="ring-text"><text font-family="var(--f-mono)" font-size="13.2" letter-spacing="3.1" fill="var(--brass-hi)"><textPath href="#rt">{ring}</textPath></text></g>
<path class="draw d3" d="M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f} L{c[0]:.1f} {c[1]:.1f} Z" fill="none" stroke="var(--paper)" stroke-width="1.4" stroke-linejoin="round"/>
<path class="draw d3" d="M{a[0]:.1f} {a[1]:.1f} L200 {214 + 46:.1f} M{b[0]:.1f} {b[1]:.1f} L200 {214 + 46:.1f} M{c[0]:.1f} {c[1]:.1f} L200 {214 + 46:.1f}" fill="none" stroke="var(--brass)" stroke-width=".6" opacity=".6"/>
<g style="transform-box:fill-box;transform-origin:center" class="node n1"><circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="13" fill="var(--seal)"/><circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="13" fill="none" stroke="var(--seal-hi)" stroke-width="1.5"/></g>
<g style="transform-box:fill-box;transform-origin:center" class="node n2"><circle cx="{b[0]:.1f}" cy="{b[1]:.1f}" r="11" fill="var(--brass)"/></g>
<g style="transform-box:fill-box;transform-origin:center" class="node n3"><circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="11" fill="var(--brass)"/></g>
<circle cx="200" cy="{214 + 46:.1f}" r="3" fill="var(--brass-hi)"/>
<path class="glint" d="M78 122 A148 148 0 0 1 162 60" fill="none" stroke="var(--brass-hi)" stroke-width="2.4" stroke-linecap="round"/>
</svg>'''


WAX = '''<svg viewBox="0 0 120 120" aria-hidden="true"><defs><radialGradient id="wx" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#C2434D"/><stop offset=".6" stop-color="#8E2A32"/><stop offset="1" stop-color="#5E161D"/></radialGradient></defs>
<path d="M60 4c9 0 12 6 20 8s15 1 19 8 0 13 3 20 10 11 10 20-7 12-10 20 1 14-3 20-12 6-19 8-11 8-20 8-12-6-20-8-15-1-19-8 0-13-3-20S8 69 8 60s7-12 10-20-1-14 3-20 12-6 19-8S51 4 60 4Z" fill="url(#wx)"/>
<circle cx="60" cy="60" r="34" fill="none" stroke="#5E161D" stroke-width="2"/><circle cx="60" cy="60" r="34" fill="none" stroke="#D86A72" stroke-width=".8" opacity=".6" transform="translate(-1 -1)"/>
<path d="M60 38 41 71h38Z" fill="none" stroke="#5E161D" stroke-width="3" stroke-linejoin="round"/><path d="M60 38 41 71h38Z" fill="none" stroke="#E0858C" stroke-width="1" stroke-linejoin="round" opacity=".7" transform="translate(-.8 -.8)"/>
<circle cx="60" cy="38" r="5" fill="#5E161D"/><circle cx="41" cy="71" r="5" fill="#5E161D"/><circle cx="79" cy="71" r="5" fill="#5E161D"/></svg>'''


def medal(roman, rings):
    circles = "".join(f'<circle cx="32" cy="32" r="{30 - i * 3.2}" fill="none" stroke="var(--brass)" stroke-width="{1 if i == 0 else .6}" opacity="{1 - i * .12}"/>' for i in range(rings + 1))
    return f'<svg class="medal" viewBox="0 0 64 64" aria-hidden="true">{circles}<text x="32" y="38" text-anchor="middle" font-family="var(--f-display)" font-size="{18 if len(roman) < 3 else 15}" fill="var(--brass-hi)">{roman}</text></svg>'


SIGILS = {
    "keeper": '<circle cx="22" cy="22" r="19" fill="none" stroke="var(--brass)"/><circle cx="22" cy="22" r="7" fill="none" stroke="var(--paper)"/><path d="M22 3v8M22 33v8M3 22h8M33 22h8" stroke="var(--brass)"/>',
    "gate": '<path d="M10 40V18a12 12 0 0 1 24 0v22" fill="none" stroke="var(--brass)"/><circle cx="22" cy="24" r="3" fill="var(--paper)"/><path d="M22 27v6" stroke="var(--paper)"/><path d="M6 40h32" stroke="var(--brass)"/>',
    "link": '<circle cx="12" cy="22" r="7" fill="none" stroke="var(--brass)"/><circle cx="32" cy="22" r="7" fill="none" stroke="var(--brass)"/><circle cx="22" cy="22" r="2.5" fill="var(--seal-hi)"/><path d="M19 22h-0M25 22h0" stroke="var(--paper)"/>',
    "bridge": '<path d="M3 32h38" stroke="var(--brass)"/><path d="M6 32Q22 6 38 32" fill="none" stroke="var(--paper)"/><path d="M14 32v-9M22 32V19M30 32v-9" stroke="var(--brass)" stroke-width=".8"/>',
    "scales": '<path d="M22 6v32M12 40h20M8 12h28" stroke="var(--brass)"/><path d="M8 12 3 24h10ZM36 12l-5 12h10Z" fill="none" stroke="var(--paper)" stroke-linejoin="round"/><circle cx="22" cy="6" r="2.5" fill="var(--seal-hi)"/>',
}


def sigil(k):
    return f'<svg class="sig" viewBox="0 0 44 44" aria-hidden="true" stroke-width="1.2">{SIGILS[k]}</svg>'


GLYPHS = {
    "match": '<circle cx="14" cy="23" r="9" fill="none" stroke="currentColor"/><circle cx="32" cy="23" r="9" fill="none" stroke="currentColor"/><path d="M23 16v14" stroke="var(--seal-hi)" stroke-width="2"/>',
    "circle": ''.join(f'<circle cx="{23 + 14 * math.cos(math.radians(i * 40 - 90)):.1f}" cy="{23 + 14 * math.sin(math.radians(i * 40 - 90)):.1f}" r="2.6" fill="currentColor"/>' for i in range(9)) + '<circle cx="23" cy="23" r="5" fill="none" stroke="var(--seal-hi)"/>',
    "bridge": '<path d="M2 32h42" stroke="currentColor"/><path d="M5 32Q23 4 41 32" fill="none" stroke="currentColor"/><circle cx="5" cy="32" r="3" fill="var(--seal-hi)"/><circle cx="41" cy="32" r="3" fill="var(--seal-hi)"/>',
}


def glyph(k):
    return f'<svg class="glyph" viewBox="0 0 46 46" aria-hidden="true" stroke-width="1.3">{GLYPHS[k]}</svg>'


# ---------- каркас ----------

def head(title, desc, full):
    t = f"{title} · {NAME}" if title != NAME else f"{NAME} · {MOTTO}"
    top = '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' if full else ""
    return f'''{top}<title>{E(t)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0C1D1A">
<meta property="og:title" content="{E(t)}">
<meta property="og:description" content="{E(desc)}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/style.css">
{"</head>" + chr(10) + "<body>" if full else ""}'''


def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    cur = ' aria-current="page"' if active == "invite.html" else ""
    return f'''<a class="skip" href="#main">К содержанию</a>
<header class="site-head gut"><div class="wrap">
  <a class="brand" href="index.html">{LOGO}<span>{NAME}<small>{MOTTO}</small></span></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Меню</button>
  <nav class="nav" id="nav" aria-label="Разделы">{links}<a class="btn btn-brass" href="invite.html"{cur}>По приглашению</a></nav>
</div></header>'''


def footer():
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    return f'''<footer class="site-foot gut"><div class="wrap">
  <div><a class="brand" href="index.html">{LOGO}<span>{NAME}</span></a>
    <p class="motto-line">Свои помогают своим. Вход только по слову того, кто уже внутри.</p></div>
  <div><h4>Разделы</h4><ul>{nav}</ul></div>
  <div><h4>Вход</h4><ul><li><a href="invite.html">По приглашению</a></li><li><a href="invite.html#faq">Вопросы</a></li><li><a href="code.html#oath">Пройти принятие кодекса</a></li></ul></div>
  <div class="base"><span>Verbum pro pignore</span><span>Закрытое сообщество предпринимателей · концепция</span></div>
</div></footer>'''


def page(name, title, desc, body, full=True, extra_js=""):
    return f'''{head(title, desc, full)}
{header(name)}
<main id="main">
{body}
</main>
{footer()}
{extra_js}<script src="assets/site.js"></script>
{"</body>" + chr(10) + "</html>" if full else ""}
'''


def page_head(eyebrow, h1, lede):
    return f'''<section class="page-head gut"><div class="bg-seal" aria-hidden="true">{seal()}</div><div class="wrap">
  <span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lede">{lede}</p>
</div></section>'''


def motto_band(text, sub, btn=("invite.html", "Как получают приглашение")):
    return f'''<section class="motto gut"><div class="wrap rv">
  <span class="eyebrow">{MOTTO}</span>
  <blockquote>{text}</blockquote>
  <p class="lede">{sub}</p>
  <a class="btn btn-brass" href="{btn[0]}">{btn[1]} <span class="arr">→</span></a>
</div></section>'''


# ---------- страницы ----------

def p_index():
    facts = "".join(f'<div class="fact"><b class="num">{n}</b><span>{E(t)}</span></div>' for n, t in FACTS)
    her = "".join(f'''<article class="her rv"><div class="meta"><span class="eyebrow">{E(era)}</span></div><h3>{E(n)}</h3><p>{E(what)}</p>
<div class="took"><b>Что мы взяли</b>{E(took)}</div></article>''' for n, era, what, took in HERITAGE)
    body = f'''<section class="hero gut"><div class="wrap">
  <div class="copy">
    <span class="eyebrow">Закрытое международное сообщество предпринимателей</span>
    <h1><span class="line"><span>Слово</span></span><span class="line"><span>вместо <em>залога</em></span></span></h1>
    <p class="lede">Сеть своих устроена так, как веками работали самые сильные диаспоры мира: поручительство, общий кодекс, взаимные обязательства и мосты между странами. Вход только по приглашению.</p>
    <div class="row"><a class="btn btn-brass" href="how.html">Как устроено <span class="arr">→</span></a><a class="btn" href="invite.html">Вход по приглашению</a></div>
  </div>
  <div class="hero-seal">{seal()}</div>
</div></section>

<section class="gut"><div class="wrap"><div class="facts">{facts}</div></div></section>

<section class="sec gut"><div class="wrap marg">
  <div class="side"><span class="roman">I</span><span class="eyebrow">Манифест</span></div>
  <div class="stack" style="gap:40px">
    <h2 class="rv">Почему свои всегда выигрывают</h2>
    <div class="prose drop rv">
      <p>Армянский купец XVII века приезжал в Амстердам и в тот же вечер ужинал у своих. Ему давали товар в долг без бумаг, потому что за него ручался дядя из Новой Джульфы. Купец из Любека в Новгороде жил на Ганзейском дворе по общему уставу. Алмазный дилер в Антверпене и сегодня закрывает сделку рукопожатием.</p>
      <p>Диаспоры выигрывали не числом и не деньгами. У них доверие стоило дешевле, чем у остальных. Там, где чужим нужны юристы, залоги и полгода проверок, своим хватало слова и человека, который за это слово отвечает.</p>
      <p>Мы взяли эти механизмы и отвязали их от происхождения. Свои здесь не по крови и не по паспорту. Свои по слову: это люди, за которых кто-то поручился и которые сами готовы поручиться за других.</p>
    </div>
    <p class="pull rv">Свои помогают своим. Вход только по слову того, кто уже внутри.</p>
  </div>
</div></section>

<section class="sec gut band"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Наследство</span><h2>Десять традиций, из которых собрана сеть</h2>
  <p class="lede">У каждой общины мы взяли один механизм, проверенный веками. Ни один не придуман с нуля.</p></div>
  <div class="heritage">{her}</div>
</div></section>

<section class="sec gut"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Что здесь происходит</span><h2>Три вещи, ради которых сюда приходят</h2></div>
  <div class="cards">
    <article class="card rv">{glyph("match")}<h3>Знакомства с согласия</h3><p>Нужен поставщик в Ташкенте, юрист по ВЭД или честный подрядчик. Связной найдёт человека, спросит его согласия и познакомит. Обычно за неделю.</p></article>
    <article class="card rv">{glyph("circle")}<h3>Круг</h3><p>Девять предпринимателей разных дел раз в месяц. Два часа о настоящих задачах, потому что сказанное не выходит за дверь.</p></article>
    <article class="card rv">{glyph("bridge")}<h3>Мосты между странами</h3><p>Приезжаете в Алматы, Дубай или Стамбул, и вас встречают свои: три встречи за три дня с людьми, которых вы искали бы годами.</p></article>
  </div>
</div></section>

<section class="sec-tight gut"><div class="wrap">
  <div class="doors">
    <a class="door rv" href="how.html"><span class="eyebrow">Устройство</span><h3>Круг, отделение, палата, совет</h3><p>Как сеть растёт от девяти стульев до десятков стран и кто за что отвечает.</p><span class="go">Читать →</span></a>
    <a class="door rv" href="degrees.html"><span class="eyebrow">Ступени и ритуалы</span><h3>От гостя до старейшины</h3><p>Пять ступеней, голос шарами, принятие, первый дар и протокол круга.</p><span class="go">Читать →</span></a>
    <a class="door rv" href="world.html"><span class="eyebrow">Карта</span><h3>25 городов, 4 волны</h3><p>Отделения, мосты и правила, по которым сеть приходит в новую страну.</p><span class="go">Открыть карту →</span></a>
  </div>
</div></section>

{motto_band("Двери нет. <span>Есть люди,</span> которые за вас поручатся.", "Сеть не принимает заявок. Сюда приходят только по личному приглашению того, кто уже внутри.")}'''
    return page("index.html", NAME, "Закрытое международное сообщество предпринимателей по модели диаспор: поручительство, кодекс, ступени, отделения и мосты между странами. Вход только по приглашению.", body)


def rings_svg():
    radii = [("council", 236, "Совет мостов"), ("chamber", 186, "Палата"), ("lodge", 136, "Отделение"), ("circle", 82, "Круг")]
    out = []
    for i, (k, r, label) in enumerate(radii):
        dots = ""
        if k == "circle":
            dots = "".join(f'<circle cx="{250 + 52 * math.cos(math.radians(j * 40 - 90)):.1f}" cy="{250 + 52 * math.sin(math.radians(j * 40 - 90)):.1f}" r="5" fill="var(--brass-hi)"/>' for j in range(9))
        elif k == "lodge":
            dots = "".join(f'<circle cx="{250 + 110 * math.cos(math.radians(j * 15)):.1f}" cy="{250 + 110 * math.sin(math.radians(j * 15)):.1f}" r="2" fill="var(--brass)" opacity=".7"/>' for j in range(24) if not 240 <= j * 15 <= 300)
        elif k == "chamber":
            dots = "".join(f'<circle cx="{250 + 161 * math.cos(math.radians(j * 51.4 + 35)):.1f}" cy="{250 + 161 * math.sin(math.radians(j * 51.4 + 35)):.1f}" r="6" fill="none" stroke="var(--brass)"/>' for j in range(7))
        else:
            dots = "".join(f'<circle cx="{250 + 211 * math.cos(math.radians(j * 30 + 15)):.1f}" cy="{250 + 211 * math.sin(math.radians(j * 30 + 15)):.1f}" r="3.2" fill="var(--seal-hi)"/>' for j in range(12))
        fill = ["var(--ink)", "var(--ink-2)", "var(--ink-3)", "var(--ink-4)"][i]
        out.append(f'''<g class="ring" data-k="{k}" tabindex="-1"><circle class="band-c" cx="250" cy="250" r="{r}" fill="{fill}" stroke="var(--line-2)" stroke-width="1"/>{dots}
<text x="250" y="{250 - r + 22}" text-anchor="middle">{label}</text></g>''')
    return f'<svg viewBox="0 0 500 500" role="img" aria-label="Четыре вложенных кольца: круг внутри отделения, отделение внутри палаты, палата внутри совета мостов">{"".join(out)}<circle cx="250" cy="250" r="8" fill="var(--seal-hi)"/></svg>'


def p_how():
    tiers = "".join(f'<button class="tier" type="button" data-k="{k}" aria-pressed="false"><span class="k">{n}</span><span><h3>{E(t)} <small>{E(s)}</small></h3><p>{E(d)}</p></span></button>' for k, n, t, s, d in TIERS)
    roles = "".join(f'<article class="role rv">{sigil(ic)}<span class="t">{E(t)}</span><h3>{E(n)}</h3><p>{E(d)}</p></article>' for n, t, ic, d in ROLES)
    mech = "".join(f'''<details class="rv"{" open" if i == 0 else ""}><summary><span><h3>{E(n)}</h3><span class="src">из традиции: {E(src)}</span></span><span class="pm" aria-hidden="true"></span></summary>
<div class="body"><p>{E(d)}</p><ol class="steps">{"".join(f"<li><span>{E(s)}</span></li>" for s in steps)}</ol></div></details>''' for i, (n, src, d, steps) in enumerate(MECHANISMS))
    rhythm = "".join(f'<div><span class="when">{E(w)}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for w, t, d in RHYTHM)
    disc = "".join(f'<article class="role rv"><span class="t">Сдержанность</span><h3>{E(t)}</h3><p>{E(d)}</p></article>' for t, d in DISCRETION)
    body = f'''{page_head("Устройство", "Четыре кольца, пять должностей, шесть механизмов", "Сеть растёт как ложи и ротари-клубы: самостоятельными ячейками, которые держит один кодекс. Наведите на кольцо или выберите уровень справа.")}

<section class="sec gut"><div class="wrap rings-wrap">
  <div class="rings rv">{rings_svg()}</div>
  <div class="tiers">{tiers}</div>
</div></section>

<section class="sec gut band"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Должности</span><h2>Кто держит отделение</h2><p class="lede">Все должности выборные и без оплаты. Их занимают Поручители и Старейшины.</p></div>
  <div class="roles">{roles}</div>
</div></section>

<section class="sec gut"><div class="wrap marg">
  <div class="side"><span class="roman">VI</span><span class="eyebrow">Механизмы</span></div>
  <div><div class="head-block rv"><h2>Как это работает каждый день</h2></div><div class="mech">{mech}</div></div>
</div></section>

<section class="sec gut band"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Ритм</span><h2>Неделя, месяц, квартал, год</h2></div>
  <div class="rhythm rv">{rhythm}</div>
</div></section>

<section class="sec gut"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Стиль</span><h2>Сдержанность как правило хорошего тона</h2><p class="lede">Закрытость сети означает то же, что в старых клубах: мы не обсуждаем, кто состоит, и не выносим сказанное. Сами правила открыты на этом сайте.</p></div>
  <div class="roles">{disc}</div>
</div></section>

{motto_band("Ячейки самостоятельны. <span>Кодекс один</span> на всех.", "Каждое отделение живёт своей жизнью, но слово, данное в Москве, стоит столько же в Алматы и в Дубае.", ("degrees.html", "Ступени и ритуалы"))}'''
    return page("how.html", "Устройство", "Как устроена Сеть своих: круг, отделение, палата, совет мостов; хранитель, привратник, связной, посол, совет чести; механизмы и ритм.", body)


def p_degrees():
    degs = "".join(f'''<article class="deg rv" style="--a:{.02 + i * .035:.3f};--h:{i * 26}px">{medal(r, i)}<span class="lv">{"Ступень " + r if r != "0" else "До ступеней"} · {E(when)}</span><h3>{E(n)}</h3>
<dl><div><dt>Может</dt><dd>{E(can)}</dd></div><div><dt>Обязан</dt><dd>{E(must)}</dd></div><div><dt>Дальше</dt><dd>{E(nxt)}</dd></div></dl></article>''' for i, (r, n, when, can, must, nxt) in enumerate(DEGREES))
    rites = "".join(f'''<li class="rite rv"><span class="n">{["I","II","III","IV","V","VI","VII","VIII"][i]}</span><div><h3>{E(t)}</h3><p class="what">{E(w)}</p></div>
<div class="detail">{"".join(f"<div><b>{E(k)}</b>{E(v)}</div>" for k, v in det)}</div></li>''' for i, (t, w, det) in enumerate(RITES))
    total = sum(m for _, _, m in PROTOCOL)
    proto = "".join(f'<div class="p"><div><h4>{E(t)}</h4><span class="d">{E(d)}</span></div><span class="m">{m} мин</span><span class="bar" style="--w:{m / total * 100:.1f}%"></span></div>' for t, d, m in PROTOCOL)
    proto += f'<div class="p"><div><h4>Итого</h4><span class="d">Раз в месяц, всегда в одно и то же время.</span></div><span class="m">{total} мин</span></div>'
    yearly = "".join(f'<div><span class="when">Раз в год</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in YEARLY)
    body = f'''{page_head("Ступени и ритуалы", "Пять ступеней и восемь обрядов", "Ступени показывают, сколько доверия у человека в сети. Ритуалы делают вход медленным и запоминающимся, поэтому его ценят.")}

<section class="sec gut"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Ступени</span><h2>Доверие растёт по слову круга</h2><p class="lede">О возвышении не просят. Его предлагает круг, когда человек сделал достаточно для других.</p></div>
  <div class="degrees">{degs}</div>
</div></section>

<section class="sec gut band"><div class="wrap marg">
  <div class="side"><span class="roman">VIII</span><span class="eyebrow">Обряды</span></div>
  <div><div class="head-block rv"><h2>От приглашения до тихого ухода</h2><p class="lede">Обряды идут в этом порядке. Пропустить ни один нельзя, даже по просьбе Старейшины.</p></div><ol class="rites">{rites}</ol></div>
</div></section>

<section class="sec gut"><div class="wrap marg">
  <div class="side"><span class="roman">105′</span><span class="eyebrow">Протокол круга</span></div>
  <div><div class="head-block rv"><h2>Сто пять минут, которые держат сеть</h2><p class="lede">Круг собирается по одному и тому же протоколу по всему миру. Гость из Дубая на круге в Казани сразу знает, что будет дальше.</p></div>
  <div class="protocol rv">{proto}</div></div>
</div></section>

<section class="sec gut band"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Годовой круг</span><h2>Три вечера, которые помнят весь год</h2></div>
  <div class="rhythm rv" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))">{yearly}</div>
</div></section>

{motto_band("Медленный вход — <span>крепкое доверие.</span>", "Месяц от приглашения до принятия кажется долгим. Зато каждый, кого вы встретите внутри, прошёл тот же путь.", ("code.html", "Кодекс и принятие"))}'''
    return page("degrees.html", "Ступени и ритуалы", "Пять ступеней Сети своих от гостя до старейшины, восемь обрядов от приглашения до тихого ухода, протокол круга и годовой цикл.", body)


def p_code():
    items = "".join(f'<li class="rv"><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for t, d in CODE)
    vows = "".join(f'<article class="vow rv"><span class="eyebrow">Обет · {E(d)}</span><blockquote>«{E(v)}»</blockquote></article>' for d, v in VOWS)
    court = "".join(f'<div class="rv"><span class="eyebrow">Шаг {i + 1}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(COURT))
    js = "<script>window.CODE=" + json.dumps(CODE, ensure_ascii=False) + ";</script>\n"
    body = f'''{page_head("Кодекс", "Десять правил, одно слово", "Кодекс один для всех отделений и всех стран. Его читают вслух при принятии, и менять его может только Совет мостов.")}

<section class="sec gut"><div class="wrap"><ol class="code-list">{items}</ol></div></section>

<section class="sec gut band" id="oath"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Принятие</span><h2>Пройдите кодекс так, как его проходят при вступлении</h2><p class="lede">Десять правил по одному. На каждом нужно решить, готовы ли вы его держать.</p></div>
  <div class="oath">
    <div class="pips" aria-hidden="true"></div>
    <div class="stage" aria-live="polite"><span class="k">Перед кругом</span><h3>Новик читает кодекс вслух</h3><p>Поручитель стоит рядом. Свои отделения слушают. После последнего правила новик говорит: «Даю слово».</p></div>
    <button class="btn btn-brass" type="button" data-act="go">Начать</button>
    <div class="stamp" aria-hidden="true">{WAX}</div>
  </div>
</div></section>

<section class="sec gut"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Обеты ступеней</span><h2>На каждой ступени даётся своё слово</h2></div>
  <div class="vows">{vows}</div>
</div></section>

<section class="sec gut band"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Совет чести</span><h2>Как сеть поступает с нарушившими слово</h2><p class="lede">Без публичных разборок и чёрных списков. Решение одно на всю сеть.</p></div>
  <div class="court">{court}</div>
</div></section>

{motto_band("Обещал — сделай. <span>Не можешь —</span> скажи сразу.", "Из всех правил это вспоминают чаще всего. На нём держится всё остальное.", ("path.html", "Путь участника"))}'''
    return page("code.html", "Кодекс", "Кодекс Сети своих: десять правил, обеты ступеней, совет чести и интерактивное принятие кодекса.", body, extra_js=js)


def world_svg():
    d = json.load(open(os.path.join(os.path.dirname(__file__), "land-dots.json")))
    L0, B1, S, K = d["L0"], d["B1"], d["S"], 6.4
    W, H = len(d["rows"][0]) * K, len(d["rows"]) * K
    parts = []
    for y, row in enumerate(d["rows"]):
        for x, ch in enumerate(row):
            if ch == "1":
                parts.append(f"M{x * K + 3.2:.1f} {y * K + 3.2:.1f}h0")
    land = "".join(parts)

    def xy(lon, lat):
        return ((lon - L0) / S * K + 3.2, (B1 - lat) / S * K + 3.2)

    pos = {c[0]: xy(c[2], c[3]) for c in CITIES}
    ph = {c[0]: c[4] for c in CITIES}
    arcs = []
    for a, b in ARCS:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dist = math.hypot(x2 - x1, y2 - y1)
        cx, cy = mx, my - dist * 0.28
        p = max(ph[a], ph[b])
        arcs.append(f'<path class="arc p{p}" data-ph="{p}" d="M{x1:.1f} {y1:.1f} Q{cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}"/>')
    # подписи: (dx, dy, выравнивание); по умолчанию справа
    lab = {"spb": (0, -11, "middle"), "min": (-9, 4, "end"), "msk": (0, 18, "middle"), "kzn": (0, -11, "middle"),
           "ekb": (0, -11, "middle"), "lon": (-9, 4, "end"), "ber": (0, -11, "middle"), "beg": (-9, 4, "end"),
           "ist": (-9, 4, "end"), "lim": (-9, 4, "end"), "tlv": (-9, 8, "end"), "tbs": (-7, -6, "end"),
           "evn": (-7, 12, "end"), "tas": (0, 17, "middle"), "sha": (-9, -6, "end"), "han": (-9, 4, "end"),
           "bkk": (-9, 4, "end")}
    cities = []
    for cid, name, lon, lat, p, role, br in CITIES:
        x, y = pos[cid]
        r = 4.5 if p == "0" else 3.5
        dx, dy, anchor = lab.get(cid, (9, 4, "start"))
        tx, ty = x + dx, y + dy
        cities.append(f'<g class="city ph{p}" data-id="{cid}" data-ph="{p}" tabindex="0" role="button" aria-label="{E(name)}"><circle class="halo" cx="{x:.1f}" cy="{y:.1f}" r="{r + 2}"/><circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="transparent"/><text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{E(name)}</text></g>')
    return f'<svg class="map-svg" viewBox="0 0 {W} {H}" role="group" aria-label="Карта задуманных отделений и мостов"><path class="land" d="{land}"/>{"".join(arcs)}{"".join(cities)}</svg>'


def p_world():
    js_data = {c[0]: {"name": c[1], "phase": f"{PHASES[c[4]][0]} · {PHASES[c[4]][1]}", "role": c[5], "bridges": c[6]} for c in CITIES}
    js = "<script>window.CITIES=" + json.dumps(js_data, ensure_ascii=False) + ";</script>\n"
    dotc = {"0": "var(--brass-hi)", "1": "var(--brass)", "2": "var(--paper-2)", "3": "transparent;border:1px solid var(--paper-2)"}
    chips = '<button class="chip" type="button" data-f="all" aria-pressed="true">Все волны</button>' + "".join(
        f'<button class="chip" type="button" data-f="{k}" aria-pressed="false"><i style="background:{dotc[k]}"></i>{E(v[0])}</button>' for k, v in PHASES.items())
    phases = "".join(f'<div class="phase rv"><span class="when">{E(v[1])}</span><h3>{E(v[0])}</h3><p>{E(v[2])}</p><p class="small num" style="color:var(--brass)">{sum(1 for c in CITIES if c[4] == k)} городов</p></div>' for k, v in PHASES.items())
    opening = "".join(f'<li class="rite rv"><span class="n">{["I","II","III","IV","V"][i]}</span><div><h3>{E(t)}</h3><p class="what">{E(d)}</p></div></li>' for i, (t, d) in enumerate(OPEN_CHAPTER))
    modes = "".join(f'<article class="mode rv"><span class="lamp" style="background:{c}"></span><h3>{E(t)}</h3><p>{E(d)}</p></article>' for t, c, d in BRIDGE_MODES)
    body = f'''{page_head("Карта", "Федерация отделений от Москвы до Нью-Йорка", "Так сеть задумана на четыре года вперёд. Отделение появляется в городе, только когда там есть свои люди, поэтому карта растёт медленно и надёжно.")}

<section class="sec-tight gut"><div class="wrap">
  <div class="map-shell rv">
    <div class="map-bar">{chips}</div>
    <p class="map-hint">Нажмите на город. На телефоне карту можно сдвигать</p>
    <div class="map-scroll">{world_svg()}</div>
    <div class="map-panel" id="map-panel" aria-live="polite">
      <div><span class="eyebrow" data-f="eyebrow"></span><h3 data-f="name"></h3></div>
      <div class="stack"><p data-f="role"></p><p class="small num" style="color:var(--brass-hi)" data-f="bridges"></p></div>
    </div>
  </div>
</div></section>

<section class="sec gut"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Четыре волны</span><h2>В каком порядке сеть приходит в мир</h2></div>
  <div class="phases">{phases}</div>
</div></section>

<section class="sec gut band"><div class="wrap marg">
  <div class="side"><span class="roman">V</span><span class="eyebrow">Новое отделение</span></div>
  <div><div class="head-block rv"><h2>Как открывается отделение в новом городе</h2><p class="lede">Как ганзейское подворье: сначала свои люди на месте, потом устав, потом знак.</p></div><ol class="rites">{opening}</ol></div>
</div></section>

<section class="sec gut"><div class="wrap">
  <div class="head-block rv"><span class="eyebrow">Мосты</span><h2>Три режима моста</h2><p class="lede">Отношения между странами меняются. Мост между отделениями переключает Совет мостов, а дружба между людьми остаётся их личным делом.</p></div>
  <div class="modes">{modes}</div>
</div></section>

{motto_band("Свой в Москве — <span>свой</span> в Алматы и в Дубае.", "Гость из другого отделения получает три встречи за три дня. Ужин за счёт хозяина: так принимали своих ливанцы и армяне.", ("path.html", "Путь участника"))}'''
    return page("world.html", "Карта", "Интерактивная карта задуманных отделений Сети своих: 25 городов в четырёх волнах, мосты между странами и правила открытия нового отделения.", body, extra_js=js)


def p_path():
    steps = "".join(f'''<div class="step"><span class="pin">{n}</span><div class="body"><div class="main"><span class="when">{E(w)}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>
<div class="gets"><div><b>Вы получаете</b>{E(g)}</div><div><b>От вас</b>{E(m)}</div></div></div></div>''' for n, w, t, d, g, m in PATH)
    body = f'''{page_head("Путь участника", "Пять лет от карточки до совета чести", "Восемь остановок. Первые четыре занимают около месяца, остальные зависят только от того, сколько вы сделаете для других.")}

<section class="sec gut"><div class="wrap"><div class="path"><span class="fill" aria-hidden="true"></span>{steps}</div></div></section>

{motto_band("Чем больше отдаёшь, <span>тем дальше</span> проходишь.", "Ступени нельзя купить, выслужить временем или попросить. Их даёт круг за дела для других.")}'''
    return page("path.html", "Путь участника", "Путь участника Сети своих: приглашение, беседа, гостевое собрание, голос шарами, первый дар и ступени до старейшины.", body)


def p_invite():
    qa = "".join(f'<details class="qa"{" open" if i == 0 else ""}><summary>{E(q)}</summary><div><p>{E(a)}</p></div></details>' for i, (q, a) in enumerate(FAQ))
    body = f'''{page_head("Вход", "Сюда не подают заявку", "Сеть не принимает писем, анкет и звонков. Есть только один путь: личное приглашение того, кто уже внутри и готов за вас поручиться.")}

<section class="sec gut"><div class="wrap invite">
  <div>
    <div class="env" id="env">
      <div class="back"></div>
      <div class="letter"><h4>Вас приглашают к своим</h4>
        <p>Этот конверт вам передали из рук в руки. Значит, кто-то готов отвечать за вас своим словом.</p>
        <p>Откройте ссылку, которую дал поручитель, прочитайте кодекс и решите, готовы ли вы его держать. Привратник свяжется с вами в течение недели.</p>
        <span class="sig">{MOTTO} · {NAME}</span></div>
      <div class="flap"></div><div class="front"></div>
      <button class="wax" type="button" aria-label="Сломать печать и открыть письмо">{WAX}</button>
    </div>
    <p class="env-cta">Нажмите на печать</p>
  </div>
  <div class="stack" style="gap:28px">
    <div class="stack"><span class="eyebrow">Если вам вручили приглашение</span><h2>Четыре шага до принятия</h2></div>
    <ol class="how-in">
      <li><span><b>Ссылка поручителя</b><span>Откройте её в Telegram. Бот покажет кодекс и спросит, принимаете ли вы его.</span></span></li>
      <li><span><b>Беседа у привратника</b><span>Сорок минут за чаем, три вопроса о вас и вашем деле.</span></span></li>
      <li><span><b>Гостевое собрание</b><span>Вы видите отделение, отделение видит вас.</span></span></li>
      <li><span><b>Голос и принятие</b><span>Белые и чёрные шары, затем кодекс вслух и рукопожатие трёх.</span></span></li>
    </ol>
    <div class="row"><a class="btn btn-brass" href="{TG_BOT}" rel="noopener">Открыть бота-привратника <span class="arr">→</span></a><a class="btn" href="path.html">Весь путь</a></div>
    <p class="small mute">Без ссылки поручителя бот только покажет кодекс. Пустить в сеть он не может.</p>
  </div>
</div></section>

<section class="sec gut band"><div class="wrap marg">
  <div class="side"><span class="roman">?</span><span class="eyebrow">Если приглашения нет</span></div>
  <div class="stack" style="gap:28px">
    <h2 class="rv">Как стать человеком, которого зовут</h2>
    <div class="prose rv">
      <p>Приглашают тех, кто уже ведёт себя как свой: держит слово, помогает без расчёта и не болтает о чужих делах. Спросите знакомых предпринимателей, которым доверяете. Возможно, кто-то из них уже внутри и ждёт, когда вы спросите сами.</p>
      <p>Если в вашем городе отделения пока нет, оно появится, когда там наберутся трое своих. Приглашение тогда придёт тоже лично.</p>
    </div>
  </div>
</div></section>

<section class="sec gut" id="faq"><div class="wrap marg">
  <div class="side"><span class="roman">VII</span><span class="eyebrow">Вопросы</span></div>
  <div>{qa}</div>
</div></section>'''
    return page("invite.html", "Вход по приглашению", "Как попасть в Сеть своих: только по личному приглашению поручителя. Четыре шага до принятия и ответы на частые вопросы.", body)


def p_404(full=True):
    body = f'''<section class="page-head gut" style="border:0"><div class="bg-seal" aria-hidden="true">{seal()}</div><div class="wrap">
  <span class="eyebrow">Ошибка 404</span><h1>Этой двери здесь нет</h1><p class="lede">Возможно, её никогда и не было. Начните с манифеста.</p>
  <div class="row"><a class="btn btn-brass" href="index.html">На главную <span class="arr">→</span></a></div></div></section>'''
    return page("404.html", "Страница не найдена", "Страница не найдена.", body, full)


PAGES = {"index.html": p_index, "how.html": p_how, "degrees.html": p_degrees, "code.html": p_code,
         "world.html": p_world, "path.html": p_path, "invite.html": p_invite, "404.html": p_404}


def build():
    for fn, f in PAGES.items():
        open(os.path.join(ROOT, fn), "w", encoding="utf-8").write(f())
    fav = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#0C1D1A"/>{LOGO[LOGO.index(">") + 1:-6]}</svg>'
    for k, v in {"var(--brass)": "#C9A45C", "var(--paper)": "#ECE5D3", "var(--seal-hi)": "#B23C45"}.items():
        fav = fav.replace(k, v)
    open(os.path.join(ROOT, "assets", "favicon.svg"), "w").write(fav)
    open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    print("built", len(PAGES), "pages")


def build_artifact(out):
    """Копия для превью на claude.ai: главная без <html>/<head>, остальные страницы целые."""
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    import shutil
    for a in ("style.css", "site.js", "favicon.svg"):
        shutil.copy(os.path.join(ROOT, "assets", a), os.path.join(out, "assets", a))
    for fn in PAGES:
        if fn == "404.html":
            continue
        src = open(os.path.join(ROOT, fn), encoding="utf-8").read()
        if fn == "index.html":
            src = src.split('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n', 1)[1]
            src = src.replace("</head>\n<body>", "").replace("</body>\n</html>", "")
        open(os.path.join(out, fn), "w", encoding="utf-8").write(src)
    print("artifact copy in", out)


if __name__ == "__main__":
    build()
    if "--artifact" in sys.argv:
        build_artifact(sys.argv[sys.argv.index("--artifact") + 1])
