#!/usr/bin/env python3
"""Generate README.md (awesome-ml4co style) from data/papers.json.

Link columns auto-detect artifacts on disk, so re-run after any stage:
    python3 tools/gen_readme.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
m = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))

CAT_INTRO = {
    "01_generative_foundations": "从 DDPM 到 MeanFlow：score → velocity → 平均速度场的一步化路线，外加机器人侧的事实标准 Diffusion Policy。",
    "02_sb_theory": "Schrödinger Bridge 的数学正典与神经化起点：path-space KL、IPF、GSB 推广。",
    "03_bridge_algorithms": "DSB 之后的算法演化主线：IPF → IMF → 免仿真 → 在线 α-IMF → 对抗式少步。",
    "04_rl_foundations": "为 SB×RL 提供 RL 侧接口的五篇经典：trust region、max-ent、mirror descent、免 critic、advantage-weighted BC。",
    "05_generative_rl": "生成式策略 × RL 的两代范式：序列建模/扩散规划 → offline Q+BC → online denoising-as-MDP → 一步策略实时控制。",
    "06_sb_x_rl": "选题主战场：四条 SB×RL 进路（动能正则、path-space mirror descent、bridge rectification、跨域轨迹翻译）。",
}

def paper_row(p):
    pdir = f"papers/{p['id']}_{p['slug']}"
    d = ROOT / pdir
    links = [f"[arXiv](https://arxiv.org/abs/{p['id']})"]
    if (d / "README.md").exists():
        links.append(f"[解读]({pdir}/README.md)")
    if (d / f"{p['id']}.pdf").exists():
        links.append(f"[EN]({pdir}/{p['id']}.pdf)")
    if (d / f"{p['id']}.zh.pdf").exists():
        links.append(f"[中文]({pdir}/{p['id']}.zh.pdf)")
    venue = p["venue"] or "arXiv"
    authors = p["authors"] or "—"
    return f"| {p['title']} | {authors} | {venue} | {p['role']} | {' · '.join(links)} |"

out = []
out.append("# Awesome Study: Schrödinger Bridge × RL × Robot Policy Learning\n")
out.append("![papers](https://img.shields.io/badge/papers-%d-blue) ![zh--pdf](https://img.shields.io/badge/%%E4%%B8%%AD%%E6%%96%%87PDF-%d-red) ![license](https://img.shields.io/badge/license-MIT-green)\n"
           % (len(m["papers"]), sum(1 for p in m["papers"] if (ROOT / f"papers/{p['id']}_{p['slug']}/{p['id']}.zh.pdf").exists())))
out.append("""围绕 **Schrödinger Bridge（SB）× 强化学习（RL）× 机器人策略学习** 的精读仓库。
每篇论文配：中文详细解读（`papers/*/README.md`）、英文原版 PDF；12 篇前沿论文另配保版式中文翻译 PDF（[SuperTranslate](https://github.com/asimfish/super_translate) 生成）。

**主线问题**：生成式策略（diffusion / flow / bridge）表达能力强，但 `log π` 不可算，经典 RL 的策略梯度/熵正则全部失效。本仓库沿三条线索组织文献：
1. **一步化**（MeanFlow 系）：把多步去噪压成 1-NFE，让 RL 微调回到普通策略优化；
2. **路径空间**（SB 系）：把 KL 正则从动作分布搬到轨迹测度，绕开 log π；
3. **桥式先验**（I2SB 系）：用 informative source 替代高斯先验，天然适配 sim-to-real 与导航。
""")
out.append("## 目录\n")
for cid, cname in m["categories"].items():
    n = sum(1 for p in m["papers"] if p["category"] == cid)
    anchor = cname.replace(" ", "-").replace("（", "").replace("）", "").replace("/", "").replace("×", "").replace("--", "-")
    out.append(f"- [{cname}](#{anchor.lower()})（{n} 篇）")
out.append("- [汇总报告](#汇总报告)")
out.append("- [趋势与 insight](#趋势与-insight)\n")

for cid, cname in m["categories"].items():
    out.append(f"## {cname}\n")
    out.append(CAT_INTRO.get(cid, "") + "\n")
    out.append("| 论文 | 作者 | 发表 | 定位 | 链接 |")
    out.append("|---|---|---|---|---|")
    for p in m["papers"]:
        if p["category"] == cid:
            out.append(paper_row(p))
    out.append("")

out.append("""## 汇总报告

| 产物 | 说明 |
|---|---|
| [`slides/overview.html`](slides/overview.html) | HTML PPT：全库综述（浏览器打开，方向键翻页） |
| [`slides/overview.pdf`](slides/overview.pdf) | PDF 版综述报告（Beamer） |
| [`reports/TRENDS_2026.md`](reports/TRENDS_2026.md) | 2026 前沿趋势与 insight 报告 |

## 趋势与 insight

见 [`reports/TRENDS_2026.md`](reports/TRENDS_2026.md)：2026 年 5 月后的新论文雷达、趋势判断、空白与机会、风险。

## 构建工具

| 脚本 | 作用 |
|---|---|
| `tools/download_papers.py` | 按 `data/papers.json` 批量下载 arXiv PDF |
| `tools/translate_batch.sh` | 批量保版式翻译（SuperTranslate + DeepSeek） |
| `tools/gen_readme.py` | 重新生成本 README（链接自动探测产物） |

## 致谢

- 翻译：[SuperTranslate](https://github.com/asimfish/super_translate)
- 排版规范参考：[awesome-ml4co](https://github.com/Thinklab-SJTU/awesome-ml4co)
- PPT：[ppt-master](https://github.com/hugohe3/ppt-master)；PDF 报告：[beamer-skill](https://github.com/Noi1r/beamer-skill)
""")

(ROOT / "README.md").write_text("\n".join(out), encoding="utf-8")
print("README.md written:", len("\n".join(out)), "chars")
