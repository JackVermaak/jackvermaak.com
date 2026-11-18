# jackvermaak.com

My personal website: projects, experience and contact details. It's plain HTML, CSS and a little JavaScript, with no framework and no build step. It's hosted on Cloudflare Pages.

## Layout

```
site/            Everything that gets published
  index.html     Home
  projects.html  Project list and "On the bench"
  about.html     Background, experience, education, tools
  contact.html   Contact details
  projects/      One write-up page per project
  photos/        Home page Instagram photos (ig-1.jpg, ig-2.jpg, ig-3.jpg)
  styles.css     All styling, with light and dark themes
  site.js        Theme toggle, mobile menu, copy button, project filter, fire simulation snapshot
tools/
  gen.py         Generates the HTML pages from the content in this file
  figs.py        SVG diagrams used on the project pages
```

## Editing

- **Text and projects:** edit `tools/gen.py`, then run `python3 tools/gen.py` to rewrite the pages in `site/`. Small fixes can also go straight into the HTML files.
- **Styling:** edit `site/styles.css`.
- **CV:** replace `site/Jack_Vermaak_CV.pdf` and keep the file name.
- **Home page photos:** put three square photos in `site/photos/` named `ig-1.jpg`, `ig-2.jpg` and `ig-3.jpg`, about 800 px wide.

To preview locally, run `python3 -m http.server -d site` and open http://localhost:8000.

## Deploying

The Cloudflare Pages project is connected to this repository. Every push to `main` deploys automatically.

- Build command: none
- Build output directory: `site`

`/ograder` is not part of this repo. It's served by the separate O-Grader Worker through the route `jackvermaak.com/ograder*`.
