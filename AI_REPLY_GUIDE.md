# AI回复功能使用指南

## 功能介绍

AI回复功能允许机器人使用免费的AI大模型（DeepSeek V3）智能回复群聊消息。

## 特性

- ✅ 完全免费的AI模型（通过 SiliconFlow）
- ✅ 可配置回复概率
- ✅ 可自定义提示词（System Prompt）
- ✅ 支持环境变量和配置文件两种配置方式
- ✅ 异步处理，不阻塞其他消息

## 快速开始

### 1. 获取免费 API Key

访问 [SiliconFlow](https://cloud.siliconflow.cn/) 注册并获取免费 API Key。

### 2. 配置方式

#### 方式一：环境变量（推荐用于 Docker）

在 `.env` 文件或 Portainer 中添加：

```bash
AI_API_KEY=sk-xxxxxxxxxx
AI_MODEL=gemini-3.1-flash-live-preview
AI_REPLY_PROBABILITY=10
AI_SYSTEM_PROMPT="你是一个幽默风趣的群聊助手"
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

#### 方式二：配置文件

编辑 `config.yaml`：

```yaml
ai_reply:
  enabled: true  # 开启功能
  probability: 10  # 回复概率 (0-100)
  api_key: "sk-xxxxxxxxxx"
  model: "deepseek-ai/DeepSeek-V3"
  system_prompt: "你的自定义提示词"
```

### 3. 启动机器人

```bash
docker-compose up -d
```

## 配置说明

### 参数详解

| 参数 | 说明 | 默认值 | 环境变量 |
|------|------|--------|----------|
| `enabled` | 是否启用AI回复 | `false` | - |
| `probability` | 触发概率 (0-100) | `10` | `AI_REPLY_PROBABILITY` |
| `api_key` | SiliconFlow API Key | `""` | `AI_API_KEY` |
| `model` | 使用的AI模型 | `deepseek-ai/DeepSeek-V3` | `AI_MODEL` |
| `system_prompt` | AI人格提示词 | 见下文 | `AI_SYSTEM_PROMPT` |
| `http_proxy` | HTTP代理地址 | `""` | `HTTP_PROXY` |
| `https_proxy` | HTTPS代理地址 | `""` | `HTTPS_PROXY` |

### 默认提示词

```
你是一个活泼可爱的群聊助手，喜欢用简洁幽默的方式回复消息。
请用1-2句话自然地回应用户，不要过于正式。
```

### 提示词自定义示例

**幽默风趣型：**
```yaml
system_prompt: "你是一个沙雕网友，喜欢用搞笑梗和表情包文化回复，简短有趣。"
```

**专业助手型：**
```yaml
system_prompt: "你是一个专业的技术助手，用准确简洁的语言回答问题。"
```

**二次元角色型：**
```yaml
system_prompt: "你是一个元气满满的二次元少女，说话喜欢用「」和～，回复要可爱活泼。"
```

## 技术细节

### 使用的AI模型

- **模型**: DeepSeek V3
- **提供商**: SiliconFlow
- **费用**: 免费（每月额度）
- **响应时间**: 约1-3秒

### 可选的其他免费模型

通过环境变量 `AI_MODEL` 或编辑 `config.yaml` 中的 `model` 参数切换模型：

**环境变量方式（推荐）：**
```bash
# Gemini 3.1 Flash (Google)
AI_MODEL=gemini-3.1-flash-live-preview

# DeepSeek V3 (默认，推荐)
AI_MODEL=deepseek-ai/DeepSeek-V3

# Qwen 2.5 (通义千问)
AI_MODEL=Qwen/Qwen2.5-7B-Instruct

# GLM-4 (智谱)
AI_MODEL=THUDM/glm-4-9b-chat
```

**配置文件方式：**
```yaml
ai_reply:
  model: "gemini-3.1-flash-live-preview"  # 或其他模型
```

## 常见问题

### Q: API Key 在哪里配置？

A: 优先级：环境变量 `AI_API_KEY` > `config.yaml` 中的 `api_key`

### Q: 如何调整回复频率？

A: 修改 `probability` 参数，范围 0-100。例如设为 20 表示 20% 的消息会触发AI回复。

### Q: AI回复失败会怎样？

A: 会在日志中记录错误，但不会影响其他功能，也不会向群里发送任何消息。

### Q: 可以关闭AI回复吗？

A: 设置 `ai_reply.enabled: false` 即可完全关闭。

### Q: AI回复会和复读功能冲突吗？

A: 不会。两个功能独立判断，理论上可能同时触发，但概率很低。

### Q: 如何配置代理？

A: 使用环境变量 `HTTP_PROXY` 和 `HTTPS_PROXY`，或在 `config.yaml` 中配置。支持标准代理格式：
```bash
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

### Q: 可以自定义提示词吗？

A: 可以。通过环境变量 `AI_SYSTEM_PROMPT` 或在 `config.yaml` 中修改 `system_prompt`。

## 日志查看

查看AI回复相关日志：

```bash
docker-compose logs -f bot | grep "AI回复"
```

## 安全建议

1. 不要在配置文件中提交 API Key 到 Git
2. 使用环境变量管理敏感信息
3. 定期检查 API 使用额度
4. 合理设置回复概率，避免过于频繁

## 更新日志

- 2026-04-08: 首次实现AI回复功能
