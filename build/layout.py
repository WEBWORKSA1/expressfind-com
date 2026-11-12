"""Shared page shell: head, owner banner, header, footer, modals."""
import json
from html import escape
from icons import icon, LOGO

SITE = "https://expressfind.com"
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
OWNER_URL = "https://web.works/contact"

NAV = [
    ("get-quotes.html", "Find a Pro"),
    ("emergency.html", "Emergency"),
    ("costs.html", "Cost Guides"),
    ("tools.html", "Tools"),
    ("videos.html", "Videos"),
    ("pros.html", "For Pros"),
]


def canon(path):
    if path == "index.html":
        return SITE + "/"
    return f"{SITE}/{path}"


def header():
    items = "".join(f'<li><a href="@/{h}">{t}</a></li>' for h, t in NAV)
    return f"""<header class="site-header"><div class="wrap nav">
<a class="brand" href="@/index.html" aria-label="ExpressFind home">{LOGO}<span>Express<b>Find</b></span></a>
<ul class="menu" id="menu">{items}</ul>
<div class="nav-cta">
<a class="btn btn-red btn-sm" href="@/emergency.html">{icon('alert')} <span>Emergency</span></a>
<a class="btn btn-amber btn-sm" href="@/get-quotes.html">Get Free Quotes</a>
<button class="icon-btn" id="themeBtn" type="button" aria-label="Toggle dark mode">{icon('moon')}</button>
<button class="icon-btn burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu">{icon('menu')}</button>
</div></div></header>"""


def footer():
    col = lambda title, links: "<div><h4>" + title + "</h4><ul>" + "".join(f'<li><a href="@/{h}">{t}</a></li>' for h, t in links) + "</ul></div>"
    return f"""<footer class="site-footer"><div class="wrap">
<div class="fgrid">
<div><a class="brand" href="@/index.html">{LOGO}<span>Express<b>Find</b></span></a>
<p style="margin-top:14px;font-size:.93rem">Fast help, fair prices and trusted pros for home emergencies and repairs across the US and Canada. Free for homeowners.</p>
<form class="js-form mini-form" data-subject="Newsletter signup" data-ok="You're in. Watch for seasonal checklists and price alerts." aria-label="Newsletter signup">
<input type="email" name="email" required placeholder="Email for seasonal alerts" aria-label="Email address"><input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="hidden" name="list" value="Footer newsletter">
<button class="btn btn-amber btn-sm" type="submit">Join</button><div class="form-msg" role="status" aria-live="polite" style="flex-basis:100%"></div></form></div>
{col('Homeowners', [('get-quotes.html','Get free quotes'),('costs.html','Cost guides'),('tools.html','Free tools'),('videos.html','How-to videos'),('tools/maintenance-calendar.html','Maintenance calendar'),('tools/license-lookup.html','Check a license')])}
{col('Emergency', [('emergency.html','Emergency help'),('emergency/burst-pipe.html','Burst pipe'),('emergency/no-heat.html','No heat'),('emergency/gas-smell.html','Smell gas'),('emergency/roof-leak.html','Roof leak'),('emergency/locked-out.html','Locked out')])}
{col('Company', [('about.html','About'),('methodology.html','How we research costs'),('pros.html','Join as a pro'),('advertise.html','Advertise &amp; sponsor'),('support.html','Support us'),('contests.html','Contests &amp; prizes'),('careers.html','Careers'),('contact.html','Contact')])}
{col('Legal', [('privacy.html','Privacy policy'),('terms.html','Terms of use'),('disclaimer.html','Disclaimer'),('cookies.html','Cookie policy'),('trademark.html','Trademark &amp; copyright'),('sitemap.html','Sitemap')])}
</div>
<p class="disclose">ExpressFind is a free information and matching service, not a contractor. When you request quotes, your request may be shared with up to three independent service providers, and we may be paid by providers and advertisers. Cost figures are estimates. In an emergency that threatens life or safety, call 911 first.</p>
<div class="fbottom"><span>© <span class="year">2026</span> ExpressFind.com. "ExpressFind" is used descriptively; no trademark is claimed. <a href="@/trademark.html">Disclosure</a>.</span><span>Website, domain &amp; partnership inquiries: <a href="{OWNER_URL}" target="_blank" rel="noopener">web.works/contact</a></span></div>
</div></footer>"""


def overlays():
    return f"""<div class="sticky-cta" id="stickyCta"><a class="btn btn-red" href="@/emergency.html">{icon('alert')} Emergency</a><a class="btn btn-amber" href="@/get-quotes.html">Get free quotes</a></div>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie notice"><strong>Cookies &amp; ads</strong><p style="margin:6px 0 0">We use cookies for essential features and Google may use cookies to show and measure ads. See our <a href="@/cookies.html">Cookie policy</a> and <a href="@/privacy.html">Privacy policy</a>.</p><div class="acts"><button class="btn btn-dark btn-sm" type="button" data-cookie="accepted">Accept</button><button class="btn btn-ghost btn-sm" type="button" data-cookie="essential">Essential only</button></div></div>
<div class="modal" id="leadMagnet" role="dialog" aria-modal="true" aria-labelledby="lmTitle"><div class="box">
<button class="icon-btn x" type="button" data-close aria-label="Close">{icon('x')}</button>
<span class="badge amber">Free printable</span>
<h2 id="lmTitle" style="margin-top:12px;font-size:1.6rem">Before you go: get the Home Emergency Playbook</h2>
<p class="muted">Shutoff locations, a 15-item emergency kit, who to call first, and a fridge card for your family. One page. Free.</p>
<form class="js-form" data-subject="Lead magnet: Home Emergency Playbook" data-ok="Done — your playbook is unlocked below." data-unlock="#lmUnlock">
<div class="field"><label for="lm-email">Email</label><input id="lm-email" type="email" name="email" required autocomplete="email"></div>
<input type="hidden" name="list" value="Emergency Playbook"><input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="check" style="margin-bottom:14px"><input type="checkbox" name="consent" value="yes" required> <span>Send me the playbook and occasional seasonal home tips. Unsubscribe anytime.</span></label>
<button class="btn btn-amber btn-block" type="submit">Get my free playbook</button><div class="form-msg" role="status" aria-live="polite"></div></form>
<p id="lmUnlock" hidden style="margin-top:14px"><a class="btn btn-dark btn-block" href="@/tools/emergency-kit.html">Open the printable playbook →</a></p>
</div></div>"""


def breadcrumb_ld(crumbs, path):
    items = []
    for i, (name, href) in enumerate(crumbs, 1):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": canon(href) if href else canon(path)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def crumbs_html(crumbs):
    if not crumbs:
        return ""
    parts = []
    for name, href in crumbs:
        parts.append(f'<a href="@/{href}">{escape(name)}</a>' if href else escape(name))
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"


def page(path, title, description, body, crumbs=None, schema=None, og_type="website", noindex=False, build="1", extra_head=""):
    depth = path.count("/")
    root = "../" * depth
    ld = list(schema or [])
    if crumbs:
        ld.append(breadcrumb_ld(crumbs, path))
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    t, d = escape(title), escape(description)
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{canon(path)}">
<meta name="robots" content="{robots}">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<meta name="theme-color" content="#0B1B2B">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="ExpressFind">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:url" content="{canon(path)}"><meta property="og:image" content="{SITE}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{SITE}/assets/img/og.png">
<link rel="icon" href="@/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="@/assets/img/icon-192.png">
<link rel="manifest" href="@/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="ExpressFind guides" href="@/feed.xml">
<script>document.documentElement.className+=' js';try{{var t=localStorage.getItem('ef-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="@/assets/css/style.css?v={build}">
{ADSENSE}
{extra_head}{ld_html}
</head>
<body data-root="@/">
<a class="skip" href="#main">Skip to content</a>
<div class="ownerbar" role="note"><a href="{OWNER_URL}" target="_blank" rel="noopener">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership →</a></div>
{header()}
<main id="main">
{body}
</main>
{footer()}
{overlays()}
<script src="@/assets/js/main.js?v={build}" defer></script>
</body>
</html>
"""
    return html.replace("@/", root)
