# 🎬 pippit-overseas-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-green.svg)](https://python.org)

## ✨简介

pippit-overseas-skills 是面向 AI Agent 的海外 Pippit 技能包（Skills），通过调用 [Pippit](https://www.pippit.ai/) 的 Agent 与社媒发布能力，快速接入 AI 素材创作、素材编辑、视频下载、社媒发布和数据分析。

`Pippit` 是字节跳动/剪映旗下的 AI 综合创作平台海外版本，同时服务于人类创作者和 AI Agent。本仓库只放海外 Pippit skills；国内小云雀 skill 继续保留在 [pippit-skills](https://github.com/Pippit-dev/pippit-skills)。

## 📦 技能列表

| 技能 | 描述 | 脚本 |
|------|------|------|
| **pippit-nest-skill** | Pippit Nest Agent 技能 — 创建会话、发送 AI 图片/视频生成与编辑请求、上传参考文件、查询进展、下载结果 | `submit_run.py` `get_thread.py` `upload_file.py` `download_results.py` |
| **pippit-one-stop-skill** | Pippit 一站式技能 — 从 AI 生成/编辑到视频下载、社媒账号查询、定时发布任务管理和数据分析 | `submit_run.py` `get_thread.py` `upload_file.py` `batchcreate_schedule_task.py` `list_videos.py` |

## 🚀 快速安装

通过 `npx skills` 一键安装技能：

```bash
# 交互式选择要安装的技能
npx skills add https://github.com/Pippit-dev/pippit-overseas-skills.git

# 直接安装指定技能
npx skills add https://github.com/Pippit-dev/pippit-overseas-skills.git --skill pippit-nest-skill -y -g
npx skills add https://github.com/Pippit-dev/pippit-overseas-skills.git --skill pippit-one-stop-skill -y -g
```

安装完成后，设置环境变量即可使用：

```bash
export PIPPIT_ACCESS_KEY="your-access-key"
```

也可以使用各 skill 内的 `save_access_key.py` 将 access key 保存到本地缓存。

## 📖 使用方式

### 🔐 鉴权

所有 API 请求通过 HTTP Header 进行 Bearer Token 鉴权：

```text
Authorization: Bearer <PIPPIT_ACCESS_KEY>
```

可选环境变量：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PIPPIT_OPENAPI_BASE` | Pippit API 基础地址 | `https://www.pippit.ai` |
| `PIPPIT_BASE_URL` | 同上（优先级低于 `PIPPIT_OPENAPI_BASE`） | `https://www.pippit.ai` |
| `PIPPIT_HOME_URL` | Pippit 页面地址 | `https://www.pippit.ai/home?` |

## 📁 项目结构

```text
pippit-overseas-skills/
├── LICENSE
├── README.md
└── skills/
    ├── pippit-nest-skill/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── .gitignore
    │   └── scripts/
    │       ├── _common.py
    │       ├── submit_run.py
    │       ├── get_thread.py
    │       ├── upload_file.py
    │       ├── download_results.py
    │       └── save_access_key.py
    └── pippit-one-stop-skill/
        ├── SKILL.md
        ├── README.md
        ├── .gitignore
        ├── references/
        └── scripts/
            ├── nest/
            └── publish/
```

## 📄 License

本项目采用 [MIT License](LICENSE) 开源。

Copyright © 2026 [Pippit-dev](https://github.com/Pippit-dev)
