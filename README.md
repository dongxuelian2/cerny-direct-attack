# Černý 猜想与同步自动机研究

本项目研究同步自动机的重置字、像扩张，以及 avoid-or-compress 问题。
设可达像 S 的大小为 s，非空真保护子集 A 的大小为 r，m=n−s、q=n−r。
**余维四、五全部参数现已确定：`F_bin(n,n−4,r) = F(n,n−4,r) = min(q,11)`，`F_bin(n,n−5,r) = F(n,n−5,r) = min(q,14)`。** 上界为纸面归约加完整有限域排除的计算辅助证明，下界有二字母可达构造的纸面证明。

一般 Černý 猜想与完整 Problem 4 尚未解决。已确定区域为全部 m≤5，以及 m≥6、q≤3m−1；剩余精确极值区域为 m≥6、q≥3m。`min(q,3m−1)` 在 m≥4 时的通项仍是猜想。

## 从哪里读

- [论文源码](papers/problem4/main.tex)：余维四、五主定理、完整匹配构造、计算归约与覆盖表、唯一 K₄,₄ 松弛幸存域的纸面排除，以及小参数构造附录。
- [论文主线与计算依据](PROOF.md#problem4-paper-synthesis)：各证明组成的入口、已有运行记录的范围和计算可信性依赖。
- [计算依赖的纸面替代](PROOF.md#problem4-paper-dependency-reductions)：余维三九步上界的完整纸面证明；[单边障碍与一点交换结构](PROOF.md#problem4-single-edge-obstruction)给出任意余维的条件压缩界，统一加强多部图和删除匹配图族。余维四、五其余计算依赖仍保留，论文稿尚未展开这些替代证明。
- [两例外闭合](PROOF.md#problem4-two-exception-closure)与[不交交换孔](PROOF.md#problem4-disjoint-exchange-holes)：统一移除十五类核心、196 个命名域的动态计算依赖；后一条件压缩界 `h+4` 适用于任意多个私人叶子对。
- [三个例外的整支闭合](PROOF.md#problem4-three-exception-closure)：四步核约束给出一般界 `h+5`，与两例外定理合计替代余维五的 521 类核心、7519 个动态域。[任意例外数的容器闭合](PROOF.md#problem4-exception-container-closure)、[支撑逐点闭包](PROOF.md#problem4-exception-support-bootstrap)及[远例外团的核闭合](PROOF.md#problem4-exception-cluster-kernel)给出更一般的 Johnson 图判据；余维四、五全域仍含计算依赖。
- [公共孔核心的完整纸面上界](PROOF.md#problem4-common-hole-complete-core)：P₇为K₄附三个私人叶子及任意孤点时，每个(n−4)集在十一字母内压缩。证明按后层删除行数分类，最后[私人删除行的三行族](PROOF.md#problem4-common-hole-one-deletion-B)由实际第一层的支撑闭合排除。该核心全部十四个命名域均已替代，与上述十五核心合计十六个完整核心、210个命名域；余维四其他核心仍含计算依赖。任意k、h的条件结果见[双退出](PROOF.md#problem4-common-hole-double-exit)、[星形路径](PROOF.md#problem4-common-hole-star-geodesics)及[后层核强迫](PROOF.md#problem4-common-hole-late-kernel)。
- [问题与全部当前边界](PROOF.md#problem)：完整成果表；[PROOF.md](PROOF.md)是唯一维护的数学研究正文。
- [余维四精确值](PROOF.md#problem4-four-exact-eleven)与[余维五精确值](PROOF.md#problem4-five-exact-fourteen)：最终依赖链及全部参数的匹配。
- [下界构造](PROOF.md#constructions)与[上界和有限归约](PROOF.md#upper)：一般方法和低余维基础。
- [全状态循环类精确值](PROOF.md#problem4-full-cycle-exact)、[完整安全族退出稀疏化](PROOF.md#problem4-quadratic-exit-sparsification)、[大余维覆盖加强](PROOF.md#problem4-large-codimension-cover-improvement)：主定理以外的结构成果，适用范围各有明确限制。
- [线性通项猜想](PROOF.md#problem4-linear-codimension-conjecture)：单保护点归约、余维六的 `[17,24]` 饱和值区间，以及同一自动机内部逐维递推的反例；没有反驳或证明全局通项。
- [其他研究方向](PROOF.md#extension)与[探索记录](PROOF.md#exploration)：像扩张、秩核、重置字及受限观察。

论文整理沿用已完成计算，不要求重新运行大型枚举。完成日志说明执行范围，不能充当独立逐域证明证书；计算依赖和唯一松弛幸存者的处理在正文中明确说明。原始日志、生成库存和二进制不提交 Git。

## 编译论文与运行程序

[运行说明](docs/RUNNING.md)首先给出只编译论文的命令，输出为 `build/paper/main.pdf`，不触发研究计算。
研究程序使用 Python 3.10+ 和 C++17，通过根目录 `run.py` 在忽略的 `build/` 研究副本中运行。例如：

```sh
python3 run.py open-point
python3 run.py reset --cerny 12
```

完整复算命令及其参数域也在运行说明中；它们供独立复算或继续研究时选择，不是阅读或编辑论文的前置步骤。

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

早期条件分支与探索源码保持可追溯；引用时以当前完整定理及其适用范围为准。

