# ORION SyncLab：从这里开始

## OpenMath final submission (2026-10-03)

Read [OPENMATH_SUBMISSION.md](../../OPENMATH_SUBMISSION.md) for the audited final
scope, exact theorem inventory and reproduction commands. Ten authoritative
Lean modules form the submission core. The general Černý conjecture remains
open; paper results and Python/C++ evidence are separately labelled.
`lean/Cerny3.lean` and `lean/Cerny4.lean` are frozen, noncompiling baseline
drafts; use `post_baseline/lean_sprint/Cerny3Checked.lean` and
`Cerny4Checked.lean`. [STATUS.json](../../STATUS.json) separates FINAL validation
from the historical imported baseline. `MANIFEST.sha256` and the original
manuals retain that baseline's scope. The actual
[final completion receipt](../../submission/COMPLETION.md) explains immutable release
identity, the seal and the detached complete-ZIP checksum.

The original getting-started text below records that baseline's scope.

本项目研究有限状态系统的同步证书与信息边界。首先复现经典 Černý 自动机，再研究压缩状态信息如何影响可证明的最短性。完整手册在 docs/ 中。

## 现在只做这三件事

解压整个文件夹，在含有 run.py 的文件夹打开终端，使用 Python 3.10 或更新版本。Windows 可以将下面的 python 换成 py；Linux/macOS 可以换成 python3。无需安装任何第三方 Python 包。

```bash
python run.py demo
python run.py compare --n 8
python -m unittest discover -s tests -v
```

第一条命令应产生 C2 到 C8 的结果，最短长度依次为 1、4、9、16、25、36、49。第二条命令应给出五种信息表示的下界；其中 marked 为 19、identity 为 49。最后一条命令当前应运行 14 个测试方法并以 OK 结束。测试方法内部包括全部 729 个三状态双字母自动机、128 个固定种子随机实例和证书破坏测试。

## 第一个真正的研究任务

运行 `python run.py landmarks --n 8`，观察只记录部分位置时的认证下界。随后阅读 `docs/THEORY.md` 中的两个锚点定理和旋转不变性障碍，选择一个命题完成 Lean 形式化，再尝试推广到 r 个锚点。相关闭式的纸面证明已附；其文献新颖性需另行核对。

## 原始 baseline 交付状态（历史记录）

Python 搜索、独立检查器、比较实验、局部变体扫描、测试均已在准备环境实跑。`reference_results/` 保存这些运行产生的结果。Lean 文件是尚未在准备环境编译的源码草案；本包不声称已通过 Lean 或赛事评审。先运行手册列出的编译命令，保存日志，再更新自己的状态记录。

`VERIFIED` 在 Python 输出中仅表示独立 Python 检查器接受该证书，不等同于 Lean 内核认证。所有 baseline 及 AI 辅助应在参赛材料中如实记录。本项目不自动调用任何付费 API，不修改系统设置，也不会自动提交外部平台。
