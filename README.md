# Černý 猜想与同步自动机研究

本项目研究同步自动机的重置字、像扩张，以及 avoid-or-compress 问题。
**一般 Černý 猜想与完整 Problem 4 尚未解决。余维四全部参数现已确定：`F_bin(n,n−4,r) = F(n,n−4,r) = min(n−r,11)`。** 上界为纸面归约加完整有限域排除的计算辅助证明，下界为统一二字母构造的纸面证明。余维五全参数上界经全部十七步候选排除进一步降为 `min(n−r,16)`；`m=5,q=15` 仍在 `[14,15]`。

新的纸面推导处理全部奇圈长度，并将大余维、全部短对图形状的条件覆盖界推进一层；有限基论证还给出随余维无界增长的加性改进。它们没有给出全参数的匹配下界。

## 从哪里读

[PROOF.md](PROOF.md) 是唯一的数学研究正文，集中维护问题、定义、推导、反例和未解边界。

- [问题与当前结论](PROOF.md#problem)：先了解正在研究什么、哪些结论仍未完成。
- [下界构造](PROOF.md#constructions)与[低余维上界](PROOF.md#upper)：已有参数族和归约。
- [余维四：短对图与入口排除](PROOF.md#frontier)：[完整布尔旗标](PROOF.md#problem4-eleven-audit)排除达到十二的全部入口组合，适用于任意有限字母表；与二字母下界十一匹配。
- [保护块收缩与新边界](PROOF.md#problem4-protected-collapse-strip)：在不要求收缩后同步的条件下传递短对图与旗标约束，推广精确值十一至整条 `m=4,q=12` 参数边界；对 `q=13` 的等号候选给出十一层公共交集与首入口大小限制。
- [q=13 的精确值十一](PROOF.md#problem4-q13-exact-eleven)：全部二十五核心、早晚分裂及不再增长域均已完整排除；结合保护收缩与二字母构造，对所有 `r≥1` 得到精确值十一。
- [一般目标长度的保护集收缩](PROOF.md#problem4-protected-slack-collapse)：距原上界 `k` 的候选可缩到至多 `k+1` 个保护点，全部字母共享至多 `2^k` 个外部保护入口。
- [稀疏短对图的前像独立性](PROOF.md#problem4-sparse-pair-entrance-independence)：`h≤L−m−2,|P_h|≤4,|P_(h+1)|≤5` 时，实际短保护前像线性独立、数量至多 `k+h`；首层结论适用于 `m=4,L≥12`，未解决剩余前像的后续演化。
- [保持同步与可达的收缩](PROOF.md#problem4-reachable-slack-collapse)：保留至多 `m+k+1` 个保护点可同时保持强连通、同步、初始集可达和精确目标长度；[只要求同步时](PROOF.md#problem4-synchronizing-slack-collapse)至多需要 `k+2` 个保护点。
- [大保护集区间的极值稳定性](PROOF.md#problem4-protected-size-stabilization)：`m≥4,q≥3m` 时，任意字母表极值在 `r≥q−2m` 后恒定；`m=4,q=13` 的进一步完整排除现已确定所有 `r≥1` 的值为十一。
- [固定余维的参数单调性](PROOF.md#problem4-parameter-monotonicity)：任意字母表极值随 `q`、`r` 分别不减；这约束未解区域的形状，未确定其精确值。
- [全部奇圈长度的纸面压缩界](PROOF.md#problem4-odd-cycle-all-lengths-bound)：`m≥4`、`P_h=C_(2m−1)` 加任意孤点时，`c(S)≤h+m+1`；不要求强连通或字母秩限制。C7 取到等号，C5 有真实反例。
- [保持行秩与实际词秩亏](PROOF.md#problem4-preserved-rank-defect-tradeoff)：全参数秩约束及[嵌套奇圈像障碍](PROOF.md#problem4-odd-image-obstruction)，不将非封闭像当作子自动机。
- [大余维的统一覆盖加强](PROOF.md#problem4-large-codimension-cover-improvement)：同步、`n≥2m,m≥13` 时，`τ(P_h)≥m` 迫使 `c(S)≤h+2m−3`；覆盖全部图形，且已证明不必要求强连通。
- [覆盖界的无界加性改进](PROOF.md#problem4-unbounded-cover-deficit)：任意固定 `a`，充分大的 `m` 都满足上述条件界 `c(S)≤h+2m−a−1`；依赖已有 α-critical 有限基定理，[共同像核心退出界](PROOF.md#problem4-common-image-core-escape)将一般阈值定量为极粗的三层指数塔。
- [余维四的较早覆盖层](PROOF.md#problem4-four-cover-third-layer)：强连通同步、`n≥8,h≥3` 时，`τ(P_h)≥4` 迫使 `c(S)≤h+5`；计算辅助证明。`h=2` 的延伸被一个八状态强连通同步实例否定。
- [余维四全参数精确值](PROOF.md#problem4-four-exact-eleven)：七层四点覆盖的 91 类核心及三点覆盖的 10142 个命名域全部排除；`n≥11` 的任意余维四集合均在十一字母内压缩。结合二字母下界得到全参数精确式，并推出余维五十八步上界。
- [余维五十六步上界](PROOF.md#problem4-five-global-sixteen)：完整生成六至十点的 1994 类核心，完整单字母对照与共同距离排除通过；17 类由整个字母池的封闭性排除，其余完成距离检查。已知下界十四，尚未匹配。
- [任意块的共同活动界](PROOF.md#problem4-transversal-all-slack-activity)与[真支持的全部安全层](PROOF.md#problem4-proper-support-guard-tower)：对全部长度≤j 的混合词给出 `2(k−R)+j` 的活动块界；饱和时准确确定禁用状态链，并有每个 k 的真实强连通同步等号构造。这是结构界的等号，尚非原极值的匹配下界。
- [饱和可达并与出口前像](PROOF.md#problem4-saturated-exit-preimages)：不依赖横截分割的出口必要条件；[余维五双共同邻点分支](PROOF.md#problem4-five-double-neighbor-exclusion)的 747 个剩余域已完整排除。十点候选因此只剩具有匹配变化部分的情形；全部参数和其余动态域仍开放。
- [实际短词的有限归约](PROOF.md#problem4-twelve-finite-domains)与[动态必要条件](PROOF.md#problem4-twelve-actual-two-step)：保留持续遗漏孤点的身份，使用双向商图及同字母平方；一般多步共同实现仍待解决。
- [任意余维的多缺口归约](PROOF.md#problem4-multiple-hole-finite-reduction)：利用经典最大独立集交并不等式，将后层全部遗漏状态限制在至多 2m 个；结合前层支持界得到与 n 无关的必要单步域。实际短词的共同实现仍待解决。
- [有限字母与共享身份短词域](PROOF.md#problem4-bounded-word-backward-frame)：选取有界字母子表，并保留短词进入核心的反向邻域，可精确检查有限长度混合词的安全性；是任意余维的必要动态归约，尚未排除余维五候选。
- [短词的持续遗漏孤点界](PROOF.md#problem4-short-word-persistent-holes)：纸面证明适用于相邻压缩谱相差多层的情形。所用支持不等式引用 Gitler–Valencia，未作为新图论定理。
- [余维五的全部覆盖层](PROOF.md#problem4-five-cover-late-layers)：强连通同步、`n≥10,h≥1` 时，`τ(P_h)≥5` 迫使 `c(S)≤h+7`；[四类核心归约](PROOF.md#problem4-next-to-maximal-rank-cores)加全部二十七核心检查。`m=5,q=15` 仍为 `[14,15]`。
- [长安全区间的周期状态约束](PROOF.md#problem4-periodic-isolated-states)：`ac≥2m+2` 时，每个字母至多有 `m−1` 个非周期状态，全部落在同一个至多 `m(m+1)` 点的短对核心中。
- [余量一的旗标归约](PROOF.md#problem4-slack-one-initial-flags)：共同短对距离、轨道秩、实际前像供应及完整终端字母表检查覆盖十二步候选；最后的核心 106 前缀 `(64,128,256)` 现也完整归零，计数见[完整覆盖](PROOF.md#problem4-q13-exact-eleven)。
- [全状态循环类的精确极值](PROOF.md#problem4-full-cycle-exact)：n>2m 时全部参数为 min(s−r+1,2m+1)，三字母全参数达界、gcd(n,m)=1 时二字母达界；[双链刚性](PROOF.md#problem4-signed-chain-rigidity)排除已有下界族的全部非原型颜色重排与换轨选择。
- [二次提升与全部词长的共同退出](PROOF.md#problem4-quadratic-exit-sparsification)：用 O(m²) 个原字母同时保持后层全部最大集的精确退出长度，改进既有指数字母数界；不声称保留全自动机同步性或获得新的全局数值上界。
- [保护覆盖饱和的有效余维](PROOF.md#problem4-protected-cover-saturation)：保护条件饱和时用剩余覆盖数控制退出；[真实安全族秩障碍](PROOF.md#problem4-real-safe-family-rank-barrier)说明加入全部实际短词与可达性后，全族行秩仍可随 n 无界，不能代替同一个 S 的轨道。
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
