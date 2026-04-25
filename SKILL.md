- 以下是针对 **PDF 论文翻译** 改造后的 `SKILL.md` 文档。它保留了原技能的核心工作流（获取源文件 → 转换 / 提取 → 翻译 → 审核 → 支持中文 → 编译 PDF → 输出报告）

  ```markdown
  ---
  name: pdf-paper-translator
  description: Translate academic papers from PDF to Chinese. Use when users want to translate a PDF paper (provided as file or URL) from English to Chinese, while preserving layout and generating a bilingual or fully translated PDF.
  license: MIT
  ---
  
  # PDF Paper Translator
  
  Translate any academic paper in PDF format into Chinese. The skill extracts content from the PDF, converts it into a LaTeX source (preserving structure, formulas, and basic formatting), translates the English narrative into Chinese, and finally compiles a new PDF with Chinese text. A technical report summarizing the paper can also be generated.
  
  ## Workflow Overview
  1. **Acquire PDF** – Download or locate the target PDF file.
  2. **Extract & Convert** – Convert PDF content (text, formulas, sections) into a LaTeX source.
  3. **Translate** – Translate English narrative content to Chinese following LaTeX‑specific rules.
  4. **REVIEW PHASE** – **MUST COMPLETE** before compiling.
  5. **CJK Support & Localize Labels** – Add xeCJK, localize labels.
  6. **Compile .tex Files** – Generate translated PDF using XeLaTeX.
  7. **Report** – Create technical summary document.
  
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

  Installation examples:
  ```bash
  # macOS
  brew install pandoc poppler tesseract ocrmypdf
  
  # Ubuntu/Debian
  sudo apt-get install pandoc poppler-utils tesseract-ocr ocrmypdf
  ```

  **If any of these tools or XeLaTeX/Docker is missing, ask the user:**
  > “The following tools are required for PDF translation: pandoc, poppler-utils, and either XeLaTeX or Docker. Which ones should I help you install?”

  ## Step 1: Obtain the PDF File

  User can provide:
  - A local path: `/path/to/paper.pdf`
  - A URL: `https://.../paper.pdf`

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

  This step produces a single `.tex` file (or a small set of files) that faithfully represents the paper’s structure, text, math, and basic formatting.

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

  ## Step 3: Translate LaTeX Files

  Now follow **exactly the same translation procedure** as the original arXiv skill, but applied to `pdf_paper/latex_source/main.tex` (and any other `.tex` files created).

  **IMPORTANT**: Before translating, read [references/translation_guidelines.md](references/translation_guidelines.md) for detailed rules.

  ### Translation Workflow

  Step 3.1. **Copy all LaTeX files** from `pdf_paper/latex_source/` to `pdf_paper/latex_cn/`:
  ```bash
  cd pdf_paper
  mkdir -p latex_cn
  cp -r latex_source/* latex_cn/
  ```

  Step 3.2. **Gather Context (MANDATORY)**:
  Before ANY translation, extract:
  1. **Paper Title**: From `\title{...}` in `latex_cn/main.tex`
  2. **Abstract**: From `\begin{abstract}...\end{abstract}`
  3. **Paper Structure**: List all sections (use `grep "\\section" main.tex`)
  4. **Key Terminologies**: Build terminology table from paper content

  Step 3.3. **Dispatch Translation Tasks** – usually only one main `.tex` file, but if the conversion produced multiple files, handle them similarly. Translate `main.tex` (or the main document) first.

  **Each translation Task**:
  - Task type: general-purpose subagent (or use the same LLM context)
  - Input: File path in `latex_cn/`
  - Action: Read file → Translate → Edit file (update content in place)
  - Must follow [references/translation_prompt.md](references/translation_prompt.md)

  ## Step 4: Review Translation

  After translation, review the content following [references/review_checklist.md](references/review_checklist.md), paying special attention to:
  - Preserved math mode (`$...$`, `\[...\]`)
  - Correct handling of `\ref`, `\cite` (may not work if the original PDF’s bibliography was not fully extracted)
  - No broken LaTeX commands (e.g., `\footnotext` vs `\footnote`)
  - CJK catcode issues (rare, but check if custom macros like `\xmax概率` appear)

  Perform fixes as needed.

  **CRITICAL**: Before proceeding to Step 5, confirm:
  - [ ] All review checks completed
  - [ ] Any issues identified and fixed
  - [ ] Translation quality verified

  ## Step 5: Add Chinese Support

  Modify `latex_cn/main.tex` to include `xeCJK` and set CJK fonts following [references/chinese_support.md](references/chinese_support.md).

  Example for Fandol fonts (included in TeX Live Docker image):
  ```latex
  \usepackage{xeCJK}
  \setCJKmainfont{FandolSong}[ItalicFont=FandolKai]
  \setCJKsansfont{FandolHei}
  \setCJKmonofont{FandolFang}
  ```

  If running locally, ask user for font preference.

  ## Step 6: Compile Translated PDF

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

  ## Step 7: Generate Technical Report

  If user requests a technical summary, spawn a subagent following [references/summary_prompt.md](references/summary_prompt.md) to create a technical report using [assets/report_template.md](assets/report_template.md).

  Save report: `pdf_paper/technical_report.md`

  ## Final Deliverables

  1. **Translated PDF**: `latex_cn/main.pdf`
  2. **Technical report** (if requested): `pdf_paper/technical_report.md`
  3. **Intermediate LaTeX source**: `latex_cn/` directory

  ## Common Issues & Solutions

  | Issue                                             | Solution                                                     |
  | ------------------------------------------------- | ------------------------------------------------------------ |
  | `pandoc` cannot convert the PDF (complex layout)  | Fallback to `pdftotext -layout paper.pdf` then manually wrap text in a basic LaTeX article. Use `\section{}`, `\subsection{}` based on detected headers. |
  | Missing figures / images                          | Extract images manually: `pdfimages paper.pdf images/`. Reference them in the LaTeX source using `\includegraphics{images/image-000.png}`. |
  | Math formulas broken after conversion             | Restore them using the original PDF as reference. Use `$...$` for inline and `\[...\]` for display math. |
  | Bibliography not present in converted LaTeX       | Either ignore it (the PDF will lack citations) or manually copy the references from the PDF. Advise user that the reference section may be incomplete. |
  | Scanned PDF with no selectable text               | First run `ocrmypdf paper.pdf paper_ocr.pdf`, then convert the OCRed PDF. |
  | `Undefined control sequence` from custom commands | The original PDF may have used custom LaTeX macros. Add `\newcommand{\customMacro}[1]{#1}` near the top of `main.tex` to suppress errors. |
  | xeCJK catcode issue (e.g., `\xmax概率`)           | Insert `{}` to separate macro from CJK: `\xmax{}概率`.       |
  | Wrong font for CJK characters                     | Ask user to install a system CJK font or use the Fandol fonts provided by TeX Live. |

  ## References

  - **Translation rules**: [references/translation_guidelines.md](references/translation_guidelines.md)
  - **Translation prompt**: [references/translation_prompt.md](references/translation_prompt.md)
  - **Review checklist**: [references/review_checklist.md](references/review_checklist.md)
  - **Chinese support**: [references/chinese_support.md](references/chinese_support.md)
  - **Report template**: [assets/report_template.md](assets/report_template.md)

  
