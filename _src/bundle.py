"""Собирает весь сайт в один HTML-файл для пересылки: python3 _src/bundle.py OUT.html

Сначала запустите build.py. Страницы переключаются по #якорю, CSS, JS и значок встроены.
"""
import base64, os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
PAGES = ["index", "how", "degrees", "code", "world", "path", "invite"]
ANCHORS = {"faq": "invite", "oath": "code"}  # якоря внутри страниц


def fix(t):
    names = "|".join(PAGES)
    t = re.sub(rf'href="(?:{names})\.html#([a-z]+)"', r'href="#\1"', t)
    return re.sub(rf'href="({names})\.html"', r'href="#\1"', t)


def bundle(out):
    css = open(R + "assets/style.css").read()
    js = open(R + "assets/site.js").read()
    fav = base64.b64encode(open(R + "assets/favicon.svg", "rb").read()).decode()
    idx = open(R + "index.html").read()
    head = idx[:idx.index('<link rel="stylesheet" href="assets/style.css">')]
    head = head.replace('href="assets/favicon.svg"', f'href="data:image/svg+xml;base64,{fav}"')
    hdr = fix(re.search(r'<a class="skip".*?</header>', idx, re.S).group(0)).replace(' aria-current="page"', "")
    ftr = fix(re.search(r"<footer.*?</footer>", idx, re.S).group(0))
    mains, data = [], []
    for p in PAGES:
        s = open(R + p + ".html").read()
        m = re.search(r'<main id="main">(.*?)</main>', s, re.S).group(1)
        mains.append(f'<div class="pg" data-page="{p}"{"" if p == "index" else " hidden"}>{fix(m)}</div>')
        data += re.findall(r"<script>window\.[A-Z]+=.*?</script>", s, re.S)
    router = """<script>(function(){var P=%s,A=%s;
function go(){var h=(location.hash||"#index").slice(1),pg=P.indexOf(h)>=0?h:(A[h]||"index");
document.querySelectorAll(".pg").forEach(function(e){e.hidden=e.dataset.page!==pg});
document.querySelectorAll(".nav a").forEach(function(a){if(a.getAttribute("href")==="#"+pg)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current")});
if(A[h]){var t=document.getElementById(h);if(t)t.scrollIntoView()}else scrollTo(0,0);dispatchEvent(new Event("scroll"))}
addEventListener("hashchange",go);go();})();</script>""" % (str(PAGES).replace("'", '"'), str(ANCHORS).replace("'", '"'))
    html = f"""{head}<style>
{css}
</style>
</head>
<body>
{hdr}
<main id="main">
{chr(10).join(mains)}
</main>
{ftr}
{"".join(data)}
<script>
{js}
</script>
{router}
</body>
</html>
"""
    open(out, "w", encoding="utf-8").write(html)
    print("bundle", out, len(html), "bytes")


if __name__ == "__main__":
    bundle(sys.argv[1] if len(sys.argv) > 1 else R + "site-bundle.html")
