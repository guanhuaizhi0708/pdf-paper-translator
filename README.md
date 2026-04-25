以下是修改后的 README.md，适用于 PDF 论文翻译技能：

```markdown
# PDF 论文翻译SKILL

这是一个用于将 PDF 学术论文翻译为**中文**的 Agent SKILL。

> Skills follow the [Agent Skills](https://agentskills.io/) format.

## Features

- 支持本地 PDF 文件或 URL 链接
- **保留原始的样式**: 自动将 PDF 内容转换为 LaTeX，编译后生成与原版布局一致的翻译版 PDF
- **可以指定翻译的章节**: 你可以在 Agent 执行翻译时指定要翻译的章节，而不是整个论文
- **支持扫描版 PDF**: 自动进行 OCR 识别（需安装 `ocrmypdf`）

> [!NOTE]
> 本技能适用于任意 PDF 论文。如果你需要单独翻译 arXiv 论文（有原始 LaTeX 源码），可以使用 [arXiv 版本](https://github.com/yrom/arxiv-paper-translator)。

## 前置条件

### 必须满足以下之一：
1. 本地安装 `xelatex` 以及 PDF 转换工具（`pandoc`, `poppler-utils`）
2. **或者** 安装 `docker`，使用 [TeXLive Docker 镜像](https://github.com/xu-cheng/latex-docker) 进行编译

### 推荐安装的附加工具（用于 PDF → LaTeX 转换）：
```bash
# macOS
brew install pandoc poppler tesseract ocrmypdf

# Ubuntu/Debian
sudo apt-get install pandoc poppler-utils tesseract-ocr ocrmypdf
```

> 如何在你电脑上安装这些工具请问你的AI助手😄

## 使用方法

安装这个 SKILL：

```sh
npx skills add your-username/pdf-paper-translator
```

在你的 AI 助手中使用它，例如：

```md
> Use pdf paper translator SKILL. 翻译本地的 /path/to/paper.pdf 为中文

> 翻译 https://example.com/paper.pdf 为中文，跳过附录和实验 eval 部分

> /pdf-paper-translator 翻译 ~/Downloads/thesis.pdf 为中文，同时整理核心观点输出一份中文博客用于分享
```

## 一行指令翻译 PDF 论文为中文

```bash
claude -p "/pdf-paper-translator 翻译 https://arxiv.org/pdf/2602.04118.pdf 为中文、Acknowledgement 部分不翻译。使用 Docker 镜像编译 pdf。注意挂载正确的 workspace 给 docker。如果内容很多，可以派发 subagent 来并行处理。翻译完成需要整体 review 一下翻译后的内容的质量，特别关注术语一致性、学术性、专业性、正确性。" --allowedTools "Read,Write,Edit,Bash,Task"
```

## LICENSE

MIT
```

主要改动：
- 标题和描述改为 “PDF 论文翻译”
- Features 中增加支持本地/URL、扫描版 PDF OCR 说明
- 前置条件增加 pandoc、poppler-utils 等 PDF 转换依赖
- 安装命令改为示例 `your-username/pdf-paper-translator`（用户可替换为自己的仓库）
- 使用示例改为 PDF 文件路径或 URL
- 一行指令示例改为 PDF URL 形式
- 保留 MIT 许可证