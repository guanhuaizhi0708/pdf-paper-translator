# Markdown-First Paper Translation Guidelines

This document provides detailed guidelines for translating academic papers from English to Chinese in a Markdown-first workflow. For local PDFs, extract text with `pdftotext`/OCR, normalize it into Markdown, protect formulas, and translate the Markdown. Do not convert PDF content into LaTeX by default.

## Core Principles

1. **Preserve Markdown structure** - Headings, lists, tables, captions, citations, URLs, and code blocks must remain stable
2. **Maintain scientific accuracy** - Mathematical expressions and technical terms must be precise
3. **Keep math immutable** - Do not translate or normalize anything inside math mode
4. **Avoid PDF-to-LaTeX conversion** - Use LaTeX-specific rules only if the user provides source `.tex` files
5. **Selective translation** - Only translate content meant for readers, not code/formulas/placeholders
6. **Use domain terminology** - For sea ice, remote sensing, and deep learning papers, read [domain_terminology.md](domain_terminology.md) before translation
7. **Follow academic translation prompt** - See [translation_prompt.md](translation_prompt.md)
8. **Draft then polish** - Complete a faithful first draft, then do a second-pass rewrite into natural academic Chinese before delivery

## What to Translate

### ✅ Always Translate

1. **Main text content**
   - Paragraphs, sentences in document body
   - Section, subsection, chapter titles
   - Abstract and conclusion text

2. **Paper title** — Translate the Markdown title or title text extracted from the PDF

3. **Captions and labels**
   - Figure captions
   - Table captions
   - Algorithm/listing titles

4. **Comments for readers**
   - Footnotes
   - Author notes
   - Margin notes meant for reading

5. **Bibliography context (optional)**
   - Paper titles in references if desired
   - Keep original for traceability

### Example: Main Text

```markdown
% Before
# Introduction
Deep learning has revolutionized computer vision.

% After
# 引言
深度学习已经彻底改变了计算机视觉领域。
```

### Example: Captions

```markdown
% Before
Figure 1. Accuracy comparison on ImageNet dataset.

% After
图 1. 在 ImageNet 数据集上的准确率对比。
```

## What NOT to Translate

### 🚯 Quick Decision Rule

If the content is **machine-executable** (code, formulas, command outputs),
do NOT translate it. Only translate narrative content meant for human readers.

### ❌ Never Translate

1. **Mathematical formulas and equations**
   ```latex
   % Keep unchanged
   \begin{equation}
   f(x) = \sum_{i=1}^{n} w_i x_i + b
   \end{equation}
   ```
   This includes text inside math commands. Keep `\text{and}`, `\mathrm{if}`,
   `\operatorname{softmax}`, equation tags, subscripts, superscripts, and escaped
   symbols exactly as in the source. Do not translate `\text{and}` to `\text{且}`.

2. **Markdown math placeholders**
   ```markdown
   @@MATH_000001@@
   ```
   Keep placeholders byte-for-byte until formulas are restored from the mapping file.

3. **LaTeX commands and environments** (only if the source is already LaTeX)
   ```latex
   % Keep these commands as-is
   \begin{figure}
   \includegraphics{image.pdf}
   \label{fig:example}
   \end{figure}
   ```

4. **Content in code blocks**
   ```latex
   % Code remains in English
   \begin{lstlisting}[language=Python]
   def train_model(data, epochs=100):
       return model.fit(data, epochs=epochs)
   \end{lstlisting}
   ```
   
   ```latex
   % Skip translation for lstlisting block
   \begin{lstlisting}[style=snippet,caption={\textbf{System prompt: Tool use}}]
   You are a helpful function-calling AI assistant. You are provided with function signatures within <functions></functions> XML tags. You may call one or more functions to assist with the user query. Output any function calls within <function_calls></function_calls> XML tags. Do not make assumptions about what values to plug into functions.
   \end{lstlisting}
   ```

```latex
   % Skip translation for minted block
   \begin{minted}[
      ]{markdown}
Runtime Error
ZeroDivisionError: division by zero
Line 73 in separateSquares (Solution.py)

Last Executed Input
[[26,30,2],[11,23,1]]
   \end{minted}
```

4. **Raw data in tables** (AI queries, code, traceback, user input examples)
   - Keep cell content in English, only translate caption and descriptive headers
   - Rule of thumb: "evidence/data" → don't translate; "narrative" → translate

5. **Algorithm pseudocode structure**
   ```latex
   % Keep structure, translate only necessary keywords/comments
   \begin{algorithm}
   \caption{Training Algorithm}  % ← Translate caption
   \begin{algorithmic}
   \STATE $x \leftarrow 0$  % ← Keep code as-is
   \FOR{$i = 1$ to $n$}
   \STATE $x \leftarrow x + i$
   \ENDFOR
   \end{algorithmic}
   \end{algorithm}
   ```

5. **Person names and proper nouns**
   - Author names: keep as-is (John Smith → John Smith)
   - Model names: keep original (ResNet, BERT)
   - Institution names — follow these rules:
     - Chinese institutions: use official Chinese name
     - Well-known foreign institutions: use established Chinese translation
     - Lesser-known institutions: keep original English name
       - e.g. Tsinghua University → 清华大学, 
6. **File paths and references**
   ```latex
   % Keep unchanged
   \input{sections/methodology}
   \includegraphics{figures/result.pdf}
   \cite{smith2020deep}
   ```

7. **URLs and hyperlinks**
   ```latex
   % Keep unchanged
   \url{https://arxiv.org/abs/2206.04655}
   \href{https://github.com/...}{code repository}
   ```

8. **Labels and reference keys**
   ```latex
   % Keep unchanged
   \label{sec:intro}
   \ref{fig:architecture}
   \cite{lecun2015deep}
   ```
9. **Inline expressions and code**
   ```latex
   % Keep unchanged
   $E = mc^2$
   \texttt{code}
   \verb|code|
   ```
## Special Cases

### Tables

Translate cell content (data descriptions), keep structure:

```latex
% Before
\begin{table}
\begin{tabular}{lcc}
\hline
Method & Accuracy & Speed \\
\hline
Ours & 95.2\% & 10ms \\
\hline
\end{tabular}
\caption{Performance comparison}
\end{table}

% After
\begin{table}
\begin{tabular}{lcc}
\hline
方法 & 准确率 & 速度 \\
\hline
本文方法 & 95.2\% & 10ms \\
\hline
\end{tabular}
\caption{性能对比}
\end{table}
```

### Inline Math in Text

Keep math unchanged, translate surrounding text:

```latex
% Before
The loss function $\mathcal{L}$ measures the error.

% After
损失函数 $\mathcal{L}$ 用于衡量误差。
```

### Markdown Formula Guard

For Markdown deliverables, protect math before translation and restore it after
translation by hand:

1. Copy `paper/${PAPER_ID}.source.md` to `paper/${PAPER_ID}.protected.md`.
2. Replace every math span with sequential placeholders such as `@@MATH_000001@@`.
3. Record the exact placeholder-to-formula mapping in `paper/${PAPER_ID}.math-map.md`.
4. Translate `paper/${PAPER_ID}.protected.md` into `paper/${PAPER_ID}.protected-zh.md`, preserving placeholders exactly.
5. Restore formulas manually from the mapping file into `paper/${PAPER_ID}-翻译.md`.

Then verify:

```bash
rg -n "@@MATH_" paper/${PAPER_ID}-翻译.md
rg -n "全球气候引擎|补充性高分辨率来源|工作空间分辨率|对大气条件的不变性更强|AI就绪|结果兴趣区域|letter-value图|原始logit输出|重分配为0%|快速发射" paper/${PAPER_ID}-翻译.md
```

Also compare source and translation side by side to confirm:
- all placeholders were restored
- placeholder numbering in `paper/${PAPER_ID}.math-map.md` is complete and unique
- math span count is unchanged
- formulas are identical
- `%` inside math remains `\%`
- no CJK characters were introduced into math

If a placeholder is missing, duplicated, or restored in the wrong position, go back to `paper/${PAPER_ID}.protected.md` and redo that segment rather than patching formulas directly in the final Markdown.

### Acronyms

First mention: provide both English and Chinese

e.g.: English "mixture-of-experts (MoE)" → Chinese "混合专家（Mixture-of-Experts，MoE）"

```latex
% Before
Convolutional Neural Networks (CNN) are widely used.

% After
卷积神经网络（Convolutional Neural Networks, CNN）被广泛应用。
```

Subsequent mentions: use acronym

```latex
% Before
CNNs achieve high accuracy.

% After
CNN具有很高的准确率。
```

### Sea-Ice and Remote-Sensing Terms

For this skill's target papers, always build a terminology table before translating. Use [domain_terminology.md](domain_terminology.md) as the default glossary.

High-risk examples:

| English | Preferred Chinese |
|---|---|
| sea ice concentration (SIC) | 海冰密集度（SIC） |
| sea ice area (SIA) | 海冰面积（SIA） |
| sea ice extent (SIE) | 海冰范围（SIE） |
| retrieval / inversion | 反演 |
| brightness temperature | 亮温 |
| backscatter | 后向散射 |
| normalized radar cross section (`\sigma^0`) | 归一化雷达截面 / 后向散射系数 |
| marginal ice zone (MIZ) | 边缘冰区（MIZ） |
| melt pond fraction (MPF) | 融池比例（MPF） |
| ice floe / floe | 浮冰块 |
| tie point | 系点 |
| reference product/dataset | 参考产品 / 参考数据 |

Keep product, mission, dataset, and model names such as Sentinel-1, AMSR2, OSI SAF, NOAA/NSIDC, DMI-ASIP, and U-Net in English unless the paper provides an official Chinese name.

### Comments and Non-Reader Text

Comments and extraction notes that are not reader-facing do not need translation. Preserve them if they help trace the source.

```latex
% TODO: Add more experiments  ← keep original, do not translate
\section{实验}
```

## File Organization

### Markdown-First Projects

1. **Source Markdown** (e.g., `paper/${PAPER_ID}.source.md`)
   - Built from `pdftotext`/OCR extraction or provided directly by the user
   - Repair headings, captions, formulas, and obvious extraction errors before translation

2. **Terminology Table** (e.g., `paper/${PAPER_ID}.terms.md`)
   - Use three columns: `English | Chinese | Notes`
   - Keep the same table visible during translation, polish, and review

3. **Protected Markdown** (e.g., `paper/${PAPER_ID}.protected.md`)
   - Replace every math span with `@@MATH_000001@@`-style placeholders
   - Keep a manual mapping file with exact original formula text

4. **Translated Markdown** (e.g., `paper/${PAPER_ID}-翻译.md`)
   - Restore formulas after translation
   - Deliver this as the primary output

### Directory Structure

```
pdf_paper/
└── paper.pdf

paper/
├── ${PAPER_ID}.source.txt       # raw pdftotext/OCR extraction
├── ${PAPER_ID}.source.md        # repaired Markdown source
├── ${PAPER_ID}.terms.md         # paper-specific terminology table
├── ${PAPER_ID}.protected.md     # math placeholders
├── ${PAPER_ID}.math-map.md      # placeholder-to-formula mapping
├── ${PAPER_ID}.protected-zh.md  # translated protected Markdown
└── ${PAPER_ID}-翻译.md          # final translated Markdown
```

## Translation Quality Checklist

For detailed checks (Markdown deliverables, formula placeholders, terminology, style, and content spot-check), see [review_checklist.md](review_checklist.md).

## Chinese Writing Guidelines

Follow these guidelines for better readability:

| 类别 | 规则 | 示例 |
|------|------|------|
| 去冗余词 | 避免"来"、"地"、"的"、"了"等非必要词 | `来表示` → `表示`；`隐式地` → `隐式` |
| 精简主语 | 削减"我们"，用"本文"或无主语句 | `在本工作中，我们提出了X` → `本文提出的X` |
| 去空洞修饰语 | 删空洞形容词，用数据代替 | `卓越的效率` → `速度快约100倍` |
| 术语标注 | 英文标注统一 Title Case | `photometric loss` → `Photometric Loss` |
| 句式精简 | 合并碎句，拆分长定语 | 三个"首先/然后/最后"短句 → 一句带顿号 |
| 避免半中半英 | 不写 `letter-value图`、`AI就绪`、`logit输出` 这类组合 | `结果兴趣区域` → `感兴趣区域（ROI）` |

## Handling Edge Cases

### Custom Macros

If paper defines custom commands:

```latex
\newcommand{\ournethod}{ProposedNet}
```

Translate the output, not the command:

```latex
% If used in text
We propose \ourmethod{} for classification.

% Translate to
我们提出\ourmethod{}用于分类。
% Keep macro unchanged, it will expand to "ProposedNet"
```

Or redefine macro to Chinese:

```latex
\newcommand{\ourmethod}{提出的网络}
```

### Theorems and Proofs

Translate theorem content, keep structure:

```latex
% Before
\begin{theorem}
For any convex function $f$, the minimum exists.
\end{theorem}

% After
\begin{theorem}
对于任意凸函数 $f$，最小值存在。
\end{theorem}
```

May need to configure theorem environment names:

```latex
\newtheorem{theorem}{定理}
\newtheorem{lemma}{引理}
\newtheorem{proof}{证明}
```
