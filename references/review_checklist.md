# Translation Review Checklist

## 1. File Completeness

- Verify the Markdown-first deliverables exist:
```bash
test -f paper/${PAPER_ID}.source.md
test -f paper/${PAPER_ID}.terms.md
test -f paper/${PAPER_ID}.protected.md
test -f paper/${PAPER_ID}.math-map.md
test -f paper/${PAPER_ID}.protected-zh.md
test -f paper/${PAPER_ID}-翻译.md
```

If the input was a PDF, verify the Markdown source was built from `pdftotext`/OCR extraction and not from a PDF-to-LaTeX conversion.

## 2. Markdown Formula Integrity

For every Markdown deliverable, run these searches before delivery:

```bash
rg -n "@@MATH_" paper/${PAPER_ID}-翻译.md
rg -n "全球气候引擎|补充性高分辨率来源|工作空间分辨率|对大气条件的不变性更强|AI就绪|结果兴趣区域|letter-value图|原始logit输出|重分配为0%|快速发射" paper/${PAPER_ID}-翻译.md
```

Verify:

- [ ] No `@@MATH_000001@@` placeholders remain
- [ ] Placeholder numbering in `paper/${PAPER_ID}.math-map.md` is complete, unique, and ordered
- [ ] Math span count and content are identical to the pre-translation source Markdown
- [ ] No CJK characters were introduced inside math
- [ ] Percent signs inside math are escaped as `\%`
- [ ] Display math delimiters (`$$...$$`, `\[...\]`) and inline math delimiters are balanced
- [ ] No sample-derived translationese phrases or mixed Chinese-English compounds remain

Before delivery, compare `source.md`, `protected.md`, `protected-zh.md`, and `-翻译.md` side by side for at least the title, one formula-heavy paragraph, one caption, and the conclusion.

If any check fails, do not deliver the Markdown. Restore formulas from the manual mapping file or repair against the original source/PDF and rerun checks.

## 3. Optional LaTeX Command Spelling

Only run this section when the user provided source `.tex` files. It is not part of the default PDF workflow.

Detect misspelled commands introduced during translation (e.g. `\footnotetext` → `\footnotext`):

```bash
diff <(cd paper_source && grep -ohrIE '\\[a-zA-Z]+' | sort -u) \
     <(cd paper_cn && grep -ohrIE '\\[a-zA-Z]+' | sort -u) \
     | grep '^>'
```

Right-side-only commands are suspicious. Verify each one — if not intentionally added (e.g. `\figurename`, `\setCJKmainfont`), it's likely a typo.

## 4. Optional CJK Catcode Issue

Only run this section when the user provided source `.tex` files.

Find custom macros directly followed by CJK characters (missing `{}`):

```bash
grep -rnE '\\[a-zA-Z]+[一-龥]' paper_cn/ --include='*.tex'
```

Each match needs `{}` inserted between macro and CJK text. Background: `xeCJK` sets CJK characters to catcode 11 (letter), so `\xmax概率` is parsed as one undefined command `\xmax概率` instead of `\xmax` + `概率`.

## 5. Terminology Consistency Check

For each translated Markdown file, verify:

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

For each translated file, verify:
- [ ] Chinese expression is natural and fluent (avoiding direct translation artifacts)
- [ ] Academic language style is maintained throughout
- [ ] Sentence structures follow Chinese expression patterns
- [ ] Key verbs translated appropriately
- [ ] No colloquial expressions or overly casual language
- [ ] Technical descriptions are precise and professional
- [ ] Title, highlights, abstract, captions, and conclusion have been polished beyond a literal first draft
- [ ] No mixed Chinese-English compounds such as `letter-value图`, `AI就绪`, or `logit输出`
- [ ] No sample-derived bad phrases such as `结果兴趣区域` or `工作空间分辨率`

## 7. Content Spot-Check

For each translated Markdown file, compare with source to verify:

- [ ] Paper title translated
- [ ] Footnotes and author notes translated where appropriate
- [ ] All section/subsection titles translated
- [ ] Figure and table captions translated
- [ ] Math formulas unchanged
- [ ] Text inside math commands unchanged (for example `\text{and}` is not translated)
- [ ] URLs, citations, figure references, and dataset names unchanged where they should be preserved

## 8. Optional Template Hard-coded Labels

Only run this section when the user provided source `.tex`, `.sty`, or `.cls` files.

Check .sty/.cls files in `paper_cn/` for visible English strings that should be localized:

```bash
grep -rnE '(Equal contribution|Correspondence to|Under review|Preprint|Proceedings of)' paper_cn/ --include='*.sty' --include='*.cls' --include='*.tex'
```

- [ ] Conference/journal template labels translated or overridden (e.g. `Equal contribution` → `同等贡献`)
- [ ] Author affiliation/institution names handled (keep original or add Chinese translation)
