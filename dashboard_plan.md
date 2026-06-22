# Margins GitHub Pages — dashboard & desiderata plan

A planning document for the two-page GitHub Pages site that accompanies the Margins ERC application. Numbers, captions, and conceptual scaffolding come from `bibliographic_units_and_marc.md`. The dashboard **complements** the existing DiJeSt Looker Studio ("Bibliography of the Hebrew Book, visualized", Sinai Rusinek with Sharon Kurant) — it does not duplicate it.

## 1. Relationship to DiJeSt

The DiJeSt dashboard covers four pages: Introduction (world map + year slider), Interact to explore (Creator / Title / Place / URI-Year facets), Quantitative views (three pie charts + flat table), Caveats & Invitation. Its core competence is **spatial faceting with KIMA place alignment** across the entire 1450–1991 BHB span.

The Margins dashboard picks up where DiJeSt stops:

| DiJeSt | Margins dashboard adds |
|---|---|
| All-corpus (1450–1991) | Margins-window scope (1470–1800), with explicit coverage-vs-target framing |
| Place as primary axis | **Time** as primary axis (decade-by-decade productivity) |
| Year as a slider | Period-aware paratext intensification (15c → 18c) |
| Creator/Title/Place facets | **Work-cluster** drill-down (130-clustered Manifestations) |
| Pie distributions, "Others" dominates | **Paratext-as-data** views (haskama 20.9%, chronogram 49.6%) |
| Free-text/data-quality caveats | **Bowers/Gaskell signal sample** + structural data-model caveats |

Sister-site relationship: each links to the other from the navigation; relevant DiJeSt views (the global map, the language coloring) embedded via iframe where useful.

## 2. Decisions taken

- **Stack**: Quarto. Methods (`bibliographic_units_and_marc.md`) and charts in `.qmd` files; built to static HTML; deployed to `gh-pages` via GitHub Actions.
- **Interactivity**: static SVG for most charts (paper-ready), 2–3 hero charts interactive (map, decade brush, paratext heatmap).
- **DiJeSt integration**: sister-site with bidirectional links **+ selective iframe embedding** (e.g. the DiJeSt world map embedded inside the Margins "in-context" panel, with the Margins window filtered if technically feasible).
- **Schema example presentation**: side-by-side three columns — raw 500-note → JSON extraction → LRMoo Turtle.

## 3. Page A — The Corpus

### 3.1 Header banner

- Scope card: **10,787 records** · **1470–1800** · **~9,628 Works (upper bound)** · **205 places** · **1,986 authors**.
- Coverage ratio bar: BHB-in-scope vs. ~60,000 proposal target (~18%) — visual `███▒▒▒▒▒▒▒`.
- Link out to DiJeSt for the full-corpus and spatial view.

### 3.2 Print-productivity curve (1470–1800)

- Bar chart by decade (data in §10.3 of the methods doc).
- Pre-annotated: **1630s dip** (Thirty Years' War, 123 records vs. ~200/decade either side); **1780s–1790s acceleration** (1.5× and 2.4× the mid-18c baseline).
- Toggleable overlay: only haskama-bearing / only chronogram-bearing records, to surface the paratext intensification visually.

### 3.3 Early-modern Hebrew print map

- MapLibre + KIMA URIs as POI metadata (re-using the DiJeSt mapping in `mapping-nli10-dijest.xlsx`).
- 205 in-scope places. Top 12 labelled: Venice (1,567), Amsterdam (1,366), Prague (595), Mantua (518), Istanbul (470), Zholkva (430), Fürth (406), Livorno (386), Salonika (357), Berlin (303), Cracow (286), Frankfurt-a-M (230).
- Bottom time-brush 1470–1800; brushing redraws point sizes for that sub-period.
- Iframe option: a small DiJeSt embed at the side to anchor the Margins window in the full-corpus context.

### 3.4 Paratext-as-data

- **Haskama panel**: heatmap, decade × place; 2,259 records in scope (20.9%). Click → sample haskama excerpt from 915.
- **Chronogram panel**: same; 5,351 records in scope (49.6%); growth curve overlaid (19% in 15c → 61% in 18c). Click → display the apostrophe-marked source phrase from 912.
- Each panel ships with a side caption naming the MARC field and noting that these are floor counts (extraction-bounded, not actual-presence-bounded).

### 3.5 Work clustering

- Top in-scope Works (from 130 frequency): Tefilot. Holim u-Metim (64), Shirim u-Fiyutim (59), Tefilot. Shonot (50), Tefilot. Berakhot (50), Tefilot. Piyutim (41), Tiqqunim. Shonim (37), Talmud Bavli (Pizaro RSO, 20).
- Click a Work → small-multiples timeline of its Manifestations (year × place).
- Visually makes the Work / Manifestation distinction concrete, and bridges to the Bowers panel below.

### 3.6 Bowers/Gaskell signal sample

- Stacked bar: **~896 records (8.3% of in-scope)** decomposed by signal type — variant (`יש טפסים`, 121) · issue (`שער חדש/אחר/מתוקן`, 34) · impression (`נדפס שנית/מחדש`, 68) · cancel (`דף מבוטל/הוחלף`, 16) · replacement (`הוחלף`, 25) · forged imprint (`מזוייף`, 15) · variant text (`נוסח אחר`, 14).
- Click any record → its full 500-note rendered, with the matched scope-marker + verb + unit phrase highlighted (the §7 grammar, made visible).
- Footer note: these are *floor* counts of records *describable* with Bowers vocabulary, not population counts of the underlying phenomena.

### 3.7 Data-quality strip

Adopt DiJeSt's three caveats (uneven survival, project choices, semi-automatic processing) and add three structural ones:

- **922 (controlled publisher)** essentially empty in scope (20 rows).
- **923 (controlled printer)** populated for 4.7% of in-scope records and only 30% deduplicated — treat as noisy upper bound.
- **533 / 535 (reproduction / originals)** dominantly serve 19c–20c records, negligible in scope (20 / 2,387).

## 4. Page B — Desiderata: from notes to ontology

The page makes the data-model gap visible and demonstrates the proposed remedy on one concrete example.

### 4.1 What the DiJeSt crosswalk already covers

Visual: coverage matrix `MARC field × target ontology` drawn straight from `mapping-nli10-dijest.xlsx`. Green ticks where a mapping exists:
- Authors (100, 700) → `foaf:Person`, with NAF / VIAF / Wikidata ID columns.
- Places (151, 951) → `foaf:Organization` / geo features, with **Kima + Wikidata (P625, P214, P1566)** alignment.
- Titles (245$a/$b) → `bibo:shortTitle` / `fabio:hasSubtitle`.
- Language (041) → `dcterms:language`.
- Subjects (650, 651, 695) → `dcterms:subject`.
- Identifiers (020, 022) → `bibo:isbn`, `bibo:issn`.

### 4.2 The white space

Same matrix overlaid with **red cells** for fields without a structured target:

- **500 (General Note)** — the largest free-text mass. No ontology mapping at all. Contains all the Bowers/Gaskell distinctions, almost all the descriptive cataloguing, and many of the paratextual specifics.
- **915 (Haskama)** — extracted as a column, but no internal structure: granting rabbi / place / date remain inside the free-text string.
- **912 (Chronogram)** — extracted, but the apostrophe-marked letters are not parsed into the numeric value they encode.
- **Bowers sub-Manifestation distinctions** (issue / state / impression / cancel / variant) — no field at all; only inferable from 500.

### 4.3 Worked example (the hero artefact of page B)

Three side-by-side columns showing the same fact at three levels of formalization:

**Source record**: BHB 000146263 — Salonika 1594, R. Samuel di Medina's responsa, with the 500-note about siman 190.

**Column 1 — Raw 500-note** (Hebrew + English translation):

> "בסימן קץ (בדפים קנז-קנח) נדפסה תשובה בעניין עבדים ושפחות של יהודה שמתגיירים. זה הנוסח המקורי. בחלק מהעותקים החליפו תשובה זו בשתי תשובות אחרות."
>
> "In siman 190 (folios 157–158) a responsum on the conversion of Jews' slaves was printed. That is the original text. In some copies this responsum was replaced by two other responsa."

**Column 2 — Structured JSON extraction**:

```json
{
  "manifestation": {
    "id": "MBI-0146263",
    "title": "פסקי...",
    "place": { "kima": "https://data.geo-kima.org/...", "label_he": "שלוניקי" },
    "year": 1594
  },
  "paratext_events": [
    {
      "type": "state",
      "scope": "in_some_copies",
      "scope_marker_he": "בחלק מהעותקים",
      "location_in_book": { "siman": 190, "folios": "157-158" },
      "change": {
        "verb": "replaced",
        "verb_marker_he": "החליפו",
        "original_unit": {
          "type": "responsum",
          "topic": "conversion of slaves owned by Jews"
        },
        "replacement_unit": { "type": "responsum", "count": 2 }
      },
      "likely_motivation": "self_censorship",
      "evidence": { "source_field": "MARC_500", "record": "MBI-0146263" }
    }
  ]
}
```

**Column 3 — LRMoo Turtle** (the ontology that natively models Bowers states — see §8 of methods):

```turtle
@prefix lrmoo: <http://iflastandards.info/ns/lrm/lrmoo/> .
@prefix crm:   <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix mbi:   <https://margins.example/mbi/> .

mbi:0146263 a lrmoo:F3_Manifestation_Product_Type ;
   rdfs:label "Pisqei Maharashdam (Salonika 1594, original setting)"@en .

mbi:0146263_state1 a lrmoo:F3_Manifestation_Product_Type ;
   crm:P130_shows_features_of mbi:0146263 ;
   lrmoo:R28i_was_produced_by [
     a lrmoo:F32_Carrier_Production_Event ;
     crm:P16_used_specific_object mbi:setting_siman190_variant ;
     crm:P14_carried_out_by mbi:printer_diGara
   ] ;
   mbi:scope "in_some_copies"@en ;
   mbi:likely_motivation "self_censorship"@en ;
   mbi:evidence_source "BHB MARC 500"@en .

mbi:setting_siman190_variant a crm:E22_Human-Made_Object ;
   crm:P130_shows_features_of mbi:setting_siman190_original ;
   rdfs:comment "Replacement type-setting of siman 190, substituting two responsa for the original one on slave-conversion."@en .
```

The three columns are aligned at the responsum-replacement assertion so the reader can see the same fact promoted from prose → JSON → linked data.

### 4.4 The desiderata themselves

A short structured list of what Margins proposes to add. Each row carries a count from `bibliographic_units_and_marc.md` §9 so the asks are sized.

| # | Desideratum | Records in scope | Method |
|---|---|---:|---|
| 1 | Parse 500-notes for scope-marker + verb + unit → `paratext_events` table | ~896 | Regex + curated grammar (§7) |
| 2 | Parse 915 haskama → structured (rabbi-URI, place, date) | 2,259 | NER + Hebrew date parsing |
| 3 | Parse 912 chronogram → source phrase + counted letters + computed year | 5,351 | Apostrophe parser + gematria summation |
| 4 | Cluster un-clustered records into Works via 100+245 fuzzy matching | 6,056 | Authority+title similarity |
| 5 | Extend place authority alignment (Kima, Wikidata, GeoNames) | 205 | Already partly done by DiJeSt |
| 6 | Build printer authority from 260f + 923 | 506 → ~150–200 distinct | Cluster + manual curation |
| 7 | Pull Item-level data from holdings catalogues (Footprints, NLI scans, Sefaria) | n/a | External data integration |
| 8 | Page-layout segmentation of digitized scans into typed zones (haskama block, marginal commentary, title page, colophon, running title, ornament frame, quire marks) | ~7,000 with high-quality scans | HTR pipelines (Transkribus / eScriptorium / Kraken) with a **SegmOnto-aligned** zone-type vocabulary, adapted with Hebrew-print–specific zone types (rabbinic-commentary surrounds, haskama blocks, chronogram panels, RTL reading order). See methods §4. |

### 4.5 What the ERC application gets from this page

A concrete answer to "what is the data-model contribution of Margins beyond DiJeSt?" — the worked example is the artefact reviewers will cite when they describe the proposal's data-engineering ambition.

## 5. Site structure

```
/                                     # Quarto _quarto.yml
  index.qmd                           # landing — Margins overview + nav to dashboard
  corpus/
    index.qmd                         # Page A — The Corpus
    _charts/                          # Vega-Lite / Plot specs, one per panel
      productivity_curve.json
      print_map.json
      haskama_heatmap.json
      chronogram_growth.json
      works_top.json
      bowers_signals.json
    _data/
      bhb_pre1800.json                # extracted in-scope subset (~5 MB gz)
      bhb_pre1800_places.geojson      # Kima-aligned points
  desiderata/
    index.qmd                         # Page B — Desiderata
    sample-note.qmd                   # the worked example (4.3) as its own deep-link
    schema-coverage.json              # the matrix from 4.1–4.2
  methods/
    bibliographic_units_and_marc.qmd  # the methods document (this repo's existing .md)
  _ext/
    bhb-helpers/                      # Quarto extension(s) if needed
  about.qmd                           # acknowledgements: DiJeSt, KIMA, Sharon Kurant, BHB
  .github/workflows/
    publish.yml                       # Quarto → gh-pages
```

## 6. Build & deploy plan

1. **Data extraction**: a one-shot script `scripts/extract_in_scope.py` that reads `mbimarc-bhb.tsv`, filters 008-Year ≤ 1800, and emits `corpus/_data/bhb_pre1800.json` + `bhb_pre1800_places.geojson`. Committed to the repo so the site builds without re-running.
2. **Chart specs as data**: each chart is a Vega-Lite spec file checked in; embeds easily and is reviewable in a PR.
3. **Quarto build** in CI: `quarto render`; output to `_site/`; publish to `gh-pages` branch.
4. **Tests / sanity**: a tiny CI step that compares the in-scope record count and a few headline numbers against the values in `bibliographic_units_and_marc.md` §9; fails the build if they drift, so methods and dashboard cannot silently disagree.

## 7. Open questions for next step

- Who owns the GitHub Pages domain — this repo's `gh-pages` branch, or a separate `margins-dashboard` repo?
- Is the BHB TSV redistribution-licensed for inclusion in the published site, or must we ship aggregates only?
- Do we want a Hebrew-language version of the Corpus page, or English-only with Hebrew labels?
- For the LRMoo example, should we link to a live SPARQL endpoint or just publish the Turtle as a static file?
