# PDF Paper Translator

A Markdown-first skill for translating academic papers from PDF, URL, or extracted Markdown into Chinese.

## What It Does

- accepts local PDFs, PDF URLs, or existing Markdown sources
- extracts PDF text into a reviewable Markdown source
- protects formulas before translation
- applies sea-ice, remote-sensing, and deep-learning terminology rules
- outputs a formula-safe Chinese Markdown translation
- can also generate a technical report

This workflow **does not** convert PDF content into LaTeX and **does not** compile a translated PDF.

## Recommended Use Cases

- translating sea-ice and polar remote-sensing papers into Chinese
- reviewing a paper in Markdown with formulas preserved
- iterating on terminology and translation quality in a repo
- generating a companion technical summary from the translated paper

## Requirements

For PDF input:
- `poppler-utils` (`pdftotext`, `pdfinfo`)

Optional:
- `ocrmypdf`
- `tesseract`

Install examples:

```bash
# macOS
brew install poppler tesseract ocrmypdf

# Ubuntu/Debian
sudo apt-get install poppler-utils tesseract-ocr ocrmypdf
```

If you already have a clean Markdown source, no extra runtime tools are required.

## Workflow

1. Put the PDF or Markdown source into the workspace.
2. For PDF input, extract and normalize it into `paper/<paper-id>.source.md`.
3. Build `paper/<paper-id>.terms.md` from the title, abstract, headings, captions, and method/results sections.
4. Protect formulas manually with placeholders and record them in `paper/<paper-id>.math-map.md`.
5. Translate `paper/<paper-id>.protected.md` into `paper/<paper-id>.protected-zh.md`, then restore formulas and review the final Markdown.

Key outputs:
- `paper/<paper-id>.source.md`
- `paper/<paper-id>.terms.md`
- `paper/<paper-id>.math-map.md`
- `paper/<paper-id>-翻译.md`
- `pdf_paper/technical_report.md` when a report is requested

## Usage Examples

```md
Use pdf paper translator SKILL. 翻译本地的 /path/to/paper.pdf 为中文。

翻译 https://example.com/paper.pdf 为中文，并输出 Markdown。

/pdf-paper-translator 翻译 ~/Downloads/thesis.pdf 为中文，同时整理一份中文技术总结。

/pdf-paper-translator 基于现有的 paper/my-paper.source.md 继续翻译，不要重新抽取 PDF。
```

## Notes

- If you need a layout-preserving workflow from source LaTeX, use a LaTeX-oriented paper translation skill instead.
- If PDF extraction quality is poor, fix the Markdown source first and then translate.
- Keep `source.md`, `protected.md`, `protected-zh.md`, `math-map.md`, and the final translation until review is complete.
- Formula integrity checks and translation style scans are part of the intended workflow.

## License

MIT
