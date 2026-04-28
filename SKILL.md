---
name: pdf-paper-translator
description: Translate academic papers from PDF, URL, or extracted Markdown to Chinese for sea ice, polar remote sensing, SAR/passive microwave/optical retrieval, and deep-learning methods while preserving formulas, structure, and scientific notation in Markdown-first outputs.
---

# PDF Paper Translator

Translate sea-ice, polar remote-sensing, and deep-learning academic papers into Chinese.

This skill is **Markdown-first**:
- it can start from a PDF, URL, or an already extracted Markdown file
- it extracts or normalizes the source into Markdown
- it protects math before translation
- it translates only reader-facing prose
- it reviews terminology and style before delivery

This skill **does not** convert PDF content into LaTeX and **does not** compile a translated PDF. The working source and final translation should both be Markdown.

## Workflow Overview
1. **Acquire Source** – Download or locate the target PDF/Markdown file.
2. **Build Source Markdown** – Extract PDF text and normalize it into `paper/${PAPER_ID}.source.md`.
3. **Build Domain Terminology** – Read `references/domain_terminology.md` and save a paper-specific terminology table.
4. **Protect Math & Translate** – Protect Markdown math, translate prose, then restore formulas.
5. **Review Translation** – Run manual formula checks, terminology checks, and `rg`-based style scans before delivery.
6. **Report** – Create a technical summary document when requested.

## Prerequisites

Required tools for PDF input:
- `poppler-utils` (`pdftotext`, `pdfinfo`)

Optional tools:
- `ocrmypdf` for scanned PDFs
- `tesseract` when OCR support is needed by `ocrmypdf`

If the user already provides a clean Markdown source, no extra runtime tools are required.

Installation examples:
```bash
# macOS
brew install poppler tesseract ocrmypdf

# Ubuntu/Debian
sudo apt-get install poppler-utils tesseract-ocr ocrmypdf
```

If these tools are missing, ask the user:
> “For this Markdown-first PDF translation workflow, I need poppler-utils, and optionally ocrmypdf for scanned PDFs. Which ones should I help you install?”

## Step 1: Obtain the Source File

User can provide:
- a local PDF path: `/path/to/paper.pdf`
- a PDF URL: `https://.../paper.pdf`
- an extracted Markdown file: `/path/to/paper.md`

Set `PAPER_ID` to the base filename without extension.

If a URL is given:
```bash
mkdir -p pdf_paper
curl -L -o pdf_paper/paper.pdf "$PDF_URL"
```

If a local PDF path is given:
```bash
mkdir -p pdf_paper
cp /path/to/paper.pdf pdf_paper/paper.pdf
```

If a Markdown file is given, copy it directly into:
```bash
mkdir -p paper
cp /path/to/paper.md paper/${PAPER_ID}.source.md
```

## Step 2: Build Source Markdown

If `paper/${PAPER_ID}.source.md` already exists and looks clean, use it directly.

If the source is a PDF, the goal of this step is to produce:
```bash
paper/${PAPER_ID}.source.md
```

### 2.1 Check PDF type
```bash
pdfinfo pdf_paper/paper.pdf | grep "Pages"
file pdf_paper/paper.pdf
```

If the PDF is scanned or has no selectable text:
```bash
ocrmypdf pdf_paper/paper.pdf pdf_paper/paper_ocr.pdf
# then use paper_ocr.pdf for extraction
```

### 2.2 Extract raw text from the PDF
```bash
mkdir -p paper
pdftotext -layout -nopgbrk pdf_paper/paper.pdf paper/${PAPER_ID}.source.txt
```

If OCR was used, extract from the OCRed PDF instead:
```bash
pdftotext -layout -nopgbrk pdf_paper/paper_ocr.pdf paper/${PAPER_ID}.source.txt
```

### 2.3 Normalize the raw text into Markdown

Create `paper/${PAPER_ID}.source.md` from `paper/${PAPER_ID}.source.txt`.

Normalization goals:
- preserve title, authors, affiliations, abstract, section headings, figure/table captions, and references as much as practical
- convert section headings into Markdown headings
- keep bullets and numbered lists as Markdown lists
- keep tables only when they remain readable; otherwise preserve them as aligned text blocks
- keep formulas unchanged whenever extraction permits
- repair obvious extraction errors in formulas, symbols, and percentages against the original PDF before translation

Important:
- do **not** attempt a PDF -> LaTeX conversion
- do **not** optimize for page layout fidelity
- optimize for readable, reviewable Markdown that is safe to translate

### 2.4 Sanity-check the source Markdown
```bash
sed -n '1,120p' paper/${PAPER_ID}.source.md
rg -n '^#|^##|^###' paper/${PAPER_ID}.source.md
```

If the section structure is badly damaged, repair the Markdown source first before translating.

## Step 3: Build Domain Terminology

Before translating any prose, read [references/domain_terminology.md](references/domain_terminology.md). Then build a paper-specific terminology table from the title, abstract, section headings, captions, tables, and method/results sections.

Save it as:
```bash
paper/${PAPER_ID}.terms.md
```

Recommended columns:
- `English`
- `Chinese`
- `Notes`

The terminology table must include:
- **Domain variables**: e.g. SIC, SIT, SIA, SIE, MPF, freeboard, snow depth.
- **Sea-ice process terms**: e.g. marginal ice zone, melt pond, floe, lead, polynya, stage of development.
- **Remote-sensing signal terms**: e.g. brightness temperature, backscatter, `\sigma^0`, polarization, incidence angle, speckle, land spillover, tie point.
- **Sensors/products/datasets**: e.g. Sentinel-1, AMSR2, OSI SAF, NOAA/NSIDC, Landsat-8, DMI-ASIP. Keep product and dataset names in English unless the glossary says otherwise.
- **Deep-learning/statistics terms**: e.g. U-Net, ConvNet, multi-task learning, knowledge distillation, logits, softmax, cross-entropy, KL divergence, RMSE, bias.

Rules for the paper-specific table:
- Start from `references/domain_terminology.md`; use it as the default authority.
- Add paper-specific product/model/dataset names as `(保留)`.
- If the paper or user already has a consistent convention that differs from the glossary, document the choice once and use it throughout.
- Prefer `海冰密集度（SIC）` for `sea ice concentration` in new translations. If updating an existing translation that already consistently uses `海冰浓度`, either keep consistency or migrate the whole document; do not mix both.
- Prefer `反演` for geophysical `retrieval`/`inversion`; use `检索` only for information retrieval/search contexts.
- Treat reference satellite products as `参考产品` or `参考数据`; do not call them `真值` unless they are true in situ ground truth.

Pass this terminology table into every translation task and keep it visible while editing. Use the same table during translation, polish, and review.

## Step 4: Protect Math and Translate Markdown

This step is mandatory for every Markdown deliverable. Treat every math span as immutable, including text inside math commands such as `\text{and}`, `\mathrm{if}`, `\operatorname{softmax}`, equation tags, subscripts, superscripts, and escaped symbols.

### 4.1 Validate and repair source math
Before protection, repair obvious extraction errors in source math against the PDF.

Manually check that:
- display math delimiters are balanced
- inline math delimiters are balanced
- intended percent signs inside math are written as `\%`
- no CJK text has been accidentally introduced into math spans

### 4.2 Protect all Markdown math manually

Create:
```bash
paper/${PAPER_ID}.protected.md
paper/${PAPER_ID}.math-map.md
```

Protection rules:
- copy `paper/${PAPER_ID}.source.md` to `paper/${PAPER_ID}.protected.md`
- replace every math span with a placeholder such as `@@MATH_000001@@`
- use six-digit numbering and increment it strictly in reading order
- map exactly one placeholder to exactly one math span
- record each placeholder-to-formula mapping in `paper/${PAPER_ID}.math-map.md`
- keep the original formula text byte-for-byte in the mapping
- never translate, delete, reorder, or partially edit placeholders

### 4.3 Translate only prose in the protected Markdown
- Input file: `paper/${PAPER_ID}.protected.md`
- Output file: `paper/${PAPER_ID}.protected-zh.md`
- Read `references/translation_prompt.md`
- Keep the paper-specific terminology table from **Step 3** visible
- Do **not** overwrite `paper/${PAPER_ID}.protected.md`
- Translate in **two passes**:
  1. **Faithful draft**: translate all reader-facing prose while preserving structure, placeholders, citations, URLs, and layout
  2. **Chinese polish**: rewrite the draft into natural academic Chinese without changing facts, formulas, labels, citations, or placeholders
- During the polish pass, explicitly fix:
  - awkward literal titles, highlights, and abstract sentences
  - missing or inconsistent first-mention handling for `中文（English Full Name, ABBR）`
  - mixed Chinese-English compounds such as `letter-value图`, `AI就绪`, `logit输出`
  - context-mismatched phrases such as `结果兴趣区域`, `工作空间分辨率`, `对大气条件的不变性更强`
- Preserve every placeholder exactly, e.g. `@@MATH_000001@@`
- Do not add, remove, reorder, or translate placeholders
- Keep Markdown headings, tables, citations, URLs, and code blocks structurally intact

Save the translated protected file as:
```bash
paper/${PAPER_ID}.protected-zh.md
```

### 4.4 Restore formulas and validate
Restore formulas in `paper/${PAPER_ID}.protected-zh.md` using `paper/${PAPER_ID}.math-map.md`, then save the final file as:
```bash
paper/${PAPER_ID}-翻译.md
```

Then validate manually:
```bash
rg -n "@@MATH_" paper/${PAPER_ID}-翻译.md
rg -n "全球气候引擎|补充性高分辨率来源|工作空间分辨率|对大气条件的不变性更强|AI就绪|结果兴趣区域|letter-value图|原始logit输出|重分配为0%|快速发射" paper/${PAPER_ID}-翻译.md
```

Also compare the source and translated Markdown side by side to ensure:
- all math spans were restored
- placeholder numbering in `paper/${PAPER_ID}.math-map.md` is complete and unique
- formulas are unchanged
- `%` inside math remains `\%`
- no CJK text appears inside math

If validation fails, fix the source or protected translation and rerun restore + checks. Do not rewrite formulas from memory. If a placeholder is missing, duplicated, or restored out of order, return to `paper/${PAPER_ID}.protected.md` and redo that translation segment instead of patching the final Markdown by hand.

## Step 5: Final Review and Sign-Off

Review the translated Markdown following [references/review_checklist.md](references/review_checklist.md). This step is mandatory and should end with a clear delivery decision, not just a quick scan.

Create:
```bash
paper/${PAPER_ID}.review-notes.md
```

Track every issue in a compact table or bullet list with:
- `ID`
- `Severity`: `stop-ship`, `major`, or `minor`
- `Location`
- `Problem`
- `Fix`
- `Status`

### 5.1 Run four review passes
1. **Structure pass**: confirm formulas, placeholders, headings, lists, tables, citations, URLs, and caption structure are intact.
2. **Source-fidelity pass**: compare source and translation side by side and verify that claims, numbers, comparisons, negations, limitations, and formula-adjacent prose still mean the same thing.
3. **Terminology pass**: check against `paper/${PAPER_ID}.terms.md` and [references/domain_terminology.md](references/domain_terminology.md), including first mention handling and acronym expansion.
4. **Chinese polish pass**: read the Chinese on its own and smooth literal phrasing, repetition, inconsistent register, and awkward sentence rhythm without changing technical meaning.

### 5.2 Mandatory spot-check coverage
The final review must explicitly cover:
- title, abstract, highlights, keywords, and conclusion
- every section and subsection heading
- every figure and table caption
- at least one formula-adjacent paragraph in each major section
- every sentence containing percentages, thresholds, inequalities, uncertainty, significance, comparisons, or negation
- dataset names, sensor/product names, and method names
- limitation statements, error analysis, and future-work claims

### 5.3 Minimum review commands
```bash
rg -n "@@MATH_" paper/${PAPER_ID}-翻译.md
rg -n "全球气候引擎|补充性高分辨率来源|工作空间分辨率|对大气条件的不变性更强|AI就绪|结果兴趣区域|letter-value图|原始logit输出|重分配为0%|快速发射" paper/${PAPER_ID}-翻译.md
rg -n '[0-9]+([.][0-9]+)?%|[<>]=?|±' paper/${PAPER_ID}.source.md paper/${PAPER_ID}-翻译.md
```

### 5.4 Stop-ship issues
Do **not** deliver the translation if any unresolved issue remains in these categories:
- a number, percentage, threshold, or comparison changed meaning
- a negation, limitation, uncertainty cue, or causal relation was weakened, strengthened, or flipped
- a formula-adjacent sentence no longer matches the formula or variable definition
- `sea ice concentration`, `sea ice area`, `sea ice extent`, `retrieval`, `brightness temperature`, `backscatter`, or other high-risk domain terms drifted from the glossary
- a figure/table caption, result statement, or conclusion contradicts the source
- any part of the document still shows extraction corruption that changes reader understanding

Before delivery, confirm:
- [ ] All review passes completed
- [ ] Review notes updated with every issue and its resolution
- [ ] All stop-ship issues resolved
- [ ] Translation quality verified
- [ ] No math placeholders remain

## Step 6: Generate Technical Report

If the user separately requests a technical summary, follow [references/summary_prompt.md](references/summary_prompt.md) and create a technical report using [assets/report_template.md](assets/report_template.md). By default, generate the report in the current context. Only split the work into separate tasks when the user explicitly asks for parallel work.

Save report:
```bash
pdf_paper/technical_report.md
```

## Final Deliverables

The only final deliverable is:

1. **Translated Markdown**: `paper/${PAPER_ID}-翻译.md`

Working files used during translation and review may include:
- `paper/${PAPER_ID}.source.md`
- `paper/${PAPER_ID}.terms.md`
- `paper/${PAPER_ID}.review-notes.md`
- protected Markdown files
- manual math mapping files
- `pdf_paper/technical_report.md` only when the user separately asks for a report

## Common Issues & Solutions

| Issue | Solution |
| --- | --- |
| PDF is scanned or has no selectable text | Run `ocrmypdf` first, then extract with `pdftotext`. |
| `pdftotext` produces broken section structure | Repair headings, captions, and lists manually in `paper/${PAPER_ID}.source.md` before translation. |
| Tables are unreadable after extraction | Preserve them as aligned text blocks or summarize them faithfully in Markdown; do not force LaTeX reconstruction. |
| Math formulas are broken during extraction | Repair them against the original PDF before creating placeholders. |
| Math formulas changed after translation | Do not deliver. Restore from `paper/${PAPER_ID}.math-map.md`, then compare the source and translated Markdown again. |
| A placeholder is lost, duplicated, or restored in the wrong position | Go back to `paper/${PAPER_ID}.protected.md`, repair that segment, and restore again. Do not hand-edit formulas in the final Markdown. |
| Translation sounds literal or contains mixed Chinese-English compounds | Run the `rg` style scan from Step 5, rewrite flagged phrases, and check again. |
| The translation seems fluent but a claim may have shifted meaning | Log it as `stop-ship` in `paper/${PAPER_ID}.review-notes.md`, compare source and translation sentence by sentence, and resolve it before delivery. |
| Unescaped percent in Markdown math | Replace `%` with `\%` before protecting, e.g. `$SIC > 0\%$`. |
| Figures are needed for a report but not preserved in Markdown | Extract them separately from the PDF and reference them in the report as images. |
| Reference section is noisy after extraction | Keep it if the user wants a full translation; otherwise note any extraction quality limits explicitly. |

## References

- **Domain terminology**: [references/domain_terminology.md](references/domain_terminology.md)
- **Translation prompt**: [references/translation_prompt.md](references/translation_prompt.md)
- **Review checklist**: [references/review_checklist.md](references/review_checklist.md)
- **Report template**: [assets/report_template.md](assets/report_template.md)
