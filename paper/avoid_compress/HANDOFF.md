# Open Problem 4 研究交接

同步日期：2026-10-10（Asia/Shanghai）。这是 Szykuła 2026 年综述中的
avoid-or-compress 问题。论文作者为 Qichao Wang，河北工业大学。
**当前是部分解答，完整问题仍未解决；不构成一般 Černý 猜想的证明。**

## 建议阅读顺序

1. [main.pdf](main.pdf) / [main.tex](main.tex)：当前七页论文及精确假设。
2. [PROOF_AUDIT.md](PROOF_AUDIT.md) 和
   [reproducibility/CODIMENSION_THREE_UPPER_PROOF.md](reproducibility/CODIMENSION_THREE_UPPER_PROOF.md)：证明边界与计算辅助证明入口。
3. [reproducibility/README.md](reproducibility/README.md)：109 个文件的论文补充材料、构造、独立检查器与有限证书。
4. [investigation/active_research.json](investigation/active_research.json)：接续研究的当前机器可读状态，重点看 `next_structural_work`。
5. [investigation/CURRENT_FRONTIER.md](investigation/CURRENT_FRONTIER.md)：按时间追加的研究记录；以末尾 2026-10-10 的 C3 staircase 更新为准。
6. [investigation/AUXILIARY_AUDIT_20261010_22.json](investigation/AUXILIARY_AUDIT_20261010_22.json)：最新累计辅助审计及来源哈希。

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

最新 C3 staircase 证书排除了全部四个剩余 C3 third geometries；独立检查
重建 748,788 个字母并核验 6,152 个 flag-tree 节点。辅助分类中剩余
136 个 B1/B2 加 1 个 B3 几何（共 137，21 个 unrestricted joints）；
binary 范围仍为 105 types / 448 profiles / 120 geometries / 18 joints。
这些是条件结构排除，不能据此宣布新的极值或完整上界。

接手者优先处理唯一剩余 B3 几何 **b3_mixed_c1_third2**，从
[C3_STAIRCASE_EXCLUSION.md](investigation/C3_STAIRCASE_EXCLUSION.md)、
[B3_STAIRCASE_CERTIFICATE_README.md](investigation/B3_STAIRCASE_CERTIFICATE_README.md)
及 `active_research.json` 的 `next_structural_work` 接续：完整保留 first-pair / plane
域及四顶点平面中的所有实际 R 选择，继续使用 literal kernel-atom pools 和 staircase flags，
随后推广到剩余 B1/B2 范围。不要把 basis-image safety 当充分条件，也不要假设平面不变。

旧 `P2<=5,P3<=6,P4<=7` 剪枝已撤回；不能复用相应负面搜索结论。
超时、受限族搜索失败和正向 maximal graph 均不是全局上界或实际 witness。
历史审计是对应时点的记录；当前状态以最新累计审计和 active_research 为准。

## 文件保存及验证

沿用现有 `paper/avoid_compress/` 路径；既有 `direct_attack/`、Lean、OpenMath
冻结成果保持原样。论文、补充材料、所有唯一 investigation 源码/数据/日志、
56 个证书归档及三个发布归档均保留。`_qa/`、`_release_*/`、编译产物、缓存和
重复版面截图留在本地，均可由源码重新生成。例外是 `_qa/` 中四个被最新审计
直接哈希绑定的参考文献标题校准源码/记录；它们也随本次交接保存。

少量历史 solver command receipts 含本机绝对路径；为保留哈希绑定的原始证据，
它们按原始字节存入 [historical-local-receipts.zip](investigation/historical-local-receipts.zip)，
不是可直接运行的跨平台命令。需要旧脚本在原位置读取这些日志时，可在 investigation 中运行
`python -B hydrate_historical_receipts.py`；解包前逐文件校验，原始日志默认不进入 Git。
辅助证书 ZIP 和历史 receipt 不赋予 solver timeout 任何证明地位。

仓库根目录的交接完整性检查（不运行新搜索）：

```sh
python -B paper/avoid_compress/check_sync_integrity.py
python -B scripts/reproduce.py --suite all
```

论文独立复现命令见 supplement README。运行会产生新 provenance 字段，建议在
`.reproduction/` 的副本中执行；不要覆盖冻结审计。当前辅助 C3 证书可在独立目录
解压 `investigation/certificates/c3_staircase.zip`，按其 README 复现。

本次实际检查范围和结果见 [SYNC_VALIDATION.json](SYNC_VALIDATION.json)；
[SYNC_SHA256.json](SYNC_SHA256.json) 绑定交接文件的原始字节，仓库 publication seal
另外绑定所有 Git 跟踪文件。原始历史清单保持其原先范围。
