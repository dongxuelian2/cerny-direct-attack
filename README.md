# Černý 猜想与同步自动机研究

本项目研究同步自动机的重置字、像扩张，以及 avoid-or-compress 问题。
**一般 Černý 猜想尚未解决；现有计算辅助十三状态结论经保护块收缩推广，得到对所有 `r≥1` 的 `F_bin(r+12,r+8,r) = F(r+12,r+8,r) = 11`。**
整条 `m=4,q=13` 边界也已通过完整有限域排除确定为 `F_bin(r+13,r+9,r) = F(r+13,r+9,r) = 11`。完整 Problem 4 仍未解决；`m=4,q≥14` 与 `m=5,q=15` 等区域仍开放。

新的纸面推导处理全部奇圈长度，并将大余维、全部短对图形状的条件覆盖界推进一层；有限基论证还给出随余维无界增长的加性改进。它们没有给出全参数的匹配下界。

## 从哪里读

[PROOF.md](PROOF.md) 是唯一的数学研究正文，集中维护问题、定义、推导、反例和未解边界。

- [问题与当前结论](PROOF.md#problem)：先了解正在研究什么、哪些结论仍未完成。
- [下界构造](PROOF.md#constructions)与[低余维上界](PROOF.md#upper)：已有参数族和归约。
- [余维四：短对图与入口排除](PROOF.md#frontier)：[完整布尔旗标](PROOF.md#problem4-eleven-audit)排除达到十二的全部入口组合，适用于任意有限字母表；与二字母下界十一匹配。
- [保护块收缩与新边界](PROOF.md#problem4-protected-collapse-strip)：在不要求收缩后同步的条件下传递短对图与旗标约束，推广精确值十一至整条 `m=4,q=12` 参数边界；对 `q=13` 的等号候选给出十一层公共交集与首入口大小限制。
- [q=13 的精确值十一](PROOF.md#problem4-q13-exact-eleven)：全部二十五核心、早晚分裂及不再增长域均已完整排除；结合保护收缩与二字母构造，对所有 `r≥1` 得到精确值十一。
- [一般目标长度的保护集收缩](PROOF.md#problem4-protected-slack-collapse)：距原上界 `k` 的候选可缩到至多 `k+1` 个保护点，全部字母共享至多 `2^k` 个外部保护入口。
- [稀疏短对图的入口独立性](PROOF.md#problem4-sparse-pair-entrance-independence)：`|P₁|≤4,|P₂|≤5` 时，实际字母排除唯一可能的四圈依赖，将首层入口数量界降为 `k+1`；适用于 `m=4,L≥12`，未解决剩余入口的后续演化。
- [保持同步与可达的收缩](PROOF.md#problem4-reachable-slack-collapse)：保留至多 `m+k+1` 个保护点可同时保持强连通、同步、初始集可达和精确目标长度；[只要求同步时](PROOF.md#problem4-synchronizing-slack-collapse)至多需要 `k+2` 个保护点。
- [大保护集区间的极值稳定性](PROOF.md#problem4-protected-size-stabilization)：`m≥4,q≥3m` 时，任意字母表极值在 `r≥q−2m` 后恒定；`m=4,q=13` 的进一步完整排除现已确定所有 `r≥1` 的值为十一。
- [固定余维的参数单调性](PROOF.md#problem4-parameter-monotonicity)：任意字母表极值随 `q`、`r` 分别不减；这约束未解区域的形状，未确定其精确值。
- [全部奇圈长度的纸面压缩界](PROOF.md#problem4-odd-cycle-all-lengths-bound)：`m≥4`、`P_h=C_(2m−1)` 加任意孤点时，`c(S)≤h+m+1`；不要求强连通或字母秩限制。C7 取到等号，C5 有真实反例。
- [保持行秩与实际词秩亏](PROOF.md#problem4-preserved-rank-defect-tradeoff)：全参数秩约束及[嵌套奇圈像障碍](PROOF.md#problem4-odd-image-obstruction)，不将非封闭像当作子自动机。
- [大余维的统一覆盖加强](PROOF.md#problem4-large-codimension-cover-improvement)：同步、`n≥2m,m≥13` 时，`τ(P_h)≥m` 迫使 `c(S)≤h+2m−3`；覆盖全部图形，且已证明不必要求强连通。
- [覆盖界的无界加性改进](PROOF.md#problem4-unbounded-cover-deficit)：任意固定 `a`，充分大的 `m` 都满足上述条件界 `c(S)≤h+2m−a−1`；依赖已有 α-critical 有限基定理，[共同像核心退出界](PROOF.md#problem4-common-image-core-escape)将一般阈值定量为极粗的三层指数塔。
- [余维四的较早覆盖层](PROOF.md#problem4-four-cover-third-layer)：强连通同步、`n≥8,h≥3` 时，`τ(P_h)≥4` 迫使 `c(S)≤h+5`；计算辅助证明。`h=2` 的延伸被一个八状态强连通同步实例否定。
- [余维五的全部覆盖层](PROOF.md#problem4-five-cover-late-layers)：强连通同步、`n≥10,h≥1` 时，`τ(P_h)≥5` 迫使 `c(S)≤h+7`；[四类核心归约](PROOF.md#problem4-next-to-maximal-rank-cores)加全部二十七核心检查。`m=5,q=15` 仍为 `[14,15]`。
- [长安全区间的周期状态约束](PROOF.md#problem4-periodic-isolated-states)：`ac≥2m+2` 时，每个字母至多有 `m−1` 个非周期状态，全部落在同一个至多 `m(m+1)` 点的短对核心中。
- [余量一的旗标归约](PROOF.md#problem4-slack-one-initial-flags)：共同短对距离、轨道秩、实际前像供应及完整终端字母表检查覆盖十二步候选；最后的核心 106 前缀 `(64,128,256)` 现也完整归零，计数见[完整覆盖](PROOF.md#problem4-q13-exact-eleven)。
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
