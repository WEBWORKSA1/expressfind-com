# ExpressFind.com

Emergency-first home-services finder for the US and Canada: safety-first emergency playbooks, self-updating cost guides, free tools and a lead-generation funnel that routes homeowner requests to local pros. Monetized with Google AdSense, pro leads, sponsorships, donation pledges and contest sponsorship.

## Go live (two one-time steps, signed in as WEBWORKSA1)

1. **Add the build workflow.** Create `.github/workflows/auto-update.yml` (Add file → Create new file) and paste the contents of [`build/auto-update.workflow.yml`](build/auto-update.workflow.yml). Committing it runs the first build: the workflow renders the PNG icons and share image, generates all 52 pages, the sitemap and the feed, and commits them to `main`. After that it rebuilds on every content change and refreshes prices every Monday.
2. **Turn on GitHub Pages.** Settings → Pages → Build and deployment → Source: *Deploy from a branch* → Branch: `main` / `(root)` → Save. The site appears at https://webworksa1.github.io/expressfind-com/ within a few minutes.

The workflow file has to be added from a signed-in GitHub session because third-party integrations need a separate permission to write workflow files.

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
