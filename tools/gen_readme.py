#!/usr/bin/env python3
"""Generate README.md (awesome-list style) from data/papers.json.

Link columns auto-detect artifacts on disk, so re-run after any stage:
    python3 tools/gen_readme.py
"""
import json
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
m = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
papers = m["papers"]

CAT_INTRO = {
    "01_generative_foundations": "从 DDPM 到 MeanFlow：score → velocity → 平均速度场的一步化路线，外加机器人侧的事实标准 Diffusion Policy。",
    "02_sb_theory": "Schrödinger Bridge 的数学正典与神经化起点：path-space KL、IPF、GSB 推广。",
    "03_bridge_algorithms": "DSB 之后的算法演化主线：IPF → IMF → 免仿真 → 在线 α-IMF → 对抗式少步；另含软约束与参考过程设计理论。",
    "04_rl_foundations": "为 SB×RL 提供 RL 侧接口的五篇经典：trust region、max-ent、mirror descent、免 critic、advantage-weighted BC。",
    "05_generative_rl": "生成式策略 × RL 的两代范式：序列建模/扩散规划 → offline Q+BC → online 微调（分解 / 噪声空间）→ 原生一步竞赛 → 流映射统一。",
    "06_sb_x_rl": "选题主战场：四条 SB×RL 进路（动能正则、path-space mirror descent、bridge rectification、跨域轨迹翻译）。",
    "07_radar_2026": "趋势报告收录的 2026 年新变量：MeanFlow 族扩张（MVP/MFPO/UCA-Flow/ReactVLA）、桥式起点上主会（BridgePolicy）、绕开似然的 RL 微调（RECAP/LP-DS/DF-ExpEnse）。",
}

def pdir(p):
    return f"papers/{p['id']}_{p['slug']}"

def has(p, name):
    return (ROOT / pdir(p) / name).exists()

n_notes = sum(1 for p in papers if has(p, "README.md"))
n_zh = sum(1 for p in papers if has(p, f"{p['id']}.zh.pdf"))
n_code = sum(1 for p in papers if p.get("code"))
today = dt.date.today().isoformat()

def paper_row(p):
    d = pdir(p)
    links = [f"[arXiv](https://arxiv.org/abs/{p['id']})"]
    if has(p, "README.md"):
        links.append(f"[解读]({d}/README.md)")
    if has(p, f"{p['id']}.pdf"):
        links.append(f"[EN]({d}/{p['id']}.pdf)")
    if has(p, f"{p['id']}.zh.pdf"):
        links.append(f"[中文]({d}/{p['id']}.zh.pdf)")
    if p.get("code"):
        links.append(f"[代码]({p['code']})")
    venue = p["venue"] or "arXiv"
    authors = p["authors"] or "—"
    return f"| {p['title']} | {authors} | {venue} | {p['role']} | {' · '.join(links)} |"

def anchor(text):
    # github-slugger: lowercase, strip ASCII punctuation + U+2000-206F/2E00-2E7F, spaces -> hyphens
    import re
    t = text.strip().lower()
    t = re.sub(r"[\u2000-\u206F\u2E00-\u2E7F\\'!\"#$%&()*+,./:;<=>?@\[\]^`{|}~]", "", t)
    return t.replace(" ", "-")

out = []
out.append("# Awesome Study: Schrödinger Bridge × RL × Robot Policy Learning\n")
out.append(
    f"![papers](https://img.shields.io/badge/papers-{len(papers)}-blue) "
    f"![notes](https://img.shields.io/badge/%E4%B8%AD%E6%96%87%E8%A7%A3%E8%AF%BB-{n_notes}-brightgreen) "
    f"![zh--pdf](https://img.shields.io/badge/%E4%B8%AD%E6%96%87PDF-{n_zh}-red) "
    f"![code](https://img.shields.io/badge/%E4%BB%A3%E7%A0%81%E9%93%BE%E6%8E%A5-{n_code}-orange) "
    f"![updated](https://img.shields.io/badge/updated-{today.replace('-', '--')}-lightgrey) "
    f"![license](https://img.shields.io/badge/license-MIT-green)\n"
)
out.append(f"""围绕 **Schrödinger Bridge（SB）× 强化学习（RL）× 机器人策略学习** 的精读仓库：{len(papers)} 篇论文，每篇配中文详细解读（`papers/*/README.md`，七节结构：一句话 / 问题与动机 / 方法核心 / 实验与证据 / 谱系位置 / 与 SB×RL 的关联 / 局限与批判）与英文原版 PDF；{n_zh} 篇前沿论文另配保版式中文翻译 PDF（[SuperTranslate](https://github.com/asimfish/super_translate) 生成）；{n_code} 篇附官方代码或项目页。

**主线问题**：生成式策略（diffusion / flow / bridge）表达能力强，但 `log π` 不可算，经典 RL 的策略梯度 / 熵正则 / 概率比全部失效。本仓库沿三条线索组织文献：
1. **一步化**（MeanFlow 系）：把多步去噪压成 1-NFE，让 RL 微调回到普通策略优化；
2. **路径空间**（SB 系）：把 KL 正则从动作分布搬到轨迹测度，绕开 log π；
3. **桥式先验**（I2SB 系）：用 informative source 替代高斯先验，天然适配 sim-to-real 与导航。

处理 `log π` 障碍的五条路线在本库均有代表：逐步分解（DPPO / ReinFlow）· 路径空间（FLAC / GSB-MDPO）· 噪声空间（DSRL / LP-DS）· 条件化 / 加权监督（AWR / RECAP）· 生成-选择（MVP / FMQ / DF-ExpEnse）；另有似然近似路线（MFPO）与之对峙。

> **先读** [十分钟速览](reports/DIGEST.md) · **要选题** [开放问题与实验设计](reports/OPEN_PROBLEMS.md) · **横向比** [三张对比表](reports/COMPARISON.md) · **按背景读** [阅读路线](reports/READING_PATHS.md) · **查词** [术语表](reports/GLOSSARY.md) · **看趋势** [2026 雷达](reports/TRENDS_2026.md)
""")

out.append("## 目录\n")
for cid, cname in m["categories"].items():
    n = sum(1 for p in papers if p["category"] == cid)
    out.append(f"- [{cname}](#{anchor(cname)})（{n} 篇）")
out.append("- [汇总报告](#汇总报告)")
out.append("- [仓库结构](#仓库结构)")
out.append("- [如何扩展](#如何扩展)")
out.append("- [质量说明](#质量说明)")
out.append("- [更新日志](#更新日志)")
out.append("- [引用](#引用)\n")

for cid, cname in m["categories"].items():
    out.append(f"## {cname}\n")
    out.append(CAT_INTRO.get(cid, "") + "\n")
    out.append("| 论文 | 作者 | 发表 | 定位 | 链接 |")
    out.append("|---|---|---|---|---|")
    for p in sorted((p for p in papers if p["category"] == cid), key=lambda p: p["id"]):
        out.append(paper_row(p))
    out.append("")

out.append("""## 汇总报告

| 产物 | 说明 |
|---|---|
| [`reports/DIGEST.md`](reports/DIGEST.md) | **十分钟速览**：核心矛盾、五条路线、三条线索现状、SB 的两个差异化资产、五个空格 |
| [`reports/OPEN_PROBLEMS.md`](reports/OPEN_PROBLEMS.md) | 五个开放问题的实验设计：假设 / 最小实验 / 对表谁 / 杀死条件 / 库内零件 |
| [`reports/COMPARISON.md`](reports/COMPARISON.md) | 横向对比：一步策略 · log π 路线 · SB 求解器 三张表 |
| [`reports/READING_PATHS.md`](reports/READING_PATHS.md) | 生成 / RL / 机器人三种背景 × 半天 / 一天 / 一周的阅读路线 |
| [`reports/GLOSSARY.md`](reports/GLOSSARY.md) | 术语表：SB 家族 · 求解器 · 一步生成 · RL 接口 |
| [`reports/TRENDS_2026.md`](reports/TRENDS_2026.md) | 2026 前沿趋势与 insight 报告（雷达论文已入库为 07 类） |
| [`slides/overview.html`](slides/overview.html) | HTML PPT：全库综述 11 页（浏览器打开，方向键翻页） |
| [`slides/overview.pdf`](slides/overview.pdf) | 同内容的 Beamer PDF |

## 仓库结构

```text
awesome_study/
├── README.md                 # 本文件，由 tools/gen_readme.py 生成
├── data/papers.json          # 唯一 manifest：id / slug / 标题 / 作者 / venue / 类别 / 定位 / 代码链接 / 是否翻译
├── papers/<arxiv_id>_<slug>/
│   ├── README.md             # 中文详细解读（七节结构）
│   ├── <arxiv_id>.pdf        # 英文原版
│   └── <arxiv_id>.zh.pdf     # 保版式中译（前沿篇目）
├── reports/                  # 综合报告（速览 / 开放问题 / 对比表 / 阅读路线 / 术语表 / 趋势）与修订日志
├── slides/                   # HTML PPT 与 Beamer 源码 / PDF
└── tools/                    # 下载、翻译、README 生成、Codex 打磨提示
```

## 如何扩展

1. 在 `data/papers.json` 追加条目（必填 `id` `slug` `title` `category` `translate` `role`；`authors` `venue` `code` 可后补）。
2. `python3 tools/download_papers.py` 下载 PDF（自动跳过已有）。
3. 在 `papers/<id>_<slug>/README.md` 写解读，沿用七节结构；写完可用 `tools/polish/PROMPT_TEMPLATE.md` 交给 Codex CLI 对照原文核对。
4. 需要中译则 `bash tools/translate_batch.sh <slug>`（依赖 SuperTranslate 与 DeepSeek key）。
5. `python3 tools/gen_readme.py` 重新生成本文件，提交。

## 质量说明

51 篇解读经三轮处理：(1) 基于 PDF 原文与知识库笔记撰写；(2) 本地 Codex CLI（GPT-6，reasoning xhigh）逐篇对照原文核对数字、归属、机制并去除套话，修订要点见 [`reports/POLISH_LOG.md`](reports/POLISH_LOG.md)；(3) 「一句话」在只允许使用正文事实的约束下重写为带判断的单句，见 [`reports/ONELINER_LOG.md`](reports/ONELINER_LOG.md)。综合报告、幻灯片与 manifest 中的事实陈述已逐条对齐到核对后的解读，见 [`reports/CONSISTENCY_LOG.md`](reports/CONSISTENCY_LOG.md)。中译 PDF 经视觉 QA，数学密集篇目的公式行保留英文属预期。

## 更新日志

| 日期 | 内容 |
|---|---|
| 2026-09-07 | README 全面更新：官方标题、作者补全、37 个代码 / 项目链接、类别内按时间排序、仓库结构与扩展指南、更新日志、引用 |
| 2026-09-06 | 综合文档 / 幻灯片 / manifest 与核对后解读对齐 181 处；51 篇「一句话」重写 |
| 2026-09-05 | Codex GPT-6 逐篇二审 51 篇解读；新增速览 / 开放问题 / 对比表 / 阅读路线 / 术语表五份综合报告 |
| 2026-09-02 | 扩展至 51 篇：新增 07 类 2026 雷达 9 篇 + 谱系补齐 10 篇；中译 PDF 增至 19 篇 |
| 2026-09-01 | 首发：32 篇解读、英文 PDF、12 篇中译、趋势报告、HTML PPT 与 Beamer PDF |

## 引用

```bibtex
@misc{awesome_study_sbrl_2026,
  title  = {Awesome Study: Schr{\\"o}dinger Bridge x RL x Robot Policy Learning},
  author = {asimfish},
  year   = {2026},
  url    = {https://github.com/asimfish/awesome_study}
}
```

## 致谢

- 翻译：[SuperTranslate](https://github.com/asimfish/super_translate)
- 排版规范参考：[awesome-ml4co](https://github.com/Thinklab-SJTU/awesome-ml4co)
- 演示：[ppt-master](https://github.com/hugohe3/ppt-master) · [beamer-skill](https://github.com/Noi1r/beamer-skill)
- 二审：[Codex CLI](https://github.com/openai/codex)
""")

(ROOT / "README.md").write_text("\n".join(out), encoding="utf-8")
print(f"README.md written: {len(chr(10).join(out))} chars | papers {len(papers)} | notes {n_notes} | zh {n_zh} | code {n_code}")
