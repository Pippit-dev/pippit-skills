# 🎬 pippit-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-green.svg)](https://python.org)

## ✨简介

pippit-skills 是一组面向 AI Agent 的创作技能包（Skills），通过调用[小云雀](https://xyq.jianying.com/)/[Pippit](https://www.pippit.ai/) 的Agent能力，快速接入AI 素材创作、素材编辑、社媒营销等能力。

`小云雀/Pippit`是字节跳动/剪映旗下的 AI 综合创作平台，同时服务于人类创作者和 AI Agent。本技能让 Openclaw/Claude Code 等 AI Agent 能够作为"传话人"，将用户的创作需求转发给Agent 处理。

## 📦 技能列表

| 技能                 | 描述 | 脚本                                                                                   |
|--------------------|------|--------------------------------------------------------------------------------------|
| **xyq-nest-skill** | Agent-会话技能 — 创建会话、发送生图/生视频消息、上传文件、查询进展、批量下载结果 | `submit_run.py` `get_thread.py` `upload_file.py` `download_results.py` |


## 🚀 快速安装

通过 `npx skills` 一键安装技能到你的项目中：

```bash
# 交互式选择要安装的技能
npx skills add Pippit-dev/pippit-skills

# 直接安装指定技能
npx skills add Pippit-dev/pippit-skills --skill xyq-nest-skill
```

安装完成后，设置环境变量即可使用：

```bash
export XYQ_ACCESS_KEY="your-access-key"
```

## 📖 使用方式

### 🔐 鉴权

所有 API 请求通过 HTTP Header 进行 Bearer Token 鉴权：

```
Authorization: Bearer <XYQ_ACCESS_KEY>
```

可选环境变量：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `XYQ_OPENAPI_BASE` | API 基础地址 | `https://xyq.jianying.com` |
| `XYQ_BASE_URL` | 同上（优先级低于 `XYQ_OPENAPI_BASE`） | `https://xyq.jianying.com` |

## 📁 项目结构

```
pippit-skills/
├── LICENSE                         # MIT License
├── README.md                       # 项目说明
└── skills/
    └── xyq-nest-skill/
        ├── SKILL.md                # 技能说明
        ├── README.md               # 项目说明
        ├── .gitignore
        └── scripts/
            ├── _common.py          # 公共模块：配置、API 请求、响应解析
            ├── submit_run.py       # 创建会话 / 发送消息
            ├── get_thread.py       # 查询会话进展
            ├── upload_file.py      # 上传文件到资产库
            └── download_results.py # 批量下载生成结果
```

## 📄 License

本项目采用 [MIT License](../../LICENSE) 开源。

Copyright © 2026 [Pippit-dev](https://github.com/Pippit-dev)
