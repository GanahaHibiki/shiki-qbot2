# QQ 机器人需求文档

## 项目概述

基于 NapCat 客户端的 QQ 群聊机器人，支持 Docker 一键部署。

## 技术栈

| 组件 | 技术选型 |
|------|----------|
| QQ 客户端 | NapCat (OneBot 11 协议) |
| 机器人框架 | Python + onebot-api |
| 部署方式 | Docker Compose (Portainer 兼容) |
| 通信协议 | WebSocket (反向 WS) |

## 架构设计

```
┌─────────────┐     WebSocket      ┌─────────────┐
│   NapCat    │ ◄────────────────► │   Bot App   │
│  (QQ客户端)  │   OneBot 11 协议   │  (Python)   │
└─────────────┘                    └─────────────┘
       │                                  │
       └──────────── Docker Compose ──────┘
```

## 功能需求

### F1: 群消息监听

- **触发条件**: 收到群聊消息
- **处理逻辑**: 解析消息内容、发送者、群号
- **数据结构**:
  ```json
  {
    "post_type": "message",
    "message_type": "group",
    "group_id": 123456,
    "user_id": 789012,
    "message": "消息内容",
    "raw_message": "原始消息"
  }
  ```

### F2: 随机复读

- **触发条件**: 收到群聊消息
- **复读概率**: 可配置 (默认 5%)
- **处理逻辑**:
  1. 生成 0-100 随机数
  2. 若随机数 < 配置概率，则复读该消息
  3. 复读内容与原消息完全一致
- **配置项**:
  ```yaml
  repeat:
    enabled: true
    probability: 5  # 百分比
  ```

## 配置文件

### config.yaml

```yaml
# 机器人配置
bot:
  # NapCat WebSocket 地址
  ws_url: "ws://napcat:3001"

# 复读功能
repeat:
  enabled: true
  probability: 5  # 复读概率 (0-100)

# 日志级别
log_level: "INFO"
```

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `WS_URL` | NapCat WS 地址 | `ws://napcat:3001` |
| `REPEAT_PROBABILITY` | 复读概率 | `5` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

## 部署配置

### docker-compose.yml 结构

```yaml
services:
  napcat:
    # NapCat 容器配置
    # 端口: 3001 (WebSocket)
    
  bot:
    # 机器人应用容器
    # 依赖: napcat
    # 配置: 通过环境变量或挂载 config.yaml
```

### 目录结构

```
shiki-qbot1/
├── bot/
│   ├── main.py           # 入口文件
│   ├── config.py         # 配置加载
│   ├── handlers/
│   │   └── message.py    # 消息处理器
│   └── requirements.txt  # Python 依赖
├── docker-compose.yml    # Docker Compose 配置
├── Dockerfile            # Bot 镜像构建
├── config.yaml           # 运行时配置
└── README.md             # 部署说明
```

## 扩展接口

为后续功能预留的接口设计:

```python
# handlers/base.py
class MessageHandler:
    async def should_handle(self, event: GroupMessageEvent) -> bool:
        """判断是否处理该消息"""
        pass
    
    async def handle(self, event: GroupMessageEvent) -> None:
        """处理消息"""
        pass

# 注册处理器
handlers: list[MessageHandler] = [
    RepeatHandler(),
    # 后续可添加更多处理器
]
```

## 部署步骤 (Portainer)

1. 在 Portainer 中创建 Stack
2. 粘贴 docker-compose.yml 内容
3. 配置环境变量 (QQ 账号等)
4. 部署启动
5. NapCat 扫码登录

## 非功能需求

- **日志**: 记录所有收发消息，便于调试
- **重连**: WebSocket 断开后自动重连
- **优雅退出**: 收到 SIGTERM 时正常关闭连接

## CI/CD

### 版本管理

- 版本号存储在 `VERSION` 文件中
- 格式: `MAJOR.MINOR.PATCH` (如 `0.2.1`)
- 初始版本: `0.2.1`

### GitHub Actions 自动构建

- **触发条件**: push 到 main 分支
- **构建流程**:
  1. 读取当前版本号
  2. 自增 PATCH 版本 (如 `0.2.1` -> `0.2.2`)
  3. 构建 Docker 镜像
  4. 推送到 Docker Hub: `ptshiki/shiki-qbot1`
  5. 提交更新后的版本号到仓库
- **镜像标签**: `latest` + 版本号 (如 `0.2.2`)
- **Secrets 依赖**:
  - `DOCKERHUB_USERNAME`: Docker Hub 用户名
  - `DOCKERHUB_TOKEN`: Docker Hub Access Token
