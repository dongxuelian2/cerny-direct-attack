# Černý 猜想与同步自动机研究

本项目研究同步自动机的重置字、像扩张，以及 avoid-or-compress 问题。
设可达像 S 的大小为 s，非空真保护子集 A 的大小为 r，m=n−s、q=n−r。
**余维四、五全部参数现已确定：`F_bin(n,n−4,r) = F(n,n−4,r) = min(q,11)`，`F_bin(n,n−5,r) = F(n,n−5,r) = min(q,14)`。** 上界为纸面归约加完整有限域排除的计算辅助证明，下界有二字母可达构造的纸面证明。

一般 Černý 猜想与完整 Problem 4 尚未解决。已确定区域为全部 m≤5，以及 m≥6、q≤3m−1；剩余精确极值区域为 m≥6、q≥3m。`min(q,3m−1)` 在 m≥4 时的通项仍是猜想。

## 阅读路线

- [正式论文](papers/problem4/main.tex)：余维四、五精确值、匹配二字母构造、完整有限归约与计算证据。
- [论文主线与计算依据](PROOF.md#problem4-paper-synthesis)：证明依赖、有限域覆盖与复现范围。
- [共用结构机制](PROOF.md#problem4-shared-proof-mechanisms)：实际前缀严格增长、Johnson 邻接保持与支撑封闭；[前缀外边界](PROOF.md#problem4-johnson-prefix-exterior)、[计数界](PROOF.md#problem4-johnson-exterior-boundary)和[分量闭合](PROOF.md#problem4-johnson-component-prefix)作为多核心共用工具。
- [证明结构压缩](PROOF.md#problem4-proof-structure-compression)：暂时冻结新增核心覆盖；五个已有分支改为一般引理的推论，另吸收一个实际第二层锚点步骤，并逐项说明仍需局部论证的假设障碍。
- [余维三纸笔证明](PROOF.md#problem4-paper-dependency-reductions)：九步压缩上界；[单边障碍](PROOF.md#problem4-single-edge-obstruction)及[两例外](PROOF.md#problem4-two-exception-closure)、[三例外](PROOF.md#problem4-three-exception-closure)、[交换孔](PROOF.md#problem4-disjoint-exchange-holes)结构界。
- [余维四核心归约](PROOF.md#problem4-common-hole-complete-core)：公共孔整核、[K₅删边整核](PROOF.md#problem4-doubleton-complete-core)和[三角交换孔](PROOF.md#problem4-triangle-exchange-classification)。十七个完整核心覆盖221个命名域，另有部分核心2域，共223域；三角交换孔仍有两种后层形状未闭合。
- [余维五结构替代](PROOF.md#problem4-three-exception-closure)：521类核心、7,519个曾需动态检查的域已有纸笔替代；其他分支继续使用完整计算证明。
- [全部参数与开放问题](PROOF.md#problem)：余维四、五精确值；[下界构造](PROOF.md#constructions)、[余维六界](PROOF.md#problem4-six-upper-twenty-four)与[线性通项猜想](PROOF.md#problem4-linear-codimension-conjecture)。


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

