# Bibliographic units, MARC mapping, and counting for the Margins project

Notes on how to count books at multiple levels (work, edition, copy, and the units in between), how MARC fields map to those levels, and which print-history units sit outside MARC but matter for paratext, typography, and graphic-element research.

## 1. The conceptual stack: FRBR / IFLA-LRM

The Library of Congress and IFLA formalized these levels into the **WEMI** model (Work → Expression → Manifestation → Item), originally in FRBR (1998), now consolidated in **IFLA-LRM** (2017).

- **Work** — the abstract intellectual creation. *Don Quixote* as such.
- **Expression** — a specific intellectual realization of the Work: a particular text version, translation, abridgment, critical edition, revision. Grossman's English translation is a different Expression from the Spanish original; the 1605 vs 1608 revised text are different Expressions.
- **Manifestation** — a specific physical embodiment / publication: an edition issued by a particular publisher at a particular time with a particular typesetting. *This is what most people call "an edition."*
- **Item** — a single physical copy: the book on your shelf, with its specific binding, annotations, stains, owner's stamps.

WEMI gives you **one intermediate unit between "work" and "edition"** (the Expression) and treats edition/copy as Manifestation/Item.

## 2. The print-history layer between Manifestation and Item

WEMI's Manifestation is too coarse for analytical bibliography. The classical Bowers/Gaskell hierarchy unpacks it into:

- **Edition** — all copies printed from substantially the same setting of type.
- **Issue** — copies of an edition forming a distinct publishing unit (e.g., the same sheets reissued with a new title page or new preliminaries — a common early-modern practice).
- **Impression / Printing** — copies pulled at one printing event from the same setting (especially meaningful in the stereotype/electrotype era when one setting yielded printings over decades).
- **State** — copies differing because of stop-press corrections or other in-press changes; states exist *within* an issue.
- **Variant** — a catch-all for copies differing in any other way.
- **Item / Copy** — the individual artifact, with binding, provenance, marginalia.

For early printed books a useful further unit is the **cancel** (a replacement leaf pasted in to correct an error) and the **forme** / **sheet** / **gathering (quire)** as the physical production units — these matter when paratext, ornaments, or marginalia migrate across reprintings.

## 3. MARC mapping (and where it leaks)

MARC was designed before FRBR, so the levels are smeared across fields rather than cleanly separated:

| Level | Main MARC fields |
|---|---|
| Work | **130 / 240** (uniform title), **1xx** (creator), **7xx** linking entries |
| Expression | partially **240 $l** (language), **250** sometimes, **546** (language note) — **not cleanly modeled** |
| Manifestation | **245** (title proper), **250** (edition statement), **260 / 264** (imprint — place, publisher, date), **300** (physical description), **490 / 830** (series) |
| Item | **561** (provenance), **562** (copy/version identification — states, variants), **563** (binding), **590** (local notes), **852** (holdings) |

A few things worth flagging:

- **Issue / state / impression** in the Bowers sense have **no dedicated MARC field**. They get recorded in **562** (copy/version), **500** (general note), or **250** (edition) when they reach the title page. This is a known weakness.
- **Imprint** (260/264) is Manifestation-level, *not* Edition-level in the Bowers sense — two issues with different title-page imprints will produce two MARC 264 statements.
- **BIBFRAME**, LC's RDF successor to MARC, replaces the smear with explicit `Work` / `Instance` / `Item` classes — closer to WEMI but still doesn't natively model issue/state/impression.

## 4. Units MARC barely sees — and that matter for "margins"

For a project counting paratext, typography, and graphic elements, the units you'll need don't live in MARC at all. They come from analytical bibliography and book-history databases:

- **Setting of type** — the foundational physical unit; "edition" in Bowers is defined by it.
- **Forme** — what gets printed in one pull on one side of one sheet; the relevant unit for stop-press correction and for how marginal notes and running titles were composed.
- **Sheet / gathering / quire** — physical production units; paratextual material (prefaces, indices, errata) often occupies its own gatherings and can be added, removed, or swapped between issues.
- **Cancel leaves** — replacement leaves; often carry corrected paratext.
- **Type / fount / case** — the actual types used; tracked in projects like the **Typenrepertorium der Wiegendrucke** (incunabula), Vervliet's work on 16th-century romans and italics, and Hebrew-specifically in the **Vinograd** *Thesaurus of the Hebrew Book* and the National Library of Israel's *Bibliography of the Hebrew Book*.
- **Ornaments, initials, printer's devices, factotums** — woodcut and metalcut stock that printers reused across many editions; databases like **Fleuron** (18th-century ornaments) and **Passe-Partout** (printer's devices) treat these as countable units in their own right.
- **Paratextual elements** in the Genette sense — title page, dedication, preface, approbations / *haskamot* (especially in Hebrew print), errata, colophon, running titles, marginal notes, indices. Each is a unit you may want to count independently of editions.
- **Copy-specific paratext** — marginalia, annotations, bindings, provenance marks. These are Item-level and only show up in 561/562/563/590, usually narratively.

Most of the units in this list are also **page-layout zones** before they are bibliographic entities — a haskama, a colophon, a marginal commentary, an ornament frame, a running title each occupy a delimitable region on a page. When Margins-scale digitization produces fresh HTR/OCR output (Transkribus, eScriptorium, Kraken), these regions need to be labelled with a controlled, interoperable vocabulary, not ad-hoc per project. The de facto standard here is **SegmOnto** (https://segmonto.github.io/) — a community-curated controlled vocabulary for zone types (e.g. `MainZone`, `MarginTextZone`, `TitlePageZone`, `RunningTitleZone`, `QuireMarksZone`, `NumberingZone`, `StampZone`) and line types, designed to be interchangeable across HTR platforms and downstream tooling. SegmOnto was developed primarily on Latin-script European material; for the Hebrew-print corpus it will need targeted **adaptation**: right-to-left reading-order conventions; zone types specific to Hebraica such as approbation blocks (*haskamot*), rabbinic-commentary surrounds (e.g. Rashi / Tosafot frames around a Talmud or Mikraot Gedolot main text), chronogram-bearing title-page panels, and bilingual / multi-script colophons. Modelling these as SegmOnto-compatible extensions — rather than as bespoke local categories — keeps the project's layout layer reusable by, and reusable from, the wider HTR community, and gives the digitization pipeline a well-defined intermediate representation between page image and structured bibliographic record.

## 5. Practical implication for the Margins counting model

If "margins" needs to count along several axes, the data model needs to be richer than MARC offers:

- For the **Work ↔ Edition** axis: **Work → Expression → Manifestation** (three levels, WEMI).
- For the **Edition ↔ Copy** axis: **Manifestation → Issue → Impression → State → Item** (Bowers hierarchy).
- Orthogonal countable units that don't fit either chain: **type-faces, ornaments, devices, paratextual components** — model these as separate entities with many-to-many links to Manifestations (and sometimes to Items, when a marginal note or binding is copy-unique).

The cleanest off-the-shelf vocabulary to align to is **IFLA-LRM + BIBFRAME 2.0** for the upper levels, and the **CIDOC-CRM / FRBRoo** (now **LRMoo**) extensions for the analytical-bibliography units, which were designed exactly for cultural-heritage objects with this kind of multi-layered identity. For Hebrew print specifically, Vinograd-style records and the NLI's *Bibliography of the Hebrew Book* schema are the local reference points.

## 6. Lessons from the MBI / Bibliography of the Hebrew Book TSV

The NLI's **Bibliography of the Hebrew Book** (BHB / מפעל הביבליוגרפיה — `MBI` in the database) is a working test of the framework above. The `mbimarc-bhb.tsv` dump in this repo holds 107,977 records across 43 columns. The column headers expose how a real Hebraica-cataloguing operation extends MARC — what they keep in standard fields, what they push into the local **9xx** range, and which paratextual units they treat as first-class.

### 6.1 The transcribed / controlled twin pattern

For every Manifestation-level imprint element, the BHB carries **two** columns: the verbatim transcription from the book and a normalized authority form.

| Aspect | Transcribed (standard MARC) | Controlled (local 9xx) |
|---|---|---|
| Place of publication | **260a** — bracketed if inferred (`[ליוורנו]`) | **951** — bilingual `Hebrew\|Latin` (`ליוורנו\|Livorno`); populated in ~99% of rows |
| Publisher | **260b** — verbatim, often in source script/orthography | **922** — controlled name; only ~1% populated (long tail) |
| Printer / manufacturer | **260f** — verbose transcription including all named partners | **923** — short controlled shop name (`דפוס ש. מונזון`) |
| Date | **260c (1)** — Hebrew-letter date as printed (`תפ"ו`); **260c (2)** — normalized Gregorian (`1726`); also redundantly in **008-Year** | — |

This is the operational answer to the FRBR-vs-MARC smear from §3: rather than reshape MARC, the BHB keeps the source-faithful transcription in the canonical field and parks the normalized/authority value in a parallel local field. A counting model that wants to group by place, publisher, or printer should join on the **9xx** column, not the **26x** one.

### 6.2 First-class paratextual fields

Section 4 listed paratextual units that "MARC barely sees." The BHB has quietly turned several of them into dedicated columns — exactly the move our model recommends:

- **915 — הסכמה (Haskama).** ~10,700 records carry an extracted rabbinic-approbation note: granting rabbi, place, date. Approbations are a major Hebrew-print paratextual genre (legal, commercial, and authorizing) and the BHB treats them as a countable, queryable unit rather than burying them in a free-text 500 note.
- **912 — Dating (chronogram).** ~14,400 records carry the **source phrase** of a Hebrew chronogram (`מנורת המאור`, `ופדויי ה' ישבון…`), with apostrophes marking the letters whose numerical values sum to the year. This is a typographic-paratextual unit in its own right (it sits on the title page, is a literary device, and was set in display type) and the BHB extracts it separately from both the Hebrew-letter date (260c-1) and the Gregorian year (260c-2, 008).
- **535 — OriginalsLocation** and **533 — ReproductionNote.** ~9,300 / ~14,400 records: standard MARC fields used heavily because so much of the corpus is documented from microfilms or facsimiles, not autopsy of an original. This is Manifestation-vs-Item-vs-surrogate noise that any counting model has to handle explicitly.

### 6.3 Local taxonomic / structural fields

- **900 — MBI ID** (`MBI-0105152`): the bibliography's own sequence number, parallel to MARC 001. Always present.
- **901 — Type:** local form/format taxonomy (`ספר`, `חוברת`, …). ~31% populated; useful for separating books from pamphlets and ephemera.
- **690 — Genre:** local Hebrew subject/genre vocabulary (`פיוט (תרגום)`, `ליטורגיה (מקור)`, `נושאים מקומיים`); thin (~4%) but a usable signal for liturgy/poetry slices.
- **921 — Location** vs **951 — Location.** Two location columns. 951 is the dense bilingual place authority (~99%); 921 is sparse (~5%) and seems to be a secondary/holdings-style location. Treat 951 as the canonical join key.

### 6.4 Non-MARC bookkeeping columns

Several columns are not MARC content fields at all:

- **005** — record transaction timestamp (sparse here).
- **008** — the fixed-length data element string; **008-Year** is the parsed publication year, used as the normalized date key.
- **041-a+** — language code(s); `heb` for almost the entire corpus, but with multi-language records appearing here.
- **record-leader** — the MARC leader; effectively constant in this dump.
- **Yael-Comments** — curator notes (~10% of rows). A reminder that any production catalogue carries a human-editorial layer alongside the structured fields.

### 6.5 What this validates (and what it warns)

**Validates:** the recommendation in §5 — that paratextual units (haskamot, chronograms, ornaments, devices) should be modelled as separate entities with their own columns rather than buried in 500-notes — is what an operational Hebraica bibliography has *already done* for the units it cared about most. The 915 / 912 / 923 columns are exactly the pattern to copy and extend (for ornaments, printer's devices, title-page typography, etc.).

**Warns:** even a 100k-record specialist database doesn't model **issue / impression / state**. Bowers-level distinctions still live in free text (500, occasionally 250 or in the Yael-Comments column) or not at all. If the Margins project needs to count below the Manifestation, it will be generating those distinctions itself, not inheriting them from the BHB.

## 7. What Bowers/Gaskell distinctions look like in BHB free text

The BHB has no dedicated field for **issue, impression, state, cancel, or variant** (see §6.5). When a cataloguer encountered one, they recorded it narratively, almost always in **500 (General Note)**. The pattern is consistent enough to be parsed: a **scope-marker** + a **verb of replacement / omission / reprinting** + a **unit**.

| Bowers/Gaskell concept | What it means | BHB example (paraphrased & translated) |
|---|---|---|
| **State** | Copies of one edition/issue differ because a leaf was reset/corrected *during* the print run. | **000146263** (Salonika 1594, di Medina responsa): "in siman 190 a responsum on conversion of slaves was printed — that is the original text. **In some copies (בחלק מהעותקים) this responsum was replaced by two other responsa.**" — classic stop-press substitution (almost certainly self-censorship). |
| **Issue** | Identical sheets re-sold later under a new title page; only the preliminaries are reset. | **000107580**: Friedberg dates the book to 1864, but notes that "**for this issue (להוצאה זאת) a new title page (שער חדש) was printed in 1866.**" <br><br> **000106487**: "This is the previous (1859) edition **with a new title page** stating that the book was printed from a manuscript" — Steinschneider's criticism prompted the printer to re-float the stock with a corrected imprint. |
| **Issue with reset preliminaries** | Same body sheets, new title page + new front matter (often politically motivated). | **000106686**: "**The body of the book is identical in both 'editions.' The title page was replaced**, the publisher-brothers' prefaces were dropped, and in the haskamot 'Mordechai Leib' was replaced with 'Zechariah.' … The publishers feared the authorities and wanted to suppress their names in some copies." |
| **Cancel (cancellans)** | A single replacement leaf pasted in to correct/disguise the original. | **000108424**: "This pamphlet was first printed as *Sifrut Yemei Qedem*. **Here only the first leaf was replaced.**" <br><br> **000105215**: "**The title page is forged**: this is in fact the Dyhrenfurth 1798 edition. **Only the title-page leaf was reprinted** (the author's preface that had been on its verso was suppressed). The body of the book is unchanged." — a fraudulent cancel. |
| **Separate impression / parallel edition** | A second setting page-for-page identical to the first, distinguishable only by typographic detail. | **000120461** (Heshel of Apta, c.1825): "**In parallel an identical edition was printed page-for-page**, with no textual changes and most ornaments identical. The conspicuous difference: in the present edition the parenthetical words are in tiny type, while in the other edition they are in large square type." — the typographic test (tiny vs. large square) is exactly the analytical-bibliographer's diagnostic for a separate setting of type. |
| **Variant (material)** | Copies differing in paper, ink, or another non-textual feature. | **000160162** (Pirkei de-Rabbi Eliezer, Warsaw 1852): "**There are copies printed on bluish paper.**" — often signals a presentation or limited sub-set within one impression. |
| **Variant (structural)** | Copies differing because a leaf or gathering is present/absent. | **000160162**: "**There are copies from which the second title page is missing.**" Often a binder's variant, sometimes an issue marker. |
| **Self-declared new edition (250-level)** | A genuine new setting, advertised on the title page. | **000105523**: 250 = `מהדורה שניה מורחבת ומתוקנת` ("second edition, enlarged and corrected"). This is the rare case where MARC 250 captures the distinction cleanly. |

### The implicit grammar

The trio that drives almost every Bowers/Gaskell observation in 500-notes is:

- **scope-marker** — `בחלק מהעותקים` (in some copies) · `יש טפסים` (there are copies) · `במקביל` (in parallel) · `בעותק זה` (in this copy)
- **verb** — `הוחלף` (was replaced) · `נשמט` / `הושמט` (was omitted / suppressed) · `נדפס מחדש` (was reprinted) · `הוסף` (was added)
- **unit** — `שער` (title page) · `דף` / `הדף הראשון` (leaf / first leaf) · `קונטרס` (gathering) · `הקדמה` (preface) · `הסכמה` (approbation) · `תשובה` (responsum) · `נייר` (paper)

Lifting Bowers-level structure out of the BHB programmatically means parsing for that pattern and routing matches into new `issue` / `state` / `cancel` / `variant` columns. Even partial extraction would give Margins a queryable analytical-bibliography layer over a corpus where none currently exists in structured form.

## 8. References and ontologies

### Foundational works (the canon)

- **Bowers, Fredson.** *Principles of Bibliographical Description.* Princeton: Princeton University Press, 1949. (Reprinted with new introduction by G. Thomas Tanselle, Oak Knoll / St Paul's Bibliographies / Bibliographical Society of the University of Virginia, 1994; latest reissue 2023.) — The source of the **edition / issue / impression / state / variant** hierarchy as used in Anglo-American descriptive bibliography. Chapters IV–V are the locus classicus for the definitions.
- **Gaskell, Philip.** *A New Introduction to Bibliography.* Oxford: Oxford University Press, 1972. (Reprinted with corrections 1974; reissued by Oak Knoll Press / St Paul's Bibliographies, 1995, ISBN 1-884718-13-2.) — Extends Bowers's framework forward through the machine-press period (to 1950) and adds the production-unit vocabulary (**forme, sheet, gathering, cancel**) used in §4 of this document.
- **Tanselle, G. Thomas.** "The Bibliographical Concepts of *Issue* and *State*." *Papers of the Bibliographical Society of America* 69 (1975): 17–66. — The most cited refinement of the Bowers definitions; widely treated as the operative standard.
- **McKerrow, R. B.** *An Introduction to Bibliography for Literary Students.* Oxford: Clarendon Press, 1927. — Gaskell's predecessor; still cited for hand-press-period definitions.

### Cataloguing standards that implement (parts of) the Bowers hierarchy

- **DCRM(B) — Descriptive Cataloging of Rare Materials (Books)**, Bibliographic Standards Committee, Rare Books and Manuscripts Section (RBMS) of the Association of College and Research Libraries (ACRL), 2007; superseded by the **DCRMR (RDA edition)**, 2022. — The standard that *operationalizes* Bowers/Gaskell distinctions for cataloguing. DCRMR explicitly defines edition/issue/impression/state and gives rules for distinguishing them in description. This is the bridge between analytical bibliography and library cataloguing practice.
- **RDA — Resource Description and Access** (RDA Toolkit, current edition). — Built on FRBR/IFLA-LRM (Work / Expression / Manifestation / Item). RDA recognizes "edition", "issue", and "impression" as Manifestation-level identifying attributes, but does not give them dedicated relation types — they sit inside the manifestation statement rather than as structural classes. Rare-materials work uses DCRMR as an RDA application profile to recover the finer distinctions.

### Ontologies that have adopted (or partly adopted) the distinctions

- **IFLA-LRM (Library Reference Model)**, IFLA, 2017 (current rev. 2020). — Provides WEMI (Work / Expression / Manifestation / Item). Does **not** model issue / impression / state below the Manifestation; those collapse into Manifestation. <https://www.ifla.org/publications/ifla-library-reference-model/>
- **FRBRoo → LRMoo (CIDOC-CRM extension)**, CIDOC Conceptual Reference Model SIG. FRBRoo v2.4 (2015); **LRMoo v1.0** approved April 2024. — The object-oriented reformulation aligned with CIDOC-CRM (cultural-heritage ontology). Key classes for our purposes:
  - **F1 Work**, **F2 Expression**, **F3 Manifestation** (Product Type), **F5 Item** — WEMI equivalents.
  - **F24 Publication Expression** — the publication-level expression, finer than F2.
  - **F32 Carrier Production Event** → R26 produced → **F3 Manifestation Product Type** — the production-run event that lets you model *impressions* as separate events on the same matrix.
  - The CIDOC-CRM working note **"Modelling States of Prints using FRBRoo"** explicitly addresses **state** by linking an **E81 Transformation** (to the matrix / setting of type) → a new F3 Manifestation Product Type, whose F5 Items embody a new F22 Self-contained Expression. This is the most fully worked-out ontological treatment of Bowers's **state** concept currently available.
  - References: <https://cidoc-crm.org/lrmoo>, LRMoo v1.0 PDF at <https://cidoc-crm.org/sites/default/files/LRMoo_V1.0.pdf>, and the states-of-prints working paper at <https://cidoc-crm.org/modelling-states-of-prints-using-frbroo>.
- **BIBFRAME 2.0** (Library of Congress, 2016–). — Three classes: **Work**, **Instance**, **Item**. Instance is the rough equivalent of Manifestation; BIBFRAME does **not** natively model issue / impression / state and treats them as notes or as separate Instances linked by `bf:hasDerivative` / `bf:otherEdition`. <https://www.loc.gov/bibframe/>
- **PRESSoo** (CIDOC-CRM extension for continuing resources, 2014–). — Less relevant for monographs but worth noting as a precedent for extending FRBRoo with serial-publication-level structure.

### Practical takeaway for the Margins data model

If Margins needs to express Bowers-level distinctions formally:

- **LRMoo** is currently the only mainstream ontology that natively supports them — through the F32 Carrier Production Event chain for impressions and the E81 Transformation pattern for states. This is what to align to if RDF/linked-data interoperability matters.
- **DCRMR** is the controlled cataloguing vocabulary to use for the *labels* of edition / issue / impression / state in any UI or export.
- **MARC 250** alone is insufficient — it captures only self-declared "second editions" and misses everything that lives in 500-notes (as §7 demonstrates from the BHB).

### Short answer: which ontologies adopted Bowers/Gaskell?

- **IFLA-LRM** and **BIBFRAME**: only WEMI / Work-Instance-Item; **issue / impression / state are not modelled** — they collapse into Manifestation or live in notes.
- **RDA**: recognizes edition/issue/impression as Manifestation attributes but without dedicated structural classes.
- **FRBRoo → LRMoo** (CIDOC-CRM extension, v1.0 April 2024): the only mainstream ontology that *natively* supports Bowers-level distinctions.
  - **Impression** = a distinct **F32 Carrier Production Event** producing an **F3 Manifestation Product Type** from the same matrix.
  - **State** = an **E81 Transformation** of the matrix yielding a new F3 with new F5 Items — laid out explicitly in the CIDOC-CRM working paper "Modelling States of Prints using FRBRoo."

If Margins needs RDF-level interoperability for these distinctions, **LRMoo** is the alignment target; for cataloguing labels, **DCRMR**.

### Sources

- [LRMoo Home — CIDOC CRM](https://cidoc-crm.org/lrmoo)
- [LRMoo v1.0 (PDF)](https://cidoc-crm.org/sites/default/files/LRMoo_V1.0.pdf)
- [Modelling States of Prints using FRBRoo — CIDOC CRM](https://cidoc-crm.org/modelling-states-of-prints-using-frbroo)
- [FRBRoo — CIDOC CRM](https://cidoc-crm.org/frbroo)
- [BIBFRAME — Library of Congress](https://www.loc.gov/bibframe/)
- [DCRMR (RDA edition) — RBMS, 2022 (PDF)](https://bsc.rbms.info/assets/pdfs/DCRM%20RDA%20edition%20release%202022_1_0_0.pdf)
- [IFLA Library Reference Model](https://www.ifla.org/publications/ifla-library-reference-model/)
- [Bowers, *Principles of Bibliographical Description* — Internet Archive](https://archive.org/details/principlesofbibl0000bowe)
- [Gaskell, *A New Introduction to Bibliography* — Internet Archive](https://archive.org/details/newintroductiont0000gask)

## 9. What we can count from BHB, level by level (Margins scope: ≤ 1800)

Counts below are restricted to records with **008-Year ≤ 1800**, matching the Margins proposal's corpus window (beginning of Hebrew print → end of 18th c.). Total **in-scope: 10,787 records**. Where the contrast with the full corpus (1470–1979, 107,977 records) is informative, the out-of-scope figure is given in italics for reference. Values are **[exact]** (populated-cell or unique-value count from a field) or **[est.]** (regex over free text). All Hebrew patterns refer to the 500-note column unless noted.

### 9.1 The in-scope corpus envelope

| Quantity | Value | Source |
|---|---:|---|
| Total in-scope records (≈ Manifestations) | **10,787** [exact] | 008-Year ≤ 1800 |
| By century | 15th: 126 · 16th: 1,772 · 17th: 2,216 · 18th: 6,673 [exact] | col 008-Year |
| Records in Hebrew only (041 = `heb`) | 8,840 [exact] | col 041 |
| Hebrew + Yiddish | 707 · Heb+Latin: 235 · Heb+Ladino: 178 · Yiddish-Heb: 78 · Heb+Aramaic: 77 · Heb+Judeo-Arabic (ghb): 76 · Heb+Italian: 71 · Ladino-only: 56 | col 041 |
| Multi-language records (041 contains `\|`) | 1,835 [exact] | col 041 |

### 9.2 Work level (in-scope)

| Quantity | Value | Source |
|---|---:|---|
| Distinct uniform titles (130) — Works with ≥ 2 known Manifestations | **3,572** [exact] | col 130 |
| Records with 130 (clustered) | 4,731 [exact] | col 130 |
| Records without 130 (presumed single-Manifestation) | 6,056 [exact] | col 130 |
| **Upper bound on distinct Works in scope** | **~9,628** [est.] | 3,572 + 6,056 |
| Most-republished in-scope Works (top 6) | תפילות. חולים ומתים. (64); שירים ופיוטים (59); תפילות. שונות. (50); תפילות. ברכות. (50); תפילות. פיוטים. (41); תיקונים. שונים. (37) | col 130 |
| Distinct main personal-name authors (100) | **1,986** [exact] *(vs. 19,661 full-corpus)* | col 100 |
| Distinct main corporate authors (110) | **125** [exact] *(vs. 3,545 full-corpus)* | col 110 |

The drop from ~19.7k authors corpus-wide to ~2k in scope is a sharp reminder of how early-modern the proposal's window is: ~90% of the authors in the BHB are 19th/20th-century.

### 9.3 Expression level (in-scope)

The BHB does not model Expressions structurally. Three proxies in scope:

| Quantity | Value | Source |
|---|---:|---|
| Records with 546 LanguageNote | 262 [exact] | col 546 |
| Records with 730 Added Uniform Title | 2,813 [exact] | col 730 |
| Multi-language records (041 contains `\|`) | 1,835 [exact] | col 041 |

### 9.4 Manifestation level (in-scope) — the early-modern Hebrew print map

| Quantity | Value | Source |
|---|---:|---|
| Distinct places of publication (951, raw) | 314 [exact] | col 951 |
| Distinct places after `Heb\|Lat` order-normalization | **205** [exact] | col 951 |
| Distinct controlled publishers (922) | 18 [exact, from only 20 populated records] | col 922 — essentially unpopulated in scope |
| Distinct controlled printers (923) | 353 [exact, from 506 populated records] | col 923 — 4.7% populated; 70% distinct → very weak dedup |
| Distinct local types (901) | 221 [exact, from 4,607 populated] | col 901 — 43% populated |
| Distinct local genres (690) | 52 [exact, from 274 populated] | col 690 — only 2.5% populated in scope |

**Top in-scope places** — this is a *completely* different geography from the full-corpus top (Tel Aviv / Jerusalem / Warsaw / Vilnius / New York). Restricting to ≤ 1800 surfaces the classical map of early-modern Hebrew print:

| Place | Records |
|---|---:|
| Venice | 1,567 |
| Amsterdam | 1,366 |
| Prague | 595 |
| Mantua | 518 |
| Istanbul (קושטא) | 470 |
| Zholkva | 430 |
| Fürth | 406 |
| Livorno | 386 |
| Salonika (שלוניקי) | 357 |
| Berlin | 303 |
| Cracow | 286 |
| Frankfurt am Main | 230 |

**Top in-scope types** (901): ספר 3,598 · סדר 432 · "זה ספר" 66 · `...` 65 · ספר שאלות ותשובות 14.

**Top in-scope genres** (690): מקרא 57 · ליטורגיה (תרגום) 54 · שירה (מקור) 25 · ליטורגיה 24 · הגדה של פסח 16. (Genre is sparse in scope — 2.5% coverage — so this is a small-sample snapshot, not a representative distribution.)

**Caveats on 9xx coverage in scope**: 922 (controlled publisher) is essentially absent in scope (20 records). 923 (printer) is populated for only 4.7% of in-scope records and is barely deduplicated (353 distinct from 506 populated). 951 (place) is the only 9xx field that delivers usable population statistics for the early-modern window.

### 9.5 Edition statements (MARC 250) in-scope

| Quantity | Value | Source |
|---|---:|---|
| Records with any 250 EditionStatement | **414** [exact] *(vs. 7,916 full-corpus)* | col 250 |
| Most common 250 phrasing | `נדפס שנית` ("printed a second time") — 7 records | col 250 |

**Finding worth noting** — see TODO in the Hebrew-terminology appendix: in the in-scope (≤ 1800) records, the dominant 250-phrasing is **`נדפס שנית`** (printed-a-second-time), *not* `מהדורה שניה` (the modern formulation, which dominates the full corpus). The שניה / שלישית / רביעית sequence in 250 is a 19th–20th-c. pattern; in early-modern records the printers and cataloguers default to the **נדפס שנית / נדפס מחדש** verbal form. This is direct in-data evidence that **the Hebrew vocabulary for "edition" has shifted historically**, and partially substantiates one of the TODOs (`הוצאה/מהדורה/הדפסה` usage being period-dependent).

### 9.6 Bowers/Gaskell sub-Manifestation signals (regex over 500-notes) — in-scope

For in-scope records, paratext-extraction and free-text notes are denser than in the full corpus (the BHB's early-modern records get more careful descriptive cataloguing). The Bowers-pattern hit-rate roughly doubles:

| Bowers/Gaskell unit | Hebrew marker | In-scope hits | (full corpus) |
|---|---|---:|---:|
| State | `בחלק.*עותק` | **3** | 3 — all in-scope |
| Variant copies | `יש טפסים` | **121** | 455 |
| Issue (new title page) | `שער חדש\|שער אחר\|שער מתוקן` | **34** | 149 |
| Cancel leaf | `דף מבוטל \| הוחלף.*דף` | **16** | 46 |
| Impression / reprint | `נדפס שנית\|נדפס מחדש` | **68** | 213 |
| Replacement (any unit) | `הוחלף` | **25** | 97 |
| Variant text | `נוסח אחר` | **14** | 34 |
| Omission / suppression | `הושמט\|נשמט` | 708 | 3,190 (over-matches) |
| Forged / fake imprint | `מזוייף\|מזויף` | **15** | 143 |
| Edition-talk anywhere in 500 | `מהדורה\|הוצאה\|הדפסה` | 1,579 | 10,384 |
| **Union: any Bowers-flavored signal** | combined | **~896 (8.3% of in-scope)** | ~3,910 (3.6% of full corpus) |

**Important**: the **8.3%** rate of Bowers signals in-scope is more than double the full-corpus rate. For Margins, that means **a 500-note parsing pass can realistically promote ~900 of 10,787 in-scope records to structured `issue` / `state` / `cancel` / `variant` fields** — still a sample rather than a population count, but a usable one (e.g. for a typology-of-issues case study).

### 9.7 Paratext (already extracted as structured fields) — in-scope is where this lives

This is the layer where in-scope numbers most dramatically outpace the full corpus. The early-modern records are *where the paratext extraction was actually done*:

| Paratextual unit | Field | In-scope records | % of in-scope | (full-corpus %) |
|---|---|---:|---:|---:|
| Haskama (rabbinic approbation) | **915** | **2,259** | **20.9%** | 9.9% |
| Chronogram (title-page dating phrase) | **912** | **5,351** | **49.6%** | 13.4% |
| Originals location | 535 | 2,387 | 22.1% | 8.7% |
| Formatted contents | (col 30) | 463 | 4.3% | 6.9% |
| Yael curator comments | (col 38) | 508 | 4.7% | 10.4% |
| Series statement | 490 | 19 | 0.2% | 9.4% |
| Reproduction note | 533 | 20 | 0.2% | 13.3% |

Two findings stand out:

- **One in five in-scope records carries a structured haskama** — the BHB has done the extraction work for the proposal already at this layer.
- **Nearly half of in-scope records carry a structured chronogram** — and the rate climbs from 19% in the 15th c. to 61% in the 18th c. (§10.4). This is **publishable as-is**.
- 490 (series) and 533 (reproduction) are negligible in scope — confirming that those fields predominantly serve 19th–20th-c. cataloguing.

### 9.8 Item level

Not derivable from the in-scope TSV (or the full corpus). The BHB describes Manifestations, not physical copies. The only Item-flavored signals in scope are:

- **535 OriginalsLocation** — 2,387 records, references a holding institution for an autopsied original.
- **In-note `בטופס שראינו` / `בעותק זה`** — copy-specific observations scattered through 500-notes (low hundreds, not separately quantified).

A true Item-level count for the Margins window requires holdings catalogues, Footprints data, or NLI-internal copy registers — not this dump.

### 9.9 What this means for Margins

For the in-scope (≤ 1800) corpus, BHB lets Margins make **strong quantitative claims** at:

- **Manifestation level**: ~10,800 dated entries, with a usable place breakdown for the 200-odd centres of early-modern Hebrew print (Venice and Amsterdam together ~27% of in-scope output).
- **Work level**: ~3,600 clustered Works + ~6,000 single-Manifestation candidates → upper bound of ~**9,600 distinct Works in scope**.
- **Paratext-unit level**: **2,259 structured haskamot** and **5,351 structured chronograms** — already big enough for serious distributional analysis without any additional extraction.
- **Author level**: ~2,000 distinct personal-name authors in scope — a tractable population for prosopography.

It allows only **weak claims** at:

- **Bowers sub-Manifestation level**: ~896 records (8.3%) carry note-level signals — useful as a study sample, *not* as a population count of issues/states/cancels in the early-modern Hebrew print world.
- **Publisher / printer authority counts** (922/923): too sparse and under-deduplicated to support population statistics in scope.
- **Item level**: not addressable from this dump.

And the in-scope dump is only **~18% of the proposal's 60,000-title target** (§10.2) — meaning all the percentages above are *of the BHB slice*, not of all early-modern Hebrew print. They should be read as a denominator-bounded sample.

## 10. Temporal dimensions relevant to the Margins proposal

The Margins proposal (B1 resubmission, §1.2 / Methods) defines its corpus as **"all books and broadsides printed in Hebrew fonts, from the beginning of Hebrew printing until the end of the 18th century"**, with target estimates of ~150 incunabula + ~10,000 16th-c. + ~20,000 17th-c. + ~30,000 18th-c. ≈ **60,000 titles**. That target window (c.1470 – 1800) imposes specific temporal axes on the data model.

### 10.1 Five distinct time axes (any "year" question has to specify which)

A printed book sits at the intersection of several timelines. They must be kept apart in any quantitative model:

| Axis | What it dates | BHB field(s) |
|---|---|---|
| **Work-creation time** | When the intellectual content was composed (Rashi: 11th c.; Karo's *Shulhan Arukh*: mid-16th c.) | Not directly recorded; inferable from 100/130/240 |
| **Manifestation / imprint time** | When *this* edition was printed | 260c (1) Hebrew-letter date · 260c (2) Gregorian · 008-Year · 912 chronogram phrase |
| **Issue / state / cancel time** | When a sub-Manifestation event happened (re-issue with new title page, stop-press correction, replacement leaf) | Only in 500-notes; usually undated |
| **Surrogate time** | When the microfilm / facsimile / digital scan was made (relevant for *access*, not for the book itself) | 533 ReproductionNote |
| **Item life-time** | When ownership marks, marginalia, censorship cuts, bindings were added — usually *centuries* after imprint | Not in BHB |

For "margins" (paratext, marginalia, censorship, provenance) the **Item life-time** axis is conceptually central but is *absent from BHB structured data*. Anything Margins wants to say at that axis must come from copy-specific datasets (Footprints, holdings catalogues, scan annotations), not from this TSV.

### 10.2 In-scope BHB coverage vs. Margins target

Recomputed from `mbimarc-bhb.tsv` restricted to 008-Year ≤ 1800:

| Century | BHB records in dump | Margins proposal estimate | BHB / target |
|---|---:|---:|---:|
| 15th (incunabula) | **126** | ~150 | **~84%** |
| 16th | **1,772** | ~10,000 | ~18% |
| 17th | **2,216** | ~20,000 | ~11% |
| 18th | **6,673** | ~30,000 | ~22% |
| **Total in scope** | **10,787** | **~60,000** | **~18%** |

**Caveat — this is not a quality judgment on BHB.** The 60,000 figure in the proposal is consistent with Vinograd's *Thesaurus* and historical print-output estimates; the 10,787 records here represent what is dumped in *this MARC-format TSV* of the MBI subset, not the full reach of the NLI Bibliography of the Hebrew Book project, and certainly not all Hebrew bibliography. Margins will need **Vinograd, Yaari, Heller's *Sixteenth-* / *Seventeenth-Century Hebrew Book*, Iakerson / Offenberg's incunabula catalogues, and similar** to approach the 60,000 target. The mbimarc dump is one channel, not the whole.

Practical takeaway for the proposal: the in-scope MBI/BHB layer gives a **~18% sample** with the richest structured paratext extraction available; the rest must be assembled from other sources or generated by Margins itself.

### 10.3 The Hebrew print-productivity curve (in-scope decades)

Counting BHB records by decade reveals the shape of early-modern Hebrew print as the BHB sees it — production grows roughly exponentially through the 18th century:

```
1480s  52   |▌
1510s 150   |█▌
1520s 120   |█▏
1530s  95   |█
1540s 175   |█▊
1550s 230   |██▎
1560s 234   |██▎
1570s 163   |█▋
1580s 197   |█▉
1590s 337   |███▎
1600s 283   |██▊
1610s 233   |██▎
1620s 178   |█▊
1630s 123   |█▏    ← Thirty Years' War dip
1640s 217   |██▏
1650s 197   |█▉
1660s 167   |█▋
1670s 197   |█▉
1680s 252   |██▌
1690s 357   |███▌
1700s 405   |████
1710s 503   |█████
1720s 508   |█████
1730s 554   |█████▌
1740s 562   |█████▋
1750s 542   |█████▍
1760s 677   |██████▊
1770s 584   |█████▊
1780s 842   |████████▍
1790s 1354  |█████████████▌
```

Two features worth flagging for the proposal:

1. **The 1630s dip** is real in the data (123 vs ~200/decade either side), consistent with the disruption of central European print during the Thirty Years' War — a finding that surfaces directly from a `count(*) group by decade` once the data is loaded.
2. **The late-18th-c. acceleration** (1780s × 1.5; 1790s × 2.4) reflects the genuine intensification of Hebrew print in Eastern Europe / Galicia / Russia — and motivates the proposal's choice of *end-of-18th-century* as the upper bound rather than, say, 1700.

### 10.4 Paratextual time-series — already extractable

A genuine quantitative win: for the in-scope corpus, paratext-extraction by century shows the well-known historical pattern of *paratextual intensification*:

| Century | Records | Haskamot (915) | % | Chronograms (912) | % |
|---|---:|---:|---:|---:|---:|
| 15th | 126 | 1 | 0.8% | 24 | 19% |
| 16th | 1,772 | 20 | 1.1% | 415 | 23% |
| 17th | 2,216 | 330 | 14.9% | 847 | 38% |
| 18th | 6,673 | 1,908 | 28.6% | 4,065 | 60.9% |

This is a real, publishable curve already sitting in the TSV — the **rise of the haskama as a standard paratextual element from ~1% (16th c.) to ~29% (18th c.)** and the parallel rise of the title-page **chronogram from ~19% to ~61%**. Both are central to the "margins of the book" thesis and quantifiable today, before any new tooling.

Caveat: the percentages are over *what the BHB has extracted*, not over what the books actually contain. A 17th-c. book without a 915 cell may still have a haskama that the cataloguer chose not to extract. So these are **floor** percentages.

### 10.5 Dating granularity (Manifestation axis)

The Manifestation date in BHB has multiple representations, useful at different granularities:

- **Decade / century** (008-Year): clean, reliable, present in 99% of records.
- **Year (Gregorian)**: 260c-2 / 008-Year — reliable for in-scope records.
- **Hebrew-letter date** (260c-1): present in nearly all in-scope records as transcribed; required for matching against rabbinic citations or other primary sources that cite books by Hebrew year.
- **Chronogram source phrase** (912): the title-page *literary expression* of the date — itself a paratextual unit. Present in 60% of 18th-c. records.

For a temporal-faceted UI (the proposal's "timeline interface"): the safe default key is **008-Year**, with chronogram-phrase as a hover/secondary display and Hebrew-letter date as the citation form.

Bracketed/inferred dates (`[תקל"ו]`, `c. 1755`) appear in 260c but not in 008-Year, which always carries a parsed numeric — so a 4-digit-numeric facet will silently drop the inference-uncertainty, which matters for incunabula and undated broadsides specifically.

### 10.6 Project time (the Margins workplan itself)

For completeness — the proposal's own timeline (5 years; sample collection and infrastructure in Y1, expansion Y2, integrated platform and broadside test in Y3, dissemination Y4-5) is the **fifth time axis** in the data model: the *processing* timestamp on every dataset and annotation. A clean implementation will record per-record (a) the BHB-imprint date, (b) the surrogate-creation date, and (c) the Margins-ingest / annotation date, so that the data state at any point in the project is reproducible.

## Appendix: Hebrew terminology for the Bowers/Gaskell vocabulary

Hebrew bibliographic scholarship (Friedberg's *Bet Eked Sefarim*, Yaari, Habermann, Vinograd's *Thesaurus*, the BHB / מפעל הביבליוגרפיה) has settled terms for most of the Bowers/Gaskell vocabulary. A few have no canonical Hebrew equivalent and are handled periphrastically. Marked **[std]** for established terms, **[var]** where usage varies, **[periphr.]** where Hebrew normally describes the concept rather than naming it.

### Conceptual hierarchy (FRBR/Bowers)

| English | Hebrew | Notes |
|---|---|---|
| Work | **יצירה** [std] | LRM Hebrew translation |
| Expression | **ביטוי** [std] | LRM Hebrew translation |
| Manifestation | **התגלמות** / **גילום** [var] | LRM Hebrew; in everyday cataloguing usually collapses into מהדורה / הוצאה |
| Item / Copy | **עותק** [std], also **טופס** [std] | טופס is heavily attested in BHB free-text notes ("בטופס שראינו…", "יש טפסים…"); עותק is the modern library term. *General claim that טופס is the "older" Hebraica term needs primary-source verification — see TODO below.* |
| Edition | **מהדורה** [std], also **הוצאה** [std] | Both appear in BHB notes ("ההוצאה הראשונה", "מהדורה שניה"). *The claim that older Hebraica bibliography (Friedberg, Vinograd) systematically prefers הוצאה while modern library Hebrew prefers מהדורה reflects general impression, not verification against those works in this analysis — see TODO below.* |
| Issue | **הוצאה** in the sense "re-issue" [var]; usually **periphr.**: `עם שער חדש`, `במהדורה זו הוחלף השער` | No fully crisp single word. Sometimes **הופעה** is proposed but not widely used. |
| Impression / Printing | **הדפסה** [std] | "נדפס שנית" / "הדפסה שניה" = second impression |
| State | **מצב** [var] (literal); often **periphr.**: `בחלק מהעותקים`, `יש טפסים ש…` | No firmly established technical term; cataloguers describe rather than label |
| Variant | **נוסח** [std] (textual), **שינוי** [std], or transliterated **וריאנט** [var] | נוסח is best for textual variants; for material variants (paper, binding) Hebrew uses descriptive phrases |

### Production / physical units (Gaskell)

| English | Hebrew | Notes |
|---|---|---|
| Setting of type | **סדר אותיות** / **סדר־דפוס** [var] | Periphrastic in most notes |
| Forme | **פורמה** [std, transliterated] | The standard term; sometimes **מסגרת דפוס** |
| Sheet | **גליון** [std], also **יריעה** [var] | גליון is most common |
| Gathering / quire | **קונטרס** [std] | Note: קונטרס also means "pamphlet/booklet" in Hebrew — context disambiguates |
| Leaf | **דף** [std] | |
| Page | **עמוד** [std] | |
| Cancel (cancellans, the replacement leaf) | **דף חליפי** / **דף מוחלף** / **דף מתוקן** [periphr.] | No single canonical word; usually `הדף הוחלף` / `נדפס מחדש` |
| Cancellandum (the leaf removed) | **דף מבוטל** / **הדף שהוחלף** [periphr.] | |
| Stop-press correction | **תיקון בדפוס** [std] | |

### Paratextual / structural elements (mostly native Hebrew terms)

| English | Hebrew | Notes |
|---|---|---|
| Title page | **שער** [std] | |
| Imprint (place/publisher/date) | **דבר־דפוס** / **פרטי הוצאה** [std] | |
| Imprint (publisher's brand) | **חותם הוצאה** [var] | Less common; often left in English |
| Colophon | **קולופון** [std, transliterated], also **סיומת** [var] | |
| Approbation | **הסכמה** [std] | English bibliography typically borrows the Hebrew word untranslated (*haskama*) |
| Errata | **לוח הטעות** [std, Hebraica], **רשימת תיקונים** [std, modern] | לוח הטעות appears in early-modern Hebrew imprints themselves (attested in BHB note 000146263 quoting the 1594 Salonika di Medina title page). *Attribution to Friedberg/Vinograd specifically needs verification — see TODO below.* |
| Marginalia / annotations | **הגהות** [std], **רשימות בשוליים** / **הערות שוליים** [std] | הגהות specifically for scholarly/corrective marginal notes |
| Provenance marks | **רישומי בעלות** [std], **חתימת בעלים** [std] | |
| Binding | **כריכה** [std] | |
| Chronogram (dating) | **כרונוגרמה** [std, transliterated], **מנין אותיות** [periphr.] | The BHB extracts these as MARC field 912 |

### A note on הוצאה / מהדורה / הדפסה

Three Hebrew words that overlap with English *edition / issue / impression* but do not map cleanly:

- **מהדורה** — primarily the Bowers **edition** (new setting of type, new text revision). "מהדורה שניה מתוקנת."
- **הוצאה** — ambiguous: covers both **edition** (older usage: הוצאה ראשונה = first edition) *and* **issue** (in the modern publishing sense: re-issue with new title page). The BHB notes use both senses without disambiguation. *Claim that Friedberg's* Bet Eked Sefarim *uses הוצאה as its default unit-of-counting is unverified in this analysis — see TODO below.*
- **הדפסה** — specifically the act/event of printing → Bowers **impression**. "הדפסה שלישית" = third impression. Used distinctively when the cataloguer wants to mark that *no* new setting was involved, only a new press run.

In practice the BHB free-text notes use all three loosely, and the analytical distinction has to be reconstructed from context (as §7 illustrates).

### TODO: claims to verify against primary sources

The Hebrew-terminology appendix above mixes two kinds of statements: (a) usage **directly attested in the mbimarc-bhb.tsv** in this repo (reliable — grepped from the data), and (b) **general claims about scholarly usage** in Friedberg, Vinograd, Yaari, Habermann, and modern NLI cataloguing practice (less reliable — drawn from general knowledge, not verified in this analysis). The latter should be checked before being relied on in publications. Specifically:

- Whether **Friedberg's *Bet Eked Sefarim*** systematically uses **הוצאה** as its unit-of-counting (vs. מהדורה, הדפסה). → Check the introduction and entry headings, e.g. via the HebrewBooks.org scans.
- Whether **Vinograd's *Thesaurus of the Hebrew Book*** distinguishes הוצאה / מהדורה / הדפסה consistently. → Check the introductory matter and column headers.
- **[Partially resolved from §9.5]**: BHB 250 statements split clearly by period. In-scope (≤ 1800) records use **`נדפס שנית`** ("printed-a-second-time") as the dominant phrasing; full-corpus (mostly 19th–20th c.) records use **`מהדורה שניה`**. This is direct in-data evidence that the Hebrew lexicon for "second edition" shifted from a verbal formula (early-modern) to a nominal one (modern). Still worth checking against Vinograd and Friedberg directly to confirm whose vocabulary tracks which period.
- Whether **טופס** vs **עותק** has a real diachronic pattern (older Hebraica → modern library) or whether the two have always coexisted. → Compare Friedberg/Vinograd (early-to-mid 20th c.) with current NLI cataloguing guidelines.
- Whether **לוח הטעות** is specifically Friedberg/Vinograd's preferred label or simply the standard Hebrew rendering of early-modern title-page formulae. The phrase appears on the books themselves (attested in BHB note 000146263 for Salonika 1594).
- Whether the term **הופעה** for "issue" has any actual currency in Hebrew bibliography or is only a calque proposed in library-science contexts.
- Whether modern NLI cataloguing guidelines codify a preference for **מהדורה** over **הוצאה** (a written rule, vs. observed usage).

Useful sources for verification: HebrewBooks.org (Friedberg full text), NLI online catalogue and cataloguing manuals, the introductions to Vinograd's *Thesaurus* (Jerusalem 1993–95), Habermann's bibliographic essays, and Y.S. Spiegel's *Amudim be-Toldot ha-Sefer ha-Ivri* for terminology discussion.

## Appendix: on כותר vs. imprint

The Hebrew **כותר** maps to **title** (MARC 245) — the name of the work as it appears on the title page (main, subtitle, parallel, alternative). It is *not* the same as **imprint**, which is the publication statement (place, publisher, date) at the foot of the title page, recorded in MARC **260 / 264**.

Two sources of confusion:

1. **Colloquial drift of כותר.** In everyday Hebrew, "כותר" is often used loosely to mean "a bibliographic item" or "a book" as a whole ("the library holds 50,000 כותרים"). That stretches it toward the English sense of *title* as "a work / an edition," but it never makes it mean *imprint*.
2. **Second meaning of *imprint* in English.** *Imprint* also denotes a **publisher's brand or sub-line** — e.g., Vintage is an imprint of Penguin Random House. This is publisher identity, not title, and again has nothing to do with כותר.

Clean mapping:

- **כותר → title** (MARC 245) — what the book is called.
- **imprint → דבר-דפוס / פרטי הוצאה** (MARC 260/264) — where, by whom, and when it was published; or, in the branding sense, a publisher's sub-label.
