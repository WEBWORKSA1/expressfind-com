"""Interactive tool pages."""
import json
from urllib.parse import quote_plus
from common import e, adj, REVIEWED
from icons import icon
from layout import crumbs_html

US = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii",
      "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
      "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
      "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
      "West Virginia", "Wisconsin", "Wyoming"]
CA = ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island", "Quebec",
      "Saskatchewan", "Northwest Territories", "Nunavut", "Yukon"]
DIRECT = {
    "Arizona": ("https://roc.az.gov/", "Registrar of Contractors"),
    "California": ("https://www.cslb.ca.gov/", "Contractors State License Board"),
    "Florida": ("https://www.myfloridalicense.com/", "DBPR license search"),
    "Georgia": ("https://verify.sos.ga.gov/verification/", "Secretary of State verification"),
    "Nevada": ("https://www.nscb.nv.gov/", "State Contractors Board"),
    "North Carolina": ("https://www.nclbgc.org/", "Licensing Board for General Contractors"),
    "Oregon": ("https://www.oregon.gov/ccb/", "Construction Contractors Board"),
    "Texas": ("https://www.tdlr.texas.gov/", "Dept. of Licensing & Regulation"),
    "Washington": ("https://secure.lni.wa.gov/verify/", "L&I contractor verify"),
    "Ontario": ("https://www.skilledtradesontario.ca/", "Skilled Trades Ontario registry"),
    "Quebec": ("https://www.rbq.gouv.qc.ca/", "Régie du bâtiment du Québec"),
    "British Columbia": ("https://www.technicalsafetybc.ca/", "Technical Safety BC"),
}

KIT = ["Water: about one gallon (4 L) per person per day for several days", "Non-perishable food for at least three days and a manual can opener",
       "Flashlights and extra batteries (no candles)", "Battery-powered or hand-crank radio", "First aid kit and a week of prescription medications",
       "Phone chargers and a charged power bank", "Fire extinguisher (ABC) in the kitchen, and you know how to use it",
       "Smoke and carbon monoxide alarms tested this month", "Adjustable wrench or pliers to turn off utilities", "Main water shutoff located and tested",
       "Breaker panel located and breakers labeled", "Gas meter located (leave operating it to the utility)", "Plastic sheeting, duct tape and a tarp",
       "Towels, buckets and a wet/dry vacuum", "Copies of insurance policy, ID and home inventory photos stored in the cloud",
       "Utility emergency numbers saved in every family phone"]

MONTHS = [
 ("January", ["Check exposed pipes during cold snaps; let faucets drip", "Clear snow from furnace intake and exhaust pipes", "Test the sump pump", "Inspect attic for ice dams or leaks"]),
 ("February", ["Replace the furnace filter", "Test smoke and CO alarms", "Check caulk around tubs and showers", "Clean range-hood filters"]),
 ("March", ["Inspect roof and gutters for winter damage", "Check the foundation for new cracks", "Clean window wells", "Service the lawn mower"]),
 ("April", ["Extend downspouts away from the foundation", "Test the sump pump with a bucket of water", "Check exterior faucets for freeze damage", "Inspect decks and railings"]),
 ("May", ["Book an AC tune-up", "Replace the HVAC filter", "Clean the outdoor AC unit and clear 2 ft around it", "Check irrigation for leaks"]),
 ("June", ["Flush the AC condensate drain line", "Clean the dryer vent", "Check window and door screens", "Inspect trees for dead limbs over the roof"]),
 ("July", ["Check the water heater for leaks and rust", "Test GFCI outlets", "Clean the refrigerator coils", "Review your storm plan and kit"]),
 ("August", ["Have hazardous trees assessed before storm season", "Clean gutters", "Inspect weatherstripping", "Check grout and caulk in wet areas"]),
 ("September", ["Schedule furnace maintenance", "Replace the furnace filter", "Test smoke and CO alarms", "Flush the water heater"]),
 ("October", ["Disconnect hoses and shut off exterior faucets", "Insulate exposed pipes", "Clean gutters after leaves fall", "Check the fireplace and chimney"]),
 ("November", ["Inspect space heaters and cords", "Reverse ceiling fans to clockwise", "Check the roof before snow", "Locate and test the main water shutoff"]),
 ("December", ["Keep heat at or above 55°F (13°C) when traveling", "Water live Christmas trees daily", "Check holiday light cords for damage", "Arrange a house-check during cold snaps"]),
]


def tool_shell(ctx, path, name, title, desc, lead, body, faqs=None, extra=""):
    faq = ""
    schema = []
    if faqs:
        faq = f'<section class="section-alt"><div class="wrap" style="max-width:860px"><h2>FAQ</h2>{ctx["faq_html"](faqs)}</div></section>'
        schema = [ctx["faq_ld"](faqs)]
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": "https://expressfind.com/" + path}
    html = f"""<section class="page-hero"><div class="wrap">{crumbs_html([("Home","index.html"),("Tools","tools.html"),(name,None)])}<span class="eyebrow">Free tool</span><h1>{e(title)}</h1><p class="lead">{e(lead)}</p></div></section>
{body}{faq}{extra}"""
    ctx["render"](path, f"{title} | ExpressFind", desc, html, "0.7", crumbs=[("Home", "index.html"), ("Tools", "tools.html"), (name, None)], schema=[app] + schema)


def build_all(ctx):
    G = ctx["GUIDES"]
    F = ctx["F"]
    opts = "".join(f'<option value="{g["slug"]}">{e(g["name"])}</option>' for g in G)

    # Tools hub
    items = [("cost-estimator", "calc", "Emergency cost estimator", "Estimate a realistic range by service, job size, time of day and region."),
             ("quote-checker", "search", "Quote checker", "Compare up to three quotes against typical prices and get the questions to ask."),
             ("repair-or-replace", "wrench", "Repair or replace calculator", "Apply the $5,000 rule, the 50% rule and lifespan math to any system."),
             ("license-lookup", "shield", "Contractor license lookup", "Links to official license searches for every US state and Canadian province."),
             ("emergency-kit", "list", "Emergency kit & fridge card", "A saved checklist plus a printable card of shutoffs and phone numbers."),
             ("maintenance-calendar", "calendar", "Home maintenance calendar", "Month-by-month tasks that highlight what to do now, with calendar export.")]
    cards = "".join(f'<a class="card card-link reveal" href="@/tools/{s}.html"><div class="ico">{icon(i)}</div><h3>{t}</h3><p class="muted">{d}</p><span class="more">Open tool →</span></a>' for s, i, t, d in items)
    body = f"""<section class="page-hero"><div class="wrap">{crumbs_html([("Home","index.html"),("Tools",None)])}<span class="eyebrow">Free tools</span><h1>Free tools for faster, smarter home repair decisions</h1>
<p class="lead">No sign-up. Everything runs in your browser and your checklists save on your device.</p></div></section>
<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>
{ctx["cta_band"]("Ready for real numbers?", "Get quotes from up to three local pros for your exact job.", "@/get-quotes.html", "Get free quotes")}"""
    ctx["render"]("tools.html", "Free Home Repair Tools — Cost Estimator, Quote Checker & More | ExpressFind",
                  "Free home repair tools: emergency cost estimator, quote checker, repair-or-replace calculator, license lookup, emergency kit and maintenance calendar.",
                  body, "0.8", crumbs=[("Home", "index.html"), ("Tools", None)])

    # Cost estimator
    body = f"""<section><div class="wrap layout"><div class="tool" id="estimator">
<div class="field"><label for="e-service">Service</label><select id="e-service">{opts}</select></div>
<span class="lbl">How big is the job?</span><div class="choice-grid"><label class="choice"><input type="radio" name="e-sev" value="minor"><span>Minor</span></label><label class="choice"><input type="radio" name="e-sev" value="moderate" checked><span>Typical</span></label><label class="choice"><input type="radio" name="e-sev" value="major"><span>Major</span></label></div>
<p class="muted" id="e-desc" style="margin-top:-6px;font-size:.92rem"></p>
<div class="row"><div class="field"><label for="e-time">When do you need it?</label><select id="e-time"><option value="1">Business hours (weekday)</option><option value="1.5">Evening</option><option value="1.75">Weekend</option><option value="2">Holiday or overnight</option></select></div>
<div class="field"><label for="e-region">Your area</label><select id="e-region"><option value="0.85">Lower-cost area (rural / South / Plains)</option><option value="1" selected>Average</option><option value="1.2">Higher-cost area (Northeast / large city)</option><option value="1.35">Very high-cost metro (SF, NYC, Boston, Seattle)</option></select></div></div>
<div class="out"><small>Estimated total</small><div class="big" id="e-range">—</div><p>Midpoint <b id="e-mid">—</b> · <span id="e-prem"></span> · <span id="e-reg"></span></p><div class="meter"><i id="e-bar"></i></div></div>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px"><a class="btn btn-amber" id="e-quote" href="@/get-quotes.html">Get real quotes</a><a class="btn btn-ghost" id="e-guide" href="@/costs.html">Read the cost guide</a></div>
</div>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">How this works</h3><p class="muted" style="font-size:.92rem">Each service has minor, typical and major ranges from our cost guides, adjusted for inflation through {e(ctx["CPI"].get("label", REVIEWED))}. We apply a timing multiplier (evenings about 1.5×, holidays about 2×) and a regional adjustment. Real quotes depend on what the pro finds.</p></div>
<div class="card"><h3 style="margin-top:0;font-size:1.05rem">Got quotes?</h3><a class="btn btn-ghost btn-block btn-sm" href="@/tools/quote-checker.html">Check them here</a></div></aside></div></section>{ctx["est_json"]()}"""
    tool_shell(ctx, "tools/cost-estimator.html", "Cost estimator", "Emergency Repair Cost Estimator",
               "Estimate emergency and repair costs for plumbing, water damage, HVAC, roofing, locksmiths, electricians and more — by job size, time of day and region.",
               "Pick a service, the size of the job, when you need it and where you live. Get a realistic range before you call.", body,
               [("How accurate is this estimate?", "It gives a realistic planning range from published cost data. Your actual price depends on what the pro finds, local rates and the parts needed."),
                ("Why do evenings and weekends cost more?", "Most trades charge a dispatch fee and a higher hourly rate outside business hours, commonly 1.5× to 2× normal pricing.")])

    # Quote checker
    rows = "".join(f'<div class="row"><div class="field"><label for="qc-n{i}">Company {i} (optional)</label><input id="qc-n{i}" placeholder="Company name"></div><div class="field"><label for="qc-v{i}">Quote {i} total ($)</label><input id="qc-v{i}" type="number" min="0" inputmode="decimal" placeholder="0"></div></div>' for i in (1, 2, 3))
    body = f"""<section><div class="wrap layout"><div class="tool" id="quoteChecker">
<div class="field"><label for="qc-service">Service</label><select id="qc-service">{opts}</select></div>{rows}
<button class="btn btn-amber" type="button" id="qc-run">Check my quotes</button><div id="qc-out" style="margin-top:16px" aria-live="polite"></div></div>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">A good quote includes</h3><ul style="margin:0;font-size:.92rem"><li>Company name, address, license number</li><li>Itemized labor, parts and fees</li><li>Permits and disposal, if needed</li><li>Start date and expected duration</li><li>Warranty on parts and labor</li><li>Payment schedule (avoid large upfront cash)</li></ul></div>
<div class="card"><h3 style="margin-top:0;font-size:1.05rem">Verify before you sign</h3><a class="btn btn-ghost btn-block btn-sm" href="@/tools/license-lookup.html">License lookup</a></div></aside></div></section>{ctx["est_json"]()}"""
    tool_shell(ctx, "tools/quote-checker.html", "Quote checker", "Contractor Quote Checker: Is Your Quote Fair?",
               "Compare up to three contractor quotes against typical prices for plumbing, HVAC, roofing, electrical and more. See which are low, fair or high.",
               "Enter up to three quotes. We compare them with typical price ranges and tell you exactly what to ask.", body,
               [("Is the lowest quote the best one?", "Not always. Very low quotes often exclude parts, permits, disposal or warranty. Compare what is included, not just the total."),
                ("How many quotes should I get?", "Two or three for non-emergency work. In an emergency, stop the damage first, then compare quotes for the permanent repair.")])

    # Repair or replace
    sys_opts = "".join(f'<option value="{k}">{e(v["name"])}</option>' for k, v in ctx["SYSTEMS"].items())
    body = f"""<section><div class="wrap layout"><div class="tool" id="ror">
<div class="field"><label for="r-sys">What needs work?</label><select id="r-sys">{sys_opts}</select><p class="hint">Typical lifespan: <b id="r-life"></b></p></div>
<div class="row"><div class="field"><label for="r-age">Age (years)</label><input id="r-age" type="number" min="0" value="10"></div><div class="field"><label for="r-rep">Repair quote ($)</label><input id="r-rep" type="number" min="0" value="600"></div></div>
<div class="field"><label for="r-new">Replacement cost ($) — edit to your quote</label><input id="r-new" type="number" min="1"></div>
<div class="out"><small>Our call</small><div class="big" id="r-verdict">—</div><ul id="r-why" style="color:#c3d1de;margin:6px 0 0;padding-left:1.1em"></ul><div class="meter"><i id="r-bar"></i></div></div></div>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">The rules we apply</h3><ul style="margin:0;font-size:.92rem"><li><b>$5,000 rule:</b> age × repair cost above $5,000 favors replacing.</li><li><b>50% rule:</b> a repair at half the replacement price or more favors replacing.</li><li><b>Lifespan:</b> past about 75% of typical life, lean toward replacing.</li></ul><p class="muted" style="font-size:.88rem;margin:10px 0 0">Two of three signals = replace. Safety issues (gas, CO, electrical) override everything.</p></div></aside></div></section>
<script type="application/json" id="rorData">{json.dumps(ctx["SYSTEMS"])}</script>"""
    tool_shell(ctx, "tools/repair-or-replace.html", "Repair or replace", "Repair or Replace Calculator for Furnaces, ACs, Water Heaters & Appliances",
               "Should you repair or replace your furnace, AC, water heater or appliance? Apply the $5,000 rule, the 50% rule and lifespan math in seconds.",
               "Enter the age, the repair quote and the replacement price. We apply three proven rules of thumb and give you a straight answer.", body,
               [("What is the $5,000 rule?", "Multiply the equipment's age by the repair cost. If the result is over $5,000, replacing is usually the better investment."),
                ("What is the 50% rule?", "If a repair costs half or more of the price of a new unit, replacement usually makes more sense, especially on older equipment.")])

    # License lookup
    def lic(name, country):
        if name in DIRECT:
            u, lab = DIRECT[name]
            return f'<a data-item href="{u}" target="_blank" rel="noopener"><span>{e(name)}<br><small>{e(lab)}</small></span>{icon("arrow")}</a>'
        q = quote_plus(f"{name} contractor license lookup" + (" site:.gov" if country == "US" else " official"))
        return f'<a data-item href="https://duckduckgo.com/?q={q}" target="_blank" rel="noopener"><span>{e(name)}<br><small>Search official lookup</small></span>{icon("search")}</a>'
    us = "".join(lic(n, "US") for n in US)
    ca = "".join(lic(n, "CA") for n in CA)
    body = f"""<section><div class="wrap"><input class="search" type="search" placeholder="Type your state or province" data-filter="#licWrap" aria-label="Filter states and provinces">
<div id="licWrap"><h2 style="font-size:1.4rem">United States</h2><div class="lic-list">{us}</div><h2 style="font-size:1.4rem;margin-top:30px">Canada</h2><div class="lic-list">{ca}</div></div>
<div class="callout info" style="margin-top:26px">{icon("info")}<p>Licensing rules differ by trade and place. Some states license general contractors; others license only specific trades (electrical, plumbing, HVAC) or leave it to cities and counties. Direct links go to official agencies; other entries open a search for the official lookup.</p></div></div></section>
<section class="section-alt"><div class="wrap grid g2"><div><h2>Verify these five things</h2><ol class="big"><li><strong>Active license</strong>For the right trade, in your state or province, not expired or suspended.</li><li><strong>Liability insurance</strong>Ask for a certificate of insurance naming you as certificate holder.</li><li><strong>Workers' compensation</strong>If they have employees; otherwise injuries on your property can become your problem.</li><li><strong>Permits</strong>Who pulls them, and is the cost in the quote?</li><li><strong>Written contract</strong>Scope, price, schedule, warranty and payment terms.</li></ol></div>
<div>{ctx["video_block"]("57CeGJR_Xow", "How to Vet a Contractor | Ask This Old House", "This Old House")}</div></div></section>"""
    tool_shell(ctx, "tools/license-lookup.html", "License lookup", "Contractor License Lookup for Every State and Province",
               "Check a contractor's license: links to official license lookups for all 50 US states, DC and Canadian provinces, plus a 5-point verification checklist.",
               "Find the official license search for your state or province and verify a contractor before you sign.", body,
               [("Do all contractors need a license?", "It depends on the trade and location. Electricians, plumbers and gas fitters are licensed almost everywhere; general contractor licensing varies widely."),
                ("What if a contractor isn't licensed?", "Where a license is required, hiring an unlicensed contractor can void warranties, complicate insurance claims and leave you without legal recourse.")])

    # Emergency kit
    kit = "".join(f'<li><input type="checkbox" id="kit{i}"><label for="kit{i}">{e(t)}</label></li>' for i, t in enumerate(KIT))
    fields = [("addr", "Home address (for 911)"), ("water", "Main water shutoff location"), ("panel", "Breaker panel location"), ("gasutil", "Gas utility emergency number"),
              ("elecutil", "Electric utility outage number"), ("plumber", "Plumber"), ("electrician", "Electrician"), ("hvac", "Heating & cooling company"),
              ("insurer", "Insurance company & claims line"), ("contact", "Emergency contact")]
    fh = "".join(f'<div class="field"><label for="fc-{k}">{e(l)}</label><input id="fc-{k}" data-save="{k}" autocomplete="off"></div>' for k, l in fields)
    body = f"""<section><div class="wrap grid g2" style="align-items:start">
<div><div class="head-row" style="margin-bottom:12px"><h2 style="font-size:1.5rem">Your emergency kit</h2><span class="badge teal" data-pct="kit">0%</span></div>
<div class="meter" style="background:var(--line);margin:0 0 14px"><i data-bar="kit"></i></div>
<ul class="checklist" data-checklist="kit">{kit}</ul>
<div class="no-print" style="display:flex;gap:10px;margin-top:14px"><button class="btn btn-ghost btn-sm" type="button" data-reset="kit">Reset checklist</button><button class="btn btn-dark btn-sm" type="button" data-print>{icon("printer")} Print kit &amp; card</button></div>
<p class="muted" style="font-size:.88rem;margin-top:14px">Based on public preparedness guidance from Ready.gov and the Red Cross. Your progress saves on this device only.</p></div>
<div><div class="card" style="border:2px dashed var(--amber)"><span class="badge amber">Fridge card</span><h2 style="font-size:1.4rem;margin-top:10px">In an emergency</h2>
<p style="font-weight:700;color:var(--red)">Danger to life, fire, smoke, CO alarm: call 911. Smell gas: get out, then call.</p>{fh}
<p class="muted" style="font-size:.85rem;margin:0">Saved on this device only. Print and stick it on the fridge.</p></div></div></div></section>
<section class="section-alt no-print"><div class="wrap grid g2"><div><h2>Fire extinguisher basics: PASS</h2><p><b>Pull</b> the pin. <b>Aim</b> low at the base of the fire. <b>Squeeze</b> the handle. <b>Sweep</b> side to side. Only fight a small, contained fire with a clear exit behind you. If in doubt, get out and call 911.</p></div>
<div>{ctx["video_block"]("kiXqIjwyV5w", "PASS Technique for Fire Extinguisher Use", "Petroleum library")}</div></div></section>"""
    tool_shell(ctx, "tools/emergency-kit.html", "Emergency kit", "Home Emergency Kit Checklist & Printable Fridge Card",
               "A 16-item home emergency kit checklist with saved progress, plus a printable fridge card for shutoff locations, utility numbers and trusted pros.",
               "Check off your kit, record where your shutoffs are and who to call, then print it for the fridge.", body,
               [("How much water should be in an emergency kit?", "Preparedness agencies recommend about one gallon (4 liters) per person per day for several days."),
                ("Where should I keep the kit?", "Somewhere everyone can reach quickly, such as a hall closet. Keep a smaller version in the car.")])

    # Maintenance calendar
    months = ""
    for i, (m, tasks) in enumerate(MONTHS):
        lis = "".join(f'<li><input type="checkbox" id="m{i}t{j}"><label for="m{i}t{j}">{e(t)}</label></li>' for j, t in enumerate(tasks))
        months += f'<div class="month" data-m="{i}"><h3>{m} <span class="badge amber" hidden>This month</span></h3><ul class="checklist" data-checklist="m{i}" style="font-size:.93rem">{lis}</ul></div>'
    body = f"""<section><div class="wrap"><div class="head-row"><div class="chips" style="margin:0"><button class="chip" type="button" data-hemi="north">Northern hemisphere</button><button class="chip" type="button" data-hemi="south">Southern hemisphere</button></div>
<div style="display:flex;gap:8px"><button class="btn btn-dark btn-sm" type="button" id="icsBtn">{icon("calendar")} Add this month to my calendar</button><button class="btn btn-ghost btn-sm" type="button" data-print>{icon("printer")} Print</button></div></div>
<div class="month-grid" id="cal">{months}</div><p class="muted" style="font-size:.88rem;margin-top:16px">Checkmarks save on this device. Southern hemisphere mode shifts the seasons by six months.</p></div></section>"""
    tool_shell(ctx, "tools/maintenance-calendar.html", "Maintenance calendar", "Home Maintenance Calendar: What to Do Every Month",
               "A month-by-month home maintenance checklist that highlights this month's tasks, saves your progress and exports reminders to your calendar.",
               "Most emergencies are cheaper to prevent. This calendar shows what to check each month and highlights the current one.", body,
               [("What home maintenance should I do every month?", "Check filters, test alarms seasonally, keep gutters and drains clear and service heating and cooling before their busy seasons."),
                ("Does the calendar work for Canada?", "Yes. Canadian winters arrive earlier in many regions, so do the October and November tasks a few weeks sooner if needed.")])
