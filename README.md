# rhobuilder-ux

A custom UX on top of [rhobuilder](https://github.com/rhovision-org/rhobuilder).

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

Test the UX before committing the bump.

## Layout

```
vendor/rhobuilder/   upstream, unmodified (submodule)
ux/                  our UX code
scripts/             helper scripts
```

## License

rhobuilder is AGPL-3.0-only. Check how that applies to this project before distributing or hosting it.
