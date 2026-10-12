# Open Problem 4 研究交接

同步日期：2026-10-12（Asia/Shanghai）。这是 Szykuła 2026 年综述中的
avoid-or-compress 问题。论文作者为 Qichao Wang，河北工业大学。
**当前是部分解答，完整问题仍未解决；不构成一般 Černý 猜想的证明。**

## 建议阅读顺序

1. [main.pdf](main.pdf) / [main.tex](main.tex)：当前七页论文及精确假设。
2. [PROOF_AUDIT.md](PROOF_AUDIT.md) 和
   [reproducibility/CODIMENSION_THREE_UPPER_PROOF.md](reproducibility/CODIMENSION_THREE_UPPER_PROOF.md)：证明边界与计算辅助证明入口。
3. [reproducibility/README.md](reproducibility/README.md)：109 个文件的论文补充材料、构造、独立检查器与有限证书。
4. [investigation/active_research.json](investigation/active_research.json)：接续研究的当前机器可读状态，重点看 `next_structural_work`。
5. [investigation/CURRENT_FRONTIER.md](investigation/CURRENT_FRONTIER.md)：按时间追加的研究记录；以末尾 2026-10-12 的 native geometry 更新为准。
6. [investigation/AUXILIARY_AUDIT_20261012_11.json](investigation/AUXILIARY_AUDIT_20261012_11.json)：最新累计 183 项辅助审计及来源哈希。

## 已证明或已核验的结论

令 `m=n-s`、`q=n-r`；二元字母表与任意有限字母表的两个极值都满足：

| 参数区域 | 精确值 |
|---|---|
| m=0 | 1 |
| 1<=m<=3 | min(q,3m) |
| m>=4 且 q<=3m-1 | q |

所有下界构造均为二元、强连通、同步自动机，S 为实际可达像。
对固定 `s-r>=3`，cofinal 构造在每个 `n>=2s-r-1` 达到 q。
任意有限字母表的余维三压缩上界为 9（n>=6；该上界不要求 S 可达），
证明包含符号归约和完整的计算辅助分类，不是 Lean 形式化证明。
猜测式 `min(n-r, binom(n-s+2,2))` 在
`n>=11,s=n-3,1<=r<=n-10` 被反驳，两个极值均为 9，而猜测式为 10。

有限证书核验了 290 个精确参数：n<=12 的全部 286 个参数，以及
(13,8,1)、(13,10,1)、(13,10,2)、(13,10,3)。有限核验与全参数证明的范围分别记录。
新颖性核查见 [LITERATURE_NOVELTY_AUDIT.md](LITERATURE_NOVELTY_AUDIT.md)，不作优先权保证。

## 未决问题与下一步位置

尚未整体确定的区域是 `m>=4,q>=3m`。最小未决点的二元和任意字母表极值
`F_bin(13,9,1)`、`F(13,9,1)` 均仍在 **[11,12]**，未发现字母表分离。

10 月 11 日的 C1 word-staircase 排除了最后一个 B3 几何，完整 B3 范围已排除。
随后 inverse-union、B2 first-pair、column、single-class 和 few_graph_06 到
few_graph_12 证书继续缩小辅助分类；10 月 12 日再经 graph-first quotient、
supplier、inverse-native 和 real-filtration 的完整原生范围排除，任意字母表
剩余 73 个 B1/B2 几何、0 个 B3、16 个 joints；binary 剩余
63 types / 348 profiles / 66 geometries / 15 joints。
最新累计审计核验 183 项通过报告、3,395 条来源绑定和 1,349 个最新绑定来源。
这些是条件结构排除，不能据此宣布新的极值或完整上界。

接手者应处理剩余 73 个任意字母表几何和 63 个 binary types / 348 个 profiles，
先读 [CONTINUATION_20261012.md](investigation/CONTINUATION_20261012.md)，包括
candidate967 的两段完整范围与数据恢复位置，再从 [FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md](investigation/FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md)、
[FEW_GRAPH_CERTIFICATE_README.md](investigation/FEW_GRAPH_CERTIFICATE_README.md)、
[BASIS_COLUMN_REACHING_PRUNING.md](investigation/BASIS_COLUMN_REACHING_PRUNING.md)
及 `active_research.json` 的 `graph_first_quotient_cuts` 接续。其旧
`next_structural_work` 摘要仍写 84/74；原始字节受审计绑定，以本次 73/63/348
计数与 continuation 说明为准。沿用可参数化的 full-pair
drivers，保留 native fields、whole-graph transports、四份 profile-cut 列表和实际可达性。
深度至少四的 column deductions 要求完整实际 prefix span；旧 28 个预算耗尽探测仍是未知。
不要把 basis-image safety 当充分条件，也不要假设平面不变。

旧 `P2<=5,P3<=6,P4<=7` 的无依据使用及相应负面搜索结论已撤回。
远程已另有 [short-pair peeling 证明](../../proofs/paper/problem4_short_pair_peeling.md)
和 [P6 C7 排除](../../proofs/paper/problem4_c7_sixth_layer.md)：在它们的精确假设下
可使用新证明的 `|P_h|<=h+3`（1<=h<=7），但新证明不追认旧失效搜索报告。
超时、受限族搜索失败和正向 maximal graph 均不是全局上界或实际 witness。
历史审计是对应时点的记录；当前状态以最新累计审计和 active_research 为准。

## 文件保存及验证

沿用现有 `paper/avoid_compress/` 路径；既有 `direct_attack/`、Lean、OpenMath
冻结成果保持原样。论文、补充材料、所有唯一 investigation 源码/数据/日志、
原有 68 个不可变证书归档及三个发布归档均保留；另外保留历史 inverse-union
探索归档，并同步本轮 14 份原始证书/范围归档及一份绑定来源归档。
本轮有证明价值的 `_qa/` 源码、笔记、证书及哈希绑定数据也纳入交接；数据可由
`hydrate_large_data.py` 按原路径恢复。
其他未绑定的 `_qa/`、`_release_*/`、编译产物、缓存和
重复版面截图留在本地，均可由源码重新生成。此外，`_qa/` 中四个被最新审计
直接哈希绑定的参考文献标题校准源码/记录；它们也随本次交接保存。

少量历史 solver command receipts 含本机绝对路径；为保留哈希绑定的原始证据，
它们按原始字节存入 [historical-local-receipts.zip](investigation/historical-local-receipts.zip)，
不是可直接运行的跨平台命令。需要旧脚本在原位置读取这些日志时，可在 investigation 中运行
`python -B hydrate_historical_receipts.py`；解包前逐文件校验，原始日志默认不进入 Git。
辅助证书 ZIP 和历史 receipt 不赋予 solver timeout 任何证明地位。

166 MB 的 `c1_word_staircase_inventory.json` 超过 GitHub 单文件限制，其原始字节
已完整存于现有 `certificates/c1_word_staircase.zip`；
[large_data_manifest.json](investigation/large_data_manifest.json) 记录原始哈希、大小和归档成员。
在 investigation 中运行 `python -B hydrate_large_data.py` 可逐字节校验并恢复，
完整性检查无需先解包。其他唯一源码和数据沿用原路径。

[inverse_union_exploration.zip](investigation/certificates/inverse_union_exploration.zip)
保存旧探索源码、逐案例探测、批次摘要和 28 个预算耗尽记录的上下文。
其中历史部分报告绑定过旧版本，归档的 `ARCHIVE_INDEX.json` 已明确列出；
这些探索记录不具有最新已接受证书的证明地位。

仓库根目录的交接完整性检查（不运行新搜索）：

```sh
python -B paper/avoid_compress/check_sync_integrity.py
python -B scripts/reproduce.py --suite all
```

论文独立复现命令见 supplement README。运行会产生新 provenance 字段，建议在
`.reproduction/` 的副本中执行；不要覆盖冻结审计。最新 first-pair 证书可在独立目录
解压 `investigation/certificates/few_graph_12_first_pair.zip`，按其 README 复现。

本次实际检查范围和结果见 [SYNC_VALIDATION.json](SYNC_VALIDATION.json)；
[SYNC_SHA256.json](SYNC_SHA256.json) 绑定交接文件的原始字节，仓库 publication seal
另外绑定所有 Git 跟踪文件。原始历史清单保持其原先范围。
