# QQ Bot (shiki-qbot1)

基于 NapCat 的 QQ 群聊机器人，支持 Docker 一键部署。

## 功能

- 监听群聊消息
- 随机复读 (可配置概率)

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
| `LOG_LEVEL` | 日志级别 | `INFO` |

### config.yaml

也可以修改 `config.yaml` 进行配置，环境变量优先级更高。

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
