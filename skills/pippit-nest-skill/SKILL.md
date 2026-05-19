---
name: pippit-nest-skill
description: Use Pippit Nest Agent to create and edit AI images and videos through Pippit's Skill OpenAPI. Trigger for text-to-image, text-to-video, image-to-video, video editing, reference image/video uploads, style transfer, video continuation, storyboard generation, short dramas, music videos, ads, product videos, checking generation progress, and downloading generated assets. Use when the user mentions Pippit, Pippit Nest, Pippit access keys, or asks to generate or edit AI media on Pippit.
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "P",
        "requires":
          {
            "bins": ["python3"],
            "env": ["PIPPIT_ACCESS_KEY"]
          },
        "primaryEnv": "PIPPIT_ACCESS_KEY"
      }
  }
---

# Pippit Nest Agent

Use Pippit Nest Agent to submit natural-language creative requests, upload image/video references, poll generation progress, and download generated image/video assets.

Pippit site: `https://www.pippit.ai/home?`.
API base defaults to `https://www.pippit.ai`.

The backend agent owns prompt expansion, tool routing, storyboarding, model choice, and workflow orchestration. The local agent should pass the user's request through, upload references when needed, poll progress, and return links or downloaded files.

## Prerequisites

Resolve the access key in this order:

1. Environment variable `PIPPIT_ACCESS_KEY`
2. Environment variable `PippitAccessKey`
3. Cached local key at `$CODEX_HOME/pippit-nest-skill/secrets.json`

Save a reusable local key when the user provides one:

```bash
python3 {baseDir}/scripts/save_access_key.py --access-key "your-access-key"
```

Optional overrides:

```bash
export PIPPIT_OPENAPI_BASE="https://www.pippit.ai"
export PIPPIT_HOME_URL="https://www.pippit.ai/home?"
```

Do not invent or retrieve access keys. If no key is available, ask the user to get one from Pippit and provide it.

## Scripts

- `scripts/save_access_key.py`
  Stores `PippitAccessKey` locally for future threads.
- `scripts/submit_run.py`
  Creates a new Pippit Nest run or sends a new message to an existing thread.
- `scripts/get_thread.py`
  Polls a thread and returns the run entries as normalized messages.
- `scripts/upload_file.py`
  Uploads one local image or video and returns a normalized `asset_id`.
- `scripts/download_results.py`
  Downloads generated image/video URLs to local files.

## Usage

### 1. Submit a Creative Request

```bash
python3 {baseDir}/scripts/submit_run.py --message "Create a cinematic product video for a new skincare serum"
```

Append to an existing thread:

```bash
python3 {baseDir}/scripts/submit_run.py --thread-id THREAD_ID --message "Make the pacing faster and add a product close-up"
```

Submit with uploaded reference assets:

```bash
python3 {baseDir}/scripts/submit_run.py --message "Use these references to create a social ad" --asset-ids ASSET_ID_1 ASSET_ID_2
```

### 2. Poll Progress

```bash
python3 {baseDir}/scripts/get_thread.py --thread-id THREAD_ID --run-id RUN_ID --after-seq 0
```

Use `run_id` from `submit_run.py`. Start with `--after-seq 0`; on later polls, advance the sequence based on how many messages have already been shown.

### 3. Upload References

Upload one local image or video at a time. Multiple files can be uploaded by running the script once per file.

```bash
python3 {baseDir}/scripts/upload_file.py /path/to/reference.png
python3 {baseDir}/scripts/upload_file.py /path/to/reference.mp4
```

Only `image/*` and `video/*` files are supported. Keep each file under 200 MB.

### 4. Download Results

When generated asset URLs appear in the thread messages, download them:

```bash
python3 {baseDir}/scripts/download_results.py --urls URL1 URL2 URL3 --output-dir ./pippit_output --prefix "artifact"
```

## Workflow

For image/video generation:

1. Call `submit_run.py --message "the user's original request"`.
2. Immediately show `web_thread_link` to the user if returned.
3. Poll every 10 seconds with `get_thread.py`.
4. If the backend asks a clarification question, show that question to the user and submit the user's answer to the same `thread_id`.
5. When result URLs appear, show the URLs and download them with `download_results.py`.
6. Return the local file list to the user.

For editing or reference-based generation:

1. Upload each local image/video with `upload_file.py`.
2. Submit the user's original edit/generation request with all returned `asset_id` values.
3. Follow the same polling and download flow.

## Local Agent Rules

- Pass the user's request through as-is. Do not rewrite, translate, embellish, or split the prompt unless the user explicitly asks.
- Do not manually storyboard, analyze style, choose models, or orchestrate sub-prompts locally.
- Do not send repeated per-shot requests for a single creative task unless the user explicitly asks for separate runs.
- Show progress messages from Pippit when useful, but keep stdout from scripts machine-readable JSON.
- Stop polling after 48 hours and tell the user they can check the web link later.
- Retry a single failed poll once. Stop after three consecutive polling failures.

## Output Shapes

`submit_run.py`:

```json
{
  "thread_id": "90f05e0c-...",
  "run_id": "abc123-...",
  "web_thread_link": "https://www.pippit.ai/home?tab_name=integrated-agent&thread_id=..."
}
```

`get_thread.py`:

```json
{
  "messages": [
    {"id": "1", "role": "user", "content": "..."},
    {"id": "2", "role": "assistant", "content": [{"type": "...", "subtype": "...", "data": {...}}]}
  ]
}
```

`upload_file.py`:

```json
{
  "asset_id": "asset_xxx"
}
```

`download_results.py`:

```json
{
  "output_dir": "./pippit_output",
  "downloaded": ["./pippit_output/artifact_01.mp4"],
  "total": 1
}
```
