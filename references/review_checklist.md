# Translation Review Checklist

## 1. File Completeness

- Verify all .tex files are translated or copied (skip files that are not translated)
```bash
diff <(cd paper_source && find . -name "*.tex" -type f | sort) \
     <(cd paper_cn && find . -name "*.tex" -type f | sort)
```
- Verify all non-text files copied correctly
```bash
diff <(cd paper_source && find . -type f -not -name "*.tex" | sort) \
     <(cd paper_cn && find . -type f -not -name "*.tex" | sort)
```

## 2. Markdown Formula Integrity

For every Markdown deliverable, run the formula guard before delivery:

```bash
python3 scripts/protect_math.py check paper/source-翻译.md --strict-cjk
python3 scripts/protect_math.py compare paper/source.md paper/source-翻译.md
```

Verify:

- [ ] No `@@MATH_000001@@` placeholders remain
- [ ] Math span count and content are identical to the pre-translation source Markdown
- [ ] No CJK characters were introduced inside math
- [ ] Percent signs inside math are escaped as `\%`
- [ ] Display math delimiters (`$$...$$`, `\[...\]`) and inline math delimiters are balanced

If any check fails, do not deliver the Markdown. Restore formulas from the manifest or repair against the original source/PDF and rerun checks.

## 3. LaTeX Command Spelling

Detect misspelled commands introduced during translation (e.g. `\footnotetext` → `\footnotext`):

```bash
diff <(cd paper_source && grep -ohrIE '\\[a-zA-Z]+' | sort -u) \
     <(cd paper_cn && grep -ohrIE '\\[a-zA-Z]+' | sort -u) \
     | grep '^>'
```

Right-side-only commands are suspicious. Verify each one — if not intentionally added (e.g. `\figurename`, `\setCJKmainfont`), it's likely a typo.

## 4. CJK Catcode Issue

Find custom macros directly followed by CJK characters (missing `{}`):

```bash
grep -rnE '\\[a-zA-Z]+[一-龥]' paper_cn/ --include='*.tex'
```

Each match needs `{}` inserted between macro and CJK text. Background: `xeCJK` sets CJK characters to catcode 11 (letter), so `\xmax概率` is parsed as one undefined command `\xmax概率` instead of `\xmax` + `概率`.

## 5. Terminology Consistency Check

For each .tex file, verify:

- [ ] Key terms translated consistently across all files
- [ ] First mention of key terms includes both English and Chinese
- [ ] Technical terms follow the paper-specific terminology table and [domain_terminology.md](domain_terminology.md)
- [ ] Proper nouns (Agent Swarm, PARL, MoonViT-3D) handled correctly
- [ ] Acronyms first appear with full name + acronym (e.g., "强化学习 (Reinforcement Learning, RL)")

For sea-ice, remote-sensing, and deep-learning papers, explicitly verify:

- [ ] `sea ice concentration (SIC)` is translated consistently, preferably as `海冰密集度（SIC）` for new translations
- [ ] `sea ice area (SIA)` and `sea ice extent (SIE)` are not confused
- [ ] `retrieval` / `inversion` are translated as `反演` in geophysical-variable contexts
- [ ] `brightness temperature` is translated as `亮温`
- [ ] `backscatter`, `\sigma^0`, `polarization`, `incidence angle`, `speckle`, and `thermal noise` use SAR/remote-sensing terminology
- [ ] `marginal ice zone`, `melt pond`, `floe`, `lead`, `polynya`, and `stage of development` use sea-ice terminology
- [ ] Sensor, mission, product, dataset, and model names remain stable: Sentinel-1, AMSR2, OSI SAF, NOAA/NSIDC, DMI-ASIP, U-Net, etc.
- [ ] Reference products/datasets are not called `真值` unless the source is true in situ ground truth
- [ ] Deep-learning terms such as `multi-task learning`, `knowledge distillation`, `logits`, `softmax`, `cross-entropy`, and `KL divergence` are translated consistently

## 6. Translation Quality Check

For each .tex file, verify:

- [ ] Chinese expression is natural and fluent (avoiding direct translation artifacts)
- [ ] Academic language style is maintained throughout
- [ ] Sentence structures follow Chinese expression patterns
- [ ] Key verbs translated appropriately
- [ ] No colloquial expressions or overly casual language
- [ ] Technical descriptions are precise and professional

## 7. Content Spot-Check

For each .tex file, compare with source to verify:

- [ ] Paper title (`\title{...}` / `\icmltitle{...}`) translated
- [ ] `\thanks{...}`, `\footnote{...}`, `\footnotetext{...}` content translated
- [ ] All section/subsection titles translated
- [ ] Figure and table captions translated
- [ ] LaTeX commands and math formulas unchanged
- [ ] Text inside math commands unchanged (for example `\text{and}` is not translated)
- [ ] File paths (`\input`, `\includegraphics`) unchanged
- [ ] Labels and references (`\label`, `\ref`, `\cite`) unchanged

## 8. Template Hard-coded Labels

Check .sty/.cls files in `paper_cn/` for visible English strings that should be localized:

```bash
grep -rnE '(Equal contribution|Correspondence to|Under review|Preprint|Proceedings of)' paper_cn/ --include='*.sty' --include='*.cls' --include='*.tex'
```

- [ ] Conference/journal template labels translated or overridden (e.g. `Equal contribution` → `同等贡献`)
- [ ] Author affiliation/institution names handled (keep original or add Chinese translation)
