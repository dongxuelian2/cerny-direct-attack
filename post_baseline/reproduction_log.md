# Baseline 复现日志

日期：2026-09-28
工作目录：<CHECKOUT>
baseline 输入包 SHA-256：62CCF3DA5BABDC02731BE54A7A88444B0AF7235B4FE76357930B4BC754742107

## 环境

- Python：Codex workspace runtime，Python 3.12.14；满足包的 Python 3.10+ 要求。
- Windows 上的系统 Python launcher 未注册解释器，因此实际执行使用 Codex bundled Python。
- Lean：elan/lean shim 可调用，但没有安装 leanprover/lean4:v4.19.0，也没有默认 toolchain。
- Manifest：冻结的 baseline/imported tree 有 125 个文件；MANIFEST.sha256 125/125 匹配；缺失0、哈希错误0、清单与冻结 tree 路径差异0。
- 原始 reference_results 未覆盖；本轮运行产物写入 post_baseline/reproduction/。

## 运行结果

| 检查 | 命令/方式 | 结果 |
|---|---|---|
| 单元测试 | python -m unittest discover -s tests -v | PASS，14 tests，0.189s |
| C_n 已知阈值 | run.py demo --max-n 10 | PASS；C2…C10 为 1,4,9,16,25,36,49,64,81 |
| C8 特征比较 | run.py compare --n 8 | PASS；cardinality=7，marked=19，maxgap=7，gap_multiset=7，identity=49 |
| C8 锚点层级 | run.py landmarks --n 8 | PASS；r=0…8 为 7,7,19,20,21,23,25,49,49 |
| C6 单转移扫描 | run.py mutate --n 6 | PASS，60 个变体都产生并检查证书 |
| baseline 独立证书 | audit/verify_saved_certificates.py | PASS，83/83；55 exact、11 bounds、17 nonsynchronizing |
| 本轮复现实验的证书 | audit/verify_saved_certificates.py | PASS，83/83；55 exact、11 bounds、17 nonsynchronizing |
| reconnaissance 证书 | audit/verify_saved_certificates.py | PASS，76/76；60 bounds、16 exact |
| 合法证书 CLI | src/check_certificate.py reference_results/demo/C4.json | PASS；lower=upper=9，checked_edges=30 |
| 故意破坏证书 | src/check_certificate.py post_baseline/audit/broken_potential.json | 按预期拒绝，exit=2；错误为 mask 15 的 local inequality 不成立 |
| 非同步样例 | run.py solve examples/nonsync3.json，再由 checker 检查 | PASS；闭包不变量含1个非单点 mask |
| Lean 编译 | lean lean/CertificateCore.lean | 未通过环境前置条件；exit=1，no default toolchain configured |

baseline 与本轮 reproduction 两个目录各有85个 JSON：83个证书，另有 environment.json 和 scope.json 两个元数据文件；reconnaissance 保存76个锚点证书。三个目录的证书逐个由 Python checker 重验；变体扫描本身也在生成时检查了全部变体证书。

Lean 编译器入口不是完整工具链。elan toolchain list 返回没有已安装工具链；lean --version 曾尝试访问工具链更新服务并以 SSL credentials 错误失败。显式编译返回 no default toolchain configured。本轮没有安装 Lean，也没有修改 Lean 源码。

Lean source present but not kernel-verified in this environment

## 可复现命令

从项目根目录执行，Python 使用任意可用的 3.10+ 解释器：

~~~~powershell
python -m unittest discover -s tests -v
python run.py demo --max-n 10 --out post_baseline/reproduction/demo
python run.py compare --n 8 --out post_baseline/reproduction/compare_C8
python run.py landmarks --n 8 --out post_baseline/reproduction/landmarks_C8
python run.py mutate --n 6 --out post_baseline/reproduction/mutations_C6
python post_baseline/audit/verify_manifest.py
python post_baseline/audit/verify_saved_certificates.py
~~~~

post_baseline/audit/broken_potential.json 是特意损坏的副本；checker 的失败是预期结果。原始证书和 reference_results 保持原样。

## 原始记录

baseline 上游日志仍保留在 reference_results/tests.log 与 reference_results/clean_start.log。主机实跑的 JSON、CSV 和两个审计脚本保存在 post_baseline/。
