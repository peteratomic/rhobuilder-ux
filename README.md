# rhobuilder-ux

Currently this is just all of the MD files presented as webpages. [rhobuilder](https://github.com/rhovision-org/rhobuilder).

rhobuilder is included unmodified as a git submodule in `vendor/rhobuilder`, pinned to a specific commit. All of our own code lives in `ux/`. **Never edit files inside `vendor/`.**

## Clone

```bash
git clone --recurse-submodules <this-repo-url>
# already cloned without it?
git submodule update --init
```

## Update rhobuilder to the latest upstream

```bash
./scripts/update-rhobuilder.sh          # latest main
./scripts/update-rhobuilder.sh <commit>  # or a specific commit/tag
git commit -am "Bump rhobuilder to <commit>"
```

Then rebuild the manual pages (below) and test the UX before committing the bump.

## The site

Open `ux/index.html` in a browser, or serve the `ux/` folder from any static host.

- `ux/index.html`: the "Choose your path" start page
- `ux/docs/`: the rhobuilder manual as web pages, **generated, don't edit by hand**
- `ux/assets/`: shared styles, role paths (`roles.js`) and page behaviour
- `ux/build.py`: generates `ux/docs/` from `vendor/rhobuilder/docs/src`

Rebuild the manual after updating rhobuilder:

```bash
pip install markdown pygments   # once
python3 ux/build.py
```

Every link to a markdown file is turned into a link to its page, so readers never see raw markdown.

## Layout

```
vendor/rhobuilder/   upstream, unmodified (submodule)
ux/                  our UX code
scripts/             helper scripts
```

## License

rhobuilder is AGPL-3.0-only. Check how that applies to this project before distributing or hosting it.
