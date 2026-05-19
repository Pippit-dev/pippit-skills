# pippit-nest-skill

`pippit-nest-skill` is the overseas Pippit version of the Nest Agent media creation skill. It keeps the same shape as the original `xyq-nest-skill`: submit a natural-language creative request, upload image/video references, poll thread progress, and download generated assets.

Pippit site: `https://www.pippit.ai/home?`

## Install

```bash
npx skills add https://github.com/Pippit-dev/pippit-overseas-skills.git --skill pippit-nest-skill -y -g
```

## Access Key

Use one of:

```bash
export PIPPIT_ACCESS_KEY="your-access-key"
export PippitAccessKey="your-access-key"
```

Or save it locally:

```bash
python3 skills/pippit-nest-skill/scripts/save_access_key.py --access-key "your-access-key"
```

Optional:

```bash
export PIPPIT_OPENAPI_BASE="https://www.pippit.ai"
export PIPPIT_HOME_URL="https://www.pippit.ai/home?"
```

## Submit a Run

```bash
python3 skills/pippit-nest-skill/scripts/submit_run.py --message "Create a cinematic product video for a new skincare serum"
```

Append to an existing thread:

```bash
python3 skills/pippit-nest-skill/scripts/submit_run.py --thread-id THREAD_ID --message "Make it faster and add captions"
```

Submit with uploaded references:

```bash
python3 skills/pippit-nest-skill/scripts/submit_run.py --message "Create a social ad using these references" --asset-ids ASSET_ID_1 ASSET_ID_2
```

## Poll Progress

```bash
python3 skills/pippit-nest-skill/scripts/get_thread.py --thread-id THREAD_ID --run-id RUN_ID --after-seq 0
```

Poll every 10 seconds. If the backend asks a clarification question, ask the user and submit the answer to the same `thread_id`.

## Upload References

```bash
python3 skills/pippit-nest-skill/scripts/upload_file.py /path/to/reference.png
python3 skills/pippit-nest-skill/scripts/upload_file.py /path/to/reference.mp4
```

Only images and videos are supported. Each file must be under 200 MB.

## Download Results

```bash
python3 skills/pippit-nest-skill/scripts/download_results.py \
  --urls URL1 URL2 URL3 \
  --output-dir ./pippit_output \
  --prefix "artifact" \
  --workers 5
```
