# ExpressFind.com — Phase-Wise Build Prompts

Use these prompts in order with any capable AI builder (or a developer). Each phase is self-contained, lists its deliverables, and ends with acceptance checks. The current repository is the result of running Phases 0–10.

**Global constants used in every phase**

```
DOMAIN            = expressfind.com
BRAND             = ExpressFind  (descriptive name only; never claim it as a trademark)
ADSENSE_CLIENT    = ca-pub-6620975821265271
ADSENSE_SCRIPT    = <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>
OWNER_CONTACT_URL = https://web.works/contact
OWNER_INBOX       = the owner's private inbox. It must NEVER appear in HTML, CSS, sitemaps, docs or
                    commit messages. Store it only as an obfuscated char-code array inside main.js and
                    assemble it at runtime for the form endpoint and "Email us" links.
HOSTING           = GitHub Pages, free plan, branch main, folder / (root)
REPO              = WEBWORKSA1/expressfind-com
```

---

## Phase 0 — Strategy guardrails

```
You are building ExpressFind.com: an emergency-first home-services finder for the US and Canada.
Value promise: "Fast help. Fair prices. Trusted pros."
Revenue stack (in priority order): 1) homeowner quote leads sold to local pros, 2) Google AdSense
Auto ads, 3) sponsorships, 4) donation pledges, 5) contest sponsorship.

Hard rules:
- Every page shows a top banner: "Contact, if you are interested in this website/domain name/
  Sponsorship/Advertisement/Partnership" linking to OWNER_CONTACT_URL (new tab).
- One inbox only (OWNER_INBOX), never exposed in source text.
- No fake reviews, ratings, user counts or "verified" claims. Use honest phrasing.
- Safety first: every emergency page starts with "If anyone is in danger, call 911".
- No trademark claim on "ExpressFind"; publish a trademark & copyright disclosure page.
Deliver: a one-page brief (audience, top 20 search intents, page inventory, monetization map).
Accept when: the brief lists every page in Phases 1–7 and maps each to a revenue driver.
```

## Phase 1 — Foundation, design system, global layout

```
Create a static site that GitHub Pages serves from main/root with no build step at request time.
Use a small Python generator (build/build.py) that renders every page from Python content
modules into plain HTML; commit the generated HTML. Add .nojekyll.

Design system (assets/css/style.css): navy ink #0B1B2B, signal amber #FFB703, trust teal #0E9AA7,
emergency red #E63946; fonts Bricolage Grotesque (display) + Plus Jakarta Sans (body); light and
dark themes; 8-pt spacing; cards, chips, tables, callouts, FAQ accordions, step indicators,
modal, sticky mobile CTA bar, cookie notice. Mobile-first, WCAG AA contrast, visible focus rings.

Global layout on every page: owner banner -> header (logo, nav: Find a Pro, Emergency, Cost Guides,
Tools, Videos, For Pros; red "Emergency" button; amber "Get Free Quotes" button; theme toggle;
burger) -> main -> footer (4 link columns, newsletter mini-form, disclosure line, trademark line).
<head>: ADSENSE_SCRIPT, <meta name="google-adsense-account" content="ADSENSE_CLIENT">, canonical,
Open Graph, Twitter card, JSON-LD (Organization + WebSite on home; Article/FAQPage/Breadcrumb on
guides). All internal links relative so the site works at /, at /expressfind-com/, and on the domain.
Also ship: ads.txt (google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0), robots.txt,
sitemap.xml, feed.xml, site.webmanifest, favicon.svg, og.png, 404.html (base-href auto-detect).
Accept when: every generated page contains the banner, the AdSense script and the canonical tag.
```

## Phase 2 — Lead-generation engine (the money page)

```
Build get-quotes.html: a 5-step funnel with a progress bar.
 1 Service (icon tiles: plumbing, water damage, HVAC heating, AC, electrical, roofing, locksmith,
   garage door, drain & sewer, mold, tree service, appliance repair, handyman, other)
 2 Urgency (Emergency now / Within 24h / This week / Planning) + property type + own/rent
 3 Location: US ZIP or Canadian postal code (validate both formats)
 4 Details: description, budget range, best time to contact
 5 Contact: name, phone, email, unticked consent checkbox with sharing disclosure (up to 3 pros),
   optional newsletter opt-in, honeypot field.
Prefill from URL params (?service=&urgency=&zip=). Capture utm_* params and referrer.
Compute a lead score (urgency + ownership + timeline + budget) and put it in the email subject,
e.g. "[HOT 86] Plumbing — 77002". Save drafts to localStorage so returning users resume.
Submit via fetch() to FormSubmit's AJAX endpoint built at runtime from OWNER_INBOX; redirect to
thank-you.html with next steps + emergency tips. Add: hero quick-finder (service + ZIP) on home,
sticky mobile CTA bar, exit-intent lead-magnet modal (desktop, once per session) offering the free
printable "Home Emergency Playbook" for an email address.
Accept when: a test submission produces one well-formatted email; no inbox text exists in HTML.
```

## Phase 3 — Emergency hub and playbooks

```
Build emergency.html with an interactive triage: "What's happening?" tiles -> instant 3-step action
card -> link to full playbook -> "Get emergency help" CTA prefilled with urgency=emergency.
Build 11 playbooks under /emergency/: burst pipe, flooded basement, no heat, AC not cooling,
electrical outage/sparking, gas smell, roof leak, locked out, sewer backup, fallen tree,
frozen pipes. Each: danger banner (911 / utility), first-15-minutes numbered steps, do/don't lists,
what to tell the pro, typical cost link, an embedded YouTube how-to (lite facade, nocookie domain),
FAQs with FAQPage schema, and a prefilled quote CTA. Water pages include a "mold clock" timer
(24–48 hour drying window, per EPA guidance).
Accept when: each playbook is 700+ words of original guidance and passes a safety review.
```

## Phase 4 — Cost guides that update themselves

```
Build costs.html (searchable hub) and 13 guides under /costs/: emergency plumber, water damage
restoration, water heater replacement, AC repair, furnace repair, roof leak repair, locksmith,
garage door repair, electrician, mold remediation, drain cleaning, tree removal, appliance repair.
Each guide: headline range card, typical-jobs table (low/high), cost factors, emergency/after-hours
premium, money-saving tips, questions to ask, red flags, FAQ (FAQPage schema), "sources consulted"
links, inline mini-estimator, related playbook, quote CTA. Store base ranges in Python data and
multiply by data/cpi.json inflation_factor at build time; show "Prices adjusted for inflation
through <month year>".
Accept when: every number on a guide traces to the data module and the sources list.
```

## Phase 5 — Interactive tools

```
Build /tools/ pages (vanilla JS, no dependencies):
 - cost-estimator: service x severity x timing (business/evening/weekend/holiday) x region
 - quote-checker: up to 3 quotes vs typical range -> flags, median, what to ask
 - repair-or-replace: $5,000 rule + 50% rule by system type, age, repair cost
 - license-lookup: US states + Canadian provinces -> official .gov lookup links + verify checklist
 - emergency-kit: checklist with progress saved locally + printable fridge card of shutoff
   locations and key phone numbers
 - maintenance-calendar: month-by-month tasks, auto-highlights current month, hemisphere toggle,
   checkboxes saved locally, .ics export of the month's tasks
Accept when: every tool works offline after first load and prints cleanly.
```

## Phase 6 — Video library

```
Build videos.html: category filter chips + grid of YouTube embeds using a click-to-load facade
(thumbnail from i.ytimg.com; iframe from youtube-nocookie.com only on click). Verify each video
ID through YouTube oEmbed before publishing; drop any that refuse embedding. Credit the channel
under each video. Reuse the same videos inside the matching playbooks.
Accept when: zero third-party iframes load before a user click.
```

## Phase 7 — Monetization and community pages

```
- pros.html: "Get emergency and local jobs" — benefits, how leads work, lead ROI calculator
  (avg job value x close rate x leads), join form (business, trade, service area, license #,
  insurance, 24/7 availability, monthly capacity).
- advertise.html: sponsorship packages (category sponsor, playbook sponsor, regional pro
  spotlight, newsletter, custom content) + inquiry form + OWNER_CONTACT_URL button.
- support.html: donation pledges (one-time / monthly tiers, purpose: operations, promotions &
  marketing, hiring talent, contests & prizes) -> secure payment link sent by email; transparency
  allocation bar; "other ways to help".
- contests.html: monthly "Home Hero" contest, auto countdown to month end, entry form, official
  rules (no purchase necessary, 18+, US/Canada, skill-based judging, skill-testing question).
- careers.html: open roles (licensed trade reviewer, cost-guide writer, video creator, local
  partnerships rep, front-end developer) + application form.
- about.html, methodology.html, contact.html.
Accept when: every form posts through the same hidden-inbox routine with a distinct subject line.
```

## Phase 8 — AdSense approval hardening, SEO, performance, accessibility

```
- Legal: privacy (Google advertising cookies, opt-out links, CCPA/PIPEDA, lead sharing),
  terms, disclaimer (estimates, emergencies, referral compensation), cookies, trademark.
- Content depth: 35+ indexable pages of original content; no empty ad placeholders; no
  "coming soon" pages; HTML sitemap page.
- SEO: unique titles/descriptions, canonical, breadcrumbs, internal linking between
  playbooks <-> cost guides <-> tools, RSS feed, XML sitemap with lastmod.
- Performance: one CSS + one JS file, deferred JS, inline SVG icons, lazy video facades.
- Accessibility: landmarks, skip link, labelled inputs, aria-live form status, reduced motion.
Accept when: Lighthouse mobile >= 90 for performance, accessibility, best practices and SEO.
```

## Phase 9 — Automation (self-updating)

```
Add .github/workflows/auto-update.yml (weekly + manual): checkout -> setup Python ->
python build/update_data.py (fetch BLS CPI-U all items CUUR0000SA0 and "repair of household items"
CUUR0000SEHP04 from the public v1 API; record the baseline on first success; compute
inflation_factor and year-over-year change; keep previous data if the API fails) ->
python build/build.py (regenerates every page, sitemap lastmod, RSS, price-pulse widget,
contest month) -> commit only if files changed. permissions: contents: write.
Client-side freshness: seasonal alerts by month, contest countdown, current-month maintenance.
Accept when: running the workflow manually produces a commit or a clean "no changes" exit.
```

## Phase 10 — Deploy, domain, growth

```
Deploy: push to WEBWORKSA1/expressfind-com main; Settings -> Pages -> Deploy from branch ->
main / (root). Custom domain: add a CNAME file containing expressfind.com, then point DNS:
A records 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 and
CNAME www -> webworksa1.github.io; enable "Enforce HTTPS".
After DNS resolves: submit sitemap in Google Search Console, apply in AdSense, enable Auto ads and
the Google certified CMP for EEA/UK.
Growth backlog: city pages only when each has unique local data (permit fees, licensing, climate
risks); newsletter automation; lead routing via Supabase + webhook to partner pros; call tracking
for emergency leads; partner API for lead buyers; Spanish and French editions.
```
