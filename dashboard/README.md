# Margins dashboard

A Quarto static site that complements the existing [DiJeSt Looker Studio dashboard](https://datastudio.google.com/u/0/reporting/73a17dcc-f092-4dec-8c57-58b606862b2d/page/FPCXD). Two pages:

- **The Corpus** — BHB restricted to the Margins window (1470–1800), with temporal, paratextual and Bowers/Gaskell-signal layers that DiJeSt does not cover.
- **Desiderata** — the data-model gap relative to the DiJeSt MARC-to-ontology crosswalk, with one real BHB note transformed side-by-side into structured JSON and LRMoo Turtle.

Plus the [methods document](methods/) and an [about page](about.qmd).

## Build locally

```bash
# from the repo root:
python3 dashboard/scripts/extract_in_scope.py   # builds _data/*.json from mbimarc-bhb.tsv
python3 dashboard/scripts/sanity_check.py        # locks in methods §9 numbers

quarto render dashboard                          # → dashboard/_site/
quarto preview dashboard                         # live preview
```

## Layout

```
dashboard/
  _quarto.yml             site config
  index.qmd               landing page
  corpus/index.qmd        The Corpus
  desiderata/index.qmd    Desiderata + worked example
  methods/                staged from ../bibliographic_units_and_marc.md at build time
  about.qmd               credits, sources, licensing
  styles.css              minimal paper-ready styling
  scripts/
    extract_in_scope.py   TSV → JSON pipeline
    sanity_check.py       methods doc / dashboard drift guard
  _data/                  built artefacts (gitignored if you prefer; checked in here for offline build)
```

## Continuous integration

`.github/workflows/publish.yml` runs the extraction, the sanity check, and `quarto render` on every push to `main` that touches the dashboard, the TSV, or the methods doc; deploys to GitHub Pages.

## Data provenance

- `mbimarc-bhb.tsv` — National Library of Israel, Bibliography of the Hebrew Book project. 107,977 MARC-format records; the dashboard uses the 10,787-record in-scope subset (008-Year ≤ 1800).
- `mapping-nli10-dijest.xlsx` — DiJeSt project crosswalk; the source for the Desiderata coverage matrix.

## Editing the methods document

The methods document lives at the repo root (`bibliographic_units_and_marc.md`). The CI workflow stages a copy of it into `dashboard/methods/` at build time. To edit, edit the root file — never the staged copy.

If you change a headline number in the methods document (any of the values locked in `scripts/sanity_check.py::EXPECTED`), update that dict in the same commit. CI will fail loudly otherwise — which is the point.
