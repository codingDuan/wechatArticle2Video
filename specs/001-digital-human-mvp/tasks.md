# 任务清单: 数字人 MVP 后端 (云LLM服务集成版)

**输入**: 设计文档位于 `/specs/001-digital-human-mvp/`
**先决条件**: plan.md, spec.md, research.md

---

## 阶段 1: 项目设置 (共享基础设施)

**目的**: 初始化项目并配置基本结构。

- [X] T001 [P] 根据 `plan.md` 创建项目目录结构 (`src/api`, `src/services`, `src/pipeline`, `tests/`)。
- [X] T002 [P] 初始化 Python 虚拟环境并创建 `requirements.txt`，添加核心依赖: `fastapi`, `uvicorn`, `pydantic`, `pytest`, `python-dotenv`, `boto3`, `ffmpeg-python`, `pydub`, `openai`, `google-generativeai`。
- [X] T003 [P] 在 `src/core/config.py` 中设置配置加载逻辑，用于读取云服务API密钥、S3配置以及新增的 `LLM_PROVIDER` (值为 "openai" 或 "gemini")。
- [X] T004 [P] 创建基础 FastAPI 应用实例在 `src/main.py`，并设置 `/health` 健康检查端点。

---

## 阶段 2: 基础模型与服务 (所有用户故事的先决条件)

**目的**: 建立所有用户故事都依赖的核心数据模型和服务接口。

- [X] T005 [P] 在 `src/models/domain.py` 中根据 `data-model.md` 实现 Pydantic 数据模型。
- [X] T006 [P] 在 `src/api/v1/router.py` 中设置 API 版本路由。
- [X] T007 [P] 创建 `tests/` 目录下的测试文件结构，包括 `tests/unit/test_pipeline.py` 和 `tests/unit/test_services.py`。

---

## 阶段 3: 用户故事 1 - 语音数据处理流水线 (优先级: P1) 🎯 MVP 核心

**目标**: 实现从本地视频文件中提取纯净、高质量语音的离线处理流程。
**独立测试**: 提供一个本地视频文件，验证S3输出目录中是否生成了符合DNSMOS标准的纯净语音片段。

### 用户故事 1 的实现任务 (无变更)

- [X] T008 [US1] 扩展 `src/pipeline/run_pipeline.py` 脚本，使其能接受本地文件路径作为输入，并自动将其上传到S3的原始数据桶中，返回S3 URI。
- [X] T009 [P] [US1] 在 `src/pipeline/steps/step_01_extract_audio.py` 中编写脚本，使用 **FFmpeg** 从视频文件中提取原始音轨并转换为16-bit 44.1kHz WAV格式。
- [X] T010 [P] [US1] 在 `src/pipeline/steps/step_02_vad_segment.py` 中编写脚本，使用 **Silero VAD** 对完整音轨进行初步切分，剔除长静音片段。
- [X] T011 [P] [US1] 在 `src/pipeline/steps/step_03_separate_instrumentals.py` 中编写脚本，应用 **UVR5 (BS-Roformer)** 分离乐器伴奏。
- [X] T012 [P] [US1] 在 `src/pipeline/steps/step_04_semantic_segment.py` 中编写脚本，应用 **inaSpeechSegmenter (smn引擎)** 进行语义分割，区分“说话声”与“歌声”。
- [X] T013 [P] [US1] 在 `src/pipeline/steps/step_05_cut_and_filter.py` 中编写脚本，精确切出纯净的说话片段，并使用 **DNSMOS (P.808标准)** 进行质量评分，丢弃OVRL分数低于3.5的片段。
- [X] T014 [P] [US1] 在 `src/pipeline/steps/step_06_normalize_audio.py` 中编写脚本，使用 **UVR-DeEcho-DeReverb模型** 进行去混响处理。
- [X] T015 [US1] 更新 `src/pipeline/run_pipeline.py`，将 T009 到 T014 的所有细化步骤串联成一个完整的自动化处理流程。
- [X] T016 [US1] 更新 `src/services/audio_processing_service.py` 业务逻辑。
- [X] T017 [US1] 更新 `src/api/v1/endpoints/processing.py` 的API端点。

### 用户故事 1 的测试任务 (无变更)

- [X] T018 [P] [US1] 为 `audio_processing_service.py` 和各个 pipeline 步骤编写单元测试 (`tests/unit/test_pipeline.py`)。
- [X] T019 [US1] 为数据处理 API 端点编写集成测试 (`tests/integration/test_api_endpoints.py`)。

---

## 阶段 4: 用户故事 2 - ASR转写与语料构建 (优先级: P2) 🧠 MVP 核心

**目标**: 将纯净语音片段转写为文本，并构建用于LLM微调的风格化语料库。
**独立测试**: 提供一批纯净语音片段，验证系统是否能生成保留口癖的转录文本，并格式化为用于云服务微调的JSONL文件。

### 用户故事 2 的实现任务 (无变更)

- [ ] T020 [P] [US2] 在 `src/pipeline/steps/07_transcribe.py` 中编写脚本，使用 **FunASR** 对所有高质量干声进行批量转写。
- [ ] T021 [US2] 调整 **FunASR** 解码参数或后处理脚本，确保转录文本中**保留**主播的口癖、填充词。
- [ ] T022 [P] [US2] 在 `src/pipeline/analysis/extract_style.py` 中，使用TF-IDF或类似方法分析全部转录文本，构建一个“主播口癖词典”。
- [ ] T023 [US2] 在 `src/pipeline/steps/08_format_for_finetune.py` 中编写脚本，将转录文本转换为 **OpenAI** 和 **Gemini** 微调服务所需的JSONL文件格式。
- [ ] T024 [US2] 更新 `src/pipeline/run_pipeline.py`，将ASR转写和格式化任务作为数据处理流程的后续步骤。

### 用户故事 2 的测试任务 (无变更)

- [ ] T025 [P] [US2] 编写单元测试，验证 `format_for_finetune.py` 脚本是否能正确生成两种平台的JSONL格式 (`tests/unit/test_pipeline.py`)。
- [ ] T026 [US2] 人工抽查至少50条转录结果，验证其是否准确地保留了主播的语言风格。

---

## 阶段 5: 用户故事 3 - 云端人格模型训练与服务 (优先级: P3)

**目标**: 微调云端LLM以复刻人格，并构建可灵活切换后端的LLM服务。
**独立测试**: 验证微调任务能成功提交，且LLM服务能根据配置调用正确的云端模型并返回结果。

### 用户故事 3 的实现任务

- [ ] T027 [P] [US3] 编写训练脚本 `scripts/finetune_openai.py`，用于上传数据集并调用 **OpenAI Fine-tuning API**。
- [ ] T028 [P] [US3] 编写训练脚本 `scripts/finetune_gemini.py`，用于上传数据集并调用 **Google Gemini Fine-tuning API**。
- [ ] T029 [US3] 在 `src/services/llm_service.py` 中设计一个抽象基类 `LLMService`，并创建 `OpenAILLMService` 和 `GeminiLLMService` 两个实现类。
- [ ] T030 [US3] 在 `src/services/llm_service.py` 中创建一个工厂函数，该函数根据 `config.py` 中的 `LLM_PROVIDER` 环境变量，动态返回 `OpenAILLMService` 或 `GeminiLLMService` 的实例。
- [ ] T031 [P] [US3] 编写训练脚本，使用筛选出的“黄金10小时”纯净语音数据，训练一个 **GPT-SoVITS** 模型。
- [ ] T032 [US3] 在 `src/services/tts_service.py` 中创建一个服务类，用于加载和调用训练好的 **GPT-SoVITS** 模型。

### 用户故事 3 的测试任务

- [ ] T033 [P] [US3] 为 `llm_service.py` 编写单元测试，使用 `unittest.mock` 模拟 OpenAI 和 Gemini 的客户端API调用。
- [ ] T034 [P] [US3] 为 `tts_service.py` 编写单元测试，使用一个预训练的测试模型。

---

## 阶段 6: 用户故事 4 - 交互式语音聊天 MVP (优先级: P4)

**目标**: 集成所有模块，跑通一个完整的实时对话流程。
**独立测试**: 运行Web客户端，对着麦克风说话，验证系统是否能以克隆的声音和风格进行回复。

### 用户故事 4 的实现任务

- [ ] T035 [US4] 在 `src/services/livekit_service.py` 中使用 **LiveKit Agents** 框架实现核心逻辑。
- [ ] T036 [US4] 在 `livekit_service` 中集成 **Deepgram Nova-2** 客户端，用于实时语音转文本。
- [ ] T037 [US4] 将抽象的 `llm_service` 工厂函数集成到 `livekit_service` 中，实现对云端LLM的调用。
- [ ] T038 [US4] 将 `tts_service` (连接到GPT-SoVITS) 集成到 `livekit_service` 中，实现流式音频合成。
- [ ] T039 [US4] 在 `src/api/v1/endpoints/interactive.py` 中创建WebSocket端点，处理来自 **LiveKit** 的回调。

### 用户故事 4 的测试任务

- [ ] T040 [P] [US4] 为 `livekit_service.py` 中的各个集成模块编写单元测试，使用模拟客户端。

---

## 阶段 7: 打磨与部署

**目的**: 完善文档、容器化并进行最终验证。

- [ ] T041 [P] 更新 `README.md`，提供包含所有具体模型依赖和云服务配置的安装和使用说明。
- [ ] T042 [P] 为自托管的服务（UVR5流水线, FunASR, GPT-SoVITS, 主API服务）创建独立的Dockerfile。
- [ ] T043 [P] 编写 `docker-compose.yml`，用于一键启动所有**本地**服务（**不包括vLLM**）。
- [ ] T044 编写并运行 `quickstart.md` 中的所有验证步骤。

---

## 依赖关系与执行顺序

- **阶段 1 & 2** 必须首先完成。
- **阶段 3 (US1)** 是获取高质量语音数据的关键，必须先完成。
- **阶段 4 (US2)** 依赖于阶段 3 的输出。
- **阶段 5 (US3)** 依赖于阶段 3 和 4 的输出。
- **阶段 6 (US4)** 依赖于前面所有阶段的全部完成。
- **阶段 7** 在所有核心功能开发完成后进行。

### MVP 优先策略

1.  完成 **阶段 1, 2, 3**。**验证点1**: 成功生成高质量的纯净语音数据集。
2.  完成 **阶段 4**。**验证点2**: 成功生成用于云平台微调的文本语料库。
3.  完成 **阶段 5**。**验证点3**: 成功提交微调任务，并构建了可切换后端的LLM服务。
4.  完成 **阶段 6**，集成所有模块，交付可交互的 MVP。