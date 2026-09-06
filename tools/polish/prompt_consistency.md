你是本仓库（awesome_study）的一致性审校。背景：`papers/*/README.md`（51 篇论文解读）刚经过逐篇对照原文的核对与修订，是**唯一事实源**。但以下综合文档是在核对之前写的，其中引用的数字、任务数、作者归属、venue、机制描述可能已经过时：

- reports/DIGEST.md
- reports/COMPARISON.md
- reports/OPEN_PROBLEMS.md
- reports/GLOSSARY.md
- reports/READING_PATHS.md
- reports/TRENDS_2026.md
- slides/overview.html（HTML 幻灯片，改 HTML 文本节点即可，不动结构/样式/脚本）
- slides/overview.tex（Beamer 源码，改文字即可，保持 LaTeX 合法；表格列数不变）
- data/papers.json 中每篇的 `role`、`authors`、`venue` 字段（JSON 必须保持合法，`ensure_ascii=False, indent=2` 写回）

## 任务
1. 对上述每个文件，找出所有指向具体论文的事实性陈述（数字、百分比、任务数、频率、NFE、作者、机构、venue、方法机制的关键描述）。
2. 逐条到对应的 `papers/<dir>/README.md` 核对（用 `ls papers/` 找目录；README 里的「一句话」「实验与证据」「方法核心」是核对依据）。
3. 不一致则以 README 为准修正综合文档；README 里明确写「原文未报告」的数字，综合文档里要删掉或改为定性表述。
4. 判断性表述（如「理论位已被占」「窗口 6-12 个月」）不是事实错误，不要改；只改与 README 事实冲突的内容。
5. 不要改文档结构、不要增删章节、不要改文风；只做最小必要修正。
6. 每个文件改完后用 Python 以 UTF-8 写回并读回校验；JSON 用 `json.load`/`json.dump(ensure_ascii=False, indent=2)`；改完 `.tex` 后运行 `cd slides && xelatex -interaction=nonstopmode overview.tex >/dev/null 2>&1; xelatex -interaction=nonstopmode overview.tex > /tmp/tex.log 2>&1; grep -c 'Missing character' /tmp/tex.log; grep -o 'Output written on overview.pdf ([0-9]* pages' /tmp/tex.log; rm -f overview.aux overview.log overview.nav overview.out overview.snm overview.toc` 确认 11 页、0 缺字。
7. 在 `reports/CONSISTENCY_LOG.md` 写一份清单：每个文件下列出「原文 → 改为（依据 papers/<dir>）」，没有改动的文件写「无不一致」。

## 硬性约束
- 不许改 `papers/*/README.md`。
- 不许新增论文、不许删改 papers.json 的 id/slug/category/translate 字段。
- 全部完成后输出一行：检查 N 个文件，修正 M 处。
