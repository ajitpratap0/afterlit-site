# afterlit-site

The public website for **afterlit: life after the cloud**.

**Visit: https://ajitpratap0.github.io/afterlit-site/**

This repository contains the website and its checks only. The experimental
Python/BLE product source is currently private. The browser lamp is an
illustration: it connects to no device and creates no conformance evidence.

## Preview

Use Python 3.12+ and Node 22+. No package installation or build is needed.

```sh
python3 scripts/check_site.py website
python3 -B -m unittest discover -s website/tests -p '*_test.py'
node --check website/site.js
node --test website/tests/site.test.cjs
python3 -m http.server 8765 --bind 127.0.0.1 --directory website
```

Open http://127.0.0.1:8765. All fonts and assets are local; the website adds
no analytics, cookies, submission forms or third-party scripts.

## Deploy

GitHub Actions checks the site and publishes `website/` to GitHub Pages when
the `gh-pages` branch changes. Pull requests run checks without deploying.
Actions are pinned to commit SHAs. No custom domain or deployment credential
is required. Site updates should go through pull requests.

The project is pre-alpha. Real-device Gate 1 validation and automated
registry acceptance remain outstanding. The site
distinguishes local prototype behavior from planned features.

Apache-2.0. See `LICENSE` and `NOTICE`.
