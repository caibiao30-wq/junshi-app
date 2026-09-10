# llama_index 工程代码库目录框架图

> 状态：**候选归纳**（只读目录调研，未读代码正文，未联网查外部资料）。仅供了解工程代码库目录布局参考，不升级为产品决策或通用模板。
> 深度：两层。仅按目录/文件层级标注职责，不涉及框架实现代码与 API。
> 数据来源：`/Users/caibiao/Downloads/llama_index-main`（仓库解压目录，v 参照仓库 HEAD）。

## 顶层结构
├── `llama-index-core/`   → 职责：框架核心包，承载 LLM 应用核心抽象与引擎（数据索引、查询、agent、workflow 等）
├── `llama-index-integrations/`   → 职责：第三方生态集成包的分域合集（LLM、向量库、读取器等，按功能域各成子目录）
├── `llama-index-instrumentation/`   → 职责：可观测性与埋点（instrumentation/event）独立包
├── `llama-index-utils/`   → 职责：与特定云/平台绑定的小工具包合集（azure、huggingface、oracleai、qianfan）
├── `llama-dev/`   → 职责：内部开发工具包（辅助包开发/测试流程的脚本代码）
├── `docs/`   → 职责：文档站源码（API 参考、示例、内容）
├── `scripts/`   → 职责：仓库级运维/发布/体检脚本（版本升级、发版、集成健康检查、文档同步）
├── `.github/`   → 职责：GitHub 工作流与贡献模板
├── 根级文件（`README.md`、`pyproject.toml`、`Makefile`、`uv.lock`、`CHANGELOG.md`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`、`STALE.md`、`LICENSE`、`CITATION.cff`、`.pre-commit-config.yaml`、`.readthedocs.yaml`、`docs.config.mjs`、`RELEASE_HEAD.md`、`.gitignore`）   → 职责：项目说明、依赖与构建配置、发布/安全/贡献规范等仓库元信息

## 第二层（职责相关的主要子目录）
### llama-index-core/（核心包）
├── `llama_index/core/`   → 职责：实际核心代码包（下分各功能模块，见下）
│   ├── `agent/`   → 职责：Agent（智能体）框架
│   ├── `chat_engine/`   → 职责：聊天引擎
│   ├── `query_engine/`   → 职责：查询引擎
│   ├── `workflow/`   → 职责：工作流（事件驱动编排）
│   ├── `indices/`   → 职责：索引结构（如 VectorStoreIndex 等）
│   ├── `storage/`   → 职责：存储抽象（文档/索引/向量库持久化）
│   ├── `vector_stores/`   → 职责：向量库抽象与接入
│   ├── `embeddings/`   → 职责：Embedding 模型抽象
│   ├── `llms/`   → 职责：LLM 抽象
│   ├── `multi_modal_llms/`   → 职责：多模态模型抽象
│   ├── `node_parser/`   → 职责：文档节点切分解析
│   ├── `text_splitter/`   → 职责：文本切分
│   ├── `readers/`   → 职责：数据读取器
│   ├── `extractors/`   → 职责：元数据/标签提取器
│   ├── `postprocessor/`   → 职责：节点后处理（重排、过滤）
│   ├── `retrievers/`   → 职责：检索器
│   ├── `response_synthesizers/`   → 职责：响应合成
│   ├── `output_parsers/`   → 职责：输出解析
│   ├── `question_gen/`   → 职责：问题生成
│   ├── `evaluation/`   → 职责：评测
│   ├── `memory/`   → 职责：对话记忆
│   ├── `tools/`   → 职责：工具抽象
│   ├── `program/`   → 职责：结构化程序/输出引导
│   ├── `callbacks/`   → 职责：回调
│   ├── `prompts/`   → 职责：提示词模板
│   ├── `schema.py`   → 职责：核心数据结构定义（Node、Document 等）
│   ├── `settings.py` / `service_context.py`   → 职责：全局配置与服务上下文
│   ├── `bridge/`   → 职责：与其他生态桥接（如 langchain）
│   ├── `composability/`   → 职责：组件组合
│   ├── `base/`   → 职责：基础公共类型/基类
│   └── `tests/`   → 职责：核心包测试
├── `pyproject.toml`   → 职责：核心包构建与依赖声明
├── `Makefile` / `uv.lock`   → 职责：构建与锁依赖
### llama-index-integrations/（集成包，按功能域分）
├── `llms/`   → 职责：各类第三方 LLM 接入包（anthropic、openai、gemini 等 90+ 子包）
├── `embeddings/`   → 职责：Embedding 模型接入包
├── `sparse_embeddings/`   → 职责：稀疏向量/BM25 类接入包
├── `vector_stores/`   → 职责：第三方向量库接入包
├── `graph_stores/`   → 职责：图数据库接入包
├── `readers/`   → 职责：数据源读取器接入包
├── `tools/`   → 职责：第三方工具接入包
├── `agent/`   → 职责：Agent 生态接入包
├── `memory/`   → 职责：记忆存储接入包
├── `storage/`   → 职责：存储后端接入包
├── `node_parser/`   → 职责：节点解析器接入包
├── `postprocessor/`   → 职责：后处理器接入包
├── `retrievers/`   → 职责：检索器接入包
├── `response_synthesizers/`   → 职责：响应合成器接入包
├── `indices/`   → 职责：索引实现接入包
├── `question_gen/`   → 职责：问题生成接入包
├── `extractors/`   → 职责：提取器接入包
├── `output_parsers/`   → 职责：输出解析器接入包
├── `selectors/`   → 职责：选择器接入包
├── `callbacks/`   → 职责：回调接入包
├── `observability/`   → 职责：可观测性接入包
├── `program/`   → 职责：程序式输出接入包
├── `ingestion/`   → 职责：摄取流水线接入包
├── `graph_rag/`   → 职责：GraphRAG 接入包
├── `voice_agents/`   → 职责：语音 agent 接入包
└── `protocols/`   → 职责：通用协议/接口接入包
### llama-index-instrumentation/（可观测性）
├── `src/llama_index_instrumentation/`   → 职责：instrumentation 与事件埋点实现
├── `tests/`   → 职责：测试
└── `pyproject.toml`   → 职责：构建与依赖声明
### llama-index-utils/（云平台小工具）
├── `llama-index-utils-azure/`   → 职责：Azure 相关工具
├── `llama-index-utils-huggingface/`   → 职责：HuggingFace 相关工具
├── `llama-index-utils-oracleai/`   → 职责：Oracle AI 相关工具
└── `llama-index-utils-qianfan/`   → 职责：百度千帆相关工具
### llama-dev/（开发工具）
├── `llama_dev/`   → 职责：内部开发辅助代码包
├── `tests/`   → 职责：测试
└── `pyproject.toml`   → 职责：构建与依赖声明
### docs/（文档站）
├── `src/content/`   → 职责：文档站正文内容
├── `api_reference/`   → 职责：API 参考
├── `examples/`   → 职责：示例代码
└── `scripts/`   → 职责：文档构建辅助脚本
### scripts/（仓库级脚本）
├── `publish_packages.sh`   → 职责：发布各子包
├── `bulk-version-bump.py`   → 职责：批量版本升级
├── `integration_health_check.py`   → 职责：集成包健康检查
├── `sync-docs-to-developer-hub.sh`   → 职责：文档同步到开发者中心
└── `convert-examples.py`   → 职责：示例转换

---

## 备注
- **层级边界**：以上为两层框架；`llama-index-integrations/` 下每个功能域（如 `llms/`、`vector_stores/`）内还各有大量具体厂商子包（如 `llama-index-llms-openai`），因深度限制未逐一下钻，归入对应功能域一并标注。
- **待核验项**：
  - 部分模块（如 `bridge/`、`composability/`、`protocols/`、`voice_agents/`、`graph_rag/`）的具体职责与用法未读代码正文，为一句话职责推断，需读源码方可确认。
  - `llama-index-utils/` 下四个子包的职责依据目录名推断（azure/huggingface/oracleai/qianfan），未见代码，标注待核验。
  - 未覆盖的顶层项（如各 md/配置文件的细微用途、`.github` 内具体 workflow）仅列名称，未深究。
- **未读代码正文**：本框架图仅基于目录/文件命名归纳，所有职责为候选推断，不代表已核实实现语义。
