# Search engines and link previews

How the live page (https://doooools.github.io/vault-print-planner/) presents itself to search engines and to the
apps that show a preview of a shared link (Discord, Reddit, WhatsApp, X, Facebook, LinkedIn, Slack…). Set up on
2026-11-24 (Dols: "Est-ce que tu peux t'occuper du référencement"). It only counts once on `main`.

## In the page (`src/template.html`, `<head>`)
- `<title>`: "3D Vault Configurator: design and print Vault by USSA in 3D". The name first, then what it is for, in the
  words people search ("Vault", "USSA", "3D", "print"). The preprod puts "Preprod · " before it.
- `<meta name="description">`: under 160 characters, what Google shows under the title.
- `<link rel="canonical">`: the live address, on the preprod too, so the two copies never compete.
- Open Graph and Twitter card: name, a shorter description, the live address and the card
  `docs/images/social.png` (1200 × 630). The image is read from `main` on GitHub
  (`raw.githubusercontent.com/…/main/docs/images/social.png`), because the published site holds only the page and its
  part pictures (`pages.yml`). Made by `tools/social-card/` (`node tools/social-card/make.js`): the page's fonts and
  a stack drawn in its colours, no render of USSA's parts (CLAUDE.md "Hard rules").
- Structured data (`application/ld+json`, schema.org `WebApplication`): name, description, free, browser, features,
  author, the original planner it is based on (`isBasedOn`, Romy's), the MIT licence, the repository. No rating: there
  are none to give, and a made-up one breaks Google's rules.
- `<noscript>`: what the configurator does, for a browser without JavaScript and for the crawlers that don't run it.
  Invisible otherwise: no notice on screen (Dols removed the footer on purpose).
- The preprod keeps its robots `noindex` (head script, `VPP_PRE`).

## What there is not, and why
- **No robots.txt.** Crawlers read it only at the root of the host (`doooools.github.io/robots.txt`), which belongs
  to a `doooools.github.io` repository, not to this one. A file in this site would be ignored. With none, everything is
  allowed, which is what we want; the preprod is kept out by its `noindex`.
- **No sitemap.xml.** The site is one page. Search Console's "URL inspection › Request indexing" does the same; a
  sitemap would also need adding to `SITE` in `pages.yml` (a workflow change, Dols's merge).
- **No tracking script, no cookie.** Search Console and Bing Webmaster Tools only need a verification tag in `<head>`.

## What only Dols can do
1. **Repository's About** (github.com/doooools/vault-print-planner, the gear next to "About"):
   - Description: `3D configurator for Vault by USSA: design your stacks in 3D and in your colors, get the exact STL files and print them plate by plate. Free, in the browser.`
   - Website: `https://doooools.github.io/vault-print-planner/`
   - Topics: `vault`, `ussa`, `3d-printing`, `configurator`, `stl`, `bambu-studio`, `modular-storage`, `threejs`,
     `gridfinity`, `storage-system`.
2. **Repository's social preview** (Settings › General › Social preview › Edit): upload `docs/images/social.png`.
   A link to the repository then shows the same card.
3. **Google Search Console** (https://search.google.com/search-console): add a "URL prefix" property for
   `https://doooools.github.io/vault-print-planner/`, choose "HTML tag", and give the `content="…"` value to a thread:
   it goes in `<head>` as `<meta name="google-site-verification" content="…">`, then to `main`. Once verified: URL
   inspection › Request indexing. **Bing Webmaster Tools** (https://www.bing.com/webmasters) can then import the site
   from Search Console (also used by DuckDuckGo and ChatGPT search).
4. **Links to the page** are what makes it rank: the README, the YouTube video's description, a post on the Vault
   communities (USSA's Discord, r/3Dprinting, r/BambuLab), the Printables / MakerWorld pages of one's own prints.

## Checking it
- Preview of a shared link: https://www.opengraph.xyz/url/https%3A%2F%2Fdoooools.github.io%2Fvault-print-planner%2F
  (or paste the link in a Discord message to oneself).
- Structured data: https://search.google.com/test/rich-results and https://validator.schema.org/.
- Indexed or not: search `site:doooools.github.io/vault-print-planner` on Google.
