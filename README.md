# ahmedharbii.github.io

Personal website and portfolio for Ahmed Harbi Elsayed - Robotics Researcher specializing in Marine and Maritime Intelligent Robotics.

## 🌐 Live Website

Visit: [ahmedharbii.github.io](https://ahmedharbii.github.io)

## 📁 Repository Structure

The site is a [Jekyll](https://jekyllrb.com) site built automatically by GitHub Pages.
Shared markup (head, nav, footer, scripts, 3D models) lives in layouts/includes so
each page only contains its own content.

```
.
├── _config.yml             # Site configuration (author, social links, scholar id)
├── _layouts/
│   └── default.html        # Shared page shell
├── _includes/              # head, nav, footer, scripts, 3D creature modules
├── _data/
│   ├── publications.yml    # Source of truth for the Publications page
│   ├── experience.yml      # Source of truth for Work Experience (homepage)
│   └── theses.yml          # Source of truth for supervised master theses
├── index.html              # Homepage (renders experience + theses from _data/)
├── projects.html           # Projects showcase
├── publications.html       # Renders cards + JSON-LD from _data/publications.yml
├── contact.html            # Contact information
├── about.html              # About page
├── privacy.html            # Privacy policy
├── llms.txt                # Curated index for AI crawlers (llmstxt.org)
├── llms-full.txt           # Full site content as one plain-text document
├── robots.txt              # Crawler rules + sitemap/llms.txt pointers
├── assets/
│   ├── css/styles.css      # Main stylesheet
│   ├── js/                 # particles.js (background) + site.js (shared behaviour)
│   ├── icons/              # Logos and social icons
│   ├── images/             # home / projects / publications image assets
│   └── media/press/        # Press articles and PDFs
├── scripts/                # Google Scholar fetch pipeline
├── tests/                  # Python test suite (runs against the built _site/)
└── .github/workflows/      # CI: build + test, and monthly publication fetch
```

## 🚀 Features

- Modern, responsive design with glassmorphism effects
- Dark/Light theme toggle
- 3D animated shark / killer whale using Three.js
- Particle background effects (Three.js)
- SEO optimized with Open Graph tags and JSON-LD structured data
- `llms.txt` / `llms-full.txt` for generative engine optimization (GEO)
- Mobile-friendly navigation

## 🛠️ Local Development

Requires Ruby (for Jekyll) and Python (for the fetch script).

```bash
git clone https://github.com/ahmedharbii/ahmedharbii.github.io.git
cd ahmedharbii.github.io
make install        # bundle install + pip install -r scripts/requirements.txt
make serve          # http://localhost:4000 with live reload
```

Other targets: `make build`, `make test`, `make clean` (see `make help`).

## 🧪 Testing

```bash
make test           # builds the site, then runs the suite against _site/
```

Tests cover HTML structure, meta tags/SEO, image and asset verification,
internal link checking, and responsive design. See [tests/README.md](tests/README.md).

## 📝 Content Management

### Update Publications

Publications are rendered from `_data/publications.yml` (cards **and** JSON-LD).
To pull new ones from Google Scholar:

```bash
pip install -r scripts/requirements.txt
make fetch          # writes NEW publications to _data/publications.draft.yml
```

Then **validate** each draft entry (author order, canonical DOI/URL, year, venue),
add a thumbnail under `assets/images/publications/`, move the entry into
`_data/publications.yml`, and delete the draft.

Google Scholar has no official API and blocks scraping from cloud IPs, so `make fetch`
is most reliable run locally. A monthly GitHub Action
([fetch-publications.yml](.github/workflows/fetch-publications.yml)) attempts the same
check and opens a Pull Request with any new entries; add a `SERPAPI_KEY` repository
secret to make that CI run reliable.

### Update Work Experience or Supervised Theses

Both render from `_data/` into the homepage **and** `llms.txt`/`llms-full.txt`, so add or edit an
entry in one place only:

- `_data/experience.yml` — `role`, `meta` (organisation, location, dates) and `description`.
- `_data/theses.yml` — `title`, `university`, optional `university_full`, and `year`.
  Student names are deliberately not listed.

Entries render in file order, newest first.

### Add New Projects

Edit `projects.html` and add project cards with images/videos under `assets/images/projects/`.

### Keep llms.txt in Sync

`llms.txt` and `llms-full.txt` follow the [llmstxt.org](https://llmstxt.org) convention: plain-text
summaries that let LLMs and AI answer engines read the site without wading through the
Three.js-heavy HTML. `llms.txt` is a short index of links; `llms-full.txt` carries the whole
content in one document.

Both are Jekyll pages, so they only appear in the build output. Anything sourced from `_data/`
stays in sync automatically — **publications** (`publications.yml`), **work experience**
(`experience.yml`) and **supervised theses** (`theses.yml`) are written once and rendered into
the homepage and the llms files alike.

The remaining prose in `llms-full.txt` (bio, education, projects, academic service, press) is
still written by hand, so **when you edit those parts of `index.html`, `about.html`, or
`projects.html`, mirror the change in `llms-full.txt`.**

`make test` verifies both files exist, are structurally valid, contain no unrendered Liquid, use
absolute links, and that every publication, experience entry and thesis in `_data/` actually
renders — but it cannot tell whether the hand-written prose is current.

## 📄 License

Copyright © 2026 Ahmed Harbi Elsayed. All rights reserved.
