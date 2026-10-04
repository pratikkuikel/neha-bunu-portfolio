# Neha Kharel — The Sky She Left Me

A public author website and a complete digital edition of Neha Kharel's debut novel.

## Experience

- Responsive author website using the manuscript's title-page artwork.
- A physical page-turn reader powered by locally bundled StPageFlip 2.0.7.
- Desktop spreads, mobile single pages, drag/swipe turns, arrow-key navigation, contents, page slider, fullscreen and remembered reading position.
- Continuous text mode, reduced-motion support, a no-JavaScript complete text edition, and local fonts with no third-party requests.

## Run

Serve `public/` with any static web server. No build or runtime dependencies are needed in production.

The `.openai/hosting.json` manifest connects this checkout to its ChatGPT Sites deployment. The public directory is the deployment artifact.

## Manuscript and pagination

`public/manuscript.json` contains the extracted prose, including Word text boxes. `public/pages.json` contains the digital pagination. Every word is retained after whitespace normalization. The web edition is newly typeset, so its page numbers differ from the print edition. Chapter labels follow the supplied manuscript, including its second "Chapter 3" label. The original document also lacks an explicit body heading for the earlier Chapter 3; its prose is included in order.

To re-extract from an authorized DOCX, install Python `python-docx` and run:

```sh
python scripts/extract-manuscript.py /path/to/manuscript.docx
npm ci
npm run paginate
```

Pagination and verification use Playwright. Set `CHROMIUM_PATH` to a local Chromium executable for verification; pagination accepts the same setting.

```sh
CHROMIUM_PATH=/path/to/chromium npm test
```

Verification covers complete-text integrity, page content bounds, desktop and mobile layouts, navigation, keyboard controls, chapter jumps, text view, saved position and deep links.

## Rights

The novel and title-page artwork are © Neha Kharel. All rights reserved. Public reading is enabled at the site owner's request; this repository does not grant republication rights.

StPageFlip's MIT license is in `public/vendor/page-flip.LICENSE`. Font redistribution notices are in `public/assets/fonts-LICENSE.txt`.
