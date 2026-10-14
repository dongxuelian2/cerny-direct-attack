# Černý 猜想与同步自动机研究

本项目研究同步自动机的重置字、像扩张，以及 avoid-or-compress 问题。
**一般 Černý 猜想尚未解决；现有计算辅助十三状态结论经保护块收缩推广，得到对所有 `r≥1` 的 `F_bin(r+12,r+8,r) = F(r+12,r+8,r) = 11`。**

## 从哪里读

[PROOF.md](PROOF.md) 是唯一的数学研究正文，集中维护问题、定义、推导、反例和未解边界。

- [问题与当前结论](PROOF.md#problem)：先了解正在研究什么、哪些结论仍未完成。
- [下界构造](PROOF.md#constructions)与[低余维上界](PROOF.md#upper)：已有参数族和归约。
- [余维四：短对图与入口排除](PROOF.md#frontier)：[完整布尔旗标](PROOF.md#problem4-eleven-audit)排除达到十二的全部入口组合，适用于任意有限字母表；与二字母下界十一匹配。
- [保护块收缩与新边界](PROOF.md#problem4-protected-collapse-strip)：在不要求收缩后同步的条件下传递短对图与旗标约束，推广精确值十一至整条 `m=4,q=12` 参数边界；对 `q=13` 的等号候选给出十一层公共交集与首入口大小限制。
- [条件分支](PROOF.md#branches)：需要额外假设的局部论证。
- [像扩张](PROOF.md#extension)、[秩与核](PROOF.md#rank)、[策略与预算](PROOF.md#policy)、[锚点与最优语言](PROOF.md#anchors)：其他数学方向。
- [探索记录](PROOF.md#exploration)：受限观察、失败路线和待证明机制。

引用结论时链接到 `PROOF.md#章节锚点`。各节的适用范围不可省略；有限搜索不等于一般定理。
论文源码见 [papers/problem4/main.tex](papers/problem4/main.tex)；最新参数点结论以研究正文为准。

## 怎样计算

需要 Python 3.10+ 和支持线程的 C++17 编译器（默认 `g++`，可用 `CXX` 指定）。

```sh
python3 run.py eleven --threads 8
python3 run.py open-point
python3 run.py reset --cerny 12
```

`eleven` 从源码复算下界、核心分类、第六层覆盖归约和扩大入口域的全部排除；不需要保存的库存或证书。`open-point` 单独重建下界见证。
完整上界源码在 `scripts/problem4/upper_bound/`：保留三点入口与 K4，检查完整后续前像和任意大小的共同字母表。
分项复算、早期条件分支和其他研究程序见 [运行说明](docs/RUNNING.md)。生成数据和可执行文件写入忽略的 `build/`。

## 目录

```text
PROOF.md                 唯一数学研究正文，按问题和章节组织
README.md                问题与阅读入口
AGENTS.md                后续研究与编辑约定
run.py                   统一运行入口
scripts/
  problem4/              avoid-or-compress 构造与计算
    upper_bound/         精确值上界的完整枚举与独立控制
    experimental/        早期受限探索
  direct_attack/         像扩张、秩、核与重置字程序
  anchors/               锚点、商与最优语言程序
  automata/              小规模 Python 参考实现
  native/                通用 C++ 搜索内核
  tests/                 程序实现的局部回归检查
papers/                  论文 LaTeX 源码
formal/                  已有 Lean 数学源码
docs/RUNNING.md          程序运行说明
build/                   本地生成内容，不提交
```

新研究写入正文对应章节，必要程序加入 `scripts/` 对应主题；不要另建零散研究 Markdown、
日期日志、结果库存或发布流程。大规模计算使用多线程 C++，Python 用于小规模参考与编排。
具体规则见 [AGENTS.md](AGENTS.md)。源码采用 MIT 许可；研究与代码包含 AI 辅助。

早期条件分支与探索源码保持可追溯。论文的二块证明只维护在 `papers/problem4/main.tex` 中。
