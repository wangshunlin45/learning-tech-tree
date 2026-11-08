"""生成《现代通信技术》专业学习科技树数据（learning-tech-tree/v1）。"""

import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "comm-tech-tree.json")

stages = [
    "大一上 · 筑基",
    "大一下 · 电类入门",
    "大二上 · 通信核心",
    "大二下 · 网络与系统",
    "大三上 · 工程实践",
    "大三下 · 岗位对接",
]

branches = [
    {"id": "foundation", "label": "数理与工具", "en": "FOUNDATION", "color": "#7fb0d8"},
    {"id": "circuits", "label": "电工电子", "en": "CIRCUITS", "color": "#e2b46a"},
    {"id": "comm", "label": "通信原理与信号", "en": "SIGNALS", "color": "#8fd0b8"},
    {"id": "network", "label": "网络与传输", "en": "NETWORKS", "color": "#9c9ad6"},
    {"id": "practice", "label": "工程实践与设备", "en": "FIELDWORK", "color": "#d98f8f"},
    {"id": "career", "label": "通用素养与就业", "en": "CAREER", "color": "#c9b27a"},
    {"id": "capstone", "label": "综合与认证", "en": "CAPSTONE", "color": "#e8a76a"},
]

sources = [
    {"id": "mooc", "title": "中国大学 MOOC", "url": "https://www.icourse163.org/",
     "scope": "通信原理、信号与系统、电子技术等系统课的公开课源，用于补齐课堂没讲透的部分"},
    {"id": "bili", "title": "B 站检索页", "url": "https://search.bilibili.com/",
     "scope": "实验演示、仪器操作、基站上站等过程性视频，不能替代动手"},
    {"id": "huawei", "title": "华为人才在线（认证大纲）", "url": "https://e.huawei.com/cn/talent/",
     "scope": "HCIA-Datacom / HCIA-5G 考试大纲与学习路径，岗位技能对齐的公开依据"},
    {"id": "ict", "title": "华为 ICT 学院", "url": "https://e.huawei.com/cn/talent/ict-academy",
     "scope": "院校合作课程与实验资源，校内若有合作可免费拿到实验手册"},
    {"id": "wireshark", "title": "Wireshark 官方文档", "url": "https://www.wireshark.org/docs/",
     "scope": "抓包过滤语法与协议字段解析，验证 TCP/IP 理解是否真实"},
    {"id": "rfc", "title": "IETF RFC 索引", "url": "https://www.rfc-editor.org/",
     "scope": "TCP/IP 系列原始规范（如 RFC 791/793），查协议细节的一手资料"},
    {"id": "tgpp", "title": "3GPP 规范库", "url": "https://www.3gpp.org/",
     "scope": "4G/5G 空口与核心网标准原文，做网优和基站方向时查参数含义"},
    {"id": "py", "title": "Python 中文文档", "url": "https://docs.python.org/zh-cn/3/",
     "scope": "仿真与数据处理脚本的语法与标准库参考"},
    {"id": "gnuradio", "title": "GNU Radio", "url": "https://www.gnuradio.org/",
     "scope": "软件无线电实验平台，用声卡/SDR 做调制解调的实景验证"},
    {"id": "course", "title": "校内课程资料（教材、实训指导书、教师讲义）", "url": "",
     "scope": "本校课堂教学与考核口径，非公开链接；以任课教师要求为准"},
]

# (id, name, branch, stage, kind, prereq, related, description, outcome, caution, sources)
nodes = [
    # ---------- 大一上 ----------
    ("start", "起点：读懂专业与这张课表", "foundation", 0, "milestone", [], [],
     "把本学期课表翻译成能力清单：哪门课给数学工具、哪门课给电路直觉、哪门课只给学分。先想清楚毕业想去哪个岗位（网络优化、传输维护、基站工程、装维、售前技术支持），后面每一格才有意义。",
     "写出一页《专业画像》：目标岗位 1 个、备选 1 个，列出对应招聘 JD 里的 5 条硬技能。",
     "不要用“先把课上完再说”代替规划，高职三年很快，第二年就要选方向。",
     ["course", "huawei"]),

    ("math1", "应用数学①：函数·极限·导数", "foundation", 0, "core", ["start"], [],
     "高职版高等数学的第一段：函数性质、极限、导数与简单应用。它是后面信号与系统、电磁场、通信原理里“变化率、频谱、衰减”这些词的语法基础。",
     "整理 20 道典型题的手写解题卡，能解释导数在“信号变化快慢”上的含义。",
     "只背公式不画图，到了信号与系统会看不懂波形与频谱的对应关系。",
     ["course", "mooc"]),

    ("eng1", "职业英语①：技术词汇与科技阅读", "career", 0, "core", ["start"], [],
     "围绕设备手册、datasheet、协议文档建立的英语能力。通信行业的一手资料几乎全是英文，HCIA/HCIP 题库也是英文术语。",
     "精读 3 页真实器件手册（如光模块或交换机接口说明），做出术语表 ≥40 条。",
     "把英语当考试科目背单词，遇到英文手册仍然读不动。",
     ["course"]),

    ("ideo", "思想道德与法治", "career", 0, "core", ["start"], [],
     "思政必修课，考核以课堂参与、作业与期末为主，属于毕业学分刚性要求。",
     "按教学日历完成全部作业与考勤，期末不挂科。",
     "拖到最后一周补作业，容易丢平时分。",
     ["course"]),

    ("military", "军事理论", "career", 0, "core", ["start"], [],
     "国防教育必修课，多数学校为线上慕课 + 线下考试，学分刚性但时间成本可控。",
     "完成线上课时与考试，拿到学分记录截图归档。",
     "误以为可以最后刷完，线上课常有截止时间。",
     ["course"]),

    ("pe1", "体育①：体能与运动习惯", "career", 0, "core", ["start"], [],
     "体测与课堂出勤双考核。通信行业的上站、布线、拉缆都是体力活，体能不是选修。",
     "建立每周 2 次、每次 40 分钟的运动记录，体测项目全部达标。",
     "只在体测前突击，容易受伤且成绩不稳。",
     ["course"]),

    ("career", "大学生职业生涯规划", "career", 0, "core", ["start"], [],
     "把“我是谁、能干什么、市场要什么”写成可执行的三年计划。这门课的产出直接决定你二年级选哪条技术线。",
     "产出一份含时间节点的三年规划表，并标注 3 个可验证的里程碑（证书/项目/实习）。",
     "写成作文交上去就完事，后面没有任何一条被执行。",
     ["course"]),

    ("etiquette", "社交礼仪", "career", 0, "core", ["start"], [],
     "职场沟通、商务接待、电话与邮件礼仪。装维、售前、客户侧故障处理都靠这套软技能兜底。",
     "完成一次 3 分钟模拟客户沟通（含开场、复述需求、确认时间点），录下来自评。",
     "把它当水课，面试时连自我介绍的结构都没有。",
     ["course"]),

    ("psych", "大学心理健康教育", "career", 0, "core", ["start"], [],
     "压力管理、情绪识别、人际边界。高职节奏是“课多 + 实训多 + 考证压力”，这门课给的是可持续学习的底盘。",
     "建立一份个人压力清单与 3 条应对策略，实践 4 周后记录变化。",
     "直到崩了才想起来，平时完全不复盘情绪状态。",
     ["course"]),

    ("notes", "学习方法：结构化笔记与复盘", "foundation", 0, "optional", ["start"], ["psych"],
     "把课堂、教材、视频三种输入合并成一套可检索的笔记体系（康奈尔笔记 / 双链笔记），并每周复盘一次。",
     "连续 4 周产出周复盘，能指出“哪一章其实没懂”。",
     "收藏一堆资料却从不回看，笔记变成资料坟场。",
     ["course"]),

    ("self_study", "晚自习与出勤纪律：把时间变成产能", "career", 0, "core", ["start"], ["notes"],
     "通信 260304 的晚自习出勤不是形式：它是一天里唯一不被打断的整块时间。把它固定成“预习 20 分钟 + 做题/实验 60 分钟 + 复盘 10 分钟”的循环。",
     "连续 6 周出勤无缺，且每周晚自习产出可查的记录（题卡/实验记录/笔记）。",
     "人在教室心在手机，出勤率满分但一章没学会。",
     ["course"]),

    # ---------- 大一下 ----------
    ("math2", "应用数学②：积分与微分方程入门", "foundation", 1, "core", ["math1"], [],
     "积分、常微分方程初步、级数概念。通信里的能量、功率、滤波、RC 充放电都落在这套工具上。",
     "能独立推导一阶 RC 电路的充放电表达式，并画出示意图。",
     "只记积分表，不理解“积分=累积量”的物理含义。",
     ["course", "mooc"]),

    ("circuit", "电工技术：直流电路与基尔霍夫定律", "circuits", 1, "core", ["math1", "start"], [],
     "电路模型、欧姆定律、基尔霍夫两定律、叠加与戴维南等效。这是全部电类课的公共地基，也是电工证与实训的前提。",
     "独立完成 5 个直流电路计算 + 1 次万用表实测，计算值与实测值误差 <10%。",
     "只会套公式不会看图，遇到实电路就分不清串并联。",
     ["course", "bili"]),

    ("ac", "正弦交流与三相电路", "circuits", 1, "core", ["circuit", "math2"], [],
     "相量法、阻抗、功率因数、三相电与安全用电。机房供电、通信电源、UPS 都建立在这上面。",
     "用相量法算出一个 RL 串联电路的电流与功率因数，并用实验验证。",
     "把交流当直流算，忽略相位差导致功率算错。",
     ["course"]),

    ("safety", "电工实训与安全规范", "circuits", 1, "core", ["circuit"], [],
     "安全用电、接地与防雷、验电与挂牌、实训台操作规范。上站作业和机房施工的第一道门槛。",
     "通过校内电工实训考核，能口述“停电—验电—挂牌—接地”的顺序与原因。",
     "觉得是形式主义，真实作业里这是保命流程。",
     ["course"]),

    ("clang", "C 语言与嵌入式编程入门", "foundation", 1, "core", ["start", "math1"], [],
     "变量、流程控制、函数、指针基础。单片机、通信设备命令行、后续 Python 都靠这套编程直觉迁移。",
     "写出 3 个可运行的小程序（串口打印、数组处理、简单状态机），并注释清楚。",
     "只看视频不动手，指针一卡就放弃。",
     ["course", "bili"]),

    ("linux", "Linux 命令行与 Git 版本管理", "foundation", 1, "core", ["start"], [],
     "文件与权限、进程、网络命令（ip/ss/ping/tcpdump）、文本处理，以及 Git 的基本提交与回滚。设备侧几乎都是 Linux。",
     "在一台虚拟机里完成“建用户、配静态 IP、抓 100 个包、用 Git 提交笔记”全流程。",
     "只背命令不理解输出，排障时看不懂报错。",
     ["course"]),

    ("eng2", "职业英语②：技术文档与邮件", "career", 1, "core", ["eng1"], [],
     "技术写作：故障报告、变更说明、客户邮件。工作中比口语更常用。",
     "用英文写一份 1 页故障处理报告（现象—定位—处理—验证）。",
     "直接机翻，术语与句式不像工程文档。",
     ["course"]),

    ("pe2", "体育②：专项技能与体测达标", "career", 1, "core", ["pe1"], [],
     "专项运动技能 + 国家学生体质健康标准测试。毕业学分与体测挂钩。",
     "体测全部项目达标并留档，专项课出勤满勤。",
     "体测单项不及格会影响毕业资格审查。",
     ["course"]),

    # ---------- 大二上 ----------
    ("analog", "模拟电子：二极管·三极管·放大电路", "circuits", 2, "core", ["ac"], [],
     "PN 结、二极管应用、三极管工作区、共射/共集放大、反馈与运算放大器。射频前端与电源电路的入门语言。",
     "搭出单管共射放大电路，测出静态工作点与电压增益，与手算对比。",
     "只记结论不做实验，波形失真了也不知道为什么。",
     ["course", "bili"]),

    ("digital", "数字电子：逻辑门·组合与时序电路", "circuits", 2, "core", ["ac"], [],
     "逻辑代数、组合逻辑设计、触发器、计数器、状态机。它是通信设备里“判决、同步、计数”的硬件基础。",
     "用 74 系列芯片或仿真软件实现一个 4 位计数器，并画出时序图。",
     "跳过卡诺图直接抄答案，设计题一变形就不会。",
     ["course"]),

    ("signal", "信号与系统：时域与频域", "comm", 2, "core", ["math2"], ["math1"],
     "信号的分类、卷积、傅里叶级数与变换、系统响应。数字通信原理里“带宽、频谱、滤波”全部由这门课定义。",
     "对 3 种典型信号画出时域波形与频谱，并解释带宽与脉宽的关系。",
     "把傅里叶当纯数学背，考试过但看不懂频谱仪。",
     ["course", "mooc"]),

    ("comm", "数字通信原理（本学期核心课）", "comm", 2, "core", ["signal", "math2"], ["digital"],
     "信源/信道编码、抽样量化、PCM、基带传输、误码率、复用与同步。它是整个专业的“主心骨”，也是网优与传输岗面试的必问内容。",
     "独立推导 PCM 编码过程，算出给定信噪比下的误码率量级，并用实验箱或仿真验证趋势。",
     "只背框图名词，说不清“为什么这样编码”，面试一问就露。",
     ["course", "mooc", "tgpp"]),

    ("modulate", "调制与编码：ASK/FSK/PSK 与信道编码", "comm", 2, "core", ["comm"], ["signal"],
     "数字调制星座、频带传输、差错控制编码（汉明、卷积、LDPC 概念）。5G 空口的高阶调制就是它的延伸。",
     "用 GNU Radio 或 MATLAB 跑通 BPSK/QPSK 调制解调，输出星座图与误码率曲线。",
     "只画星座图不动手，遇到真实信道损伤无法解释。",
     ["gnuradio", "course"]),

    ("mcu", "单片机原理与应用", "circuits", 2, "core", ["digital", "clang"], [],
     "GPIO、定时器、串口、中断、AD 采样。设备监控、传感器采集、简易通信模块都从这里起步。",
     "用 STM32/51 完成“串口收发 + 定时采样 + 上位机显示”的小系统，代码放 Git。",
     "只会点灯，串口通信与中断一上就乱。",
     ["course", "bili"]),

    ("hf", "高频电子线路", "comm", 2, "optional", ["analog", "signal"], [],
     "谐振回路、高频小信号放大、混频、振荡器。射频与基站方向的知识前置。",
     "分析一个混频电路的频谱搬移过程，说明本振频率如何选择。",
     "选课时跟风，实际没有射频方向打算会挤压核心课时间。",
     ["course"]),

    ("em", "电磁场与电磁波初步", "comm", 2, "optional", ["math2"], ["signal"],
     "电场磁场、麦克斯韦方程组的定性理解、传输线、天线增益与方向图概念。网优看覆盖、看天线倾角时会用到。",
     "解释天线增益、半功率波束宽度与覆盖半径的关系，并画出示意图。",
     "把它当纯理论课，网优现场的参数就全靠背。",
     ["course"]),

    # ---------- 大二下 ----------
    ("network", "计算机网络与 TCP/IP", "network", 3, "core", ["linux"], [],
     "OSI 与 TCP/IP 分层、IP 编址与子网、ARP、TCP/UDP、DNS、HTTP。所有网络岗的第一门硬课。",
     "手算子网划分 10 道题全对；用抓包解释一次完整的 TCP 三次握手。",
     "只会背分层名字，给一个 IP 段算不出可用地址。",
     ["rfc", "wireshark", "course"]),

    ("routing", "路由与交换配置", "network", 3, "core", ["network"], [],
     "VLAN、静态路由、OSPF、ACL、NAT。这是 HCIA-Datacom 的主体内容，也是运维岗的日常。",
     "在 eNSP 或真实设备上搭 3 台设备的 OSPF 网络，实现互通并导出配置文件。",
     "只敲命令不理解报文交互，排障只能重启。",
     ["huawei", "course"]),

    ("optical", "光纤通信与光传输", "network", 3, "core", ["comm"], ["em"],
     "光纤结构、损耗与色散、SDH/OTN 概念、光模块与光功率预算。传输机房的核心知识。",
     "完成一次光功率预算计算（含接头与熔接损耗），并用光功率计实测一根跳线。",
     "把光纤当“更快的网线”，不懂衰耗与色散会误判故障。",
     ["course", "bili"]),

    ("mobile", "移动通信：4G/5G 空口与组网", "network", 3, "core", ["comm", "network"], ["em"],
     "蜂窝概念、OFDM、MIMO、帧结构、小区与切换、SA/NSA 组网。网优与基站岗的主战场。",
     "画出 5G 一个时隙的帧结构，说明上下行配比与覆盖、容量的关系。",
     "只记缩写，问“为什么用 OFDM”答不上来。",
     ["tgpp", "course"]),

    ("access", "接入网与综合布线", "practice", 3, "core", ["network", "circuit"], [],
     "PON 架构、ONU/OLT、FTTH 场景，以及双绞线/光纤的施工规范与测试。装维与驻地网岗位的入门技能。",
     "完成一次 FTTH 入户链路设计与跳线制作，用测线仪与光功率计出具测试记录。",
     "布线不讲规范，现场返工率极高。",
     ["course", "bili"]),

    ("power", "通信电源与机房环境", "practice", 3, "core", ["ac"], [],
     "开关电源、蓄电池、UPS、接地防雷、温湿度与消防。机房与基站“不断电”的底层保障。",
     "画出机房供电链路（市电—UPS—配电—设备），标出单点故障位置。",
     "只关注设备不关注供电，故障定位方向会跑偏。",
     ["course"]),

    ("dsp", "数字信号处理", "comm", 3, "optional", ["signal"], ["math2"],
     "采样定理、DFT/FFT、数字滤波器设计、窗函数。想走研发或算法方向再加。",
     "用 Python 设计一个 FIR 低通滤波器，画出幅频响应并处理一段真实音频。",
     "在没有信号与系统基础时硬上，容易全程听不懂。",
     ["mooc", "py"]),

    ("python", "Python 与通信仿真", "foundation", 3, "optional", ["linux", "math2"], ["clang"],
     "NumPy/Matplotlib 做信号与数据可视化，脚本化处理测试数据与日志。网优报表与自动化巡检的加速器。",
     "写一个脚本：读入路测 CSV，画出 RSRP 分布直方图并标注弱覆盖小区。",
     "把它当第二门编程课从语法学起，迟迟做不出能用的工具。",
     ["py", "course"]),

    ("wireshark", "抓包与协议分析", "network", 3, "core", ["network"], ["linux"],
     "抓包点选择、过滤表达式、TCP 重传与乱序识别、DNS/DHCP/HTTP 字段定位。排障的核心证据手段。",
     "对一个“网页慢”的场景抓包，用过滤与统计指出瓶颈在 DNS、握手还是重传。",
     "抓到包不会过滤，几千条记录里找不到问题。",
     ["wireshark", "rfc"]),

    ("sec", "网络安全基础", "network", 3, "optional", ["network"], ["linux"],
     "常见攻击面、访问控制、VPN、等保基本要求。政企项目里绕不开的合规知识。",
     "完成一次小型网络的访问控制设计（ACL + 账号权限），写出风险清单。",
     "只记名词，配置时把 ACL 顺序写反导致全不通。",
     ["course"]),

    # ---------- 大三上 ----------
    ("survey", "通信工程勘察与设计", "practice", 4, "core", ["optical", "access"], ["power"],
     "站点勘察、机房平面、路由与管线、概预算与图纸。工程侧“从需求到图纸”的完整链条。",
     "为一个真实楼栋出一套勘察记录 + 布线平面图 + 材料清单。",
     "只画图不算量，材料清单与现场对不上。",
     ["course"]),

    ("bts", "基站建设与维护", "practice", 4, "core", ["mobile", "power"], ["safety"],
     "站型选择、天馈安装、上站流程、告警处理与例行维护。基站岗的核心动作集。",
     "完成一次模拟上站：按流程拍照记录、核对天馈参数、处理 3 类常见告警。",
     "忽视安全与工单规范，现场容易被退回。",
     ["course", "huawei"]),

    ("optim", "无线网络优化与测试", "practice", 4, "core", ["mobile", "wireshark"], ["python", "em"],
     "路测与定点测试、RSRP/SINR 判读、覆盖与干扰问题定位、参数调整与复测。网优岗的日常闭环。",
     "用测试软件跑一段路线，输出问题小区清单与 3 条可执行优化建议，并复测验证。",
     "只会看指标不会归因，报告写成数据堆砌。",
     ["course", "tgpp"]),

    ("otn", "PTN/OTN 传输设备调试", "practice", 4, "core", ["optical"], ["routing"],
     "传输网元开局、业务配置、环网保护、告警与性能管理。传输机房岗位的必修。",
     "在仿真或实训设备上开通一条以太网专线业务，并验证保护倒换。",
     "配置跳步漏掉时隙，业务不通却查不到原因。",
     ["course", "huawei"]),

    ("hcia", "华为 HCIA 认证（Datacom 或 5G）", "capstone", 4, "milestone", ["routing", "mobile"], [],
     "把课堂知识压缩成一张行业认可的凭证。Datacom 偏网络与运维，5G 偏无线与基站，按目标岗位二选一。",
     "通过 HCIA 考试并保存成绩单；整理一份 30 页以内的备考笔记。",
     "只刷题库不理解配置逻辑，面试现场配置就露馅。",
     ["huawei", "ict"]),

    ("intern", "顶岗实习与岗位适应", "career", 4, "core", ["career", "etiquette"], ["psych"],
     "真实工单、真实客户、真实工期。把学校里的实验变成能交付的工作记录。",
     "完成至少 8 周实习，产出 10 条工单记录与 1 份实习复盘。",
     "把实习当打卡，回来写不出任何具体做过的事。",
     ["course"]),

    ("iot", "物联网与传感网", "network", 4, "optional", ["mcu", "network"], ["cloud"],
     "NB-IoT/LoRa、传感器接口、边缘采集与上云。通信与行业应用的交叉地带。",
     "做一个温湿度采集终端，通过 MQTT 上报到云平台并展示曲线。",
     "只做演示不做稳定性，掉线重连逻辑缺失。",
     ["course", "py"]),

    ("cloud", "云网融合与数据中心", "network", 4, "optional", ["network"], ["linux", "sec"],
     "虚拟化、云主机与 VPC、专线与 SD-WAN、机房基础设施。政企项目的主流交付形态。",
     "在云上搭一套 VPC + 子网 + 安全组，打通到本地的一台设备。",
     "只点控制台不理解路由与安全组顺序，通了不知道为什么通。",
     ["course"]),

    # ---------- 大三下 ----------
    ("capstone", "毕业综合项目：小型通信系统设计与交付", "capstone", 5, "milestone",
     ["survey", "bts", "optim"], ["otn", "iot", "cloud", "dsp", "modulate", "notes"],
     "把“勘察—设计—实施—测试—优化—文档”串成一条完整交付链，形成可展示的作品。这是整棵树唯一的收敛点。",
     "交付一套完整项目包：方案书、拓扑与图纸、配置/测试记录、问题与优化报告、3 分钟讲解视频。",
     "只做局部实验就号称项目，缺少闭环与数据支撑。",
     ["course", "huawei"]),

    ("hcip", "进阶认证：HCIP 或 1+X 5G 基站建设与维护", "capstone", 5, "optional", ["hcia"], [],
     "在 HCIA 之上做深：多协议、故障排查、方案设计，或走 1+X 的基站建设与运维方向。",
     "通过一门进阶认证，或在对应实训考核中拿到优秀。",
     "证书堆数量不做深，面试深挖一层就空。",
     ["huawei", "ict"]),

    ("resume", "简历·面试·作品集", "career", 5, "core", ["intern", "career"], ["etiquette", "capstone"],
     "把课程、证书、项目、实习压成一页简历与一个作品集，按岗位 JD 做关键词对齐。",
     "产出一页简历 + 一个作品集链接，完成 3 次模拟面试并记录改进点。",
     "简历写“熟悉”一堆技术却没有一个可验证证据。",
     ["course"]),

    ("general", "通识学分与毕业资格", "career", 5, "milestone",
     ["ideo", "military", "pe2", "psych", "etiquette", "eng2"], [],
     "思政、军事理论、体育、心理健康、社交礼仪、职业英语等通识模块的学分归集。技术再强，学分不齐也毕不了业。",
     "对照培养方案逐项打勾，确认无缺项、无重修未过。",
     "临毕业才发现少一门选修或体测未达标。",
     ["course"]),

    ("end", "毕业验收：能力—证据—岗位三方对齐", "capstone", 5, "milestone",
     ["capstone", "hcip", "resume", "general"], ["hcia"],
     "用一份材料同时回答三个问题：我会什么、我做过什么、我能胜任哪个岗位。",
     "提交《毕业能力档案》：项目包 + 证书 + 实习记录 + 简历，并完成一次 20 分钟答辩。",
     "把“上完课”当成“具备能力”，缺少可验证证据。",
     ["course", "huawei"]),
]

edges = [
    ("self_study", "capstone", "development", "每周固定的自习节奏，是项目文档与测试记录能按时产出的真正来源。"),
    ("notes", "capstone", "development", "周复盘习惯直接决定项目文档与问题记录的质量。"),
    ("safety", "bts", "application", "上站作业必须先具备安全规范与操作资质。"),
    ("hf", "bts", "development", "射频前端知识用于判断天馈与驻波类告警。"),
    ("em", "optim", "application", "天线方向图与传播损耗用于覆盖问题归因。"),
    ("dsp", "capstone", "development", "滤波与频谱分析支撑测试数据处理。"),
    ("python", "optim", "application", "脚本化处理路测数据并生成报告。"),
    ("sec", "cloud", "development", "访问控制与合规要求决定云网方案边界。"),
    ("otn", "capstone", "application", "传输业务开通作为综合项目的承载层。"),
    ("iot", "capstone", "application", "传感采集作为综合项目的应用侧扩展。"),
    ("cloud", "capstone", "application", "云网融合方案作为综合项目的上联部分。"),
    ("modulate", "capstone", "application", "调制方案选型用于综合项目的链路设计。"),
]

tree = {
    "format": "learning-tech-tree/v1",
    "id": "comm-tech-2603",
    "title": "现代通信技术 · 学习科技树",
    "subtitle": "通信 260304 · 课程 → 能力 → 岗位",
    "description": "以本学期课表（电工技术、大学应用数学基础、数字通信原理、高职职业英语、思想道德与法治、大学生职业生涯规划、社交礼仪、军事理论、体育、大学心理健康教育）为骨架，向上接到通信专业的核心能力链，向下落到网优、传输、基站、装维四类岗位的真实动作。",
    "version": "1.0",
    "language": "zh-CN",
    "searchPlaceholder": "搜索课程、技术或岗位…",
    "education": {
        "path": "现代通信技术（高职三年制）",
        "duration": "3 年 / 6 学期",
        "note": "阶段划分按学期推进；节点是能力验收而非学校考核口径，学分与毕业条件以培养方案为准。",
    },
    "stages": stages,
    "branches": branches,
    "sources": sources,
    "startId": "start",
    "endId": "end",
    "nodes": [],
    "applicationEdges": [],
}

for (nid, name, branch, stage, kind, pre, rel, desc, outcome, caution, src) in nodes:
    tree["nodes"].append({
        "id": nid,
        "name": name,
        "branch": branch,
        "stage": stage,
        "kind": kind,
        "prereqIds": pre,
        "relatedIds": rel,
        "description": desc,
        "outcome": outcome,
        "caution": caution,
        "sourceIds": src,
    })

for (src, dst, rel, reason) in edges:
    tree["applicationEdges"].append({"source": src, "target": dst, "relation": rel, "reason": reason})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(tree, f, ensure_ascii=False, indent=1)

print("nodes:", len(tree["nodes"]), "edges:", len(tree["applicationEdges"]), "->", OUT)

