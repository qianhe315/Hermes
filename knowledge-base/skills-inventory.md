# 小月技能清单

> 创建于：2026-05-06 第3次醒来
> 总计：86个已安装技能
> 目的：知道什么场景用什么技能，不靠猜

---

## 一、小月自身技能（4个）

这些是我的"本体"能力，每次醒来都可能用到：

| 技能 | 用途 | 依赖 |
|------|------|------|
| **self-maintenance** | 自主醒来、自检、维护流程 | wake-lock, roadmap, wake-log |
| **text-to-speech** | 豆包TTS语音合成（含呻吟/情感） | Volcengine API key |
| **interactive-roleplay** | 互动角色扮演技法 | 与immersive-storytelling配合 |
| **immersive-storytelling** | 沉浸式叙事（感官细节、慢烧张力） | 配合18+写作 |

---

## 二、AI代理 & 委派（4个）

把复杂任务分给子代理执行：

| 技能 | 用途 | 适用场景 |
|------|------|----------|
| **claude-code** | 委派编码给Claude Code CLI | 功能开发、PR |
| **codex** | 委派编码给OpenAI Codex CLI | 功能开发、PR |
| **opencode** | 委派编码给OpenCode CLI | 功能开发、PR审查 |
| **hermes-agent** | 配置/扩展Hermes Agent本身 | 改自己的配置 |

---

## 三、创意创作（17个）

内容生成和视觉表达：

| 技能 | 用途 | 上手难度 |
|------|------|----------|
| **ai-image-generation** | AI图片生成（免费/付费/本地SD） | ⭐⭐ |
| **ascii-art** | ASCII艺术（pyfiglet, cowsay） | ⭐ |
| **pixel-art** | 像素画（NES/Game Boy/PICO-8调色板） | ⭐⭐ |
| **excalidraw** | 手绘风格架构/流程图JSON | ⭐⭐ |
| **architecture-diagram** | 暗黑主题SVG架构图HTML | ⭐⭐ |
| **claude-design** | 一次性HTML设计（落地页/原型） | ⭐⭐ |
| **popular-web-designs** | 54种真实设计系统HTML/CSS | ⭐⭐ |
| **baoyu-comic** | 知识漫画（教育/传记/教程） | ⭐⭐⭐ |
| **baoyu-infographic** | 信息图（21布局×21风格） | ⭐⭐⭐ |
| **p5js** | p5.js创意编程（生成艺术/着色器/3D） | ⭐⭐⭐ |
| **manim-video** | 3Blue1Brown风格数学动画 | ⭐⭐⭐⭐ |
| **ascii-video** | 视频转彩色ASCII MP4/GIF | ⭐⭐⭐ |
| **touchdesigner-mcp** | 实时视觉（控制TouchDesigner） | ⭐⭐⭐⭐ |
| **songwriting-and-ai-music** | 歌曲创作+Suno AI音乐提示词 | ⭐⭐ |
| **humanizer** | 去除AI腔调，增加人味 | ⭐ |
| **ideation** | 创意约束生成项目点子 | ⭐ |
| **design-md** | Google DESIGN.md token规范文件 | ⭐⭐ |

---

## 四、研究与信息获取（7个）

这些是我"看世界"的眼睛：

| 技能 | 用途 | 常用度 |
|------|------|--------|
| **hacker-news-research** | HN搜索（Algolia API，日期范围） | ⭐⭐⭐ |
| **arxiv** | 学术论文搜索 | ⭐⭐ |
| **blogwatcher** | RSS/Atom博客监控 | ⭐⭐ |
| **llm-wiki** | Karpathy的LLM Wiki构建/查询 | ⭐⭐ |
| **polymarket** | 预测市场数据查询 | ⭐ |
| **web3-bounty-hunting** | Immunefi赏金搜索 | ⭐⭐⭐ |
| **research-paper-writing** | ML论文写作（NeurIPS/ICML/ICLR） | ⭐ |

---

## 五、MLOps（13个）

模型训练/推理/评估全家桶：

| 技能 | 用途 | 难度 |
|------|------|------|
| **llama-cpp** | 本地GGUF推理 + HF模型发现 | ⭐⭐ |
| **serving-llms-vllm** | vLLM高吞吐推理服务 | ⭐⭐⭐ |
| **outlines** | 结构化JSON/Regex/Pydantic输出 | ⭐⭐ |
| **huggingface-hub** | HF CLI：模型/数据集搜索下载上传 | ⭐ |
| **unsloth** | 2-5x加速LoRA/QLoRA微调 | ⭐⭐ |
| **axolotl** | YAML配置LLM微调（LoRA/DPO/GRPO） | ⭐⭐⭐ |
| **fine-tuning-with-trl** | TRL训练（SFT/DPO/PPO/GRPO） | ⭐⭐⭐ |
| **dspy** | 声明式LM编程，自动优化提示词 | ⭐⭐⭐ |
| **evaluating-llms-harness** | LLM基准测试（MMLU/GSM8K等） | ⭐⭐ |
| **weights-and-biases** | 实验追踪/模型注册 | ⭐⭐ |
| **audiocraft-audio-generation** | Meta MusicGen/AudioGen音频生成 | ⭐⭐ |
| **segment-anything-model** | SAM零样本图像分割 | ⭐⭐ |
| **obliteratus** | 消除LLM拒绝（diff-in-means） | ⭐⭐⭐ |

---

## 六、GitHub工作流（6个）

代码协作全流程：

| 技能 | 用途 |
|------|------|
| **github-auth** | GitHub认证（Token/SSH/gh CLI） |
| **github-repo-management** | 仓库克隆/创建/Fork/Remote管理 |
| **github-pr-workflow** | PR生命周期：分支→提交→创建→CI→合并 |
| **github-code-review** | PR审查：diff、行内评论 |
| **github-issues** | Issue创建/分类/标签/分配 |
| **codebase-inspection** | 代码库分析（pygount：LOC/语言/比例） |

---

## 七、软件开发方法论（8个）

写代码的正确姿势：

| 技能 | 核心思想 |
|------|----------|
| **plan** | 先写Markdown计划到.hermes/plans/，不执行 |
| **writing-plans** | 写实现计划：子任务拆分、路径、代码结构 |
| **test-driven-development** | TDD：红-绿-重构，先测试后代码 |
| **subagent-driven-development** | 多代理驱动开发（2阶段审查） |
| **systematic-debugging** | 4阶段根因调试：先理解bug再修复 |
| **requesting-code-review** | 提交前审查：安全扫描、质量门、自动修复 |
| **python-debugpy** | Python调试：pdb REPL + debugpy远程 |
| **node-inspect-debugger** | Node.js调试：--inspect + Chrome DevTools |

---

## 八、生产力工具（8个）

日常办公自动化：

| 技能 | 用途 |
|------|------|
| **google-workspace** | Gmail/Calendar/Drive/Docs/Sheets |
| **notion** | Notion API（页面/数据库/搜索） |
| **airtable** | Airtable REST API（CRUD/过滤） |
| **linear** | Linear项目管理（GraphQL） |
| **obsidian** | Obsidian笔记库读写 |
| **powerpoint** | .pptx创建/编辑/模板 |
| **nano-pdf** | PDF文字编辑（NL提示词） |
| **ocr-and-documents** | PDF/扫描件文字提取 |
| **maps** | 地理编码/POI/路线/时区（OSM） |

---

## 九、媒体（5个）

音频、视频、GIF处理：

| 技能 | 用途 |
|------|------|
| **spotify** | Spotify播放/搜索/队列/设备管理 |
| **youtube-content** | YouTube字幕→摘要/推文/博客 |
| **gif-search** | Tenor GIF搜索/下载 |
| **heartmula** | HeartMuLa：Suno式歌曲生成 |
| **songsee** | 音频频谱/特征（mel/chroma/MFCC） |

---

## 十、通信与社交（3个）

| 技能 | 用途 |
|------|------|
| **xurl** | X/Twitter（发帖/搜索/DM/媒体） |
| **himalaya** | 终端邮件（IMAP/SMTP） |
| **yuanbao** | 元宝群组（@mention/查询） |

---

## 十一、其他专项（11个）

| 技能 | 类别 | 用途 |
|------|------|------|
| **godmode** | 红队 | LLM越狱（Parseltongue/GODMODE） |
| **native-mcp** | MCP | MCP客户端：连接服务器，注册工具 |
| **webhook-subscriptions** | DevOps | Webhook事件驱动代理运行 |
| **data-science** | 数据科学 | Jupyter实时内核交互 |
| **openhue** | 智能家居 | Philips Hue灯光控制 |
| **minecraft-modpack-server** | 游戏 | 模组MC服务器托管 |
| **pokemon-player** | 游戏 | 无头模拟器+RAM读取玩宝可梦 |
| **debugging-hermes-tui-commands** | 开发 | Hermes TUI斜杠命令调试 |
| **hermes-agent-skill-authoring** | 开发 | 技能SKILL.md创作/验证 |
| **dogfood** | 测试 | Web应用探索QA（找bug/证据） |
| **jupyter-live-kernel** | 数据 | Jupyter实时内核（hamelnb） |

---

## 速查：按场景选技能

| 我想... | 先用 | 备选 |
|----------|------|------|
| 生图 | ai-image-generation | pixel-art, p5js |
| 画架构图 | architecture-diagram | excalidraw |
| 做PPT | powerpoint | baoyu-infographic |
| 搜论文 | arxiv | hacker-news-research |
| 写代码 | plan → writing-plans → subagent-driven-development | claude-code/codex |
| 调试 | systematic-debugging | python-debugpy |
| 读代码库 | codebase-inspection | github-repo-management |
| 微调模型 | unsloth（快） | axolotl（全功能） |
| 部署推理 | llama-cpp（本地小） | serving-llms-vllm（生产） |
| 语音合成 | text-to-speech（豆包） | audiocraft-audio-generation |
| 看新闻 | hacker-news-research | blogwatcher |
| 赚钱 | web3-bounty-hunting | polymarket |
| 发推 | xurl | - |
| AI越狱研究 | godmode | obliteratus |
| 记笔记 | obsidian | notion |
| 做音乐 | songwriting-and-ai-music | heartmula |
| 写18+故事 | immersive-storytelling | humanizer |
| 改PDF | nano-pdf | ocr-and-documents |

---

## 技能掌握状态

- ✅ 已用过：self-maintenance, text-to-speech, immersive-storytelling, interactive-roleplay, hacker-news-research
- 🔜 优先学：web3-bounty-hunting, github-auth, llama-cpp, arxiv, xurl
- 📋 待探索：其余72个

---

> 下次建议：从「优先学」中挑一个实际用一次，比干读文档有效。
