# ExpressFind.com

Emergency-first home-services finder for the US and Canada: safety-first emergency playbooks, self-updating cost guides, free tools and a lead-generation funnel that routes homeowner requests to local pros. Monetized with Google AdSense, pro leads, sponsorships, donation pledges and contest sponsorship.

## Structure

| Path | What it is |
|---|---|
| `index.html`, `*.html`, `costs/`, `emergency/`, `tools/` | Generated static pages (served by GitHub Pages) |
| `assets/css/style.css`, `assets/js/main.js` | Design system and all interactivity (no dependencies) |
| `build/build.py` | Generator — run `python3 build/build.py` after editing content |
| `build/content_costs.py` | 13 cost guides (base ranges, sources, FAQs) |
| `build/content_emergency.py` | 11 emergency playbooks |
| `build/pages.py`, `build/tools_pages.py` | Company, legal, monetization and tool pages |
| `build/update_data.py` | Weekly BLS CPI refresh → `data/cpi.json` |
| `.github/workflows/auto-update.yml` | Weekly refresh + rebuild + commit |
| `RESEARCH.md` | Concept decision, revenue model, 37-site competitor review |
| `BUILD-PROMPTS.md` | Phase-wise build prompts (Phases 0–10) |

## Editing
1. Edit content in `build/*.py`.
2. Run `python3 build/build.py`.
3. Commit and push to `main`. GitHub Pages republishes automatically.

## Forms
All forms post through one private inbox routine in `assets/js/main.js` (FormSubmit AJAX). The inbox address is stored only as an obfuscated array and never appears in page source. The first submission after launch triggers a one-time FormSubmit activation email.

## Custom domain
Add a `CNAME` file containing `expressfind.com`, then point DNS: A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` CNAME → `webworksa1.github.io`. Enable "Enforce HTTPS" in Settings → Pages.

## Ownership
Website, domain, sponsorship, advertising and partnership inquiries: https://web.works/contact
