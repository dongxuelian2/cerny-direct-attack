# Černý 猜想与同步自动机研究

本项目研究同步自动机、子集压缩以及 avoid-or-compress 问题。设状态数为 `n`，初始像大小 `s=n−m`，保护子集大小 `r`，并记 `q=n−r`。

## 主要结果

- **余维三（纸面证明）：** 对每个 `n≥5`、`1≤r<n−3`，
  `F_bin(n,n−3,r) = F(n,n−3,r) = min(q,9)`。其中 `n≥6` 的九字母压缩上界由早期短对结构分类、轨迹秩与原字母作用证明；二字母构造给出匹配下界。
- **余维四（计算辅助证明）：** `F_bin(n,n−4,r) = F(n,n−4,r) = min(q,11)`。
- **余维五（计算辅助证明）：** `F_bin(n,n−5,r) = F(n,n−5,r) = min(q,14)`。

余维四、五的上界使用数学归约与完整有限域计算，匹配下界来自二字母构造。一般 Černý 猜想及 `m≥6, q≥3m` 的全部精确极值仍是开放问题。

## 论文与证明

- [现有论文源码](papers/problem4/main.tex)：余维四、五精确结果、构造及计算辅助证明。保持现有主定理和有限覆盖；不追加大批局部纸面特例。
- [余维三的完整证明主线](PROOF.md#problem4-codimension-three-upper-proof)：九种短对类型及 `c(S)≤9`；[统一秩与实际像引理](PROOF.md#problem4-paper-three-domain-ranks) 给出纸面替代。
- [余维三的独立证明](PROOF.md#problem4-defect-three-independent-lemmas)：来自 PR #18 的五圈出口和紧层核心引理，作为交叉核验；[验证命令](docs/RUNNING.md#codimension-three-independent-controls)。
- [完整研究正文](PROOF.md)：余维四、五计算归约、覆盖范围、历史引理和其他结构结果。
- [运行说明](docs/RUNNING.md)：论文编译、验证程序及大型计算的复现命令。

论文以余维三的纸面证明和余维四、五的完整计算辅助结果为重点。局部结构替代、探索记录及对应小域控制在研究正文中保存，不扩张论文的主证明链。

## 运行

Python 3.10+ 与 C++17。研究程序通过 `run.py` 启动；编译论文不会自动运行枚举。

```sh
python3 run.py upper
python3 run.py script scripts/problem4/check_paper_rank_reductions.py
python3 run.py script scripts/problem4/check_type6_single_exit_lemma.py
python3 run.py open-point
```

更多运行方式见 [RUNNING.md](docs/RUNNING.md)。临时构建产物保存在被忽略的 `build/` 下，源码及数学正文保留版本记录。项目代码采用 MIT 许可。
