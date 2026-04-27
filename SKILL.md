---
name: pdf-paper-translator
description: Translate academic papers from PDF, URL, or extracted Markdown to Chinese for sea ice, polar remote sensing, SAR/passive microwave/optical retrieval, and deep-learning methods while preserving formulas, layout, figures, and scientific notation. Use when users need domain-accurate Chinese paper translation, formula-safe Markdown output, a bilingual/translated PDF, or a technical report.
---

# PDF Paper Translator

Translate sea-ice, polar remote-sensing, and deep-learning academic papers into Chinese. The skill can work from a PDF/URL or from an already extracted Markdown file. It extracts or converts the source while preserving structure, formulas, figures, and basic formatting, translates only reader-facing prose, applies a domain terminology glossary, and can produce formula-safe Markdown, translated LaTeX/PDF, and/or a technical report.

## Workflow Overview
1. **Acquire Source** – Download/locate the target PDF or Markdown file.
2. **Extract & Convert** – Convert PDF content into LaTeX or Markdown while preserving formulas.
3. **Build Domain Terminology** – Read `references/domain_terminology.md` and create a paper-specific terminology table.
4. **Protect Math** – For Markdown deliverables, protect math with `scripts/protect_math.py` before translation.
5. **Translate** – Translate English narrative content to Chinese; never translate math.
6. **REVIEW PHASE** – **MUST COMPLETE** before compiling or delivering Markdown.
7. **CJK Support & Localize Labels** – Add xeCJK, localize labels when producing LaTeX/PDF.
8. **Compile .tex Files** – Generate translated PDF using XeLaTeX when requested.
9. **Report** – Create technical summary document when requested.

## Prerequisites

Check local xelatex installation:
```bash
xelatex --version
```
If not installed, make sure Docker is installed and available.
```bash
docker --version
```
**Additional required tools** (for PDF → LaTeX conversion):
- `pandoc` (universal document converter)
- `poppler-utils` (provides `pdftotext`, `pdfinfo`)
- Optional: `ocrmypdf` (if the PDF is scanned, requires OCR)
Optionally `tesseract` for OCR.
- Python 3 standard library is enough for formula protection (`scripts/protect_math.py`).

Installation examples:
```bash
# macOS
brew install pandoc poppler tesseract ocrmypdf

# Ubuntu/Debian
sudo apt-get install pandoc poppler-utils tesseract-ocr ocrmypdf
```

**If any of these tools or XeLaTeX/Docker is missing, ask the user:**
> “The following tools are required for PDF translation: pandoc, poppler-utils, and either XeLaTeX or Docker. Which ones should I help you install?”

## Step 1: Obtain the Source File

User can provide:
- A local path: `/path/to/paper.pdf`
- A URL: `https://.../paper.pdf`
- An extracted Markdown file: `/path/to/paper.md`

If a Markdown file is provided or the user asks for Markdown output, keep a pre-translation source Markdown file and use **Step 4A**.

If a URL is given, download it:
```bash
PDF_URL="https://example.com/paper.pdf"
mkdir -p pdf_paper
curl -L -o pdf_paper/paper.pdf "$PDF_URL"
```
If a local path is provided, copy it into the working directory:
```bash
cp /path/to/paper.pdf pdf_paper/paper.pdf
```
Set a working variable `PAPER_ID` (e.g., `paper_basename` without .pdf) for later use.

## Step 2: Convert PDF to LaTeX Source

This step produces a single `.tex` file (or a small set of files) that faithfully represents the paper's structure, text, math, and basic formatting. If the requested deliverable is Markdown, also keep a Markdown source file and run the formula guard in **Step 4A** before translation.

### 2.1 Check PDF type
```bash
pdfinfo pdf_paper/paper.pdf | grep "Pages"
file pdf_paper/paper.pdf
```
If the PDF is scanned (no selectable text), perform OCR first:
```bash
ocrmypdf pdf_paper/paper.pdf pdf_paper/paper_ocr.pdf
# then use paper_ocr.pdf for conversion
```

### 2.2 Convert to LaTeX using pandoc
```bash
mkdir -p pdf_paper/latex_source
pandoc pdf_paper/paper.pdf -o pdf_paper/latex_source/main.tex \
  --pdf-engine-opt=-shell-escape \
  --wrap=preserve \
  --extract-media=pdf_paper/media
```
> **Note:** `pandoc` can extract embedded images into `media/` and reference them in the generated `.tex`. It also converts math (if present) into LaTeX math mode.

If the PDF contains complex multi‑column layouts or tables that are poorly converted, consider using `pdftotext -layout` as a fallback, then manually wrap content into a basic LaTeX article. However, `pandoc` works well for most academic PDFs.

### 2.3 Verify the generated LaTeX file
```bash
head -50 pdf_paper/latex_source/main.tex
```
Check that the document class, title, sections, and abstract are present. If important parts (e.g., references, figures) are missing, you may need to fall back to a simpler `pdftotext` + manual LaTeX structuring (see **Common Issues**).

## Step 3: Build Domain Terminology

Before translating any prose, read [references/domain_terminology.md](references/domain_terminology.md). Then build a paper-specific terminology table from the title, abstract, section headings, captions, tables, and method/results sections.

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

Pass this terminology table into every translation task. When translating in one context without subagents, keep the table visible while editing.

## Step 4: Translate

Choose one path:
- **Step 4A** for Markdown output or Markdown input.
- **Step 4B** for LaTeX/PDF output.

### Step 4A: Translate Markdown with Formula Guard

This path is mandatory whenever the final deliverable is `.md`. Treat every math span as immutable, including text inside math commands such as `\text{and}`, `\mathrm{if}`, `\operatorname{softmax}`, equation tags, subscripts, superscripts, and escaped symbols.

Step 4A.1. **Prepare a pre-translation source Markdown file**:
```bash
mkdir -p paper
# Example source path:
# paper/${PAPER_ID}.source.md
```

Before translation, repair obvious converter errors in source math (for example `0%` inside math should be `0\%`) by checking:
```bash
python3 scripts/protect_math.py check paper/${PAPER_ID}.source.md --strict-cjk
```

Step 4A.2. **Protect all Markdown math before translation**:
```bash
python3 scripts/protect_math.py protect \
  paper/${PAPER_ID}.source.md \
  --output paper/${PAPER_ID}.protected.md \
  --manifest paper/${PAPER_ID}.math.json
```

Step 4A.3. **Translate only prose in the protected Markdown**:
- Read `paper/${PAPER_ID}.protected.md`.
- Translate English narrative text into Chinese.
- Apply the paper-specific terminology table from **Step 3**.
- Preserve every placeholder exactly, e.g. `@@MATH_000001@@`.
- Do not add, remove, reorder, or translate placeholders.
- Keep Markdown headings, tables, figure references, citations, URLs, and code blocks structurally intact.

Save the translated protected file as:
```bash
paper/${PAPER_ID}.protected-zh.md
```

Step 4A.4. **Restore formulas and validate**:
```bash
python3 scripts/protect_math.py restore \
  paper/${PAPER_ID}.protected-zh.md \
  --manifest paper/${PAPER_ID}.math.json \
  --output paper/${PAPER_ID}-翻译.md

python3 scripts/protect_math.py check paper/${PAPER_ID}-翻译.md --strict-cjk
python3 scripts/protect_math.py compare paper/${PAPER_ID}.source.md paper/${PAPER_ID}-翻译.md
```

If validation fails, fix the source/protected translation and rerun restore + checks. Do not manually rewrite formulas from memory; compare with the source Markdown or original PDF.

### Step 4B: Translate LaTeX Files

Now follow **exactly the same translation procedure** as the original arXiv skill, but applied to `pdf_paper/latex_source/main.tex` (and any other `.tex` files created).

**IMPORTANT**: Before translating, read [references/translation_guidelines.md](references/translation_guidelines.md) and [references/domain_terminology.md](references/domain_terminology.md).

### Translation Workflow

Step 4B.1. **Copy all LaTeX files** from `pdf_paper/latex_source/` to `pdf_paper/latex_cn/`:
```bash
cd pdf_paper
mkdir -p latex_cn
cp -r latex_source/* latex_cn/
```

Step 4B.2. **Gather Context (MANDATORY)**:
Before ANY translation, extract:
1. **Paper Title**: From `\title{...}` in `latex_cn/main.tex`
2. **Abstract**: From `\begin{abstract}...\end{abstract}`
3. **Paper Structure**: List all sections (use `grep "\\section" main.tex`)
4. **Key Terminologies**: Build the terminology table from **Step 3** and include paper-specific terms

Step 4B.3. **Dispatch Translation Tasks** – usually only one main `.tex` file, but if the conversion produced multiple files, handle them similarly. Translate `main.tex` (or the main document) first.

**Each translation Task**:
- Task type: general-purpose subagent (or use the same LLM context)
- Input: File path in `latex_cn/`
- Action: Read file → Translate → Edit file (update content in place)
- Must follow [references/translation_prompt.md](references/translation_prompt.md)
- Math content is immutable. Do not translate inside `$...$`, `\[...\]`, `equation`, `align`, table math cells, or math commands such as `\text{and}`.

## Step 5: Review Translation

After translation, review the content following [references/review_checklist.md](references/review_checklist.md), paying special attention to:
- Domain terminology consistency against [references/domain_terminology.md](references/domain_terminology.md)
- Preserved math mode (`$...$`, `\[...\]`)
- For Markdown output: run `scripts/protect_math.py check --strict-cjk` and `scripts/protect_math.py compare`
- Correct handling of `\ref`, `\cite` (may not work if the original PDF's bibliography was not fully extracted)
- No broken LaTeX commands (e.g., `\footnotext` vs `\footnote`)
- CJK catcode issues (rare, but check if custom macros like `\xmax概率` appear)

Perform fixes as needed.

**CRITICAL**: Before proceeding to Step 6, confirm:
- [ ] All review checks completed
- [ ] Any issues identified and fixed
- [ ] Translation quality verified

## Step 6: Add Chinese Support

Modify `latex_cn/main.tex` to include `xeCJK` and set CJK fonts following [references/chinese_support.md](references/chinese_support.md).

Example for Fandol fonts (included in TeX Live Docker image):
```latex
\usepackage{xeCJK}
\setCJKmainfont{FandolSong}[ItalicFont=FandolKai]
\setCJKsansfont{FandolHei}
\setCJKmonofont{FandolFang}
```

If running locally, ask user for font preference.

## Step 7: Compile Translated PDF

### Option 1: Local XeLaTeX
```bash
cd pdf_paper/latex_cn
xelatex main.tex
# If bibliography present:
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```
Or use `latexmk -xelatex main.tex`.

### Option 2: Docker with TeX Live
```bash
cd /path/to/pdf_paper
docker run --rm \
  -v "$(pwd)/latex_cn":/workspace \
  -w /workspace \
  ghcr.1ms.run/xu-cheng/texlive-debian:20260101 \
  latexmk -xelatex main.tex
```

The output PDF will be `latex_cn/main.pdf`.

## Step 8: Generate Technical Report

If user requests a technical summary, spawn a subagent following [references/summary_prompt.md](references/summary_prompt.md) to create a technical report using [assets/report_template.md](assets/report_template.md).

Save report: `pdf_paper/technical_report.md`

## Final Deliverables

1. **Translated Markdown** (if requested): `paper/${PAPER_ID}-翻译.md`
2. **Translated PDF** (if requested): `latex_cn/main.pdf`
3. **Technical report** (if requested): `pdf_paper/technical_report.md`
4. **Intermediate sources**: protected Markdown manifest and/or `latex_cn/` directory

## Common Issues & Solutions

| Issue                                             | Solution                                                     |
| ------------------------------------------------- | ------------------------------------------------------------ |
| `pandoc` cannot convert the PDF (complex layout)  | Fallback to `pdftotext -layout paper.pdf` then manually wrap text in a basic LaTeX article. Use `\section{}`, `\subsection{}` based on detected headers. |
| Missing figures / images                          | Extract images manually: `pdfimages paper.pdf images/`. Reference them in the LaTeX source using `\includegraphics{images/image-000.png}`. |
| Math formulas broken after conversion             | Restore them using the original PDF as reference before translation. For Markdown, run `python3 scripts/protect_math.py check source.md --strict-cjk`, fix source math, then protect it. |
| Math formulas changed after Markdown translation  | Do not deliver. Restore with `scripts/protect_math.py restore`, then run `check --strict-cjk` and `compare source.md translated.md`. If `compare` fails, placeholders were altered or formulas were edited. |
| Unescaped percent in Markdown math                | Change intended percent signs inside math from `%` to `\%` before protecting, e.g. `$SIC > 0\%$`. |
| Bibliography not present in converted LaTeX       | Either ignore it (the PDF will lack citations) or manually copy the references from the PDF. Advise user that the reference section may be incomplete. |
| Scanned PDF with no selectable text               | First run `ocrmypdf paper.pdf paper_ocr.pdf`, then convert the OCRed PDF. |
| `Undefined control sequence` from custom commands | The original PDF may have used custom LaTeX macros. Add `\newcommand{\customMacro}[1]{#1}` near the top of `main.tex` to suppress errors. |
| xeCJK catcode issue (e.g., `\xmax概率`)           | Insert `{}` to separate macro from CJK: `\xmax{}概率`.       |
| Wrong font for CJK characters                     | Ask user to install a system CJK font or use the Fandol fonts provided by TeX Live. |

## References

- **Translation rules**: [references/translation_guidelines.md](references/translation_guidelines.md)
- **Domain terminology**: [references/domain_terminology.md](references/domain_terminology.md)
- **Translation prompt**: [references/translation_prompt.md](references/translation_prompt.md)
- **Review checklist**: [references/review_checklist.md](references/review_checklist.md)
- **Chinese support**: [references/chinese_support.md](references/chinese_support.md)
- **Report template**: [assets/report_template.md](assets/report_template.md)
