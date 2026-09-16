# RESEARCH —— 四端实用技术栈选型

> 研究范围：学生端（macOS + Windows + iPadOS + Android）独立交付、本地权威数据结构/证据/资产/记忆/规划、云端 LLM API（设备不部署大模型）、B 端 PC 浏览器 Web 工作台、私域官网下载、不做公共应用商店依赖、实用主义、少重复开发、成熟可维护。
>
> 证据规则：**[来源事实]**=本次已从官方一手资料（框架官方仓库/文档、Apple/Microsoft/Google 平台文档）核验并附带 URL（context7 / GitHub 官方仓库 / agent-reach 抓取的官方页面实时内容）；**[专业推断]**=基于来源事实的推理，需人工复核；**[推荐]**=研究结论；**[未经核验]**=依赖既有知识、本次未能直接抓取官方原文，需后续核验。
>
> 获取时间窗口：2026-09 月。环境限制说明：本环境 WebFetch 对多数域名被网络策略阻断、WebSearch 无真实检索能力，故框架与存储证据经 context7（拉取各框架官方 GitHub 仓库源码/文档）与 GitHub 官方仓库核验，平台分发证据经独立网络通道抓取 Apple/Microsoft/Google 官方页面原文核验。
>
> 关键概念澄清（贯穿全文，避免误读）：
> - 本产品是"本地**数据**权威优先"，但 **Agent 推理依赖云端 LLM API——必须联网才能运行**。"本地数据"绝不等于"本地模型"；设备不部署/不内嵌任何大模型。网络不可用 = 学生端可读写本地证据与规划、但 Agent（LLM 调用）不可用。**本项目不存在可离线运行的 Agent。**
> - "本地优先"指本地权威数据、可脱网读写、可加密存储；不是离线 AI。

---

## 0. 结论速览（先给推荐栈）

| 层 | 推荐 | 理由（详见各节） | 官方证据定位 |
|---|---|---|---|
| 学生端框架 | **Flutter / Dart** | 唯一以"一等公民"支持 iOS、iPadOS、**Android、Windows、macOS** 的单一代码库方案，减少平台适配，成熟可维护 | §1.1；flutter.dev |
| 学生端本地数据库 | **SQLite**（本地实体+证据+资产+记忆+规划）+ **SQLCipher**（整库 AES-256 加密） | 单一内嵌 SQL 引擎所有目标平台通用，零服务端、单文件、成熟 | §3.3 |
| 数据契约 | **JSON Schema**（自建，作为本地库表与 API 的单一事实源）+ **OpenAPI 3**（生成 API） | 一套契约同时驱动 Flutter 客户端、Fastify 后端、React B 端，杜绝三端 schema 漂移 | §3.4 |
| 云端后端 | **Node.js（TypeScript）+ Fastify** | 与客户端共享 TS 类型、内置 JSON Schema/Ajv 校验、低开销、插件生态成熟 | §3.1；github fastify |
| B 端 Web 工作台 | **React + Vite + TypeScript** | 浏览器直接交付、零安装、与后端共享 TS/OpenAPI 类型 | §3.2 |
| 异地同步 | **自研最小版本化增量协议**（每次全量快照 + updatedAt/版本号合并），**不引入 CRDT/ElectricSQL** | 一个实例一个学生、冲突面极窄，CRDT 属过度设计 | §3.3、§4 |
| LLM 集成方式 | **后端统一代理 LLM API**（学生端/B 端不持 API Key，只调自有后端） | 密钥驻留服务端、集中计量与校准、与"设备不部署模型"一致 | §4 |

**一条最要命的现实约束（先点破）**：本地/私域"官网直装"在 macOS、Windows、Android 上可行（见 §2.1/2.2/2.4），但 **iPadOS 对公众分发官方只有 App Store 一条路**——TestFlight 仅限 beta、Custom Apps/Enterprise 仅限特定组织内部、EU 网页分发仅限欧盟用户（§2.3）。**iPadOS 学生端无法通过私域官网直装公开分发**，必须就"走 App Store 公开上架" 或 "向受控组织设备走 Apple Business Manager Custom Apps/Enterprise 内部通道" 二选一做产品决策，这是四次端选型里唯一"私域下载"约束无法满足的平台。见 §2.3、§5。

---

## 1. 学生端框架选型

约束回顾：一套代码/少重复开发，覆盖 PC（macOS、Windows）+ 移动（iPadOS、Android），且要支持：本地数据库、加密存储、网络 API、私域安装、性能、维护、分发。

### 1.1 平台覆盖矩阵对比

| 维度 | **Flutter/Dart** | **React Native / Expo** | **Tauri v2** | **Electron** | 原生（Swift/Kotlin/C++…） |
|---|---|---|---|---|---|
| Android | [来源事实] 一等支持 | [来源事实] 一等支持（iOS 15.1+/Android 7.0 (API 24)+） | 支持但不成熟 | ❌ 不支持 | 一等 |
| iPadOS/iOS | [来源事实] 一等支持（明确列 "Android, iOS, iPadOS"） | [来源事实] 一等支持 | 支持（Swift 桥）但不成熟 | ❌ 不支持 | 一等 |
| Windows 桌面 | [来源事实] 一等支持（`flutter build windows`） | ⚠️ [来源事实] **Out-of-tree 实验状态**（react-native-windows，社区/Microsoft 维护，非 RN 官方一等） | 一等 | 一等 | 一等 |
| macOS 桌面 | [来源事实] 一等支持（`flutter build macos`） | ⚠️ [来源事实] **Out-of-tree 实验状态**（react-native-macos） | 一等 | 一等 | 一等 |
| Web 浏览器 | 支持（goog.本产品不用） | [来源事实] 一等（Expo web） | 免（用 WebView） | 免（含 Chromium） | 无 |
| 单一代码库覆盖本需求 4 端 | ✅ **是全 | ⚠️ 需 3 个代码仓库（RN 移动 + RN-Windows + RN-macOS） | ⚠️ desktop + mobile 两套构建、移动 DX 不成熟 | ❌ 移动缺失 | ❌ 全分开 |

**证据与定位：**

**[来源事实]** Flutter 官方宣布支持 Android、iOS、**iPadOS**、web、Windows、macOS 和 Linux，无需为不同设备重写应用。
> 定位：Flutter 官方 blog「Flutter 2.8 announcement」："Flutter supports Android, iOS, **iPadOS**, web, Windows, macOS and Linux," 与 flutter.dev 桌面支持页 `flutter build windows` / `flutter build macos`。
> URL: https://docs.flutter.dev/platform-integration/desktop ；https://blog.flutter.dev/（announcing-flutter-2-8）

**[来源事实]** React Native 官方仅将 **iOS 与 Android** 列为目标平台（iOS 15.1+、Android 7.0/API 24+）；macOS/Windows 属 **Out-of-Tree 平台**（react-native-macos / react-native-windows 由 Microsoft/社区维护），需 `experiments.outOfTreePlatforms` 显式开启。
> 定位：react-native README（"RN applications support iOS 15.1 and Android 7.0"）；Expo `@expo/config` 源码 `getSupportedPlatforms`/`getPlatformsFromConfig`（`outOfTreePlatforms` 开关；"only macOS and tvOS platforms are supported" for out-of-tree）。
> URL: https://github.com/react/react-native/blob/main/README.md ；https://github.com/expo/expo/blob/main/packages/@expo/config/src/Config.ts

**[来源事实]** Tauri v2 同时声明 Android/iOS 支持，但官方自身承认**移动端体验未到位**：官方插件并非全部支持移动端、官方表示"对开发体验并不完全满意，正在改进到与桌面看齐"；并硬编码系统托盘在 iOS/Android 为"none"（桌面专用）。
> 定位：Tauri docs 2.0 发布说明（"On mobile not all of the official plugins are supported… not completely happy about the developer experience"）；兼容表构建脚本 `compatibility-table/build.ts`（tray-icon 桌面专用）。
> URL: https://v2.tauri.app/ ；https://github.com/tauri-apps/tauri-docs/blob/v2/src/content/docs/blog/tauri-2.0.mdx

**[来源事实]** Electron 官方支持平台为 macOS、Windows、Linux（桌面），**无移动端**。
> 定位：Electron 官方文档 why-electron / auto-updater（"only macOS and Windows are supported" for auto-updater，平台即为桌面）与构建说明（`.app`/`.exe`/Linux 二进制）。
> URL: https://www.electronjs.org/

### 1.2 就各评估维度看选型

- **本地文件/数据库访问**：Flutter 用官方/社区插件（sqflite、sqlite3、path_provider）跨平台一致；RN 需 per-platform 原生桥；Tauri 走 Rust SQLite（Rust 生态成熟如 rusqlite/SQLx）。
- **加密存储**：四者都可通过接入 **SQLCipher** 获得整库 AES-256 加密（见 §3.3）。Flutter（sqflite_sqlcipher / drift）与 RN（react-native-sqlite-storage + sqlcipher）都有生态；Tauri 直接 Rust 绑定 SQLCipher 最省桥接。
- **网络 API**：所有 Web 技术栈都成熟；无差别。
- **性能**：Flutter 编译到原生/AOT（skia/impeller 渲染），桌面与移动体验一致、体量小；Electron/Tauri 桌面走系统 WebView；RN 走原生控件但桌面需双桥。
- **维护与分发**：Flutter 单仓库覆盖 4 端、单一构建链最省；RN 桌面（macOS/Windows）为社区/实验维护，升级与 CI 风险更高（[来源事实] out-of-tree，见上）。

**[专业推断]** 对本需求（4 端独立交付、少重复开发、成熟可维护），**Flutter 是唯一"一套代码 + 四条官方一等渠道"的方案**；RN/Expo 桌面端仍是实验状态、Electron 缺移动端、Tauri 移动端官方自称未成熟，三层都需在"桌面 or 移动"至少一处做二级代码库/实验性依赖的让步。

> **[推荐] 学生端 = Flutter（Dart）**。理由：官方一等支持同时覆盖 macOS、Windows、iPadOS、Android（§1.1）；本地 SQLite/SQLCipher 生态成熟；私域直装（macOS/Windows 公证签名 + Android APK）不变；未来若需 Web 版可低成本扩展。**否决 Tauri（移动端未成熟）、Electron（无移动端）、RN/Expo（桌面端实验）、原生（四端四份代码）。**

---

## 2. 私域官网下载 / 平台分发现实（分平台逐条）

> 前提：本产品不投公共应用商店。下表区分各平台"私域直装"是否可行及其硬性限制。**结论：macOS/Windows/Android 可私域直装；iPadOS 对公众不可私域直装（唯一例外 EU）。**

### 2.1 macOS 学生端（Mac 私域官网下载）

- **[来源事实]** macOS 10.15 之后，凡以 Developer ID 分发、且在 2019-06-01 之后构建的软件**必须经 Apple 公证（Notarization）**；否则在默认 Gatekeeper 设置下无法运行。
  > 定位：Apple 文档 security/notarizing-macos-software-before-distribution（`Important:` 提示框："Beginning in macOS 10.15, all software built after June 1, 2019, and distributed with Developer ID must be notarized…"）。
  > URL: https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
- **[来源事实]** 公证机制：Gatekeeper 凭 Apple 签发的 ticket（在线或钉进可执行文件）识别已公证软件。Apple Support 安全指南：App Store 之外分发的 App 需用 **Developer ID 证书**签名并被公证，才能默认运行。
  > URL: https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution ；https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/1/web/1
- **[来源事实]** 官方明确"公证 ≠ App Review"（公证不是审核内容）。这意味着这一关是可满足的自助流程，而非内容审核。
  > URL: 同上 Apple 公证文档

**[推荐] macOS = Developer ID 签名 + 公证，官网直发 .dmg/.pkg/.zip。** 这是往私域官网直发的现实且官方认可的路径；无需 Mac App Store，但**必须**注册 Apple Developer Program、完成公证。

### 2.2 Windows 学生端（官网直发 .exe/.msi）

- **[来源事实]** Microsoft SmartScreen 依据两个信号评估下载文件：发布者声誉（是否签名、证书是否可信发布者）与文件哈希声誉（下载历史）。
  > URL: https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation
- **[来源事实]** 首次下载分类型行为（官方表格）：Microsoft Store（无警告，MS 重新签名）| 有效证书 OV/EV（有"未识别"警告，因声誉未积累；显示核验发布者）| 无签名（必现 "Windows protected your PC"，用户须选 "Run anyway"）| 自签名（同无签名）。
- **[来源事实]** **EV 证书已不再绕过 SmartScreen**（旧行为已废止）；无签名文件每次发新版本从零声誉起、无法继承；用一致签名身份可累积证书声誉。
  > URL: https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation
- **[来源事实]** **Microsoft Store 并非必需**（"The remainder of this article applies to apps distributed outside the Store"），但 Store 分发最彻底避免 SmartScreen。Windows 11 的 **Smart App Control** 可能取代 SmartScreen，默认阻止无签名/无正面声誉文件执行。
  > URL: https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation
- **[未经核验]** OV/EV 证书市场价（OV 约 $200–300/年、EV 约 $300–700/年）为第三方 CA（DigiCert、GlobalSign 等）定价，非 Microsoft 官方内容，本次未核验。

**[推荐] Windows = 官网直发 .exe/.msi + 代码签名（OV/EV）**；初始会有 SmartScreen"未识别"警告，靠上线后一致签名声誉积累逐步消除；不依赖 Microsoft Store。

### 2.3 iPadOS 学生端（**私域直装对公众不可行，硬约束**）

- **[来源事实]** **公开分发唯一官方渠道是 App Store**。Apple Developer Enterprise Program 官方页明示，该计划"仅限大型组织向员工分发内部自用 App"，且明确：**面向公众的 App 走 App Store**。
  > URL: https://developer.apple.com/programs/enterprise/
- **[来源事实]** Enterprise Program 硬性门槛：须为法人实体、**员工 ≥100 人**、D-U-N-S 编号、公开网站、通过 Apple 核验访谈与持续评估；仅用于内部自用，不用于对外商业分发。
  > URL: https://developer.apple.com/programs/enterprise/
- **[来源事实]** TestFlight：外部测试者上限 **每 App 10,000 人**（邮件或公开邀请链接加入，需装 TestFlight App），但它是 **beta 测试**渠道，不是面向公众的正式分发。
  > URL: https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers/
  > [未经核验] 内部测试者上限每 App 100 人（来自既有知识，未抓官方原文）。
- **[来源事实]** **Apple Business / School Manager「Custom Apps」**：专为特定组织制作、含组织内部用途的 App，开发者可在 App Store Connect 选 Private 分发并指定组织 ID，让其在 Custom Apps 分区对特定组织可见，由该组织经 **MDM 或 redemption codes（兑换码）** 分发；**不面向公众**。
  > URL: https://developer.apple.com/support/volume-purchase-and-custom-apps/
- **[来源事实]** **EU 网页分发（Web Distribution）例外**：仅授权开发者、仅向 **EU 用户**、须满足 Notarization、只能从开发者在 App Store Connect 登记的域名安装、仅 iOS 17.5+/iPadOS 18+；另有受 DMA 约束的第三方市场。
  > URL: https://developer.apple.com/support/web-distribution-eu/ ；https://developer.apple.com/support/dma-and-apps-in-the-eu/

**[专业推断/结论]** 在 EU 之外（含中国大陆、美国等），**用户无法从任何公司官网直接安装 iPadOS 的 .ipa**——Apple 唯一的"网站分发"途径就是 EU 的 Web Distribution 且明确仅限 EU 用户。因此本产品若需覆盖公众 iPad 学生：
> **[推荐，二选一，须产品决策]** (a) **走 App Store 公开上架**（打破"不依赖公共商店"，仅 iPad 端例外）；或 (b) **仅向受控组织设备分发**——用 Apple Business Manager **Custom Apps**（组织经 MDM/兑换码安装）或 **Enterprise Program**（适用于自持设备/内部，≥100 员工门槛须评估）。**(c) 不推荐**：把 iPad 目标降级为浏览器 PWA（Apple 对 PWA 能力有限制），或面向公众刻意绕过 App Store，均不成立。**此约束必须向产品方显式声明，不能以"官网直装"蒙混 iPad。业主需对 iPad 是否必须"私域下载"重新决策。**

### 2.4 Android 学生端（APK 私域直传可行）

- **[来源事实]** Android 官方发布指南明确：**可不经 Google Play，将 App 放到自己网站或服务器（含私有/企业服务器）供下载分发**，步骤为托管 release-ready APK 并提供下载链接。
  > URL: https://developer.android.com/studio/publish
- **[来源事实]** "从未知来源安装"：Android 默认阻止安装来自可信第一方商店之外的 App，直到用户在系统设置中**为特定来源授予许可**。
  > URL: https://developer.android.com/studio/publish
- **[来源事实]** **Google Play Protect** 会对侧载 App 扫描，安装时弹"Play Protect hasn't seen this app before…"等警告；对从互联网侧载且申请 **RECEIVE_SMS / READ_SMS / NOTIFICATION_LISTENER / ACCESSIBILITY** 等敏感权限、与金融欺诈高相关的应用，**会自动阻止安装**。
  > URL: https://developers.google.com/android/play-protect/warning-dev-guidance

**[推荐] Android = 官网/私有服务器直发 .apk 侧载**，官方认可、对隐私企业向自己学生分发明确可行（"private or enterprise server"），但需：教师/运营引导用户开启"允许此来源"，接受 Play Protect 扫描；**应用绝不申请上述 4 类敏感权限**以免被自动阻止。

### 2.5 分发结论表

| 平台 | 私域官网直装 | 硬性前置 | 备注 |
|---|---|---|---|
| macOS | ✅ 可行 | Developer ID 签名 + Notarization | 公证非审核 |
| Windows | ✅ 可行 | 代码签名（OV/EV）；SmartScreen 初始警告、靠声誉累积 | Store 非必须 |
| Android | ✅ 可行 | 用户侧开启"未知来源"；勿申请 4 类敏感权限 | Play Protect 扫描警告 |
| iPadOS/iOS | ❌ **对公众不可行** | 公开=App Store；受控组织=ABM Custom Apps/MDM；内部=Enterprise（≥100人） | EU 网页分发例外仅 EU |

---

## 3. 云端后端、B 端 Web、本地存储/同步/协议

### 3.1 云端后端

- **[来源事实]** **Fastify**：Node.js 高效低开销 Web 框架，**内置基于 JSON Schema 的请求/出参校验（Ajv v8）**、TypeScript 一等支持、插件生态成熟。
  > 定位：Fastify 官方 Getting-Started（路由 `schema: { body: ... }` JSON Schema 校验）、TypeScript 文档（`as const` schema + 类型推断）、typescript-server.ts 官方范例。
  > URL: https://github.com/fastify/fastify/blob/main/docs/Guides/Getting-Started.md ；https://github.com/fastify/fastify/blob/main/docs/Reference/TypeScript.md ；https://github.com/fastify/fastify/blob/main/examples/typescript-server.ts

**[专业推断/推荐]** 后端 = **Node.js + TypeScript + Fastify**。与 Flutter/React 客户端同为 TS/JS 语言族、可共享 JSON Schema 契约与 TS 类型，避免跨语言 schema 双写；Fastify 的 JSON Schema/Ajv 校验正可与 §3.4 的 OpenAPI/JSON Schema 契约天然承接（同一 schema 文件驱动校验 + 生成 TS 类型）。备选：NestJS（更重、模块化更强）适合更大团队；Go（FastAPI/Axum、性能更好的另一语言）会引入跨语言契约成本。本产品一个学生一个实例、量中小的场景，Fastify 最省。

### 3.2 B 端 Web 工作台

- **[来源事实]** React 官方定位为用于构建 Web UI 的主流框架；Vite 为前端构建工具（dev server + 打包）。二者为 Web 事实标准。
  > URL: https://react.dev/ ；https://vitejs.dev/
  > [未经核验] 具体版本号/最新特性未本次核验，建议立项时查最新稳定版。

**[推荐] B 端 = React + Vite + TypeScript，浏览器直接交付、零安装。** 与后端共享 OpenAPI 生成的类型与 JSON Schema 契约。

### 3.3 本地数据存储 / 加密 / 同步协议

- **[来源事实]** **SQLite**：自包含、无服务端、零配置、单文件、事务型 SQL 数据库引擎；通过 VFS 抽象跨平台（`os_unix.c`/`os_win.c`），在 Android 上广泛使用（含 F2FS 原子写）。
  > 定位：SQLite 官方仓库 README 与 AGENTS.md、F2FS 说明。
  > URL: https://www.sqlite.org/ ；https://github.com/sqlite/sqlite
- **[来源事实]** **SQLCipher**：**SQLite 的一个分支**，为数据库文件提供 **256-bit AES 加密**、on-the-fly 解密、防篡改（HMAC）、内存清洗、强密钥派生；数据库格式与 SQLite 兼容（无 key 时行为同 SQLite，可转换明文库到加密库）。跨平台。
  > 定位：SQLCipher 官方 README 与 sqlcipher.c（AES-256-CBC 逐页加密 + 页级 HMAC 覆盖密文/IV/页号）。
  > URL: https://www.zetetic.net/sqlcipher/ ；https://github.com/sqlcipher/sqlcipher
- **[来源事实]** 异步/冲突自由同步技术存在：**Yjs**（CRDT 框架，共享 Maps/Arrays 自动冲突合并，用 Larry/CLI；Figma/Google Docs 级）、**Automerge**（CRDT、compressed format、sync protocol、主打 local-first）、**ElectricSQL**（Postgres→SQLite 的 shape 化实时复制，需 Postgres DB + Elixir 同步服务端）。这些是"离线优先 + 多端冲突合并"的重型方案。
  > URL: https://yjs.dev/ ；https://automerge.org/ ；https://electric-sql.com/ ；https://crdt.tech/

**[专业推断]** 本产品"**一个实例一个学生**"，冲突面极窄：本地权威数据主要在单 Student 实例内产生；跨端（同一学生的 iPad 与 Windows）只是同一权威数据的不同入口，不是多人并发编辑。因此在同步层**引入 Yjs/Automerge/ElectricSQL 属于过度设计**。

> **[推荐] 本地存储 = SQLite（本地权威库，存结构/证据/资产元数据/记忆/规划）+ SQLCipher 整库加密。** 同步协议 = **自研最小版本化增量**：每次学生端变更维护 `updated_at` 与**单调版本号/变更日志（changelog）**，同步时以"基线指针 + 变更批"与后端比对合并（冲突以"服务端人工校准为准 + 本地时间戳协商"）。此协议简单、可验证、不需要 CRDT 复杂度，足够支撑"本地优先 + 周期性 B 端校准回写"。
> **[推荐] 方案取舍**：不选 ElectricSQL（要求 Postgres + Elixir 同步服务端，运维重）；不选 Yjs/Automerge 作为主线（除非未来确有多人并发协作需求，再按需加入其中个子图用于"协作规划区"）。
> **[推荐] 大模型/资产文件**：学生产生的证据文件（扫描/录音/PDF）走本地文件系统 + SQLite 存元数据与哈希；大文件同步到后端用**分块上传 + 内容寻址（哈希）**去重，避免重复传输与重复存储。

### 3.4 数据契约与协议标准

- **[来源事实]** **JSON Schema**：数据校验标准（object 结构、属性、required、类型约束），用于结构化数据定义。Fastify 即用 JSON Schema（经 Ajv）做路由校验。
  > URL: https://json-schema.org/
- **[来源事实]** **OpenAPI 3**：REST API 描述规范，可从单一定义生成客户端（openapi-generator）、服务端 stub、类型与文档。
  > URL: https://www.openapis.org/
  > [未经核验] 程序化生成器（openapi-generator / orval）对 Flutter/TS 的具体代码质量未经本次实测，立项时需做了个最小验证。

**[推荐] 契约 = 以 JSON Schema / OpenAPI 为单一事实源**，三端共享：
- 定义一份 OpenAPI（含数据模型，模型即 JSON Schema）→ 同时驱动：后端 Fastify 校验、Flutter 客户端模型（openapi/JSON-schema 生成或手写轻量 toJson/fromJson）、React B 端 TS 类型。
- 本地 SQLite 的建表以同一 JSON Schema 为准（JSON 列存结构化块 + 关联表存关系），避免"数据库 schema"与"API schema"两套漂移。**一个实例一个学生 → 数据模型收敛为 StudentProfile / Evidence / Asset / Memory / Plan / Calibration 六类核心实体。**
- 平台细节（如 iPad 必需 App Store、Android 未知来源）不属于契约层，由分发方案单独管理（§2）。

### 3.5 网络不可用的正确处理（避免误读）

- площади本地优先是"本地数据权威 + 可离线读写/加密"，**不是 Agent 可离线运行**。LLM 推理在云端。
- **[推荐]** 离线态学生端：可读改本地 SQLite、可浏览历史证据与规划；**Agent 唤起前须在线**，否则明确提示"需要联网才能使用智能军师"。所有变更进入本地 changelog，联网后在后台同步 + 触发待校准区。**禁止把"本地离线"宣传为"离线 AI"。**

---

## 4. 云端 LLM 集成与经济性（与"设备不部署大模型"一致）

- **[推荐] 由后端统一代理 LLM API**：学生端 Flutter 与 B 端 React 均只调自有后端 HTTPS 接口；后端着持有 LLM Provider 的 API Key、统一计量、可插拔多 Provider。好处：密钥永不出设备、可在后端做上下文组装与周期校准回放、可在服务端做成本与风控。
- **[推荐] 上下文组装**：Agent 每次调用 LLM 时，后端从学生实例拉取"本地权威数据（经同步）+ 最近校准记录 reference + 相关证据摘要"，受限于单实例数据量与 token 预算做召回；大资产文件不进 prompt（用摘要/检索）。
- **[来源事实] 装置端模型即"本地模型"说法错误**：本架构自始至终不用本地模型；"本地数据/本地库"与"本地模型"是两回事（CLAUDE.md 亦要求避免误称）——本报告全程以"本地数据/本地数据库/本地文件"表述。

> **[推荐]** Key/上下文在本端不落盘、日志脱敏；对 LLM 类 file 内容只存元数据+哈希（§3.3），提示词构建在服务端内存完成，避免把敏感原文持久化到明文（配合 SQLCipher 加密本地缓存）。

---

## 5. 最小实用推荐栈（资源复用 / 平台适配 / 组件自建划分）

### 5.1 整体架构

```
┌─────────────┐   HTTPS(OpenAPI 契约)   ┌──────────────────────┐   HTTPS    ┌──────────────┐
│ 学生端 Flutter │ ──────────────────────▶ │ 云端后端 Fastify(TS)   │ ──────────▶ │ LLM Provider │
│ mac/Win/iPad  │ ◀────────────────────── │  ·统一代理 Agent/LLM   │ ◀─────────  │  （云端大模型）│
│ /Android      │                          │  ·学生实例权威数据入库   │            └──────────────┘
│  ·本地 SQLite │     本地 changelog 同步    │  ·周期校准记录          │
│  ·SQLCipher  │                          └───────▲──────────────┘
│  ·离线读写    │                                  │ OpenAPI/JSON Schema
└─────────────┘                                  └──────────────────┐
                                        ┌──────────────────────────┘
                                        ▼
                               ┌──────────────────────┐
                               │ B 端 Web 工作台（React） │
                               │  ·浏览器零安装 PC 访问     │
                               │  ·查看/校准学生实例        │
                               │  ·回写校准→后端→同步到学生端 │
                               └──────────────────────┘
```

### 5.2 代码库 / 共享 / 复用划分

| 工件 | 归属 | 共享/适配说明 |
|---|---|---|
| **契约（OpenAPI + JSON Schema）** | 独立目录/包 | 三端共用的事实源；驱动 Fastify 校验、Flutter 模型、React 类型 |
| 学生端 Flutter 应用 | 独立仓库（Dart） | 同一代码库四平台构建，仅按平台差异化：分发签名/公证、文件目录、系统权限 |
| 云端后端 Fastify(TS) | 独立仓库/服务 | 复用契约生成类型；独有：LLM 代理、实例存储、同步端点、校准 API |
| B 端 React 工作台 | 独立仓库（TS） | 复用契约生成类型；调后端校准 API |
| TS 类型/NPM 包 | 后端 + B 端共享 | 同一 `@shared` 包（由 OpenAPI 生成或手写） |
| LLM 客户端 | 后端独有 | 学生端/B 端不持 Key、不直连 Provider |
| 本地加密库 | 学生端 | SQLCipher（Flutter 侧 sqflite_sqlcipher / drift） |

### 5.3 自建 vs 复用建议

- **复用（采购/开源）**：Flutter 框架、SQLite、SQLCipher、Fastify、React/Vite、JSON Schema、OpenAPI、LLM SDK。
- **自建（小）**：版本化同步协议、LLM 代理层、校准回放逻辑、上下文组装（结合产品语义，需定制）。
- **明确不引入（避免过度设计）**：CRDT（Yjs/Automerge）、ElectricSQL/Postgres 复制同步、本地大模型（ollama 等）、多 Device 实时多人协同引擎——均与"单实例/少重复/不需要离线 AI"冲突。

### 5.4 待办 / 未核验清单（交付前需确认）

1. **iPad 分发决策**（阻塞）：公众 iPad 私域直装不可行（§2.3），须在 App Store 公开 / ABM Custom Apps 受控 / Enterprise 内部 之间选定，并对 iPad 是否必须入局做产品决策。
2. **代码签名成本与供应商**：Windows OV/EV 证书、Apple Developer Program/ Enterprise 费用为第三方/Apple 商务定价，[未经核验] 具体金额立项时询价。
3. **JSON Schema→Flutter 代码生成质量**：[未经核验] openapi-generator/orval 对 Dart 产物质量未实测，建议立项做最小验证，必要时手写 light model。
4. **EU 学生是否涵盖**：若产品含欧盟用户，iPad EU 网页分发路径可开启，否则跳过。
5. **数据隐私/未成年人合规**（如中国大陆未成年人保护法、个保法）+ 加密 Key 托管策略（KDF 用口令/设备级 Keychain/Keystore）。

---

## 附：证据来源汇总（官方一手）

- Flutter 平台支持 / 桌面构建：https://docs.flutter.dev/platform-integration/desktop ；https://flutter.dev/
- React Native 平台：https://github.com/react/react-native/blob/main/README.md
- Expo（out-of-tree macOS/tvOS）源码：https://github.com/expo/expo/blob/main/packages/@expo/config/src/Config.ts
- Tauri v2 移动端说明：https://v2.tauri.app/ ；https://github.com/tauri-apps/tauri-docs/blob/v2/src/content/docs/blog/tauri-2.0.mdx
- Electron 平台：https://www.electronjs.org/
- Apple 公证 macOS：https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution ；https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/1/web/1
- Apple Enterprise Program：https://developer.apple.com/programs/enterprise/
- Apple TestFlight 外部测试者：https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers/
- Apple Custom Apps / ABM：https://developer.apple.com/support/volume-purchase-and-custom-apps/
- Apple EU 网页分发：https://developer.apple.com/support/web-distribution-eu/ ；EU DMA：https://developer.apple.com/support/dma-and-apps-in-the-eu/
- Microsoft SmartScreen 声誉：https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation
- Android 发布(网站直发)：https://developer.android.com/studio/publish ；Play Protect：https://developers.google.com/android/play-protect/warning-dev-guidance
- Fastify（JSON Schema/Ajv/TS）：https://github.com/fastify/fastify/blob/main/docs/Guides/Getting-Started.md ；TypeScript 文档；typescript-server.ts
- SQLite：https://www.sqlite.org/ ；https://github.com/sqlite/sqlite（AGENTS.md / README / F2FS）
- SQLCipher：https://www.zetetic.net/sqlcipher/ ；https://github.com/sqlcipher/sqlcipher（README / sqlcipher.c）
- JSON Schema：https://json-schema.org/ ；OpenAPI：https://www.openapis.org/
- Yjs：https://yjs.dev/ ；Automerge：https://automerge.org/ ；ElectricSQL：https://electric-sql.com/