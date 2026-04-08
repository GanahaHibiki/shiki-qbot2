# QQ Bot (shiki-qbot1)

基于 NapCat 的 QQ 群聊机器人，支持 Docker 一键部署。

## 功能

- 监听群聊消息
- 随机复读 (可配置概率)
- AI智能回复 (使用免费AI模型，可配置提示词)

## 快速部署 (Portainer)

1. 复制 `.env.example` 为 `.env`，填入 QQ 账号
2. 在 Portainer 中创建 Stack
3. 上传 `docker-compose.yml` 或粘贴内容
4. 添加环境变量 `QQ_ACCOUNT`
5. 部署启动
6. 访问 `http://<host>:6099` 扫码登录 NapCat

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `QQ_ACCOUNT` | QQ 账号 | 必填 |
| `REPEAT_PROBABILITY` | 复读概率 (0-100) | `5` |
| `AI_REPLY_PROBABILITY` | AI回复概率 (0-100) | `10` |
| `AI_MODEL` | AI模型名称 | `deepseek-ai/DeepSeek-V3` |
| `AI_SYSTEM_PROMPT` | AI提示词 | 见配置文件 |
| `AI_API_KEY` | AI API密钥 (SiliconFlow) | 可选 |
| `HTTP_PROXY` | HTTP代理 | 可选 |
| `HTTPS_PROXY` | HTTPS代理 | 可选 |
| `LOG_LEVEL` | 日志级别 | `INFO` |

### config.yaml

也可以修改 `config.yaml` 进行配置，环境变量优先级更高。

#### AI回复配置说明

AI回复功能使用免费的 DeepSeek V3 模型，通过 SiliconFlow 提供的免费API。

```yaml
ai_reply:
  enabled: false  # 开启/关闭
  probability: 10  # 回复概率
  api_key: "your-api-key"  # SiliconFlow API Key
  model: "deepseek-ai/DeepSeek-V3"  # 模型名称
  system_prompt: "你的自定义提示词"  # 自定义AI人格
```

**获取免费API Key:**
1. 访问 [SiliconFlow](https://cloud.siliconflow.cn/)
2. 注册并获取免费API Key
3. 每月有免费额度，足够个人使用

**默认提示词:**
> 你是一个活泼可爱的群聊助手，喜欢用简洁幽默的方式回复消息。请用1-2句话自然地回应用户，不要过于正式。

可以根据需要自定义提示词来改变AI的回复风格。

## 目录结构

```
shiki-qbot1/
├── bot/                  # 机器人代码
│   ├── main.py           # 入口
│   ├── config.py         # 配置加载
│   └── handlers/         # 消息处理器
├── docker-compose.yml    # Docker 编排
├── Dockerfile            # 镜像构建
├── config.yaml           # 配置文件
└── .env.example          # 环境变量示例
```

## 本地开发

```bash
cd bot
pip install -r requirements.txt
python main.py
```
