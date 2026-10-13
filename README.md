# Černý 猜想与同步自动机研究

本项目研究同步自动机的重置字、像扩张，以及 avoid-or-compress 问题。
**一般 Černý 猜想尚未解决；参数点 `(13,9,1)` 的计算辅助结论为 `F_bin = F = 11`。**

## 从哪里读

[PROOF.md](PROOF.md) 是唯一的数学研究正文，集中维护问题、定义、推导、反例和未解边界。

- [问题与当前结论](PROOF.md#problem)：先了解正在研究什么、哪些结论仍未完成。
- [下界构造](PROOF.md#constructions)与[低余维上界](PROOF.md#upper)：已有参数族和归约。
- [余维四：短对图与入口排除](PROOF.md#frontier)：[完整布尔旗标](PROOF.md#problem4-full-fiber-flag)排除达到十二的全部入口组合，适用于任意有限字母表；与二字母下界十一匹配。
- [条件分支](PROOF.md#branches)：需要额外假设的局部论证。
- [像扩张](PROOF.md#extension)、[秩与核](PROOF.md#rank)、[策略与预算](PROOF.md#policy)、[锚点与最优语言](PROOF.md#anchors)：其他数学方向。
- [探索记录](PROOF.md#exploration)：受限观察、失败路线和待证明机制。

引用结论时链接到 `PROOF.md#章节锚点`。各节的适用范围不可省略；有限搜索不等于一般定理。
论文源码见 [papers/problem4/main.tex](papers/problem4/main.tex)；最新参数点结论以研究正文为准。

## 怎样计算

需要 Python 3.10+ 和支持线程的 C++17 编译器（默认 `g++`，可用 `CXX` 指定）。

```sh
python3 run.py reset --cerny 12
python3 run.py open-point
python3 run.py c7 --threads 8
python3 run.py c7 --threads 8 --independent
python3 run.py tau4 --threads 8
python3 run.py script scripts/problem4/problem4_p3_entry.cpp --threads 3
python3 run.py script scripts/problem4/problem4_p3_entry.cpp --two-three --threads 4
python3 run.py script scripts/problem4/problem4_p3_entry.cpp --overlap-two-two --threads 4
python3 run.py script scripts/problem4/problem4_tau2_overlap.cpp --threads 4
python3 run.py script scripts/problem4/problem4_tau2_overlap.cpp --tau3-disjoint --sizes 1 1 --quotient --threads 8
```

`open-point` 重建并验证下界十一的自动机；上界来自完整旗标排除。
`tau4` 重建并排除第六层四点覆盖的全部九个核心，包含两种独立字母枚举。
`problem4_p3_entry.cpp` 重建三点入口剩余的三个核心，独立核对字母域和距离后排除它们。
加 `--two-three` 则排除三点覆盖路线中“二点第一入口、三点第二入口”的完整分支。
加 `--overlap-two-two` 则排除该路线中两个二点入口相交的全部 86 个有序核心选择。
`problem4_tau2_overlap.cpp` 从九个无三角形核心扩展到全部剩余入口组合，逐层生成完整前像域，并检查共同字母表的短词安全性。全域复现需运行[运行说明](docs/RUNNING.md)中的全部模式。
程序、输入和运行方式见 [运行说明](docs/RUNNING.md)。生成数据和可执行文件写入忽略的 `build/`。

## 目录

```text
PROOF.md                 唯一数学研究正文，按问题和章节组织
README.md                问题与阅读入口
AGENTS.md                后续研究与编辑约定
run.py                   统一运行入口
scripts/
  problem4/              avoid-or-compress 构造与计算
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
