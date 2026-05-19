# 🎬 pippit-one-stop-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-green.svg)](https://python.org)

Self-contained end-to-end Pippit.ai skill for AI creative generation, asset downloads, overseas social video publishing, scheduled task management, and analytics.

## Install

```bash
npx skills add https://github.com/Pippit-dev/pippit-overseas-skills.git --skill pippit-one-stop-skill -y -g
```

## Features

Use one natural-language request to complete the full flow: create or edit a video with Pippit Nest, download generated assets, upload the final video, and create a scheduled publishing task for TikTok, Facebook Page, or Instagram.

This skill helps with common Pippit workflow gaps:

- AI generation and social publishing are handled in one skill directory.
- Reference image/video upload, thread polling, and output downloads are available as local scripts.
- Social account lookup, video upload, scheduled publishing, task CRUD, and analytics are available as local scripts.
- Publishing payload details for TikTok, Facebook Page, and Instagram are documented in references.

## Prerequisites

| Dependency | Purpose | Setup |
|------------|---------|-------|
| Python 3 | Run local helper scripts | Use the system Python or a project Python 3 runtime |
| Pippit access key | Authenticate Pippit.ai API calls | Get it from [Pippit](https://www.pippit.ai) |
| Bound social account | Publish to TikTok, Facebook Page, or Instagram | Bind the account in Pippit before scheduling |

The scripts resolve the access key in this order:

1. `PIPPIT_ACCESS_KEY`
2. `PippitAccessKey`
3. `$CODEX_HOME/pippit-one-stop-skill/secrets.json`

Save a key locally:

```bash
python3 scripts/nest/save_access_key.py --access-key "..."
```

## Usage

Invoke the skill from an agent with natural language, for example:

- "Use Pippit to create a product video and schedule it to TikTok."
- "Generate a video from these reference assets, download it, and publish it to Instagram."
- "List my bound Pippit social accounts."
- "Show recent analytics for this TikTok account."
- "Update this scheduled publishing task."

## Workflow

### Step 1: Prepare Inputs

Provide the creative request, optional reference image/video files, target platform, bound platform account, caption or title, and publish timing.

If the user does not ask for a specific schedule, the skill treats the request as default publish and implements it as a near-future scheduled task.

### Step 2: Generate or Edit Assets

Use the Nest scripts to upload references, submit the creative request, poll the thread, handle Pippit clarification questions, and download generated results:

```bash
python3 scripts/nest/upload_file.py /path/to/reference.png
python3 scripts/nest/submit_run.py --message "Create a product video..."
python3 scripts/nest/get_thread.py --thread-id THREAD_ID --run-id RUN_ID --after-seq 0
python3 scripts/nest/download_results.py --urls URL1 URL2 --output-dir ./pippit_output --prefix artifact
```

### Step 3: Upload the Final Video

Check bound social accounts, then upload the final local video:

```bash
python3 scripts/publish/list_user_platform_account.py
python3 scripts/publish/upload_file.py /path/to/video.mp4
```

### Step 4: Create the Publishing Task

Create a scheduled publishing task. The publishing API is scheduled-task based, so even default publish is represented as a near-future scheduled task.

```bash
python3 scripts/publish/batchcreate_schedule_task.py \
  --platform tiktok \
  --platform-user-id PLATFORM_USER_ID \
  --asset-id ASSET_ID \
  --title "TITLE_OR_CAPTION" \
  --schedule-time "2026-05-15T20:00:00+08:00"
```

### Step 5: Follow Up

Use the publish scripts to list, update, or delete scheduled tasks, and to query social video analytics:

```bash
python3 scripts/publish/list_schedule_task.py --platform tiktok --platform-user-id PLATFORM_USER_ID
python3 scripts/publish/update_schedule_task.py --id TASK_ID --platform tiktok --platform-user-id PLATFORM_USER_ID --asset-id ASSET_ID --title "TITLE_OR_CAPTION" --schedule-time "2026-05-15T20:00:00+08:00"
python3 scripts/publish/delete_schedule_task.py --ids TASK_ID
python3 scripts/publish/list_videos.py --platform tiktok --platform-user-id PLATFORM_USER_ID --start-time-sec START --end-time-sec END
```

## Directory Structure

```
pippit-one-stop-skill/
├── SKILL.md                       # Agent-facing skill instructions
├── README.md                      # User-facing documentation
├── .gitignore                     # Local artifact ignore rules
├── references/
│   ├── command-map.md             # Common command examples
│   └── publishing-api.md          # Publishing API fields and platform payload notes
└── scripts/
    ├── nest/                      # Pippit Nest generation/editing helpers
    └── publish/                   # Social publishing, task, and analytics helpers
```

## Validation

Run a syntax check after script edits:

```bash
python3 -m compileall scripts
```
