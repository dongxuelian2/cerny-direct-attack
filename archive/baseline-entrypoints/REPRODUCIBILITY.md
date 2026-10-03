# 复现、版本与交付状态

Current final-submission checks and proof status are in
[OPENMATH_SUBMISSION.md](../../OPENMATH_SUBMISSION.md) and `submission/`.
The [final completion receipt](../../submission/COMPLETION.md) describes archive
verification. The ten authoritative Lean modules were compiled and validated;
the two frozen drafts remain excluded. [STATUS.json](../../STATUS.json) records both
the final status and the preserved historical baseline.
This page's original v1.0 environment and uncompiled-Lean statements below
are historical baseline records. `MANIFEST.sha256` seals the imported Git
baseline; `submission/SHA256.json` seals the final package. The baseline
checker reports explicitly documented preparation overrides separately.

以下为原始 baseline v1.0 的历史记录，准备日期为 2026-09-27。手册内容保持原样，发布时仅改为 ASCII 文件名：[PDF 手册](../../docs/ORION_RESEARCH_MANUAL.pdf)、[Word 手册](../../docs/ORION_RESEARCH_MANUAL.docx)；Markdown 版在 docs/ 中。

## 已实际运行的部分

准备环境为 CPython 3.13.5、Linux x86_64；Python 部分只使用标准库。reference_results/tests.log 保存 14 个测试方法的完整通过日志；方法内部覆盖全部 729 个有标号三状态双字母自动机、128 个固定种子随机实例、经典族、特征比较、边界条件及错误证书拒绝。reference_results/clean_start.log 保存从全新复制目录运行 sh start_unix.sh 的输出和退出码。STATUS.json 记录全部随包证书再次独立检查的数量。

Windows 批处理启动器已提供，准备环境未在 Windows 上运行它。macOS 用户可使用 Unix 启动脚本，但本包的实际平台测试记录来自 Linux。最低支持目标为 Python 3.10；其他版本由使用者重跑测试确认。

## 结果对应关系

reference_results/demo 对应 C2 至 C10 的精确实例；compare_C8 对应五种特征的比较；landmarks_C8 对应 0 至 8 个锚点；mutations_C6 对应全部 60 个单转移修改；marked_scaling.csv 对应 n=3 至 12 的两锚点数据。运行命令生成的新文件默认进入 results/，不会覆盖 reference_results/。

所有 JSON 证书同时保留自动机定义。对任意证书可运行 python src/check_certificate.py 文件路径。此命令不调用搜索程序。Python 的 VERIFIED 表示独立 Python 检查器接受，不代表 Lean 内核已接受。

## 原始 baseline 尚未完成的形式化工作（历史记录）

lean/ 中提供一般势函数下界和具体实例的 Lean 源码草案。准备环境缺少可用 Lean 编译器，未取得工具链；因此没有 Lean 通过日志。使用指定工具链实际运行手册第 11 节的命令，修复编译错误并保留日志后，才能更新验证状态。抽象闭式及一般 DFA 语义连接是手册明确列出的后续任务。

## 来源与贡献记录

本包属于 AI 辅助形成的准备基线，包含代码、实跑数据和纸面推导。经典 Černý 族的阈值及一般最短路径原理应保留来源；指定抽象的信息边界结论仍需独立文献查重和数学复核。赛事基线、窗口内增量、作者与工具贡献应分别记录，不将已有材料自动登记成新增成果。

## 文件完整性

MANIFEST.sha256 保留原始 baseline 文件的 SHA-256 和历史文件名；清单自身不计入清单。`sha256sum -c MANIFEST.sha256` 仅适用于原始 baseline 的原始字节序列，不适用于最终包。最终 Git checkout 使用 `python submission/check.py --suite integrity`；解压后的最终 ZIP 使用 `python submission/package.py --check-extracted`。重命名映射在 [submission/PATH_MIGRATIONS.json](../../submission/PATH_MIGRATIONS.json)。哈希校验不代替数学或软件正确性验证。
