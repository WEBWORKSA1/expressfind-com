"""Company, monetization, community and legal pages."""
import os
from common import e, ROOT_DIR, REVIEWED, SERVICES
from icons import icon
from layout import crumbs_html, OWNER_URL

TRADES = ["Plumbing", "Water damage / restoration", "Heating & cooling (HVAC)", "Electrical", "Roofing", "Locksmith", "Garage doors", "Drain & sewer", "Mold remediation", "Tree service", "Appliance repair", "Handyman"]


def hero(crumb, eyebrow, h1, lead, extra=""):
    return f'<section class="page-hero"><div class="wrap">{crumbs_html([("Home","index.html"),(crumb,None)])}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div></section>'


def consent(text="I agree to be contacted about this submission and accept the"):
    return (f'<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true"><div class="field"><label class="check"><input type="checkbox" name="consent" value="yes" required> '
            f'<span>{text} <a href="@/privacy.html">Privacy Policy</a>.</span></label></div>')


def legal(ctx, path, crumb, title, h1, desc, updated, sections):
    toc = "".join(f'<li><a href="#s{i}">{e(t)}</a></li>' for i, (t, _) in enumerate(sections))
    body_s = "".join(f'<h2 id="s{i}">{e(t)}</h2>{c}' for i, (t, c) in enumerate(sections))
    body = f"""{hero(crumb, "Legal", h1, desc, f'<div class="meta-line"><span>Last updated {updated}</span></div>')}
<section><div class="wrap layout"><article class="prose">{body_s}</article>
<aside class="aside"><div class="card toc"><h3 style="margin-top:0;font-size:1rem">Contents</h3><ol>{toc}</ol></div><div class="card"><h3 style="margin-top:0;font-size:1rem">Questions?</h3><a class="btn btn-ghost btn-block btn-sm" href="@/contact.html">Contact us</a></div></aside></div></section>"""
    ctx["render"](path, f"{title} | ExpressFind", desc, body, "0.3", crumbs=[("Home", "index.html"), (crumb, None)])


def build_all(ctx):
    R = ctx["render"]
    cta = ctx["cta_band"]

    # ---------------- For pros
    trades = "".join(f'<label class="choice"><input type="checkbox" name="trades" value="{e(t)}"><span>{e(t)}</span></label>' for t in TRADES)
    faqs = [("How much do leads cost?", "Pricing depends on trade, market and urgency. We share current rates with each partner before they accept any requests, and founding partners get introductory pricing."),
            ("Are leads exclusive?", "Each request is shared with no more than three providers so homeowners can compare. Some categories and regions offer exclusive emergency requests."),
            ("Can I choose my service area and hours?", "Yes. You set the ZIP or postal codes you serve, the trades you take and whether you accept after-hours emergency requests."),
            ("What do you require from partners?", "A valid license where your trade requires one, active liability insurance, and a commitment to respond to homeowners quickly and honestly.")]
    body = f"""{hero("For pros", "For contractors", "Get emergency and local jobs from homeowners ready to hire", "ExpressFind homeowners arrive mid-problem: burst pipes, no heat, roof leaks, lockouts. Join the network and receive requests that match your trade, area and hours.", f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn btn-amber" href="#join">Join the pro network</a><a class="btn btn-ghost" style="color:#fff;border-color:#ffffff44" href="#roi">Run the ROI math</a></div>')}
<section><div class="wrap grid g4">
<div class="card"><div class="ico">{icon("alert")}</div><h3>Emergency-ready</h3><p class="muted" style="font-size:.93rem">Requests are flagged by urgency, so you know which jobs need a truck tonight.</p></div>
<div class="card"><div class="ico">{icon("pin")}</div><h3>Your area, your rules</h3><p class="muted" style="font-size:.93rem">Choose ZIP or postal codes, trades and after-hours availability.</p></div>
<div class="card"><div class="ico">{icon("list")}</div><h3>Better-qualified requests</h3><p class="muted" style="font-size:.93rem">Service, urgency, ownership, budget and details come with every request.</p></div>
<div class="card"><div class="ico">{icon("users")}</div><h3>Max three providers</h3><p class="muted" style="font-size:.93rem">Homeowners compare a short list, not a bidding war of ten.</p></div></div></section>
<section class="section-alt" id="roi"><div class="wrap layout"><div class="tool"><h2 style="font-size:1.5rem">Lead ROI calculator</h2>
<div class="row"><div class="field"><label for="roi-job">Average job value ($)</label><input id="roi-job" type="number" value="650"></div><div class="field"><label for="roi-close">Close rate (%)</label><input id="roi-close" type="number" value="35"></div></div>
<div class="row"><div class="field"><label for="roi-leads">Requests per month</label><input id="roi-leads" type="number" value="20"></div><div class="field"><label for="roi-cpl">Cost per request ($)</label><input id="roi-cpl" type="number" value="40"></div></div>
<div class="field"><label for="roi-margin">Gross margin (%)</label><input id="roi-margin" type="number" value="45"></div>
<div class="out"><small>Monthly outcome</small><div class="big" id="roi-profit">—</div><p>Gross profit after lead cost</p>
<div class="kv"><span>Jobs won</span><span id="roi-jobs">—</span><span>Revenue</span><span id="roi-rev">—</span><span>Lead spend</span><span id="roi-cost">—</span><span>Cost per job won</span><span id="roi-cpa">—</span><span>Return</span><span id="roi-x">—</span></div></div></div>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">Benchmarks to sanity-check</h3><p class="muted" style="font-size:.92rem;margin:0">Home-services search ads average several dollars per click, and paid-search cost per lead in plumbing, HVAC and roofing commonly runs from about $50 to well over $150. Compare your blended cost per job won, not just cost per lead.</p></div></aside></div></section>
<section id="join"><div class="wrap layout"><div class="form-card"><h2 style="font-size:1.6rem">Join the ExpressFind pro network</h2><p class="muted">Takes two minutes. We'll reply within one business day with pricing for your area.</p>
<form class="js-form" data-subject="PRO SIGNUP" data-redirect="@/thank-you.html" data-type="pro">
<div class="row"><div class="field"><label for="p-biz">Business name</label><input id="p-biz" name="business" required></div><div class="field"><label for="p-name">Your name</label><input id="p-name" name="name" required autocomplete="name"></div></div>
<div class="row"><div class="field"><label for="p-email">Email</label><input id="p-email" name="email" type="email" required autocomplete="email"></div><div class="field"><label for="p-phone">Phone</label><input id="p-phone" name="phone" type="tel" required autocomplete="tel"></div></div>
<span class="lbl">Trades you serve</span><div class="choice-grid">{trades}</div>
<div class="field"><label for="p-area">Service area (ZIP/postal codes or cities)</label><input id="p-area" name="service_area" required placeholder="e.g. 77002, 77003, Houston metro"></div>
<div class="row"><div class="field"><label for="p-lic">License number (if required)</label><input id="p-lic" name="license"></div><div class="field"><label for="p-ins">Liability insurance</label><select id="p-ins" name="insured"><option>Yes, active</option><option>In progress</option><option>No</option></select></div></div>
<div class="row"><div class="field"><label for="p-hrs">After-hours emergencies</label><select id="p-hrs" name="after_hours"><option>Yes, 24/7</option><option>Evenings &amp; weekends</option><option>Business hours only</option></select></div><div class="field"><label for="p-cap">Requests you can handle / month</label><select id="p-cap" name="capacity"><option>1–10</option><option>11–30</option><option>31–75</option><option>75+</option></select></div></div>
<div class="field"><label for="p-web">Website or Google Business profile</label><input id="p-web" name="website" type="url" placeholder="https://"></div>
<div class="field"><label for="p-notes">Anything else?</label><textarea id="p-notes" name="message"></textarea></div>
{consent()}<button class="btn btn-amber btn-block" type="submit">Apply to join</button><div class="form-msg" role="status" aria-live="polite"></div></form></div>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">Prefer to advertise?</h3><p class="muted" style="font-size:.92rem">Sponsor a category or emergency playbook in your region.</p><a class="btn btn-ghost btn-block btn-sm" href="@/advertise.html">Advertising options</a></div></aside></div></section>
<section class="section-alt"><div class="wrap" style="max-width:860px"><h2>Pro FAQ</h2>{ctx["faq_html"](faqs)}</div></section>"""
    R("pros.html", "Get Emergency Plumbing, HVAC & Roofing Leads — Join as a Pro | ExpressFind",
      "Contractors: receive homeowner emergency and repair requests in your service area. Choose trades, hours and ZIP codes. Lead ROI calculator included.", body, "0.8",
      crumbs=[("Home", "index.html"), ("For pros", None)], schema=[ctx["faq_ld"](faqs)])

    # ---------------- Advertise
    pk = [("Category sponsor", "Your brand on every cost guide and playbook in one category (for example, all plumbing pages), with a sponsor card and link."),
          ("Emergency playbook sponsor", "Exclusive placement on a high-urgency playbook such as burst pipe, no heat or roof leak."),
          ("Regional pro spotlight", "Featured provider card for a city or region on matching pages, plus priority routing of requests."),
          ("Newsletter & seasonal alerts", "Sponsor the monthly seasonal checklist email and the maintenance calendar."),
          ("Custom content & tools", "Co-branded calculators, checklists or guides, clearly labeled as sponsored.")]
    cards = "".join(f'<div class="card"><div class="ico">{icon("megaphone")}</div><h3>{e(t)}</h3><p class="muted" style="font-size:.93rem">{e(d)}</p></div>' for t, d in pk)
    opts = "".join(f"<option>{e(t)}</option>" for t, _ in pk)
    body = f"""{hero("Advertise", "Advertise & sponsor", "Reach homeowners at the exact moment they need help", "Sponsorships on ExpressFind sit beside emergency playbooks, cost guides and free tools that people use right before they hire.")}
<section><div class="wrap"><div class="grid g3">{cards}<div class="card" style="background:var(--ink);color:#fff"><h3 style="color:#fff">Buy the site or domain</h3><p style="color:#c3d1de;font-size:.93rem">Interested in this website, the ExpressFind.com domain name or a strategic partnership?</p><a class="btn btn-amber" href="{OWNER_URL}" target="_blank" rel="noopener">web.works/contact</a></div></div></div></section>
<section class="section-alt"><div class="wrap layout"><div class="form-card"><h2 style="font-size:1.6rem">Request a media kit</h2>
<form class="js-form" data-subject="ADVERTISING INQUIRY" data-redirect="@/thank-you.html" data-type="advertise">
<div class="row"><div class="field"><label for="a-co">Company</label><input id="a-co" name="business" required></div><div class="field"><label for="a-name">Your name</label><input id="a-name" name="name" required></div></div>
<div class="row"><div class="field"><label for="a-email">Work email</label><input id="a-email" name="email" type="email" required></div><div class="field"><label for="a-phone">Phone (optional)</label><input id="a-phone" name="phone" type="tel"></div></div>
<div class="row"><div class="field"><label for="a-pk">Interested in</label><select id="a-pk" name="package">{opts}<option>Website / domain purchase</option><option>Partnership</option></select></div><div class="field"><label for="a-bud">Monthly budget</label><select id="a-bud" name="budget"><option>Under $500</option><option>$500 – $2,000</option><option>$2,000 – $10,000</option><option>$10,000+</option></select></div></div>
<div class="field"><label for="a-reg">Target regions</label><input id="a-reg" name="regions" placeholder="e.g. Texas, Ontario, nationwide"></div>
<div class="field"><label for="a-msg">Goals</label><textarea id="a-msg" name="message"></textarea></div>
{consent()}<button class="btn btn-amber btn-block" type="submit">Send inquiry</button><div class="form-msg" role="status" aria-live="polite"></div></form></div>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">Our ad standards</h3><ul style="margin:0;font-size:.92rem"><li>Sponsored content is always labeled.</li><li>No sponsor changes our cost data or safety advice.</li><li>We decline advertisers with unresolved consumer complaints or licensing problems.</li></ul></div></aside></div></section>"""
    R("advertise.html", "Advertise & Sponsor on ExpressFind — Home Services Audience | ExpressFind",
      "Sponsorship packages for home-services brands: category sponsorships, emergency playbook placements, regional pro spotlights, newsletter and custom tools.", body, "0.6",
      crumbs=[("Home", "index.html"), ("Advertise", None)])

    # ---------------- Support / donate
    amt = "".join(f'<label class="choice"><input type="radio" name="amount" value="{a}" required><span>{a}</span></label>' for a in ["$5", "$15", "$25", "$50", "$100", "$250"])
    body = f"""{hero("Support us", "Support ExpressFind", "Keep honest prices and safety guides free for everyone", "Your contribution pays for operations, new guides and tools, promotion to reach more homeowners, hiring licensed reviewers and monthly contest prizes.")}
<section><div class="wrap layout"><div>
<h2>Where your support goes</h2>
<div class="alloc" aria-hidden="true"><i style="width:35%;background:var(--teal)"></i><i style="width:25%;background:var(--amber)"></i><i style="width:25%;background:#5b7fa3"></i><i style="width:15%;background:var(--red)"></i></div>
<div class="legend"><span><i style="background:var(--teal)"></i>Operations &amp; hosting 35%</span><span><i style="background:var(--amber)"></i>Promotions &amp; marketing 25%</span><span><i style="background:#5b7fa3"></i>Hiring talent 25%</span><span><i style="background:var(--red)"></i>Contests &amp; prizes 15%</span></div>
<p class="muted" style="font-size:.9rem;margin-top:8px">Target allocation. You can direct your contribution to one purpose in the form.</p>
<div class="grid g2" style="margin-top:20px">
<div class="card"><div class="ico">{icon("wrench")}</div><h3>Operations</h3><p class="muted" style="font-size:.93rem">Hosting, data updates, tool maintenance and security.</p></div>
<div class="card"><div class="ico">{icon("megaphone")}</div><h3>Promotions &amp; marketing</h3><p class="muted" style="font-size:.93rem">Reaching homeowners before emergencies, not just during them.</p></div>
<div class="card"><div class="ico">{icon("briefcase")}</div><h3>Hiring talent</h3><p class="muted" style="font-size:.93rem">Paying licensed plumbers, electricians and HVAC techs to review our guides.</p></div>
<div class="card"><div class="ico">{icon("trophy")}</div><h3>Contests &amp; prizes</h3><p class="muted" style="font-size:.93rem">Monthly gift cards for the best home-save stories and tips.</p></div></div>
<h2 style="margin-top:34px">Monthly supporter tiers</h2><div class="grid g3">
<div class="card tier"><h3>Neighbor</h3><div class="price">$5</div><ul><li>Name on the supporters list (optional)</li><li>Early seasonal checklists</li></ul></div>
<div class="card tier featured"><h3>Helper</h3><div class="price">$15</div><ul><li>Everything in Neighbor</li><li>Vote on the next guide we publish</li><li>Supporter badge on contest entries</li></ul></div>
<div class="card tier"><h3>Champion</h3><div class="price">$50</div><ul><li>Everything in Helper</li><li>Sponsor a month's contest prize (credited)</li><li>Quarterly impact note</li></ul></div></div></div>
<aside class="aside" style="position:static"><div class="form-card"><h2 style="font-size:1.4rem">Make a contribution</h2>
<form class="js-form" data-subject="DONATION PLEDGE" data-redirect="@/thank-you.html" data-type="donation">
<span class="lbl">Type</span><div class="choice-grid" style="grid-template-columns:1fr 1fr"><label class="choice"><input type="radio" name="frequency" value="One-time" required><span>One-time</span></label><label class="choice"><input type="radio" name="frequency" value="Monthly"><span>Monthly</span></label></div>
<span class="lbl">Amount (USD)</span><div class="choice-grid" style="grid-template-columns:repeat(3,1fr)">{amt}</div>
<div class="field"><label for="d-other">Other amount (optional)</label><input id="d-other" name="other_amount" type="number" min="1" placeholder="$"></div>
<div class="field"><label for="d-purpose">Direct my support to</label><select id="d-purpose" name="purpose"><option>Wherever it's needed most</option><option>Operations &amp; hosting</option><option>Promotions &amp; marketing</option><option>Hiring talent</option><option>Contests &amp; prizes</option></select></div>
<div class="field"><label for="d-name">Name</label><input id="d-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="d-email">Email</label><input id="d-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label class="check"><input type="checkbox" name="public" value="Show my name"> <span>Show my name on the supporters list</span></label></div>
{consent("I agree to be contacted about my contribution and accept the")}
<button class="btn btn-amber btn-block" type="submit">Continue to secure payment</button><div class="form-msg" role="status" aria-live="polite"></div></form>
<p class="notice">We email you a secure payment link from an established payment provider. We never ask for card details in a form. ExpressFind is not a registered charity, so contributions are not tax-deductible.</p></div></aside></div></section>
<section class="section-alt"><div class="wrap"><h2>Other ways to help</h2><div class="grid g4">
<div class="card"><h3>Share a guide</h3><p class="muted" style="font-size:.92rem">Send a playbook to a friend before their pipes freeze.</p></div>
<div class="card"><h3>Report an error</h3><p class="muted" style="font-size:.92rem">Spot a wrong price or unsafe advice? <a href="@/contact.html">Tell us</a>.</p></div>
<div class="card"><h3>Enter the contest</h3><p class="muted" style="font-size:.92rem">Your home-save story helps others. <a href="@/contests.html">Enter</a>.</p></div>
<div class="card"><h3>Sponsor</h3><p class="muted" style="font-size:.92rem">Companies can <a href="@/advertise.html">sponsor a category</a> or prize.</p></div></div></div></section>"""
    R("support.html", "Support ExpressFind — Donate to Keep Home Safety Guides Free | ExpressFind",
      "Support free home emergency guides and honest cost data. Contributions fund operations, promotion, licensed reviewers and monthly contest prizes.", body, "0.5",
      crumbs=[("Home", "index.html"), ("Support us", None)])

    # ---------------- Contests
    faqs = [("Do I have to buy anything to enter?", "No. No purchase or payment is necessary to enter or win."),
            ("Who can enter?", "Legal residents of the United States (50 states and DC) and Canada who are 18 or older, or the age of majority where they live. Void where prohibited."),
            ("How is the winner chosen?", "Entries are judged on usefulness to other homeowners (40%), clarity (30%) and originality (30%). It is a contest of skill, not a random draw."),
            ("What if a Canadian resident wins?", "Canadian winners must correctly answer a time-limited mathematical skill-testing question before receiving the prize.")]
    body = f"""{hero("Contests", "Monthly contest", "The Home Hero Contest", "Share the time you saved your home from disaster — or your best maintenance tip. Each month, the most useful entry wins a $100 home-improvement gift card.")}
<section><div class="wrap layout"><div>
<div class="card" style="background:var(--ink);color:#fff;border:0"><span class="badge amber">Now open: <span id="contestMonth">this month</span></span><h2 style="color:#fff;margin-top:14px">Entries close in</h2><div class="countdown" id="contestCountdown">—</div><p style="color:#c3d1de;margin:10px 0 0">Deadline: <span id="contestDeadline">end of month</span></p></div>
<h2 style="margin-top:30px">How to enter</h2><ol class="big"><li><strong>Pick a category</strong>Emergency save story, maintenance tip, or before-and-after fix.</li><li><strong>Tell it in your own words</strong>What happened, what you did, what you'd tell a neighbor. 100–500 words is ideal.</li><li><strong>Add a photo link (optional)</strong>A link to a photo you took and own.</li></ol>
<div class="form-card" style="margin-top:20px"><h2 style="font-size:1.5rem">Submit your entry</h2>
<form class="js-form" data-subject="CONTEST ENTRY" data-redirect="@/thank-you.html" data-type="contest">
<div class="row"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name"></div><div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="row"><div class="field"><label for="c-country">Country</label><select id="c-country" name="country"><option>United States</option><option>Canada</option></select></div><div class="field"><label for="c-region">State / province</label><input id="c-region" name="region" required></div></div>
<div class="field"><label for="c-cat">Category</label><select id="c-cat" name="category"><option>Emergency save story</option><option>Maintenance tip</option><option>Before-and-after fix</option></select></div>
<div class="field"><label for="c-story">Your story or tip</label><textarea id="c-story" name="story" required minlength="80" style="min-height:180px"></textarea></div>
<div class="field"><label for="c-photo">Photo link (optional)</label><input id="c-photo" name="photo_link" type="url" placeholder="https://"></div>
<div class="field"><label class="check"><input type="checkbox" name="age" value="18+" required> <span>I am 18 or older (or the age of majority where I live) and a legal resident of the US or Canada.</span></label></div>
<div class="field"><label class="check"><input type="checkbox" name="rules" value="accepted" required> <span>I accept the official rules below and grant ExpressFind permission to publish my entry with my first name and region.</span></label></div>
{consent("I agree to be contacted about my entry and accept the")}
<button class="btn btn-amber btn-block" type="submit">Submit my entry</button><div class="form-msg" role="status" aria-live="polite"></div></form></div>
<h2 id="rules" style="margin-top:34px">Official rules (summary)</h2>
<div class="prose" style="font-size:.95rem"><p><strong>No purchase necessary.</strong> Sponsor: ExpressFind.com. Each contest period runs from the first day to the last day of a calendar month (local time of the entrant). One entry per person per month.</p>
<p><strong>Eligibility:</strong> legal residents of the 50 United States, DC and Canada, 18 or older or the age of majority in their jurisdiction. Void where prohibited or restricted by law. Employees and contractors of the sponsor and their immediate families are not eligible.</p>
<p><strong>Judging:</strong> entries are judged by the ExpressFind editorial team on usefulness to homeowners (40%), clarity (30%) and originality (30%). Entries must be the entrant's own original work, must not include unsafe advice, and must not include another person's image without permission.</p>
<p><strong>Prize:</strong> one (1) home-improvement retailer gift card with a value of $100 USD per month. No cash alternative except at the sponsor's discretion. Canadian residents must correctly answer a time-limited mathematical skill-testing question to receive a prize.</p>
<p><strong>Winner notification:</strong> by email within 10 days after each period ends. If a winner does not respond within 14 days, an alternate may be selected.</p>
<p><strong>Publicity and privacy:</strong> by entering, you allow ExpressFind to publish your entry, first name and state or province. Personal information is handled under our <a href="@/privacy.html">Privacy Policy</a>. The sponsor may modify or cancel a contest period if it cannot be run as planned.</p></div></div>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">Fund the prize</h3><p class="muted" style="font-size:.92rem">Companies and supporters can sponsor a month's prize and be credited on this page.</p><a class="btn btn-ghost btn-block btn-sm" href="@/support.html">Support or sponsor</a></div>
<div class="card"><h3 style="margin-top:0;font-size:1.05rem">Need inspiration?</h3><ul style="margin:0;font-size:.92rem"><li><a href="@/emergency/frozen-pipes.html">Frozen pipe saves</a></li><li><a href="@/tools/maintenance-calendar.html">Maintenance habits</a></li><li><a href="@/emergency/no-heat.html">No-heat fixes</a></li></ul></div></aside></div></section>
<section class="section-alt"><div class="wrap" style="max-width:860px"><h2>Contest FAQ</h2>{ctx["faq_html"](faqs)}</div></section>"""
    R("contests.html", "Home Hero Contest — Win a $100 Home-Improvement Gift Card | ExpressFind",
      "Share your best home emergency save or maintenance tip. Monthly skill-based contest for US and Canadian residents. No purchase necessary.", body, "0.6",
      crumbs=[("Home", "index.html"), ("Contests", None)], schema=[ctx["faq_ld"](faqs)])

    # ---------------- Careers
    roles = [("Licensed trade reviewer", "Contract · Remote · Per review", "Licensed plumbers, electricians, HVAC techs and roofers who fact-check our playbooks and cost guides. You'll be credited on the pages you review."),
             ("Cost guide writer", "Freelance · Remote", "Clear, careful writers who can turn messy pricing data into honest, readable guides. Home-services experience is a plus."),
             ("Short-form video creator", "Freelance · Remote", "Create 30–90 second safety and how-to videos for YouTube Shorts, TikTok and Instagram."),
             ("Local partnerships representative", "Commission · Remote (US/Canada)", "Recruit reputable local pros into the network in your region."),
             ("Front-end developer", "Contract · Remote", "Vanilla JS and accessible HTML/CSS. Help build new calculators and tools.")]
    rc = "".join(f'<div class="card"><span class="badge teal">{e(m)}</span><h3>{e(t)}</h3><p class="muted" style="font-size:.93rem">{e(d)}</p></div>' for t, m, d in roles)
    ro = "".join(f"<option>{e(t)}</option>" for t, _, _ in roles)
    body = f"""{hero("Careers", "Careers", "Help homeowners get through their worst days", "We're building the most useful, most honest home emergency resource on the web. We hire flexible, remote talent across the US and Canada.")}
<section><div class="wrap"><div class="grid g3">{rc}<div class="card" style="background:var(--surface-2)"><h3>Don't see your role?</h3><p class="muted" style="font-size:.93rem">Tell us how you'd help. We read every application.</p></div></div></div></section>
<section class="section-alt"><div class="wrap layout"><div class="form-card"><h2 style="font-size:1.6rem">Apply</h2>
<form class="js-form" data-subject="CAREERS APPLICATION" data-redirect="@/thank-you.html" data-type="careers">
<div class="row"><div class="field"><label for="j-name">Name</label><input id="j-name" name="name" required autocomplete="name"></div><div class="field"><label for="j-email">Email</label><input id="j-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="row"><div class="field"><label for="j-role">Role</label><select id="j-role" name="role">{ro}<option>Other</option></select></div><div class="field"><label for="j-loc">Location</label><input id="j-loc" name="location" required></div></div>
<div class="row"><div class="field"><label for="j-link">Portfolio, LinkedIn or license number</label><input id="j-link" name="link"></div><div class="field"><label for="j-rate">Rate expectation</label><input id="j-rate" name="rate" placeholder="e.g. $40/hr or per piece"></div></div>
<div class="field"><label for="j-msg">Why you, in a few sentences</label><textarea id="j-msg" name="message" required></textarea></div>
{consent()}<button class="btn btn-amber btn-block" type="submit">Send application</button><div class="form-msg" role="status" aria-live="polite"></div></form></div>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">How we work</h3><ul style="margin:0;font-size:.92rem"><li>Remote and asynchronous</li><li>Paid per project or per review</li><li>Safety and accuracy over speed</li><li>Credit on the work you do</li></ul></div></aside></div></section>"""
    R("careers.html", "Careers at ExpressFind — Trade Reviewers, Writers, Video Creators | ExpressFind",
      "Remote and freelance roles: licensed trade reviewers, cost guide writers, short-form video creators, partnerships reps and front-end developers.", body, "0.5",
      crumbs=[("Home", "index.html"), ("Careers", None)])

    # ---------------- About
    body = f"""{hero("About", "About", "Fast help, fair prices, trusted pros", "ExpressFind exists for the worst ten minutes of homeownership: water on the floor, no heat, a smell of gas, a locked door. We help people act safely first, understand the price, and reach a qualified local pro.")}
<section><div class="wrap layout"><article class="prose">
<h2>What we do</h2><ul><li><strong>Emergency playbooks</strong> with safety-first steps for the first 15 minutes.</li><li><strong>Cost guides</strong> that compile multiple independent sources into honest ranges and adjust for inflation weekly.</li><li><strong>Free tools</strong> to estimate, compare quotes, decide repair vs. replace and verify licenses.</li><li><strong>Request routing</strong> that sends one homeowner request to up to three independent local pros.</li></ul>
<h2>What we don't do</h2><ul><li>We are not a contractor and do not perform repairs.</li><li>We are not an emergency service and never replace 911 or your utility.</li><li>We don't publish fake reviews, inflated user counts or "verified" badges we can't back up.</li><li>We don't let advertisers change our cost data or safety advice.</li></ul>
<h2>How we make money</h2><p>ExpressFind is free for homeowners. We earn revenue from display advertising (including Google AdSense), from service providers who receive homeowner requests, from clearly labeled sponsorships, and from voluntary supporter contributions. This may influence which providers receive requests in a given area, but it never changes the prices or safety steps we publish.</p>
<h2>Editorial standards</h2><p>Every guide lists the sources we consulted and the date it was reviewed. Safety steps follow published public-safety guidance from agencies such as Ready.gov and the U.S. EPA. We correct errors promptly — use the <a href="@/contact.html">contact form</a> and choose "Correction".</p>
<h2>Where we operate</h2><p>ExpressFind serves homeowners and renters across the United States and Canada. Cost data is published in US dollars.</p>
<h2>Website, domain and partnerships</h2><p>Interested in this website, the ExpressFind.com domain, sponsorship, advertising or a partnership? Contact the owner at <a href="{OWNER_URL}" target="_blank" rel="noopener">web.works/contact</a>.</p></article>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">Quick links</h3><ul style="margin:0;font-size:.93rem"><li><a href="@/methodology.html">How we research costs</a></li><li><a href="@/disclaimer.html">Disclaimer</a></li><li><a href="@/trademark.html">Trademark &amp; copyright</a></li><li><a href="@/contact.html">Contact</a></li></ul></div></aside></div></section>"""
    R("about.html", "About ExpressFind — Emergency-First Home Services Finder | ExpressFind",
      "ExpressFind helps homeowners act safely in home emergencies, understand fair prices and reach local pros. How we work, how we make money and our standards.", body, "0.5",
      crumbs=[("Home", "index.html"), ("About", None)])

    # ---------------- Methodology
    cpi = ctx["CPI"]
    body = f"""{hero("Methodology", "Methodology", "How we research and update cost data", "Our goal is a range you can trust before you call — not the lowest number, not a sales pitch.")}
<section><div class="wrap layout"><article class="prose">
<h2>1. We compile, compare and round</h2><p>For each service we review several independent sources: national cost surveys, contractor price lists and published pricing guides. We look for agreement across sources, discard outliers and publish a rounded low-to-high range plus a typical midpoint. Each guide lists the sources we consulted.</p>
<h2>2. We separate the job from the timing</h2><p>Emergency and after-hours pricing is shown separately because it changes the bill more than almost anything else. Our estimator applies common multipliers — roughly 1.5× for evenings, about 1.75× for weekends and about 2× for holidays or overnight — and regional adjustments from about 0.85× for lower-cost areas to about 1.35× for the most expensive metros.</p>
<h2>3. We adjust for inflation automatically</h2><p>Base ranges were compiled in {REVIEWED}. A scheduled job checks the U.S. Bureau of Labor Statistics Consumer Price Index (CPI-U, all items) every week and scales every published range by the change since that baseline. Current adjustment factor: <strong>{float(cpi.get("factor", 1.0)):.3f}</strong> (through {e(cpi.get("label", REVIEWED))}). We also track the CPI index for repair of household items as a "Price Pulse" signal.</p>
<h2>4. Safety guidance comes from public-safety agencies</h2><p>Emergency playbooks follow widely published guidance from agencies such as Ready.gov and the U.S. EPA, along with standard trade safety practice. When advice differs between sources, we choose the more cautious option.</p>
<h2>5. We review and correct</h2><p>Guides show their review date. We re-review guides at least once a year and immediately when a reader reports a problem. Licensed trade reviewers are being added to the review process — <a href="@/careers.html">apply here</a>.</p>
<h2>Limits</h2><p>National ranges cannot reflect every home. Your price depends on your market, access, materials, code requirements and what the pro finds. Always get written quotes.</p></article>
<aside class="aside"><div class="card"><h3 style="margin-top:0;font-size:1.05rem">See it in action</h3><a class="btn btn-ghost btn-block btn-sm" href="@/costs.html">Cost guides</a><a class="btn btn-ghost btn-block btn-sm" style="margin-top:8px" href="@/tools/cost-estimator.html">Cost estimator</a></div></aside></div></section>"""
    R("methodology.html", "How We Research Home Repair Costs — Methodology | ExpressFind",
      "How ExpressFind compiles cost ranges, separates emergency pricing, adjusts for inflation weekly with BLS CPI data and sources its safety guidance.", body, "0.5",
      crumbs=[("Home", "index.html"), ("Methodology", None)])

    # ---------------- Contact
    body = f"""{hero("Contact", "Contact", "Talk to ExpressFind", "Questions, corrections, partnerships or press. We reply within one business day. For a service request, use the quote form so it reaches local pros faster.")}
<section><div class="wrap grid g2" style="align-items:start"><div class="form-card">
<form class="js-form" data-subject="CONTACT FORM" data-ok="Message sent. We'll reply within one business day.">
<div class="row"><div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required autocomplete="name"></div><div class="field"><label for="ct-email">Email</label><input id="ct-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="field"><label for="ct-topic">Topic</label><select id="ct-topic" name="topic"><option>General question</option><option>Correction</option><option>Pro network</option><option>Advertising / sponsorship</option><option>Partnership</option><option>Website / domain purchase</option><option>Press</option><option>Privacy request</option></select></div>
<div class="field"><label for="ct-msg">Message</label><textarea id="ct-msg" name="message" required></textarea></div>
{consent()}<button class="btn btn-amber btn-block" type="submit">Send message</button><div class="form-msg" role="status" aria-live="polite"></div></form></div>
<div><div class="card" style="border:2px solid var(--red)"><h3 style="margin-top:0">{icon("alert")} Emergency?</h3><p class="muted">We can't dispatch help through this form. Call 911 if anyone is in danger, then use our <a href="@/emergency.html">emergency help center</a>.</p></div>
<div class="card" style="margin-top:16px"><h3 style="margin-top:0">Buy, sponsor or partner</h3><p class="muted">Interested in this website, the domain name, sponsorship, advertising or a partnership?</p><a class="btn btn-amber" href="{OWNER_URL}" target="_blank" rel="noopener">web.works/contact</a></div>
<div class="card" style="margin-top:16px"><h3 style="margin-top:0">Prefer email?</h3><p class="muted">Opens your email app with our address filled in.</p><a class="btn btn-ghost" href="@/contact.html" data-mail="Inquiry from ExpressFind.com">{icon("mail")} Email us</a></div>
<div class="card" style="margin-top:16px"><h3 style="margin-top:0">Need a pro?</h3><a class="btn btn-dark" href="@/get-quotes.html">Get free quotes</a></div></div></div></section>"""
    R("contact.html", "Contact ExpressFind | ExpressFind", "Contact ExpressFind for questions, corrections, the pro network, advertising, partnerships, press or website and domain inquiries.", body, "0.5",
      crumbs=[("Home", "index.html"), ("Contact", None)])

    # ---------------- Thank you
    body = f"""{hero("Thank you", "Received", "Thank you — we've got it", "Here's what happens next.")}
<section><div class="wrap" style="max-width:860px" id="tyBox">
<div data-ty="quote"><div class="card"><span class="badge teal">Request reference <span id="refNo">—</span></span><h2 style="margin-top:12px">Your request is on its way</h2><ol class="big"><li><strong>We route it</strong>Your request goes to up to three local pros who serve your area.</li><li><strong>Pros contact you</strong>Keep your phone nearby. Emergency requests are flagged urgent.</li><li><strong>You choose</strong>Compare availability, price and warranty. No obligation.</li></ol></div>
<div class="callout danger" id="tyEmergency" hidden>{icon("alert")}<p><strong>While you wait:</strong> stop the source if you safely can (water main, breaker), keep people away from hazards and call 911 if anyone is in danger. <a href="@/emergency.html">Open the emergency playbooks</a>.</p></div>
<div class="grid g3" style="margin-top:18px"><a class="card card-link" href="@/tools/quote-checker.html"><h3 style="margin-top:0">Check quotes</h3><span class="more">Quote checker →</span></a><a class="card card-link" href="@/tools/license-lookup.html"><h3 style="margin-top:0">Verify a license</h3><span class="more">License lookup →</span></a><a class="card card-link" href="@/costs.html"><h3 style="margin-top:0">Know the price</h3><span class="more">Cost guides →</span></a></div></div>
<div data-ty="pro" hidden><div class="card"><h2 style="margin-top:0">Application received</h2><p>We'll reply within one business day with pricing and coverage for your service area.</p><a class="btn btn-dark" href="@/costs.html">See what homeowners read before they call</a></div></div>
<div data-ty="donation" hidden><div class="card"><h2 style="margin-top:0">Thank you for supporting ExpressFind</h2><p>We'll email you a secure payment link within 24 hours. No card details are ever requested through a form.</p></div></div>
<div data-ty="contest" hidden><div class="card"><h2 style="margin-top:0">Your entry is in</h2><p>Winners are notified by email within 10 days after the month ends. Good luck!</p></div></div>
<div data-ty="careers" hidden><div class="card"><h2 style="margin-top:0">Application received</h2><p>We read every application and reply to shortlisted candidates within a week.</p></div></div>
<div data-ty="advertise" hidden><div class="card"><h2 style="margin-top:0">Inquiry received</h2><p>We'll send the media kit and availability within one business day.</p></div></div>
<div data-ty="form" hidden><div class="card"><h2 style="margin-top:0">Message received</h2><p>We'll reply within one business day.</p></div></div>
<p style="margin-top:20px"><a href="@/index.html">← Back to home</a></p></div></section>"""
    R("thank-you.html", "Thank You | ExpressFind", "Your submission was received.", body, "0.1", noindex=True)

    # ---------------- Legal pages
    U = REVIEWED
    legal(ctx, "privacy.html", "Privacy policy", "Privacy Policy", "Privacy Policy", "How ExpressFind collects, uses and shares information, including advertising cookies and service requests.", U, [
        ("Who we are", "<p>ExpressFind.com (\"ExpressFind\", \"we\") is an independent online publisher of home emergency information, cost guides and tools, and a service-request routing service for homeowners in the United States and Canada.</p>"),
        ("Information you give us", "<p>When you submit a form we collect what you enter, such as your name, email, phone number, ZIP or postal code, a description of your request and your preferences. Forms are delivered to our private inbox through a third-party form processor (FormSubmit). We also record the page you submitted from and campaign tags (such as utm parameters) to understand which pages help people most.</p>"),
        ("How we use it", "<ul><li>To route your service request to up to three independent local providers who may contact you about it.</li><li>To reply to messages, applications, contest entries, sponsorship inquiries and contributions.</li><li>To send seasonal tips if you opted in (unsubscribe anytime).</li><li>To prevent fraud and abuse and to improve the site.</li></ul>"),
        ("Sharing with service providers", "<p>If you request quotes, you authorize us to share your request details and contact information with up to three independent service providers. Those providers are not our agents; their use of your information is governed by their own policies. We do not sell your information to data brokers or list resellers.</p>"),
        ("Advertising and Google cookies", "<p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this site and/or other sites on the internet.</p><p>You can opt out of personalized advertising by visiting <a href=\"https://www.google.com/settings/ads\" target=\"_blank\" rel=\"noopener\">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies for personalized advertising at <a href=\"https://www.aboutads.info/choices/\" target=\"_blank\" rel=\"noopener\">aboutads.info</a> (US) and <a href=\"https://youradchoices.ca/\" target=\"_blank\" rel=\"noopener\">youradchoices.ca</a> (Canada). Learn more in <a href=\"https://policies.google.com/technologies/partner-sites\" target=\"_blank\" rel=\"noopener\">How Google uses information from sites that use its services</a>.</p>"),
        ("Other third parties", "<ul><li><strong>YouTube</strong>: videos load in privacy-enhanced mode only after you press play; YouTube's policies then apply.</li><li><strong>Google Fonts</strong>: fonts are loaded from Google's servers.</li><li><strong>Hosting</strong>: the site is hosted on GitHub Pages, which may log technical data such as IP addresses for security.</li></ul>"),
        ("Data stored on your device", "<p>Our tools save checklists, form drafts, your theme preference and your cookie choice in your browser's local storage. This data stays on your device; clear it any time through your browser settings.</p>"),
        ("Your rights", "<p>Depending on where you live (for example, California, other US states with privacy laws, or Canada under PIPEDA and Quebec's Law 25), you may have rights to access, correct, delete or limit the use of your personal information and to opt out of targeted advertising. Send requests through our <a href=\"@/contact.html\">contact form</a> and choose \"Privacy request\". We will not discriminate against you for exercising your rights.</p>"),
        ("Retention and security", "<p>We keep submissions only as long as needed for the purpose you submitted them for, and for legal and accounting obligations. No method of transmission is perfectly secure, but we limit access to submissions to people who need them.</p>"),
        ("Children", "<p>ExpressFind is intended for adults. We do not knowingly collect personal information from children under 13 (or under 16 where applicable).</p>"),
        ("Changes", "<p>We will post updates on this page with a new \"last updated\" date.</p>"),
    ])
    legal(ctx, "terms.html", "Terms of use", "Terms of Use", "Terms of Use", "The rules for using ExpressFind.com, its tools and its service-request routing.", U, [
        ("Acceptance", "<p>By using ExpressFind.com you agree to these terms. If you do not agree, do not use the site.</p>"),
        ("What ExpressFind is", "<p>ExpressFind is an information and matching service. We are not a contractor, do not perform any work and are not a party to any agreement between you and a service provider. We are not an emergency service.</p>"),
        ("Service providers", "<p>Providers who receive requests are independent businesses. We ask partners to confirm licensing where required and insurance, but we do not guarantee their work, pricing, availability, licensing or conduct. You are responsible for verifying any provider before hiring and for the agreements you make.</p>"),
        ("Information on the site", "<p>Cost ranges, playbooks, tools and videos are general information, not professional advice. Prices are estimates and can differ substantially from actual quotes. Follow instructions from emergency services, utilities and licensed professionals.</p>"),
        ("Your submissions", "<p>You agree to provide accurate information and to submit requests only for properties you own, rent or manage, or with permission. Contest entries and other content you submit must be your own; you grant us a non-exclusive, royalty-free license to publish and adapt them on the site and in promotion.</p>"),
        ("Acceptable use", "<p>Do not misuse the site, submit false or automated requests, scrape at scale, interfere with security, or use the site to harass anyone.</p>"),
        ("Intellectual property", "<p>The site's original text, design, code and graphics are protected by copyright. Third-party names, marks and videos belong to their owners. See our <a href=\"@/trademark.html\">trademark &amp; copyright disclosure</a>.</p>"),
        ("Disclaimers and limitation of liability", "<p>The site is provided \"as is\" without warranties of any kind. To the fullest extent permitted by law, ExpressFind is not liable for indirect, incidental or consequential damages, or for any loss arising from your use of the site or from any service provider's work.</p>"),
        ("Changes and contact", "<p>We may update these terms by posting a new version. Questions: <a href=\"@/contact.html\">contact us</a>.</p>"),
    ])
    legal(ctx, "disclaimer.html", "Disclaimer", "Disclaimer", "Disclaimer", "Important limits on the information, estimates and services on ExpressFind.com.", U, [
        ("Emergencies", "<p>ExpressFind is not an emergency service. If anyone is in danger, there is a fire, smoke, a gas smell, a carbon monoxide alarm or a downed power line, call 911 or your utility immediately.</p>"),
        ("General information only", "<p>Playbooks, guides, tools and videos are general information and not a substitute for advice from a licensed professional who has inspected your home.</p>"),
        ("Cost estimates", "<p>All prices are national estimates in US dollars compiled from third-party sources and adjusted for inflation. Actual prices vary by location, access, materials, code requirements and provider.</p>"),
        ("Compensation disclosure", "<p>We may be paid by service providers who receive requests, by advertisers (including through Google AdSense) and by sponsors. Sponsored content is labeled. Compensation does not change our published prices or safety advice.</p>"),
        ("External links and videos", "<p>Links to other websites and embedded YouTube videos are provided for convenience. We do not control and are not responsible for third-party content.</p>"),
    ])
    legal(ctx, "cookies.html", "Cookie policy", "Cookie Policy", "Cookie Policy", "What cookies and local storage ExpressFind and its partners use, and how to control them.", U, [
        ("Essential storage", "<p>We use your browser's local and session storage to remember your theme, cookie choice, checklist progress, quote-form drafts and campaign source. This information stays on your device.</p>"),
        ("Advertising cookies", "<p>Google and its partners may set cookies to show and measure ads through Google AdSense, including personalized ads where permitted. See our <a href=\"@/privacy.html\">Privacy Policy</a> for opt-out links.</p>"),
        ("Embedded content", "<p>YouTube videos use privacy-enhanced mode and load only when you press play. After that, YouTube may set cookies under its own policy.</p>"),
        ("Managing cookies", "<p>You can block or delete cookies in your browser settings. Blocking some cookies may affect site features. Visitors in regions that require consent will see a consent message managed through Google's certified consent tools.</p>"),
    ])
    legal(ctx, "trademark.html", "Trademark & copyright", "Trademark & Copyright Disclosure", "Trademark &amp; Copyright Disclosure", "Our position on the ExpressFind name, third-party trademarks, embedded videos and copyright.", U, [
        ("The ExpressFind name", "<p>\"ExpressFind\" is used on this website only as the descriptive name of the domain ExpressFind.com — finding help quickly (\"express\") for home emergencies and repairs. <strong>No trademark rights are claimed in the words \"ExpressFind\", \"Express Find\", \"Express\" or \"Find\"</strong>, and no trademark registration has been filed for them by this website.</p>"),
        ("No affiliation", "<p>ExpressFind.com is independent. It is not affiliated with, endorsed by or sponsored by any company or brand whose name includes \"Express\" — including, for example, Express, Inc. (retail), American Express, Express Scripts, Express Employment Professionals, FedEx Express or any business named \"Express Search\" — or any other business using a similar name. Any similarity is coincidental.</p>"),
        ("Third-party trademarks", "<p>Names of companies, products and services mentioned on this site (for example, in cost-guide source lists or video credits such as Angi, Thumbtack, HomeAdvisor, This Old House, Ace Hardware, Lowe's, The Home Depot, SERVPRO, YouTube and Google) are trademarks of their respective owners. They are used only to identify those owners' content or services (nominative use) and do not imply endorsement.</p>"),
        ("Embedded videos", "<p>Videos are embedded using YouTube's standard embed player in privacy-enhanced mode. They remain the property of their creators and are credited by channel name. We do not host, download or modify them. Rights holders can ask us to remove an embed through the <a href=\"@/contact.html\">contact form</a>.</p>"),
        ("Cost data and sources", "<p>Cost ranges are our own compilation of facts drawn from multiple sources, summarized in our own words. Sources are listed and linked on each guide. We do not reproduce third-party articles.</p>"),
        ("Our copyright", "<p>Original text, page designs, illustrations, icons and code on ExpressFind.com are © ExpressFind.com. You may link to and quote short excerpts with attribution. Do not republish full guides or tools without permission.</p>"),
        ("Notice and takedown", "<p>If you believe content on this site infringes your rights, send the details (the work, the page URL and your contact information) through our <a href=\"@/contact.html\">contact form</a>. We review notices promptly and remove infringing material.</p>"),
        ("Website, domain and partnership inquiries", f"<p>For inquiries about this website or the ExpressFind.com domain name, sponsorship, advertising or partnership, use <a href=\"{OWNER_URL}\" target=\"_blank\" rel=\"noopener\">web.works/contact</a>.</p>"),
    ])

    # ---------------- HTML sitemap
    G, PB = ctx["GUIDES"], ctx["PLAYBOOKS"]
    li = lambda xs: "".join(f'<li><a href="@/{h}">{e(t)}</a></li>' for h, t in xs)
    main_l = [("index.html", "Home"), ("get-quotes.html", "Get free quotes"), ("emergency.html", "Emergency help center"), ("costs.html", "Cost guides"), ("tools.html", "Tools"), ("videos.html", "Videos")]
    co = [("about.html", "About"), ("methodology.html", "Methodology"), ("pros.html", "For pros"), ("advertise.html", "Advertise"), ("support.html", "Support us"), ("contests.html", "Contests"), ("careers.html", "Careers"), ("contact.html", "Contact")]
    lg = [("privacy.html", "Privacy policy"), ("terms.html", "Terms of use"), ("disclaimer.html", "Disclaimer"), ("cookies.html", "Cookie policy"), ("trademark.html", "Trademark & copyright")]
    tl = [("tools/cost-estimator.html", "Cost estimator"), ("tools/quote-checker.html", "Quote checker"), ("tools/repair-or-replace.html", "Repair or replace"), ("tools/license-lookup.html", "License lookup"), ("tools/emergency-kit.html", "Emergency kit"), ("tools/maintenance-calendar.html", "Maintenance calendar")]
    body = f"""{hero("Sitemap", "Sitemap", "Every page on ExpressFind", "Find any guide, playbook or tool.")}
<section><div class="wrap grid g3"><div><h2 style="font-size:1.3rem">Main</h2><ul>{li(main_l)}</ul><h2 style="font-size:1.3rem">Tools</h2><ul>{li(tl)}</ul></div>
<div><h2 style="font-size:1.3rem">Emergency playbooks</h2><ul>{li([(f"emergency/{p['slug']}.html", p['name']) for p in PB])}</ul><h2 style="font-size:1.3rem">Company</h2><ul>{li(co)}</ul></div>
<div><h2 style="font-size:1.3rem">Cost guides</h2><ul>{li([(f"costs/{g['slug']}.html", g['name'] + ' cost') for g in G])}</ul><h2 style="font-size:1.3rem">Legal</h2><ul>{li(lg)}</ul></div></div></section>"""
    R("sitemap.html", "Sitemap | ExpressFind", "All pages on ExpressFind: emergency playbooks, cost guides, tools, videos and company pages.", body, "0.3",
      crumbs=[("Home", "index.html"), ("Sitemap", None)])

    # ---------------- 404
    body = f"""{hero("Not found", "404", "That page isn't here", "It may have moved. Try one of these instead.")}
<section><div class="wrap grid g3"><a class="card card-link" href="@/emergency.html"><h3 style="margin-top:0">Emergency help</h3><span class="more">Open →</span></a><a class="card card-link" href="@/costs.html"><h3 style="margin-top:0">Cost guides</h3><span class="more">Open →</span></a><a class="card card-link" href="@/get-quotes.html"><h3 style="margin-top:0">Get free quotes</h3><span class="more">Open →</span></a></div></section>"""
    R("404.html", "Page Not Found | ExpressFind", "The page you requested could not be found.", body, "0.1", noindex=True)
    p404 = os.path.join(ROOT_DIR, "404.html")
    with open(p404, encoding="utf-8") as f:
        h = f.read()
    base = "<script>(function(){var m=location.pathname.match(/^\\/expressfind-com\\//);document.write('<base href=\"'+(m?'/expressfind-com/':'/')+'\">');})();</script>"
    h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + base, 1)
    with open(p404, "w", encoding="utf-8") as f:
        f.write(h)
