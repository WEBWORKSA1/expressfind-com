#!/usr/bin/env python3
"""ExpressFind.com static site generator. Run: python3 build/build.py"""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import ROOT_DIR, REVIEWED, SERVICES, CATS, VIDEOS, VCATS, load_cpi, adj, money, rnd, e
from icons import icon
from layout import page, canon, crumbs_html, SITE
from content_costs import GUIDES, SYSTEMS
from content_emergency import PLAYBOOKS
import pages as P
import tools_pages as T

CPI = load_cpi()
F = float(CPI.get("factor", 1.0))
TODAY = datetime.date.today()
BUILD = TODAY.strftime("%Y%m%d")
GBY = {g["slug"]: g for g in GUIDES}
PBY = {p["slug"]: p for p in PLAYBOOKS}
OUT = []  # (path, priority)


def write(path, html, prio="0.6"):
    full = os.path.join(ROOT_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    OUT.append((path, prio))


def render(path, title, desc, body, prio="0.6", **kw):
    write(path, page(path, title, desc, body, build=BUILD, **kw), prio)


# ---------------------------------------------------------------- shared bits
def est_json():
    svc = {}
    for g in GUIDES:
        svc[g["slug"]] = {"name": g["name"], "guide": g["slug"], "quote": g["quote"], "sev": {k: list(v) for k, v in g["sev"].items()},
                          "sevText": g["sevText"], "typical": list(g["typical"]), "cap": g["cap"]}
    return '<script type="application/json" id="estData">' + json.dumps({"factor": F, "services": svc}) + "</script>"


def pulse_html():
    yo = CPI.get("yoy_repair")
    ya = CPI.get("yoy_all")
    if yo is None and ya is None:
        return (f'<div class="pulse">{icon("dollar")}<span><b>Price Pulse</b></span><span class="muted">Cost ranges compiled {REVIEWED} and re-checked weekly against U.S. inflation data (BLS CPI). '
                f'<a href="@/methodology.html">How we keep prices current →</a></span></div>')
    parts = []
    if yo is not None:
        cls = "up" if yo > 0 else "down"
        parts.append(f'<span>Household repair prices <b class="{cls}">{yo:+.1f}%</b> year over year</span>')
    if ya is not None:
        cls = "up" if ya > 0 else "down"
        parts.append(f'<span>All consumer prices <b class="{cls}">{ya:+.1f}%</b></span>')
    return (f'<div class="pulse">{icon("dollar")}<span><b>Price Pulse</b></span>{"".join(parts)}<span class="muted">BLS CPI, data through {e(CPI.get("data_label", CPI.get("label", "")))}. '
            f'<a href="@/methodology.html">Method</a></span></div>')


SEASONAL = [
    "January: Watch for frozen pipes. Keep the heat at or above 55°F (13°C) and let faucets drip on the coldest nights.",
    "February: Check the furnace filter, test CO alarms and clear snow from high-efficiency furnace vent pipes.",
    "March: Inspect the roof and gutters for winter damage before spring rains arrive.",
    "April: Test the sump pump and extend downspouts away from the foundation.",
    "May: Book an AC tune-up before the first heat wave fills technicians' calendars.",
    "June: Clear debris from around the outdoor AC unit and flush the condensate drain line.",
    "July: Peak storm and heat season. Know where your main water shutoff and breaker panel are.",
    "August: Have trees near the house checked before storm season peaks.",
    "September: Schedule furnace maintenance and replace filters before heating season.",
    "October: Disconnect garden hoses, shut off exterior faucets and insulate exposed pipes.",
    "November: Test smoke and CO alarms, check space heaters and clean the dryer vent.",
    "December: Keep heat on while traveling and ask someone to check the house during cold snaps.",
]


def seasonal_html():
    ps = "".join(f'<p data-month="{i}" hidden style="margin:0">{e(t)}</p>' for i, t in enumerate(SEASONAL))
    return f'<div class="callout info">{icon("calendar")}<div><strong>This month at home</strong>{ps}<p style="margin:6px 0 0"><a href="@/tools/maintenance-calendar.html">Open the full maintenance calendar →</a></p></div></div>'


def svc_options(selected=""):
    return "".join(f'<option value="{e(s)}"{" selected" if s == selected else ""}>{e(s)}</option>' for s, _ in SERVICES)


def finder(urgency=None, label="Get free quotes"):
    du = f' data-urgency="{urgency}"' if urgency else ""
    return (f'<form class="finder" action="@/get-quotes.html"{du} aria-label="Find a pro">'
            f'<label class="hp" for="f-svc">Service</label><select id="f-svc" name="service" aria-label="What do you need?">{svc_options()}</select>'
            f'<input name="zip" inputmode="text" autocomplete="postal-code" placeholder="ZIP or postal code" aria-label="ZIP or postal code" maxlength="10">'
            f'<button class="btn btn-amber" type="submit">{label} {icon("arrow")}</button></form>')


def guide_card(g):
    return (f'<a class="card card-link reveal" data-item data-cat="{g["cat"]}" href="@/costs/{g["slug"]}.html"><div class="ico">{icon(g["icon"])}</div>'
            f'<h3>{e(g["name"])} cost</h3><div class="price-tag">{adj(g["low"], F)} – {adj(g["high"], F)}</div>'
            f'<p class="muted" style="font-size:.92rem">{e(g["unit"])}</p><span class="more">See the full breakdown →</span></a>')


def play_card(p):
    return (f'<a class="card card-link reveal" data-item href="@/emergency/{p["slug"]}.html"><div class="ico" style="color:var(--red)">{icon(p["icon"])}</div>'
            f'<h3>{e(p["name"])}</h3><p class="muted" style="font-size:.93rem">{e(p["quick"][0])}.</p><span class="more">Open the playbook →</span></a>')


def video_block(vid, title, ch):
    return f'<div class="video" data-yt="{vid}" data-title="{e(title)}"></div><p class="vcap"><strong>{e(title)}</strong><span>Video: {e(ch)} on YouTube</span></p>'


def faq_html(faqs):
    return "".join(f'<details class="faq"><summary>{e(q)}</summary><div>{e(a)}</div></details>' for q, a in faqs)


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def cta_band(title, text, href, btn, red=False):
    cls = "btn-red" if red else "btn-amber"
    return (f'<section class="section-tight"><div class="wrap"><div class="band"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<div><a class="btn {cls} btn-block" href="{href}">{btn}</a><p style="font-size:.85rem;margin:10px 0 0;color:#9fb3c6">Free · No obligation · US &amp; Canada</p></div></div></div></section>')


# ---------------------------------------------------------------- cost guides
def build_guide(g):
    path = f"costs/{g['slug']}.html"
    mid = (g["low"] + g["high"]) / 2
    rows = "".join(f'<tr><td>{e(j)}</td><td class="num">{adj(lo, F, u)} – {adj(hi, F, u)}{" / sq ft" if u == "sqft" else ""}</td><td class="muted">{e(n)}</td></tr>' for j, lo, hi, u, n in g["rows"])
    factors = "".join(f"<li><strong>{e(t)}.</strong> {e(x)}</li>" for t, x in g["factors"])
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    sources = "".join(f'<li><a href="{s[1]}" target="_blank" rel="noopener nofollow">{e(s[0])}</a></li>' for s in g["sources"])
    rel_pb = "".join(f'<li><a href="@/emergency/{s}.html">{e(PBY[s]["name"])} playbook</a></li>' for s in g["related"] if s in PBY)
    others = [x for x in GUIDES if x["cat"] == g["cat"] and x["slug"] != g["slug"]][:3] or [x for x in GUIDES if x["slug"] != g["slug"]][:3]
    rel_g = "".join(f'<li><a href="@/costs/{x["slug"]}.html">{e(x["name"])} cost</a></li>' for x in others)
    video = ""
    if g.get("video"):
        v = next((x for x in VIDEOS if x["id"] == g["video"]), None)
        if v:
            video = f'<h2 id="video">Watch: a quick how-to</h2>{video_block(v["id"], v["title"], v["ch"])}'
    sevsel = "".join(f'<option value="{k}"{" selected" if k == "moderate" else ""}>{k.title()} — {e(g["sevText"][k])}</option>' for k in ("minor", "moderate", "major"))
    mini = (f'<div class="tool mini-est" data-svc="{g["slug"]}" style="margin:22px 0"><h3 style="margin-top:0">{icon("calc")} Quick estimate</h3>'
            f'<div class="row"><div class="field"><label>How big is the job?</label><select name="sev">{sevsel}</select></div>'
            f'<div class="field"><label>When do you need it?</label><select name="tm"><option value="1">Business hours</option><option value="1.5">Evening</option><option value="1.75">Weekend</option><option value="2">Holiday / overnight</option></select></div></div>'
            f'<div class="out"><small>Estimated range</small><div class="big mini-out">—</div><p>National estimate. Use the <a href="@/tools/cost-estimator.html?service={g["slug"]}" style="color:var(--amber)">full estimator</a> to adjust for your region.</p></div></div>')
    body = f"""<section class="page-hero"><div class="wrap">{crumbs_html([("Home","index.html"),("Cost guides","costs.html"),(g["name"],None)])}
<span class="eyebrow">Cost guide</span><h1>{e(g["title"])}</h1><p class="lead">{e(g["desc"])}</p>
<div class="meta-line"><span>{icon("calendar")} Reviewed {REVIEWED}</span><span>{icon("dollar")} Prices adjusted for inflation through {e(CPI.get("label", REVIEWED))}</span><span>{icon("pin")} US national estimates (USD)</span></div></div></section>
<section><div class="wrap layout"><article class="prose">
<div class="range-card"><div><small>Low</small><strong>{adj(g["low"], F)}</strong></div><div class="hl"><small>Typical midpoint</small><strong>{adj(mid, F)}</strong></div><div><small>High</small><strong>{adj(g["high"], F)}</strong></div></div>
<p class="muted" style="margin-top:-14px">Range {e(g["unit"])}. Your price depends on your market, the timing of the call and what the pro finds on site.</p>
{''.join(f"<p>{e(p)}</p>" for p in g["intro"])}
<h2 id="jobs">What common jobs cost</h2>
<div class="table-wrap"><table class="data"><thead><tr><th>Job</th><th>Typical range</th><th>Notes</th></tr></thead><tbody>{rows}</tbody></table></div>
{mini}
<h2 id="factors">What drives the price</h2><ul>{factors}</ul>
<h2 id="emergency">Emergency and after-hours pricing</h2><p>{e(g["premium"])}</p>
<div class="callout warn">{icon("alert")}<p><strong>Safety first.</strong> If anything involves fire, smoke, a gas smell, a downed power line or someone who is hurt, call 911 before you call a contractor.</p></div>
<h2 id="save">How to save money</h2><ul>{li(g["save"])}</ul>
<h2 id="ask">Questions to ask before you hire</h2><ol>{li(g["ask"])}</ol>
<h2 id="flags">Red flags</h2><ul>{li(g["flags"])}</ul>
{video}
<h2 id="faq">Frequently asked questions</h2>{faq_html(g["faqs"])}
<h2 id="sources">Sources consulted</h2><p class="muted" style="font-size:.93rem">We compare several independent cost surveys and contractor price lists, then publish a rounded range. Figures are summarized in our own words. See our <a href="@/methodology.html">methodology</a>.</p><ul style="font-size:.93rem">{sources}</ul>
<div class="share no-print" style="margin-top:20px"><button class="btn btn-ghost btn-sm" type="button" data-share>{icon("share")} Share this guide</button><button class="btn btn-ghost btn-sm" type="button" data-print>{icon("printer")} Print</button></div>
</article>
<aside class="aside">
<div class="card"><h3 style="margin-top:0">Get real quotes</h3><p class="muted" style="font-size:.93rem">Compare up to 3 local pros. Free, no obligation.</p><a class="btn btn-amber btn-block" href="@/get-quotes.html?service={e(g["quote"])}">Get free quotes</a><a class="btn btn-red btn-block" style="margin-top:8px" href="@/get-quotes.html?service={e(g["quote"])}&amp;urgency=emergency">It's an emergency</a></div>
<div class="card toc"><h3 style="margin-top:0;font-size:1rem">On this page</h3><ol><li><a href="#jobs">Common job costs</a></li><li><a href="#factors">Price factors</a></li><li><a href="#emergency">Emergency pricing</a></li><li><a href="#save">How to save</a></li><li><a href="#ask">Questions to ask</a></li><li><a href="#flags">Red flags</a></li><li><a href="#faq">FAQ</a></li></ol></div>
{f'<div class="card"><h3 style="margin-top:0;font-size:1rem">Emergency playbooks</h3><ul style="margin:0">{rel_pb}</ul></div>' if rel_pb else ''}
<div class="card"><h3 style="margin-top:0;font-size:1rem">Related cost guides</h3><ul style="margin:0">{rel_g}</ul></div>
<div class="card"><h3 style="margin-top:0;font-size:1rem">Got quotes already?</h3><p class="muted" style="font-size:.92rem">Check them against typical prices.</p><a class="btn btn-ghost btn-block btn-sm" href="@/tools/quote-checker.html">Open the quote checker</a></div>
</aside></div></section>
{cta_band("Need this fixed? Get matched with local pros.", "Tell us what's happening in about a minute. We'll route your request to up to three available local pros.", "@/get-quotes.html?service=" + e(g["quote"]), "Get free quotes")}
{est_json()}"""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"], "dateModified": TODAY.isoformat(),
           "datePublished": "2026-11-12", "author": {"@type": "Organization", "name": "ExpressFind Editorial"}, "publisher": {"@type": "Organization", "name": "ExpressFind", "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/icon-512.png"}},
           "mainEntityOfPage": canon(path)}
    render(path, f"{g['name']} Cost ({TODAY.year}) — Prices, Fees & Tips | ExpressFind", g["desc"], body, "0.8",
           crumbs=[("Home", "index.html"), ("Cost guides", "costs.html"), (g["name"], None)], schema=[art, faq_ld(g["faqs"])], og_type="article")


# ---------------------------------------------------------------- playbooks
def build_playbook(p):
    path = f"emergency/{p['slug']}.html"
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    steps = "".join(f"<li><strong>{e(t)}</strong>{e(x)}</li>" for t, x in p["steps"])
    costs = "".join(f'<a class="card card-link" href="@/costs/{s}.html"><h3 style="margin-top:0">{e(GBY[s]["name"])} cost</h3><div class="price-tag">{adj(GBY[s]["low"], F)} – {adj(GBY[s]["high"], F)}</div><span class="more">See the breakdown →</span></a>' for s in p["costs"] if s in GBY)
    video = f'<h2 id="video">Watch how</h2>{video_block(*p["video"])}' if p.get("video") else ""
    mold = ""
    if p.get("moldclock"):
        mold = (f'<div class="tool no-print" id="moldClock" style="margin:24px 0"><h3 style="margin-top:0">{icon("clock")} Mold clock: your 24–48 hour drying window</h3>'
                f'<p class="muted" style="font-size:.93rem">EPA guidance is to dry wet materials within 24 to 48 hours to prevent mold. Enter when the water started.</p>'
                f'<div class="row"><div class="field"><label for="mc-in">Water started at</label><input id="mc-in" type="datetime-local"></div><div class="field"><label>&nbsp;</label><button class="btn btn-ghost btn-block" type="button" data-now>It just happened</button></div></div>'
                f'<div class="out mc-out"></div></div>')
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener nofollow">{e(n)}</a></li>' for n, u in p.get("sources", []))
    others = "".join(f'<li><a href="@/emergency/{x["slug"]}.html">{e(x["name"])}</a></li>' for x in PLAYBOOKS if x["slug"] != p["slug"])
    body = f"""<section class="page-hero red"><div class="wrap">{crumbs_html([("Home","index.html"),("Emergency","emergency.html"),(p["name"],None)])}
<span class="eyebrow">Emergency playbook · {e(p["tag"])}</span><h1>{e(p["title"])}</h1><p class="lead">{e(p["desc"])}</p>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn btn-red" href="@/get-quotes.html?service={e(p["quote"])}&amp;urgency=emergency">{icon("alert")} Get emergency help</a><a class="btn btn-ghost" style="color:#fff;border-color:#ffffff55" href="#steps">Jump to the steps</a></div></div></section>
<section><div class="wrap layout"><article class="prose">
<div class="callout danger">{icon("alert")}<p><strong>Safety first.</strong> {e(p["danger"])}</p></div>
<div class="card" style="border-left:5px solid var(--red)"><h3 style="margin-top:0">Right now, in 3 steps</h3><ol style="margin:0">{li(p["quick"])}</ol></div>
{''.join(f"<p style='margin-top:18px'>{e(x)}</p>" for x in p["intro"])}
<h2 id="steps">The first 15 minutes</h2><ol class="big">{steps}</ol>
{mold}
<div class="dolist"><div class="card do"><h3>{icon("check")} Do</h3><ul>{li(p["do"])}</ul></div><div class="card dont"><h3>{icon("x")} Don't</h3><ul>{li(p["dont"])}</ul></div></div>
<h2 id="tell">What to tell the pro when you call</h2><ul>{li(p["tell"])}</ul>
<h2 id="after">The next 24–48 hours</h2><ul>{li(p["after"])}</ul>
{video}
<h2 id="costs">What this usually costs</h2><div class="grid g2">{costs}</div>
<h2 id="faq">Frequently asked questions</h2>{faq_html(p["faqs"])}
{f'<h2>Sources</h2><ul style="font-size:.93rem">{src}</ul>' if src else ''}
<p class="muted" style="font-size:.88rem;margin-top:24px">This playbook is general safety information, not professional advice. Follow instructions from emergency services, your utility and licensed professionals. <a href="@/disclaimer.html">Disclaimer</a>.</p>
<div class="share no-print"><button class="btn btn-ghost btn-sm" type="button" data-share>{icon("share")} Share</button><button class="btn btn-ghost btn-sm" type="button" data-print>{icon("printer")} Print this playbook</button></div>
</article>
<aside class="aside">
<div class="card" style="border:2px solid var(--red)"><h3 style="margin-top:0">Need help now?</h3><p class="muted" style="font-size:.93rem">Send one request; we route it to available local pros. If anyone is in danger, call 911 first.</p><a class="btn btn-red btn-block" href="@/get-quotes.html?service={e(p["quote"])}&amp;urgency=emergency">Get emergency help</a></div>
<div class="card toc"><h3 style="margin-top:0;font-size:1rem">On this page</h3><ol><li><a href="#steps">First 15 minutes</a></li><li><a href="#tell">What to tell the pro</a></li><li><a href="#after">Next 24–48 hours</a></li><li><a href="#costs">Costs</a></li><li><a href="#faq">FAQ</a></li></ol></div>
<div class="card"><h3 style="margin-top:0;font-size:1rem">Other emergencies</h3><ul style="margin:0;font-size:.93rem">{others}</ul></div>
<div class="card"><h3 style="margin-top:0;font-size:1rem">Be ready next time</h3><p class="muted" style="font-size:.92rem">Free printable emergency kit and fridge card.</p><a class="btn btn-ghost btn-block btn-sm" href="@/tools/emergency-kit.html">Build your kit</a></div>
</aside></div></section>
{cta_band("Get a pro on the way.", "Describe the emergency once. We'll route it to up to three available local pros so you can compare fast.", "@/get-quotes.html?service=" + e(p["quote"]) + "&amp;urgency=emergency", "Get emergency help", red=True)}"""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["desc"], "dateModified": TODAY.isoformat(), "datePublished": "2026-11-12",
           "author": {"@type": "Organization", "name": "ExpressFind Editorial"}, "publisher": {"@type": "Organization", "name": "ExpressFind"}, "mainEntityOfPage": canon(path)}
    render(path, f"{p['title']} | ExpressFind", p["desc"], body, "0.8",
           crumbs=[("Home", "index.html"), ("Emergency", "emergency.html"), (p["name"], None)], schema=[art, faq_ld(p["faqs"])], og_type="article")


# ---------------------------------------------------------------- hubs
def build_emergency_hub():
    tiles = "".join(f'<button class="tile" type="button" data-key="{p["slug"]}" aria-pressed="false">{icon(p["icon"])}<span>{e(p["name"])}</span><small>{e(p["tag"])}</small></button>' for p in PLAYBOOKS)
    panels = "".join(
        f'<div class="card" data-panel="{p["slug"]}" hidden style="margin-top:16px;border:2px solid var(--red)"><span class="badge red">{e(p["tag"])}</span><h3>{e(p["name"])}: do this now</h3>'
        f'<div class="callout danger" style="margin:10px 0">{icon("alert")}<p>{e(p["danger"])}</p></div><ol>{"".join(f"<li>{e(x)}</li>" for x in p["quick"])}</ol>'
        f'<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-dark" href="@/emergency/{p["slug"]}.html">Full step-by-step playbook</a><a class="btn btn-red" href="@/get-quotes.html?service={e(p["quote"])}&amp;urgency=emergency">Get emergency help</a></div></div>'
        for p in PLAYBOOKS)
    cards = "".join(play_card(p) for p in PLAYBOOKS)
    faqs = [("When should I call 911 instead of a contractor?", "Call 911 for fire, smoke, someone injured or shocked, a carbon monoxide alarm, or any situation where life is at risk. Call your gas utility or 911 for a gas smell, and your electric utility for downed lines."),
            ("How fast will a pro respond?", "Availability depends on your area and the time of day. Emergency requests are flagged as urgent so available pros can prioritize them. ExpressFind does not dispatch crews itself."),
            ("Is it cheaper to wait until morning?", "Often yes. After-hours rates commonly run 1.5× to 2× normal pricing. If you can stop the damage safely, waiting for business hours can save a lot."),
            ("Is ExpressFind an emergency service?", "No. We publish safety information and route service requests to independent local pros. We are not a substitute for 911, your utility or a licensed professional.")]
    body = f"""<section class="page-hero red"><div class="wrap">{crumbs_html([("Home","index.html"),("Emergency",None)])}<span class="eyebrow">Emergency help center</span>
<h1>What's happening? Get the right first steps fast.</h1><p class="lead">Pick your emergency for immediate, safety-first steps. Then send one request to reach available local pros.</p>
<div class="callout danger" style="max-width:760px;margin-top:20px">{icon("alert")}<p><strong>If anyone is in danger, call 911 now.</strong> Smell gas? Leave the building, then call 911 or your gas utility from outside. Downed power line? Stay at least 35 feet away and call your utility.</p></div></div></section>
<section><div class="wrap" id="triage"><div class="head-row"><div><span class="eyebrow">Step 1</span><h2>Tap what's happening</h2></div><a class="btn btn-red" href="@/get-quotes.html?urgency=emergency">Skip to emergency request</a></div>
<div class="em-grid">{tiles}</div>{panels}</div></section>
<section class="section-alt"><div class="wrap"><div class="head-row"><div><span class="eyebrow">All playbooks</span><h2>Step-by-step emergency guides</h2></div></div><div class="grid g3">{cards}</div></div></section>
<section><div class="wrap grid g2">
<div><span class="eyebrow">Be prepared</span><h2>Know these three things before anything goes wrong</h2>
<ol class="big"><li><strong>Where your main water shutoff is</strong>Usually where the water line enters the house. Make sure it turns.</li><li><strong>Where your breaker panel is</strong>Label the breakers so you can cut power to one room fast.</li><li><strong>Who to call</strong>Save your gas and electric utility emergency numbers in your phone today.</li></ol>
<a class="btn btn-dark" href="@/tools/emergency-kit.html">Build your free emergency kit &amp; fridge card</a></div>
<div>{video_block("VLrku55gWr4", "How To Turn Off The Main Water Valve", "Ace Hardware")}</div></div></section>
<section class="section-alt"><div class="wrap" style="max-width:860px"><h2>Emergency FAQ</h2>{faq_html(faqs)}</div></section>
{cta_band("Can't wait? Send one emergency request.", "We'll flag it urgent and route it to up to three available local pros.", "@/get-quotes.html?urgency=emergency", "Get emergency help", red=True)}"""
    render("emergency.html", "Home Emergency Help: Burst Pipe, No Heat, Gas Smell & More | ExpressFind",
           "Safety-first steps for home emergencies — burst pipes, flooding, no heat, gas smells, roof leaks, lockouts — plus fast routing to local pros.", body, "0.9",
           crumbs=[("Home", "index.html"), ("Emergency", None)], schema=[faq_ld(faqs)])


def build_costs_hub():
    chips = "".join(f'<button class="chip{" on" if k == "all" else ""}" type="button" data-cat="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in CATS)
    cards = "".join(guide_card(g) for g in GUIDES)
    rows = "".join(f'<tr><td><a href="@/costs/{g["slug"]}.html">{e(g["name"])}</a></td><td class="num">{adj(g["low"], F)} – {adj(g["high"], F)}</td><td class="muted">{e(g["unit"])}</td></tr>' for g in GUIDES)
    body = f"""<section class="page-hero"><div class="wrap">{crumbs_html([("Home","index.html"),("Cost guides",None)])}<span class="eyebrow">Honest cost guides</span>
<h1>What home repairs really cost in {TODAY.year}</h1><p class="lead">Typical price ranges for {len(GUIDES)} emergency and repair services, emergency premiums, money-saving tips and questions to ask — adjusted for inflation every week.</p></div></section>
<section><div class="wrap">{pulse_html()}
<div style="margin-top:26px"><input class="search" type="search" placeholder="Search cost guides (e.g. water heater, roof, locksmith)" data-filter="#guideGrid" aria-label="Search cost guides">
<div class="chips" data-chips="#guideGrid">{chips}</div></div>
<div class="grid g3" id="guideGrid">{cards}</div></div></section>
<section class="section-alt"><div class="wrap"><h2>All prices at a glance</h2><p class="muted">US national estimates in USD, adjusted for inflation through {e(CPI.get("label", REVIEWED))}. Canadian homeowners: convert and expect regional variation.</p>
<div class="table-wrap"><table class="data"><thead><tr><th>Service</th><th>Typical range</th><th>Basis</th></tr></thead><tbody>{rows}</tbody></table></div>
<p><a href="@/methodology.html">How we build and update these numbers →</a></p></div></section>
{cta_band("Prices are a starting point. Quotes are the real number.", "Compare up to three local pros for your exact job.", "@/get-quotes.html", "Get free quotes")}"""
    render("costs.html", f"Home Repair Cost Guides {TODAY.year} — Plumbing, HVAC, Roofing & More | ExpressFind",
           "Typical costs for emergency plumbers, water damage, water heaters, AC and furnace repair, roof leaks, locksmiths, electricians, mold and more.", body, "0.9",
           crumbs=[("Home", "index.html"), ("Cost guides", None)])


def build_videos():
    chips = "".join(f'<button class="chip{" on" if k == "all" else ""}" type="button" data-cat="{k}">{n}</button>' for k, n in VCATS)
    cards = "".join(f'<div class="card" data-cat="{v["cat"]}" style="padding:14px">{video_block(v["id"], v["title"], v["ch"])}<p style="font-size:.92rem;margin:8px 0 6px">{e(v["note"])}</p><a href="@/{v["link"]}" style="font-size:.9rem;font-weight:700">Related guide →</a></div>' for v in VIDEOS)
    body = f"""<section class="page-hero"><div class="wrap">{crumbs_html([("Home","index.html"),("Videos",None)])}<span class="eyebrow">Video library</span><h1>Watch before you call: home emergency how-tos</h1>
<p class="lead">Short, practical videos from hardware retailers, utilities and trade pros — shutoffs, breakers, frozen pipes, furnace checks and hiring tips. Videos load only when you press play.</p></div></section>
<section><div class="wrap"><div class="chips" data-chips="#vgrid">{chips}</div><div class="grid g3" id="vgrid">{cards}</div>
<p class="muted" style="font-size:.88rem;margin-top:24px">Videos are embedded with YouTube's privacy-enhanced player and remain the property of their creators. ExpressFind is not affiliated with these channels. See our <a href="@/trademark.html">trademark &amp; copyright disclosure</a>.</p></div></section>
{cta_band("Watched it and still stuck?", "Send one request and compare local pros.", "@/get-quotes.html", "Get free quotes")}"""
    render("videos.html", "Home Repair & Emergency How-To Videos | ExpressFind",
           "Free how-to videos: shut off your water, reset a breaker, thaw frozen pipes, troubleshoot a furnace or AC, use a fire extinguisher and vet a contractor.", body, "0.7",
           crumbs=[("Home", "index.html"), ("Videos", None)])


# ---------------------------------------------------------------- home
def build_home():
    disp = "".join(f'<a href="@/emergency/{p["slug"]}.html">{icon(p["icon"])}{e(p["name"])}</a>' for p in PLAYBOOKS[:8])
    top = ["emergency-plumber", "water-damage-restoration", "water-heater-replacement", "ac-repair", "furnace-repair", "roof-leak-repair"]
    gcards = "".join(guide_card(GBY[s]) for s in top)
    tools = [("cost-estimator", "calc", "Emergency cost estimator", "Service × severity × timing × region = a realistic range."),
             ("quote-checker", "search", "Quote checker", "See if your quotes are fair, low or high — and what to ask."),
             ("repair-or-replace", "wrench", "Repair or replace?", "The $5,000 rule and 50% rule, done for you."),
             ("license-lookup", "shield", "License lookup", "Official contractor license search for every state and province."),
             ("emergency-kit", "list", "Emergency kit & fridge card", "A printable checklist with your shutoffs and key numbers."),
             ("maintenance-calendar", "calendar", "Maintenance calendar", "What to do this month, with calendar export.")]
    tcards = "".join(f'<a class="card card-link reveal" href="@/tools/{s}.html"><div class="ico">{icon(i)}</div><h3>{t}</h3><p class="muted" style="font-size:.93rem">{d}</p><span class="more">Open tool →</span></a>' for s, i, t, d in tools)
    vids = "".join(f'<div>{video_block(v["id"], v["title"], v["ch"])}</div>' for v in VIDEOS[:3])
    faqs = [("Is ExpressFind free for homeowners?", "Yes. Requesting quotes, reading guides and using every tool is free. We earn money from advertising and from service providers who receive requests."),
            ("How does ExpressFind find a pro?", "You describe the job once. We route the request to up to three independent local service providers who serve your area and handle that kind of work. They contact you directly with availability and pricing."),
            ("Do you vet the pros?", "We ask partner pros to confirm licensing where required and liability insurance. Always verify yourself before hiring — our free license lookup tool links to official state and provincial databases."),
            ("Where do your cost numbers come from?", "Each guide compiles several independent cost surveys and contractor price lists into a rounded range, lists its sources, and is adjusted weekly for inflation using U.S. Bureau of Labor Statistics data."),
            ("Do you serve Canada?", "Yes. The request form accepts US ZIP codes and Canadian postal codes. Cost guides are published in USD; Canadian prices vary by province.")]
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "ExpressFind", "url": SITE + "/", "logo": SITE + "/assets/img/icon-512.png",
           "description": "Emergency-first home services finder with cost guides and free tools for US and Canadian homeowners."}
    web = {"@context": "https://schema.org", "@type": "WebSite", "name": "ExpressFind", "url": SITE + "/"}
    body = f"""<section class="hero"><div class="wrap hero-grid"><div>
<span class="eyebrow" style="color:var(--amber)">US &amp; Canada · Free for homeowners</span>
<h1>Home emergency? <em>Find the right pro fast.</em></h1>
<p class="lead">Safety-first steps for the moment something breaks, honest prices so you don't overpay, and one free request that reaches up to three local pros.</p>
{finder()}
<div class="hero-note"><span>{icon("check")} Free, no obligation</span><span>{icon("clock")} About 60 seconds</span><span>{icon("users")} Up to 3 local pros</span></div></div>
<div class="dispatch"><h3><span class="dot"></span> What's happening right now?</h3><div class="tiles">{disp}</div>
<p class="foot">Anyone in danger? Call 911 first. <a href="@/emergency.html" style="color:var(--amber)">All emergencies →</a></p></div></div></section>
<div class="strip"><div class="wrap"><div>{icon("shield")} Free &amp; no obligation</div><div>{icon("clock")} Request in about a minute</div><div>{icon("dollar")} Prices re-checked weekly</div><div>{icon("alert")} Safety-first guidance</div></div></div>
<section><div class="wrap"><div class="head-row"><div><span class="eyebrow">Know before you call</span><h2>What it should cost</h2></div><a class="btn btn-ghost" href="@/costs.html">All {len(GUIDES)} cost guides →</a></div>
<div class="grid g3">{gcards}</div><div style="margin-top:22px">{pulse_html()}</div></div></section>
<section class="section-alt"><div class="wrap"><div class="center" style="margin-bottom:30px"><span class="eyebrow">How it works</span><h2>One request. Up to three local pros.</h2><p class="lead">No account, no spam lists, no obligation to hire.</p></div>
<div class="steps"><div class="card reveal"><h3>Tell us what's wrong</h3><p class="muted">Pick the service, how urgent it is, your ZIP or postal code and a few details. It takes about a minute.</p></div>
<div class="card reveal"><h3>We route your request</h3><p class="muted">Your request goes to up to three independent pros who serve your area and do that kind of work. Emergencies are flagged urgent.</p></div>
<div class="card reveal"><h3>Compare and choose</h3><p class="muted">Pros contact you directly. Use our quote checker and license lookup to compare, then hire who you trust — or no one.</p></div></div>
<div class="center" style="margin-top:28px"><a class="btn btn-amber" href="@/get-quotes.html">Start my free request</a></div></div></section>
<section><div class="wrap grid g2" style="align-items:center"><div><span class="eyebrow">Seasonal</span><h2>Stay ahead of the next emergency</h2><p class="lead">Most emergencies are cheaper to prevent than to fix. Here's the one thing to do this month.</p>{seasonal_html()}</div>
<div class="card"><span class="badge amber">Free printable</span><h3>The Home Emergency Playbook</h3><p class="muted">Shutoff locations, a 15-item kit, who to call first and a fridge card for your family.</p><button class="btn btn-dark" type="button" data-open-magnet>Get the free playbook</button></div></div></section>
<section class="section-alt"><div class="wrap"><div class="head-row"><div><span class="eyebrow">Free tools</span><h2>Make smarter calls in minutes</h2></div><a class="btn btn-ghost" href="@/tools.html">All tools →</a></div><div class="grid g3">{tcards}</div></div></section>
<section><div class="wrap"><div class="head-row"><div><span class="eyebrow">Watch before you call</span><h2>60-second fixes and safety basics</h2></div><a class="btn btn-ghost" href="@/videos.html">Video library →</a></div><div class="grid g3">{vids}</div></div></section>
<section class="section-tight"><div class="wrap"><div class="band"><div><span class="eyebrow" style="color:var(--amber)">For contractors</span><h2>Plumbers, HVAC, roofers, electricians: get emergency jobs in your area.</h2><p>Join the ExpressFind pro network. Pay only for the requests you want, set your service area and emergency hours.</p></div><div><a class="btn btn-amber btn-block" href="@/pros.html">Join as a pro</a><a class="btn btn-ghost btn-block" style="margin-top:8px;color:#fff;border-color:#ffffff44" href="@/advertise.html">Advertise or sponsor</a></div></div></div></section>
<section><div class="wrap"><div class="center" style="margin-bottom:26px"><span class="eyebrow">Community</span><h2>Help us keep it free and honest</h2></div><div class="grid g4">
<a class="card card-link" href="@/support.html"><div class="ico">{icon("heart")}</div><h3>Support us</h3><p class="muted" style="font-size:.92rem">Fund operations, promotion, new tools and prizes.</p><span class="more">Contribute →</span></a>
<a class="card card-link" href="@/contests.html"><div class="ico">{icon("trophy")}</div><h3>Monthly contest</h3><p class="muted" style="font-size:.92rem">Share your best home save or tip. Win a gift card.</p><span class="more">Enter →</span></a>
<a class="card card-link" href="@/careers.html"><div class="ico">{icon("briefcase")}</div><h3>Careers</h3><p class="muted" style="font-size:.92rem">Licensed trade reviewers, writers, video creators.</p><span class="more">See roles →</span></a>
<a class="card card-link" href="@/advertise.html"><div class="ico">{icon("megaphone")}</div><h3>Sponsor</h3><p class="muted" style="font-size:.92rem">Put your brand next to high-intent homeowners.</p><span class="more">Packages →</span></a></div></div></section>
<section class="section-alt"><div class="wrap" style="max-width:860px"><div class="center"><span class="eyebrow">FAQ</span><h2>Questions homeowners ask</h2></div>{faq_html(faqs)}</div></section>
{cta_band("Something broken right now?", "Get safety-first steps, then reach up to three local pros with one request.", "@/get-quotes.html", "Get free quotes")}"""
    render("index.html", "ExpressFind — Find a Trusted Local Pro Fast for Home Emergencies & Repairs",
           "Home emergency? Get safety-first steps, honest cost guides and free quotes from up to 3 local plumbers, HVAC techs, roofers, electricians and locksmiths. US & Canada.",
           body, "1.0", schema=[org, web, faq_ld(faqs)])


# ---------------------------------------------------------------- quote funnel
def build_quotes():
    svc = "".join(f'<label class="svc"><input type="radio" name="service" value="{e(s)}" required><span>{icon(i)}{e(s)}</span></label>' for s, i in SERVICES)
    urg = "".join(f'<label class="choice"><input type="radio" name="urgency" value="{v}" required><span>{v}</span></label>' for v in ["Emergency — right now", "Within 24 hours", "This week", "Planning / flexible"])
    own = "".join(f'<label class="choice"><input type="radio" name="ownership" value="{v}" required><span>{v}</span></label>' for v in ["I own it", "I rent it", "I manage it"])
    body = f"""<section class="page-hero" style="padding-bottom:40px"><div class="wrap">{crumbs_html([("Home","index.html"),("Get free quotes",None)])}<span class="eyebrow">Free · No obligation</span>
<h1>Get quotes from up to 3 local pros</h1><p class="lead">Answer five quick questions. Emergencies are flagged urgent. If anyone is in danger, call 911 first.</p></div></section>
<section style="padding-top:36px"><div class="wrap layout"><div>
<form class="form-card funnel" id="quoteForm" novalidate>
<div class="progress" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></div>
<div class="progress-label"><span id="stepLabel" aria-live="polite">Step 1 of 5 · Service</span><span>About 60 seconds</span></div>
<div class="step active" data-step="1"><h2>What do you need help with?</h2><p class="muted">Pick the closest match. You can add details later.</p><div class="svc-grid">{svc}</div>
<div class="step-nav"><span></span><button class="btn btn-amber" type="button" data-next>Continue {icon("arrow")}</button></div></div>
<div class="step" data-step="2"><h2>How urgent is it?</h2><div class="choice-grid">{urg}</div>
<div class="row"><div class="field"><label for="q-prop">Property type</label><select id="q-prop" name="property"><option>House</option><option>Townhouse / condo</option><option>Apartment</option><option>Business / commercial</option></select></div>
<div class="field"><span class="lbl">Do you own the property?</span><div class="choice-grid" style="grid-template-columns:repeat(3,1fr);margin:0">{own}</div></div></div>
<div class="step-nav"><button class="btn btn-ghost" type="button" data-prev>Back</button><button class="btn btn-amber" type="button" data-next>Continue {icon("arrow")}</button></div></div>
<div class="step" data-step="3"><h2>Where is the job?</h2>
<div class="row"><div class="field"><label for="q-zip">ZIP or postal code</label><input id="q-zip" name="zip" required autocomplete="postal-code" placeholder="e.g. 77002 or M5V 2T6" maxlength="10"><p class="hint">US ZIP or Canadian postal code.</p></div>
<div class="field"><label for="q-city">City (optional)</label><input id="q-city" name="city" autocomplete="address-level2"></div></div>
<div class="step-nav"><button class="btn btn-ghost" type="button" data-prev>Back</button><button class="btn btn-amber" type="button" data-next>Continue {icon("arrow")}</button></div></div>
<div class="step" data-step="4"><h2>Tell us what's going on</h2>
<div class="field"><label for="q-det">Describe the problem</label><textarea id="q-det" name="details" required minlength="10" placeholder="e.g. Pipe burst under the kitchen sink, water is off at the main, cabinet and floor are wet."></textarea></div>
<div class="row"><div class="field"><label for="q-bud">Budget (optional)</label><select id="q-bud" name="budget"><option>Not sure yet</option><option>Under $500</option><option>$500 – $1,000</option><option>$1,000 – $5,000</option><option>$5,000+</option></select></div>
<div class="field"><label for="q-time">Best time to reach you</label><select id="q-time" name="contact_time"><option>As soon as possible</option><option>Morning</option><option>Afternoon</option><option>Evening</option></select></div></div>
<div class="step-nav"><button class="btn btn-ghost" type="button" data-prev>Back</button><button class="btn btn-amber" type="button" data-next>Continue {icon("arrow")}</button></div></div>
<div class="step" data-step="5"><h2>Where should pros reach you?</h2>
<div class="row"><div class="field"><label for="q-name">Full name</label><input id="q-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" required autocomplete="tel" minlength="10" maxlength="20"></div></div>
<div class="row"><div class="field"><label for="q-email">Email</label><input id="q-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="q-pref">Preferred contact</label><select id="q-pref" name="contact_pref"><option>Call</option><option>Text</option><option>Email</option></select></div></div>
<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="field"><label class="check"><input type="checkbox" name="consent" value="yes" required> <span>I agree that ExpressFind and up to three matched service providers may contact me by phone, text or email about this request, including by automated means. Consent is not a condition of any purchase. Message and data rates may apply; reply STOP to opt out. I accept the <a href="@/terms.html">Terms</a> and <a href="@/privacy.html">Privacy Policy</a>.</span></label></div>
<div class="field"><label class="check"><input type="checkbox" name="newsletter" value="yes"> <span>Also send me seasonal maintenance reminders (optional).</span></label></div>
<div class="step-nav"><button class="btn btn-ghost" type="button" data-prev>Back</button><button class="btn btn-amber" type="submit">Send my request {icon("arrow")}</button></div>
<div class="form-msg" role="status" aria-live="polite"></div></div>
<div class="assure"><span>{icon("check")} Free</span><span>{icon("check")} No obligation</span><span>{icon("check")} Shared with max. 3 pros</span><span>{icon("check")} Your draft saves automatically</span></div>
</form></div>
<aside class="aside">
<div class="card" style="border:2px solid var(--red)"><h3 style="margin-top:0">{icon("alert")} Emergency?</h3><p class="muted" style="font-size:.93rem">Fire, smoke, gas smell, CO alarm or injury: call 911. For water, cut the main shutoff first.</p><a class="btn btn-ghost btn-block btn-sm" href="@/emergency.html">Emergency first steps</a></div>
<div class="card"><h3 style="margin-top:0;font-size:1.05rem">What happens next</h3><ol style="margin:0;font-size:.93rem"><li>We review and route your request to up to three local pros.</li><li>Pros contact you directly with availability and pricing.</li><li>You compare and choose — or don't. No obligation.</li></ol></div>
<div class="card"><h3 style="margin-top:0;font-size:1.05rem">Before you hire</h3><ul style="margin:0;font-size:.93rem"><li><a href="@/tools/license-lookup.html">Check their license</a></li><li><a href="@/tools/quote-checker.html">Check their quote</a></li><li><a href="@/costs.html">See typical prices</a></li></ul></div>
<div class="card"><h3 style="margin-top:0;font-size:1.05rem">How we use your info</h3><p class="muted" style="font-size:.9rem;margin:0">Only to handle this request. We never sell your data to list brokers. <a href="@/privacy.html">Privacy policy</a>.</p></div>
</aside></div></section>"""
    render("get-quotes.html", "Get Free Quotes from Local Pros — Plumbing, HVAC, Roofing & More | ExpressFind",
           "Describe your home repair or emergency once and get matched with up to three local pros. Free, no obligation, about 60 seconds. US & Canada.", body, "0.9",
           crumbs=[("Home", "index.html"), ("Get free quotes", None)])


# ---------------------------------------------------------------- feeds & sitemaps
def build_xml():
    now = TODAY.isoformat()
    urls = "".join(f"<url><loc>{canon(p)}</loc><lastmod>{now}</lastmod><priority>{pr}</priority></url>\n" for p, pr in OUT if p not in ("404.html", "thank-you.html"))
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    items = []
    for g in GUIDES:
        items.append((g["title"], f"costs/{g['slug']}.html", g["desc"]))
    for p in PLAYBOOKS:
        items.append((p["title"], f"emergency/{p['slug']}.html", p["desc"]))
    pub = datetime.datetime.combine(TODAY, datetime.time(12, 0)).strftime("%a, %d %b %Y %H:%M:%S +0000")
    it = "".join(f"<item><title>{e(t)}</title><link>{canon(u)}</link><guid>{canon(u)}</guid><description>{e(d)}</description><pubDate>{pub}</pubDate></item>\n" for t, u, d in items)
    with open(os.path.join(ROOT_DIR, "feed.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>ExpressFind — Cost guides &amp; emergency playbooks</title><link>{SITE}/</link><description>Home emergency steps and repair cost guides, updated weekly.</description><lastBuildDate>{pub}</lastBuildDate>\n{it}</channel></rss>\n')
    with open(os.path.join(ROOT_DIR, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /thank-you.html\n\nSitemap: {SITE}/sitemap.xml\n")


def main():
    for g in GUIDES:
        build_guide(g)
    for p in PLAYBOOKS:
        build_playbook(p)
    build_home()
    build_quotes()
    build_emergency_hub()
    build_costs_hub()
    build_videos()
    ctx = dict(render=render, F=F, CPI=CPI, GUIDES=GUIDES, PLAYBOOKS=PLAYBOOKS, SYSTEMS=SYSTEMS, est_json=est_json, cta_band=cta_band,
               faq_html=faq_html, faq_ld=faq_ld, video_block=video_block, guide_card=guide_card, play_card=play_card, svc_options=svc_options,
               TODAY=TODAY, OUT=OUT)
    T.build_all(ctx)
    P.build_all(ctx)
    build_xml()
    meta = {"built": TODAY.isoformat(), "pages": len(OUT), "factor": F}
    with open(os.path.join(ROOT_DIR, "data", "site.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Built {len(OUT)} pages · inflation factor {F}")


if __name__ == "__main__":
    main()
