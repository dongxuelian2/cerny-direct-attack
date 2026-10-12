# Problem 4：2026-10-12 研究交接

本次快照截至 `AUXILIARY_AUDIT_20261012_11.json`，也纳入上次提交后生成的
`AUXILIARY_AUDIT_20261011_13.json`。累计 183 项通过报告、3,395 条来源绑定、
1,349 个最新绑定来源。论文及发布成果保持原样；两个极值在 (13,9,1) 仍为
**[11,12]**，没有完整解答、字母表分离或新的 Lean 定理。

## 本轮已接受的条件排除

这些报告覆盖其明确给出的完整 native geometry / first-pair 范围，前提是
目标 avoid-or-compress 长度达到 12 及报告列出的 equality / flag 归约。

| 方法 | 几何与报告 |
|---|---|
| graph-first quotient | `b1_out_c3_third10_graph_quotient_full_audit.json`、`b1_out_c3_third11_graph_quotient_full_audit.json` |
| supplier-image | `b2_in_c5_third3_supplier_image_full_audit.json`、`b2_mixed_c6_third11_supplier_image_full_audit.json`、`b1_out_c3_third12_supplier_image_full_audit.json` |
| inverse-native | `b2_mixed_c4_third7_inverse_native_full_audit.json` |
| real filtration | `b2_in_c5_third4_filtration_full_audit.json`、`b2_in_c5_third1_filtration_full_audit.json`、`b2_in_c1_third3_filtration_full_audit.json`、`b1_out_c4_third3_filtration_full_audit.json` |
| binary scope，再组合为 arbitrary scope | `b2_mixed_c4_third2_binary_supplier_full_audit.json`、`b2_mixed_c4_third2_composite_filtration_full_audit.json` |

组合后任意字母表剩余 **73 个 B1/B2 几何 / 16 joints**，B3=0；binary 剩余
**63 types / 348 profiles / 66 geometries / 15 joints**。保留四份既有 profile-cut
列表，不把条件结构排除当成新的极值。

`b2_mixed_c4_third2` 的任意字母表排除必须合并完整的 **0..966** 和
**967..1638** 两个范围。第一份报告的 candidate967 不计为负面结果；其排除
来自第二份完整证明。组合报告及 scope-assembly controls 是接续时的必读证据。

## 接续位置与证明限制

先读 [CURRENT_FRONTIER.md](CURRENT_FRONTIER.md) 末尾本轮更新，以及
[最新累计审计](AUXILIARY_AUDIT_20261012_11.json)。`active_research.json` 的
`graph_first_quotient_cuts` 和前沿计数字段记录本轮结果；它的
`next_structural_work` 仍保留较早的 84/74 摘要。该文件被最新审计按原始字节绑定，
本次不修改它；后续范围以本说明的 73/63/348 和最新审计为准。

关键证明笔记：

- [GRAPH_FIRST_TRANSPORTS.md](../_qa/GRAPH_FIRST_TRANSPORTS.md)：完整图与 first-pair 的传输。
- [SUPPLIER_IMAGE_PROPAGATION.md](../_qa/SUPPLIER_IMAGE_PROPAGATION.md)、[SUPPLIER_ESCAPE_WORDS.md](../_qa/SUPPLIER_ESCAPE_WORDS.md)：supplier 与实际词约束。
- [REAL_FILTRATION_POOL_20261012.md](../_qa/REAL_FILTRATION_POOL_20261012.md)：完整 literal pool 的实际 flag 必要条件。
- [FLAG_STABILIZER_QUOTIENT_20261012.md](../_qa/FLAG_STABILIZER_QUOTIENT_20261012.md)：stabilizer quotient 的精确前提。
- [FOLD_COMPRESSIBILITY_PREMISE_20261012.md](../_qa/FOLD_COMPRESSIBILITY_PREMISE_20261012.md)：folded 对应关系仍需的前提，不能据此宣称完整 folded-profile transport。

代码入口包括 `_qa/audit_replayed_filtration_full_20261012.py`、
`_qa/audit_replayed_composite_filtration_20261012.py`、
`_qa/audit_full_graph_quotient.py` 和 `_qa/audit_full_supplier_image_quotient.py`。
原始入口可能检查旧 isolated reproduction 目录；从证书包自身的 README 和
checksums 复现能避免把本机目录当作公共依赖。不要覆盖冻结报告。

## 数据保存与复现

本轮 14 份原始证书/范围 ZIP 沿用 `_qa/certificates/` 原路径。
哈希绑定的 QA 数据按原始字节保存在这些 ZIP 或
`investigation/certificates/qa_bound_sources_20261012.zip` 中，映射见
[large_data_manifest.json](large_data_manifest.json)。其中两份新原始数据分别约
185 MB 和 139 MB，均完整保存。需要原路径数据时，在 investigation 中运行
`python -B hydrate_large_data.py`；恢复前逐文件校验，已有不同字节的文件不会被覆盖。

完整性检查不需要先恢复数据。同步时的实际检查范围见
[SYNC_VALIDATION.json](../SYNC_VALIDATION.json)。昂贵的完整 case 再生成保持为
原始哈希绑定的独立复现记录；旧 28 个预算耗尽探测仍是未知。
