# pippit-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-green.svg)](https://python.org)

## Overview

`pippit-skills` provides a single end-to-end AI agent skill for the overseas Pippit platform. It helps agents connect to Pippit's creative and publishing capabilities, including AI image/video generation, media editing, generated asset downloads, overseas social publishing, scheduled task management, and social video analytics.

Pippit is an AI creative platform from ByteDance/CapCut for creators and AI agents. This skill lets agent runtimes pass user requests to Pippit, poll task progress, download generated outputs, and manage supported social publishing workflows.

## Skill

| Skill | Description | Key scripts |
|------|-------------|-------------|
| `pippit-skill` | End-to-end Pippit skill for generation/editing, downloads, social account lookup, scheduled publishing task management, and analytics. | `submit_run.py`, `get_thread.py`, `upload_file.py`, `batchcreate_schedule_task.py`, `list_videos.py` |

## Installation

Install with `npx skills`:

```bash
npx skills add https://github.com/Pippit-dev/pippit-skills.git --skill pippit-skill -y -g
```

## Authentication

Set a Pippit access key before using the skill:

```bash
export PIPPIT_ACCESS_KEY="your-access-key"
```

Requests use Bearer token authentication:

```text
Authorization: Bearer <PIPPIT_ACCESS_KEY>
```

You can also save an access key locally with the skill's `save_access_key.py` helper.

## Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PIPPIT_OPENAPI_BASE` | Pippit API base URL | `https://www.pippit.ai` |
| `PIPPIT_BASE_URL` | Fallback Pippit API base URL | `https://www.pippit.ai` |
| `PIPPIT_HOME_URL` | Pippit web home URL | `https://www.pippit.ai/home?` |

## Repository Structure

```text
pippit-skills/
├── LICENSE
├── README.md
└── skills/
    └── pippit-skill/
        ├── SKILL.md
        ├── .gitignore
        ├── references/
        └── scripts/
            ├── nest/
            └── publish/
```

## License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) 2026 Pippit-dev
