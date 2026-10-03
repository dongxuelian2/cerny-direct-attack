# ORION 项目：Post-baseline 研究台账

日期：2026-09-28
范围：冻结 ZIP 中的内容作为既有 baseline；后续计算只写入本分支的 post_baseline 目录。

Historical research ledger: baseline status descriptions below refer to the
imported kit at the stated date. Current FINAL validation is in
[OPENMATH_SUBMISSION.md](OPENMATH_SUBMISSION.md) and
[STATUS.json](STATUS.json). Manual filenames below were updated for portable
packaging; the originals remain in immutable historical manifests and receipts.

## Provenance 与验证边界

- 输入压缩包：<LOCAL_PATH>
- 输入 ZIP SHA-256：62CCF3DA5BABDC02731BE54A7A88444B0AF7235B4FE76357930B4BC754742107
- 解压目录：<CHECKOUT>
- 冻结 baseline commit：b36adeac34a5088a7e2cd588f8c55221d04bd6eb
- 研究分支：research/post-baseline-r-anchor
- ZIP 未移动、覆盖或重新打包。冻结提交保留了完整的导入内容。
- MANIFEST.sha256 的 125 个条目全部匹配；未发现缺失或额外的导入文件。清单自身不列入其中。
- baseline 的“数学证明”表示包内有可读的纸面证明；不表示该证明已经过 Lean 内核验证。
- OPEN_AFTER_BASELINE 表示压缩包未解决此问题；本轮没有作文献新颖性审计，不能据此声称它在数学文献中仍是开放问题或具有优先权。

## 项目地图

| 路径 | 作用 | 研究入口 |
|---|---|---|
| README.md、START_HERE.md | 快速开始、三条首跑命令、状态声明 | 首次复现 |
| STATUS.json、REPRODUCIBILITY.md | 准备环境、测试数量、运行平台和 Lean 状态 | baseline 环境与验证范围 |
| MANIFEST.sha256 | 导入文件 SHA-256 清单 | 完整性 |
| run.py | demo、solve、compare、mutate、verify、witness、export-lean、landmarks 命令入口 | 实验执行 |
| src/engine.py | C_n 定义、幂集转移、反向 BFS、特征商图、landmark 实验 | 数学定义到算法 |
| src/check_certificate.py | 不调用搜索器的证书检查器；用集合/算术重算像并检查局部势函数不等式 | 证书信任边界 |
| src/lean_export.py | 从 exact Python 证书生成有限实例 Lean 源码草案 | Python/Lean 接口 |
| tests/test_lab.py | 14 个测试方法：穷举、随机交叉检查、抽象、证书正反例 | 回归覆盖范围 |
| examples/ | C4 同步样例、三状态不可同步样例 | 输入格式与不变量 |
| docs/THEORY.md | 势函数、抽象最短距离、两锚点闭式、旋转不变性和 B_r 定义 | 数学核心 |
| docs/MANUAL.md | 完整实操手册：命令、实验、研究任务、Lean 范围与风险 | 执行细节 |
| [docs/ORION_RESEARCH_MANUAL.docx](docs/ORION_RESEARCH_MANUAL.docx)、[.pdf](docs/ORION_RESEARCH_MANUAL.pdf) | 手册的可编辑版与排版版；分别含 439 个段落和 23 页 | 与 Markdown 手册交叉核对 |
| docs/REFERENCES.md | 项目所引用的同步自动机与工具来源 | 背景来源；不是本轮新颖性审查 |
| reference_results/demo/ | C2 至 C10 的有限精确证书与汇总 | 已保存的阈值实验 |
| reference_results/compare_C8/ | C8 上 cardinality、marked、maxgap、gap_multiset、identity 的比较 | 特征抽象实验 |
| reference_results/landmarks_C8/ | C8 的 r=0…8 锚点证书与表格 | 锚点层级 |
| reference_results/marked_scaling.csv | n=3…12 两锚点数据 | 两锚点数值缩放 |
| reference_results/mutations_C6/ | 60 个单转移变体、CSV 与证书 | 局部变体扫描 |
| reference_results/tests.log、clean_start.log | 包内原有 Linux 测试和干净目录启动日志 | 准备环境记录 |
| lean/CertificateCore.lean | 通用局部势函数累积下界和基数斜率引理 | Lean 源码草案 |
| lean/Cerny3.lean、Cerny4.lean | 固定实例的幂集表、单步一致性及最短路径草案 | Lean 源码草案 |
| lean-toolchain | 声明 leanprover/lean4:v4.19.0 | 固定工具链目标 |
| prompts/ | 五份运行、数学、Lean、审阅、扩展任务契约 | 协作流程 |
| templates/ | 研究日志、查重、结果报告和提交材料模板 | 记录流程 |
| start_unix.sh、start_windows.bat | 启动脚本 | 平台入口 |

## 数学对象的精确定义

### 自动机和子集最短路

包中采用的 Černý 自动机 C_n（n≥2）为完整 DFA：
- Q={0,…,n−1}，Σ={a,b}；
- δ(q,a)=q+1 mod n；
- δ(n−1,b)=0；q<n−1 时 δ(q,b)=q。

对非空集合 S⊆Q 和字母 c，定义 S·c={δ(q,c):q∈S}，再按从左到右的顺序推广到词。幂集图的顶点是非空子集，边 S→S·c 对应一个字母。同步词恰好是从 Q 到某个单点集的路径；最短同步词长度是这些目标中的最短路距离。Python 用位掩码表示子集。

C_n 的经典阈值 (n−1)² 被 baseline 当作已知背景并引用文献；程序只在有限 n 上给出计算验证。此阈值是实际自动机的最短路，不应与下文的信息受限抽象下界混为一谈。

### 势函数证书

势函数是非空子集上的非负整数 d，满足：
1. 对每个单点集 {q}，d({q})=0；
2. 对每个非空 S 和每个字母 c，d(S)≤1+d(S·c)。

沿长度 L 的词逐步应用局部不等式，得到 d(Q)≤L+d(Q·w)。若 w 同步，则末项为0，因此任何同步词长度至少为 d(Q)。给出长度恰为 d(Q) 的同步词时，上下界相等，词最短。

搜索器反向 BFS 产生精确距离表；检查器独立重算所有非空集合的每条边并验证局部条件、单点值、同步词终点和上下界字段。这里的“独立”指检查器不调用搜索器，且集合像用另一种实现重算；它仍是 Python 检查，不是 Lean 证明。

### 特征商图与“最强证书”

给定特征映射 α:S↦α(S)，顶点为可实现特征类。只要存在非空 S 和一个字母 c 使 α(S)=x 且 α(S·c)=y，就建有向边 x→y。目标顶点是单点集的特征像。令 D(x) 为此存在型抽象图到任一目标类的最短距离。

若自动机同步，则每个真实集合都能用同一个 reset word 到单点，所以抽象距离有限。d(S)=D(α(S)) 满足势函数局部条件。反过来，任何只依赖 α 且满足局部条件的势函数 h，必须沿每条抽象边满足 h(x)≤1+h(y)，故沿抽象最短路有 h(x)≤D(x)。因此 D 是该特征空间内、该局部势函数证书类所能达到的最大值；这不限制其他证明方法。

存在型抽象边每一步可以由不同代表集合见证，抽象路径未必是一个具体集合轨迹。所有真实路径仍投影为抽象路径，所以抽象最短距离仍是有效下界，只是可能偏小。

### 锚点、间隙与 B_r(n)

对 0≤r≤n，定义 A_0=∅；r≥1 时 A_r=(0,n−1,n−2,…,n−r+1)，正好含 r 个锚点。特征 α_r(S) 记录 |S| 以及 S 在 A_r 中每个位置的成员位。定义 B_r(n) 为上述存在型抽象图中，从 α_r(Q) 到任一单点类的最短距离。r=0 只记录基数；r=1 只标记0；r=2 标记0与n−1；r=3 标记0、n−1、n−2。

engine.py 中的 circular gaps 是按状态编号排序后逐点到下一个点的循环距离，包含最后一个点绕回第一个点的间隙。maxgap 保存最大间隙；gap_multiset 保存排序后的全部间隙。二者都不记录整体循环相位，故对 a 的循环旋转不变。

### 两锚点闭式为何是 3n−5

令 k=|S|、u=1[0∈S]、v=1[n−1∈S]。baseline 的势函数为：

| 特征 | p₂(k,u,v) |
|---|---:|
| k=1 | 0 |
| k≥2 且 v=0 | 3k−3 |
| k≥2、v=1、u=0 | 3k−4 |
| k≥2、v=1、u=1 | 3k−5 |

对 a，特征变为 (k,v,t)，其中 t=1[n−2∈S]；直接代入上表，p₂ 至多下降1。对 b：v=0 时特征不变；(u,v)=(0,1) 时变成 (1,0)，p₂ 上升1；(u,v)=(1,1) 时，n−1 与已有的0合并，变为 (k−1,1,0)，p₂ 恰下降1，包括 k=2 时从1降到0。所有单点势值为0。因此从 Q 出发的任何抽象路径长度至少为 p₂(n,1,1)=3n−5。

上界从 (n,1,1) 先用 b 到 (n−1,1,0)，之后对每个 2≤k≤n−1 走三条存在型边：
(k,1,0) → (k,0,1) → (k,1,1) → (k−1,1,0)。
前两条分别由含 {0,n−2} 且不含 n−1 的 k 元集合、含 {n−1,n−2} 且不含0的 k 元集合见证；对 n≥3、2≤k≤n−1 均可从其余 n−3 个位置补齐。总长 1+3(n−2)=3n−5。因上下界相等，指定两锚点抽象的精确距离即为该值。

基数单独保存时，循环 a 不改变 d；经典同步词 b(a^(n−1)b)^(n−2) 只用 n−1 个 b，结合 |S|−1 作为合法势函数，说明 B_0(n)=n−1。maxgap 与 gap_multiset 也不记录循环相位，所以具有同一线性上限；这解释了 C8 中二者虽然有更多抽象类，下界仍只有7。

## Baseline 数学台账

下列标签严格按包内证据分类。有限运行不能代替普遍证明，Lean 源码不能代替实际编译。

### PROVED_IN_BASELINE

- 局部势函数定理：docs/THEORY.md 给出了累加证明；CertificateCore.lean 有未编译的对应证明草案。
- 特征抽象最短距离定理：包内证明 D 可行，且任何同特征局部势函数不超过 D。
- 两锚点闭式 B_2(n)=3n−5（n≥3）：纸面证明逐项检查 a、b 的局部转移，再构造长度 1+3(n−2) 的抽象路径。它是抽象图下界，不是 C_n 真实阈值；此结论在 baseline，不能算本轮新结果。纸面证明已逐项复核代表集合的可选性和 k=1、k=2、n=3 边界；没有 Lean 验证。
- 旋转不变势函数在 Q 上至多给 n−1；d(S)=|S|−1 达到该值，所以基数抽象 B_0(n)=n−1。
- 由上项直接得到 maxgap 和 gap_multiset 抽象的最强下界也是 n−1：这些特征在 a 下不变，而 |S|−1 是它们可表示的合法势函数。
- 记录 n−1 个成员位并加总基数可恢复最后一位，故 α_(n−1) 为单射，并有 B_(n−1)(n)=C_n 的真实 reset threshold。将它代入数值 (n−1)² 还依赖 baseline 引用的经典阈值结论。
- 单步子集像、exact BFS 的具体实现和证书 checker 的检查规则是程序规格，不应误称为任意 n 的 Lean 形式化。

### COMPUTATIONALLY_VERIFIED_IN_BASELINE

- C2 至 C10 的 reverse BFS 证书给出长度 1、4、9、16、25、36、49、64、81；测试另用前向 BFS 交叉验证这些长度。
- 14 个单元测试通过；覆盖全部 729 个有标号三状态双字母完整自动机、128 个固定种子随机样例，以及坏势函数、坏词、坏转移、截断势函数、伪造非同步不变量、上下界不匹配等拒绝情形。
- 随包 83 个证书由包内记录报告独立重验；本轮重新运行 baseline 检查器后，83/83 接受：55 exact、11 bounds、17 nonsynchronizing。
- C8 五种特征比较：cardinality 7，marked 19，maxgap 7，gap_multiset 7，identity 49；真实阈值49。
- C8 锚点 r=0…8 的下界为 7、7、19、20、21、23、25、49、49；测试还在 n=3…8 检查了随 r 非降及 r=n−1 时恢复 exact。
- marked 两锚点公式在 n=3…10 的每一个非空子集上经过程序对照；marked_scaling.csv 保存 n=3…12 的起点数值。
- C6 单转移邻域完整列出 60 个有标号变体：43 个同步、17 个非同步；同步样例的最大阈值17。不是全部 C6 自动机的分类，也没有同构约简。

### STATED_BUT_NOT_VERIFIED

- 对所有 n，C_n 的经典真实阈值为 (n−1)²：baseline 引用了外部来源，但包内没有一般 n 的纸面证明；本地有限计算只覆盖 n=2…10。
- B_(n−1)(n)=(n−1)² 的一般数值闭式，依赖上项的经典结果。结构等价部分（α_(n−1) 单射）有包内论证。
- Lean/CertificateCore.lean、Cerny3.lean、Cerny4.lean 是源码草案；STATUS.json 和手册均说明未编译。Python 的 VERIFIED 不构成 Lean 内核认证。
- 两锚点结果的文献新颖性、优先权与可否作为原创结果未在 baseline 审查；本轮也未做查重。

### OPEN_AFTER_BASELINE

这里的“open”只表示 baseline 未完成，并非独立确认文献仍开放。

- 固定 r=3 的 B_3(n) 一般公式和证明；baseline 只有 C8 的 r=3 数值20。
- 单锚点 B_1(n) 是否对所有 n 都等于 n−1；包内只给有限点。
- 任意 r 的精确式、递推、稳定化或可靠分段公式；尤其 r=n−2。
- 两锚点证明结构如何扩展到三锚点/更多锚点。
- 把通用势函数、子集像与一般 DFA 同步语义做成实际编译且可重用的 Lean 定理。
- 对两锚点结果及未来候选结果进行独立文献审查。

## Post-baseline 小规模 reconnaissance

命令为现有 exact quotient 实验：从项目根目录对 n=5…12 分别运行 run.py landmarks --n n --out post_baseline/reconnaissance/landmarks_Cn。程序逐一枚举该 n 的全部非空子集，构造存在型抽象边，并为 r=0…n 计算精确抽象 BFS 距离；并非 heuristic。

原始 JSON、每个 n 的 landmarks.csv、合并后的 all_landmarks.csv 与 summary.csv 均保存在 post_baseline/reconnaissance/。C8 的 r 全表和 marked 的 r=2 部分已在 baseline；这些行属于复跑。除这些重叠外，本轮增加了小规模参数点。aggregate_landmarks.py 可重建汇总 CSV。

| n | (n−1)² | B0 | B1 | B2 | B3 | B4 | B_(n−2) | B_(n−1) | B_n |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 16 | 4 | 4 | 10 | 11 | 16 | 11 | 16 | 16 |
| 6 | 25 | 5 | 5 | 13 | 14 | 15 | 15 | 25 | 25 |
| 7 | 36 | 6 | 6 | 16 | 17 | 18 | 20 | 36 | 36 |
| 8 | 49 | 7 | 7 | 19 | 20 | 21 | 25 | 49 | 49 |
| 9 | 64 | 8 | 8 | 22 | 23 | 24 | 30 | 64 | 64 |
| 10 | 81 | 9 | 9 | 25 | 26 | 27 | 35 | 81 | 81 |
| 11 | 100 | 10 | 10 | 28 | 29 | 30 | 41 | 100 | 100 |
| 12 | 121 | 11 | 11 | 31 | 32 | 33 | 47 | 121 | 121 |

表内数值是精确有限图计算结果，不是普遍证明。除 C8 和已有 r=2 scaling 行外，其余新增参数点归本轮 post-baseline 实验。

### Pattern candidates（均未证明）

1. **观察到 / 猜想：** B_3(n)=3n−4，对 n=5…12 的计算成立；n=8 的值已在 baseline，其他这些 r=3 新增点由本轮运行产生。推荐作为唯一第一目标。
2. **观察到 / 猜想：** B_1(n)=n−1，对 n=5…12 计算成立。baseline 有 n=8 点，本轮补算其余范围。
3. **观察到 / 猜想：** 4≤r≤n−4 时 B_r(n)=3n+2r−11；在已计算的 15 个参数对（n=8…12 的有效三角区域）成立。有限范围内的规律需要优先反例搜索。

作为 r=n−2 的对照，n=5…12 的值为 11、15、20、25、30、35、41、47；这组样本没有给出像 r=3 那样清楚的一般式。目前没有把它列为第一目标。

## 唯一推荐的第一定理目标

候选命题：对每个 n≥5，按 A_3=(0,n−1,n−2) 记录基数和三个成员位，令 B_3(n) 是相应存在型抽象图从 α_3(Q) 到任一 α_3({q}) 的最短距离，则

    B_3(n)=3n−4.

状态：有限范围观测 + 明确 conjecture；没有证明。这个精确定义与数值目标在 baseline 中没有一般解；baseline 只含 n=8 单点。它自然接续已证明的 B_2(n)=3n−5，且可以通过可行势函数与抽象见证路径形成 exact theorem。r=n−2 数据当前不如它清楚。此选择不声称 novelty。

## 下一步证明路线（本轮未执行证明）

1. 形式化可实现顶点 (k,u,v,w)，其中 u=1[0∈S]、v=1[n−1∈S]、w=1[n−2∈S]；写清 k 与未锚点数之间的可实现性条件。目标类是所有单点像。
2. 从 r=3 的小规模 exact 距离表归纳候选势函数 p_3(k,u,v,w)。对字母 a，观测位移是 (u,v,w)↦(v,w,t)，其中 t=1[n−3∈S]；对 b，若 v=0 则不变，若 v=1,u=0 则变为 (k,1,0,w)，若 v=u=1 则变为 (k−1,1,0,w)。证明每一种可实现的 t 均满足局部不等式。
3. 逐个处理单点类、k=2 边界以及 n=5 的最小 n 边界；不把不可实现的 bit tuple 当作顶点。
4. 构造长度 3n−4 的抽象路径，并为每条边给出真实代表集合存在性条件。路径上各边的见证可以不同，但都必须符合存在型抽象边定义。
5. 将 p_3(Q)=3n−4 的下界与抽象路径上界合并，得到等式；随后加固定案例 Lean formalization，并保留 Python 表仅作发现和回归数据。

post_baseline/reproduction_log.md 记录环境、命令和复现状态；Git 中 baseline 与 post-baseline 是两个连续提交。

## 2026-09-28 连续研究：已闭合的第一结果

- **PROVED:** B_3(n)=3n-4，对全部 n>=5。证明见
  `post_baseline/B3_PROOF.md`：给出 k=2,3 的边界势函数表和 k>=4
  的仿射表，检查每类 a/b 边，并构造长度 3n-4 的统一抽象路径。
- **PROVED:** B_1(n)=n-1，对全部 n>=2，同文件给出基数下界和抽象 b 链。
- **PROVED:** 连续锚点的商图可直接写成二进制窗口加隐藏占用数的转移系统，
  无需枚举 2^n 个真实子集。`post_baseline/anchor_quotient.py` 实现该精确关系。
- **COMPUTATIONALLY VERIFIED:** 商图解析边与真实子集枚举在 n=3..10、
  1<=r<n 的44个参数对完全相同；三锚点完整距离表在 n=5..100 与证明势函数相同。
- 更多锚点推广正在单独研究；原先的 3n+2r-11 猜想不能继续作为一般公式。

复现：`python post_baseline/verify_structural.py`。
以上没有修改冻结 baseline，也没有将 Lean 源码或有限 n 实验当作一般证明。

## 2026-09-28 主线升级：一般稳定化与二进制分段

本节是最新结论；前面的 OPEN_AFTER_BASELINE 与 Pattern candidates 是历史状态。

### PROVED：不依赖有限实验的一般定理

对任意固定 r>=2 和 n>=r+1，B_r(n+1)<=B_r(n)+3。
因此存在 N_r、整数 C_r，使全部 n>=N_r 满足 B_r(n)=3n+C_r；
并有 -5<=C_r<=r^2-3r-3。证明是容量商图嵌入加 baa 三步路径，
以及两锚点下界保证的单调整数序列稳定化。
完整证明见 `post_baseline/GENERAL_STABILIZATION.md`。
这没有给出一般 N_r 或一般 C_r，也不能直接用于 r 随 n 增长的边界。

### PROVED：有限符号证书证明的无限 n 族

对每个 2<=r<=17、全部 n>=r+2，令 L=floor(log_2(r-1))，则

    B_r(n)=3n+L*r-2^(L+1)-3.

`post_baseline/AFFINE_CERTIFICATES.md` 给出有限表仿射延拓引理与完整证明：
下界表在隐藏占用数 j 超过 J 后按斜率3延拓，故只需检查 j<=J+1
的局部类型；上界为容量2的明确路径，加任意多个 baa 周期。
`post_baseline/affine_certificates/` 保存16份全量整数表及路径，
`check_affine_certificates.py` 不调用搜索器，独立检查10,343,428条
代表不等式、单点、全状态值、见证路径及文件哈希，全部通过。
这里是计算机辅助的有限证书证明，不是有限 n 拟合，也没有 Lean 内核声明。

特别得到 B4=3n-3；r=5..8 时为3n+2r-11；r=9..16 时为3n+3r-19；
r=17 时为3n+33。这将旧公式的有效区间扩大到 n>=r+2，但限制其 r 范围。

### PROVED：旧推广猜想的严格反例

旧候选 4<=r<=n-4 上的3n+2r-11，被 (n,r)=(13,9) 严格反驳：
B9(13)=47，而旧式是46。r9符号势函数给出47下界，容量2路径加两个
baa周期给出47上界。按 n 排序这是原候选范围内的最小反例：更小 n
所有可用 r<=8，已由上述证书定理覆盖。

### CONJECTURED：新的全 r 结构

猜想上述 L 公式对所有 r>=2、n>=r+2 成立。等价地，令
h=ceil(log_2 r)，E(r)=(h+1)r-2^h 是 r 叶满二叉树最小外部路径长，则

    B_r(n)=3n+E(r)-2r-3.

若成立，B_(n-2)(n)=n+1+E(n-2)（n>=4），以及固定 k>=2 的 r=n-k
边界为 n log n 量级。目前 n-2 边界只被证书覆盖到 n=19。
二叉树解释与任意商图路径之间的严格成本对应仍未证明。
稳定化从容量2就开始也尚未对一般 r 证明。

### COMPUTATIONALLY VERIFIED 与复现

额外保存91个 r=2..14、隐藏容量2/3/4/5/8/12/20 的有限 BFS 参数点，
以及 C13,r9 的完整距离表和最短路径。它们仅作为有限计算证据。
直接窗口边关系与真实幂集枚举在44参数对一致；两个独立商图 BFS
实现于18参数对的全距离表一致；三锚点表在 n=5..100 的每个顶点匹配。
命令与状态边界见 `post_baseline/STRUCTURAL_REPRODUCTION.md`。

## 后续自主冲刺：全参数公式闭合（2026-09-28）

**PROVED:** 对全部 r>=2、n>=r+2，

    B_r(n)=3n+E(r)-2r-3=3n+Lr-2^(L+1)-3,
    L=floor(log_2(r-1)).

`post_baseline/GENEALOGY_LOWER_BOUND.md` 给出任意路径的粒子谱系下界。
有效合并之间至少隔2个其他字母；合并粒子回到两端分别至少需要r、r+1
个其他字母。因此反向分裂时刻满足延迟递推，其精确解给出目标下界。
论证包含非合并b和隐藏区任意置换，不依赖有限势函数表。

`post_baseline/ALL_PARAMETER_PROOF.md` 给出确定性的容量2上界：
设C=Lr-2^(L+1)、F(i)=min_d(2^(d+1)i-dr)，在时刻s_i=C+F(i)
反向分裂。分裂时刻与子粒子的释放时刻交错，严格满足容量2的成员位
可实现条件，最后窗口全满、隐藏数为2。追加baa得到全部更大容量。
`post_baseline/uniform_construction.py` 实现此无需搜索的统一见证。

**COMPUTATIONALLY VERIFIED:** 独立集合像检查111个r（含多个二的幂附近），
时刻交错算术检查到r=65537；1750条随机前缀加最短尾部的抽象路径中，
含18446次非合并b，粒子谱系等待界与递推界全部成立。
`post_baseline/check_uniform.py` 可复现；这些检验不代替一般纸面证明。

前面一般r公式的CONJECTURED状态和两个gap已由上述纸面证明取代。
形式化、更多锚点布局与文献审计在本轮继续推进，状态另行记录。

## 2026-09-28 结构推广与内核验证

**PROVED:** 全参数下界可缩短为 s_(2i)>=s_i+r 与相邻事件至少间隔2：
s_(2^d)>=dr，随后补齐事件便得到目标值，无需解完整 Bellman 递推。
详见 `post_baseline/GENEALOGY_LOWER_BOUND.md` 的 Short dyadic proof。

**PROVED:** 连续信息层级满足 B_(r+1)-B_r=floor(log2 r)（2<=r<=n-3）；
固定 k>=2 时 B_(n-k)=n+2k-3+E(n-k)，特别 B_(n-2)=n+1+E(n-2)。
最后一层恢复经典(n-1)^2，最后增量=n^2-3n-E(n-2)。
全部单 anchor 位置精确分类：0位置n-1；n-1位置2n-3；内部位置n。
对任意 g>=2|n，若所有隐藏状态同余mod g，则 B_A(n)>=(g-1)^2。
由此每个固定隐藏数k>=2都有周期布局Theta(n^2)，而连续布局Theta(n log n)。
数量相同并不能决定距离的渐近量级。
完整证明见 `post_baseline/LAYOUT_AND_INFORMATION_THEOREMS.md`。

**FORMALLY VERIFIED（限定边界）:** 仓库指定Lean4.19.0已安装并编译：
任意商图路径的势函数定理；monotone simulation transfer；有限事件的
dyadic等待界；容量2输入算术；单调自然数列稳定；二/三anchor所有符号
局部不等式；显式三anchor count/window图任意路径的3n-4下界；
修复副本中的C3/C4真实子集最优路径。没有sorry、额外axiom或native_decide。
主公式的谱系/实际商图桥梁与统一上界尚未整体形式化；不能称完整主定理
FORMALLY VERIFIED。边界和日志见 `post_baseline/lean_sprint/README.md`。

**COMPUTATIONALLY VERIFIED:** 任意单anchor位置n=2..12；全部隐藏两点布局
n=4..12，使用独立真实子集枚举商图，验证精确单anchor式与gcd投影下界。
数据见 `post_baseline/sprint_results/layout_pairs.csv`。

**NOVELTY OPEN:** 文献已存在prefix-code解码器同步、lopsided-tree广播调度、
置换群同步和幂集双向搜索。未找到此anchor公式及容量2定理的直接已有表述；
仅能说看起来新、尚未完全确认。完整审计见 `post_baseline/NOVELTY_AUDIT.md`。

## 2026-09-28 最优语言与第三种布局量级

**PROVED:** 任意最优路径的全部b都有效；反向dyadic索引形成实际谱系spine，
s_(2^d)=dr；i>=p=2^L 的事件刚性为s_i=C+2i。每个最优词都有
(baa)^(n-1-p)b前缀。r2/3/4的最优字母词唯一，代表子集路径不必唯一。
一般最优时序系统存在唯一逐分量最晚向量，统一构造同时达到所有分量。
完整证明见 `post_baseline/GENEALOGY_NORMAL_FORM.md`。

**PROVED:** 定义W_r为容量2长度的全部最优 relaxed clock向量对应词；
从容量m最优词剥去(baa)^(m-2)后的语言R_r(m)单调增加且包含于W_r。
其精确最终稳定容量是

    M_2=2;
    M_r=1+2^(L-1), r>=3, L=floor(log2(r-1)).

当m>=M_r时R_r(m)=W_r；容量M_r-1下最早时刻表必在强制0输入处溢出。
距离稳定容量始终为2，最优语言稳定容量则为2,3,5,9,...的dyadic阶梯。
完整上下界见 `post_baseline/OPTIMAL_LANGUAGE_THRESHOLD.md`。
`OPTIMAL_LANGUAGE_BOUNDARY.md`给出r5、m2到m3的最小anchor数严格例子。

**PROVED:** 隐藏H={1,...,k-1,n-1}、2<=k<=n-1时，
B_A(n)=2n-k-2，匹配词b^(k-1)(ab)^(n-k-1)b。
因此对每个固定k>=2，相同n-k anchor数量可出现Theta(n)、Theta(n log n)、
Theta(n^2)三种布局量级。完整证明在LAYOUT_AND_INFORMATION_THEOREMS.md。

**FORMALLY VERIFIED（核心算术）:** 最优终段rigidity及精确语言阈值所用
split/nonsplit两种缓冲算术、容量不足算术已追加到ResearchCore.lean并通过
Lean4.19.0；完整normal-form/语言定理仍是纸面证明，不称整体形式化。

**COMPUTATIONALLY VERIFIED:** 66个模型中全部最优路径边共3579顶点、3659边
符合强制前缀/无无效b；r2..16全部1352个relaxed最优向量及各容量的完整
语言传播符合M_r；2700条较大随机向量/容量见证及135个r的独立集合像检查
到r1025；最早时刻表的失败时刻与通用反例一致。线性布局族在55个小参数
完整BFS验证、集合见证到n1000。均为独立有限检验，不作为一般证明前提。

`post_baseline/manuscript.tex`已形成包含上述一般定理和完整证明的单文件稿。
内置LaTeX编译器报告平台标准目录缺失，故PDF编译状态未验证，源码保留。

**PROVED（语言计数结构）:** 对L>=2、p=2^L，W_(2p-2)、W_(2p-1)、W_(2p)
经归一化slack数组显式双射，末端三值平台并非仅数据巧合；共同大小C_L
至少为2^(p/2-1)。一般C_L计数仍OPEN。独立整数数组product枚举给出
C2=3、C3=279，并与时刻表DFS的三个语言集合逐项相同。
证明与checker见 `post_baseline/OPTIMAL_LANGUAGE_COUNTS.md`、
`post_baseline/check_language_counts.py`。

最终统一复现入口：`python post_baseline/run_sprint_checks.py`。
逐项实际输出、退出码保存在 `post_baseline/sprint_results/FINAL_CHECKS.json`；
Lean内核日志与权限/环境边界见 `post_baseline/lean_sprint/README.md`。
全部新增资料/失败路线/可选SMT依赖的状态见 `post_baseline/SPRINT_REPRODUCTION.md`。
