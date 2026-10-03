# 锚点层级 reconnaissance（post-baseline）

## 定义与范围

对每个 n=5,…,12，运行 baseline 的 run.py landmarks 命令。它对该 C_n 枚举所有非空子集，按特征 α_r(S)=(|S|,成员位于 A_r) 合并为特征类，以“存在某个代表集合和字母”的规则建边，再用精确 BFS 求从 α_r(Q) 到任一单点类的最短距离 B_r(n)。因此表内数值是这张有限抽象图的精确距离；它们不是 heuristic，也不构成关于任意 n 的证明。

锚点顺序固定为 A_0=∅，A_r=(0,n−1,n−2,…,n−r+1)。不能在解释数据时改变顺序或抽象边含义。

## 可复现命令

从项目根目录执行。Python 需要 3.10 或更新版本。

~~~~powershell
python run.py landmarks --n 5 --out post_baseline/reconnaissance/landmarks_C5
python run.py landmarks --n 6 --out post_baseline/reconnaissance/landmarks_C6
python run.py landmarks --n 7 --out post_baseline/reconnaissance/landmarks_C7
python run.py landmarks --n 8 --out post_baseline/reconnaissance/landmarks_C8
python run.py landmarks --n 9 --out post_baseline/reconnaissance/landmarks_C9
python run.py landmarks --n 10 --out post_baseline/reconnaissance/landmarks_C10
python run.py landmarks --n 11 --out post_baseline/reconnaissance/landmarks_C11
python run.py landmarks --n 12 --out post_baseline/reconnaissance/landmarks_C12
python post_baseline/reconnaissance/aggregate_landmarks.py
python post_baseline/audit/verify_saved_certificates.py
~~~~

每个 landmarks_Cn 目录保存 r=0…n 的 JSON 证书和 landmarks.csv。all_landmarks.csv 保存76行原始结果；summary.csv 提取 B0…B4、B_(n−2)、B_(n−1)、B_n。aggregate_landmarks.py 从每个目录的 CSV 重建汇总。每个 JSON 都由 landmark_experiment 中的 checker 检查，并可由 verify_saved_certificates.py 再次检查。

## 起点距离表

| n | C_n reset 长度 | B0 | B1 | B2 | B3 | B4 | B_(n−2) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 16 | 4 | 4 | 10 | 11 | 16 | 11 |
| 6 | 25 | 5 | 5 | 13 | 14 | 15 | 15 |
| 7 | 36 | 6 | 6 | 16 | 17 | 18 | 20 |
| 8 | 49 | 7 | 7 | 19 | 20 | 21 | 25 |
| 9 | 64 | 8 | 8 | 22 | 23 | 24 | 30 |
| 10 | 81 | 9 | 9 | 25 | 26 | 27 | 35 |
| 11 | 100 | 10 | 10 | 28 | 29 | 30 | 41 |
| 12 | 121 | 11 | 11 | 31 | 32 | 33 | 47 |

B_(n−1) 和 B_n 都等于对应的已知真实 reset length，因为该特征能识别全部非空子集；这些列不是新发现。C8 的完整 r 表在 reference_results/landmarks_C8；marked_scaling.csv 已含 n=3…12 的 B2 值。n=8 的对应行和全部 B2 行是复跑，不计入新增数学。

## 目前观察与研究状态

- B3 的值为 11、14、17、20、23、26、29、32，与 3n−4 一致。B3(8)=20 已在 baseline；其他本表 n 值补充了 baseline 之外的实例。猜测 B3(n)=3n−4（n≥5），尚未证明。
- B1 在这组数据中与 B0 相同，均为 n−1。一般 n 的等式尚未证明。
- 在本次数据的 15 个三角区域参数对 4≤r≤n−4（n=8…12）上，B_r(n)=3n+2r−11。它只是有限观察。
- B_(n−2) 在 n=5…12 为 11、15、20、25、30、35、41、47；在本次范围内没显示与 B3 一样清楚的式子。
- baseline 已证明 B2(n)=3n−5（n≥3）。本实验对这些 B2 数值的复跑不能重新登记为新结果。

## 原始材料

原始 JSON 和逐 n CSV 仍保留在本目录。POST_BASELINE_RESEARCH_LEDGER.md 记录了 baseline/new 的逐项边界与唯一推荐目标。
