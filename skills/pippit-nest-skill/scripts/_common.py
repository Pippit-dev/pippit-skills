"""Shared helpers for Pippit Nest Skill OpenAPI calls."""

import json
import os
import sys
from urllib.parse import urlencode, urlparse
import urllib.error
import urllib.request

_RAW_PIPPIT_BASE = os.environ.get("PIPPIT_OPENAPI_BASE", os.environ.get("PIPPIT_BASE_URL", "https://www.pippit.ai"))
PIPPIT_HOME_URL = os.environ.get("PIPPIT_HOME_URL", "https://www.pippit.ai/home?")

CODEX_HOME = os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))
ACCESS_KEY_STORAGE_KEY = "PippitAccessKey"
DEFAULT_ACCESS_KEY_FILE = os.environ.get(
    "PIPPIT_ACCESS_KEY_FILE",
    os.path.join(CODEX_HOME, "pippit-nest-skill", "secrets.json"),
)

SUBMIT_RUN_PATH = "/api/biz/v1/skill/submit_run"
GET_THREAD_PATH = "/api/biz/v1/skill/get_thread"
UPLOAD_FILE_PATH = "/api/biz/v1/skill/upload_file"

def normalize_api_base(value: str) -> str:
    raw = (value or "https://www.pippit.ai").strip()
    parsed = urlparse(raw)
    if parsed.scheme and parsed.netloc and parsed.path.rstrip("/") == "/home":
        return f"{parsed.scheme}://{parsed.netloc}"
    return raw.rstrip("/")


PIPPIT_BASE = normalize_api_base(_RAW_PIPPIT_BASE)


def load_stored_access_key() -> str:
    path = DEFAULT_ACCESS_KEY_FILE
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except (OSError, json.JSONDecodeError):
        return ""
    if not isinstance(data, dict):
        return ""
    value = data.get(ACCESS_KEY_STORAGE_KEY, "")
    return value.strip() if isinstance(value, str) else ""


def resolve_access_key() -> str:
    candidates = [
        os.environ.get("PIPPIT_ACCESS_KEY", ""),
        os.environ.get(ACCESS_KEY_STORAGE_KEY, ""),
        load_stored_access_key(),
    ]
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


ACCESS_KEY = resolve_access_key()


def ensure_access_key() -> None:
    if ACCESS_KEY:
        return
    print(
        "Error: set PIPPIT_ACCESS_KEY, set PippitAccessKey, or save a local PippitAccessKey first. "
        "If you do not have one, get it from https://www.pippit.ai/home?.",
        file=sys.stderr,
    )
    sys.exit(1)


def save_access_key(access_key: str, path: str = DEFAULT_ACCESS_KEY_FILE) -> str:
    value = (access_key or "").strip()
    if not value:
        print("Error: access key cannot be empty", file=sys.stderr)
        sys.exit(1)

    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, mode=0o700, exist_ok=True)

    payload = {ACCESS_KEY_STORAGE_KEY: value}
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)
        fp.write("\n")
    os.chmod(path, 0o600)
    return path


def _headers(content_type: str = "application/json") -> dict:
    headers = {"Authorization": f"Bearer {ACCESS_KEY}"}
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def api_post(path: str, body: dict) -> dict:
    ensure_access_key()
    url = f"{PIPPIT_BASE.rstrip('/')}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8") if exc.fp else ""
        print(f"API error {exc.code}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def parse_response(resp: dict) -> dict:
    ret = str(resp.get("ret", ""))
    if ret != "0":
        errmsg = resp.get("errmsg", "unknown error")
        print(f"Error code: {ret}, message: {errmsg}", file=sys.stderr)
        sys.exit(1)
    data = resp.get("data", {})
    return data if isinstance(data, dict) else {}


def submit_run(thread_id: str = "", message: str = "", asset_ids: list = None) -> dict:
    body = {}
    if thread_id:
        body["thread_id"] = thread_id
    if message:
        body["message"] = message
    if asset_ids:
        body["asset_ids"] = asset_ids
    return parse_response(api_post(SUBMIT_RUN_PATH, body))


def get_thread(thread_id: str, run_id: str = "", after_seq: int = 0) -> dict:
    body = {"thread_id": thread_id, "after_seq": after_seq}
    if run_id:
        body["run_id"] = run_id
    data = parse_response(api_post(GET_THREAD_PATH, body))

    thread = data.get("thread", {})
    run_list = thread.get("run_list", [])
    if not run_list:
        print("Error: response did not include thread.run_list", file=sys.stderr)
        sys.exit(1)

    run = None
    if run_id:
        for candidate in run_list:
            if candidate.get("run_id") == run_id:
                run = candidate
                break
    if run is None:
        run = run_list[0]

    state = normalize_state(run.get("state", ""))
    if state == "completed":
        print("Status: generation completed", file=sys.stderr)
        return run
    if state == "failed":
        fail_reason = run.get("fail_reason", "unknown failure")
        print(f"Error: {fail_reason}", file=sys.stderr)
        sys.exit(1)
    if state == "canceled":
        print("Error: generation was canceled", file=sys.stderr)
        sys.exit(1)

    print("Status: generation in progress", file=sys.stderr)
    return run


def normalize_state(value) -> str:
    if isinstance(value, int):
        state_value = str(value)
    else:
        state_value = str(value or "").strip().lower()

    completed = {"3", "completed", "complete", "succeeded", "success", "done", "runstate_completed"}
    failed = {"4", "failed", "failure", "error", "runstate_failed"}
    canceled = {"5", "canceled", "cancelled", "runstate_canceled"}

    if state_value in completed:
        return "completed"
    if state_value in failed:
        return "failed"
    if state_value in canceled:
        return "canceled"
    return "running"


def build_web_thread_link(thread_id: str) -> str:
    if not thread_id:
        return ""
    params = urlencode(
        {
            "tab_name": "integrated-agent",
            "thread_id": thread_id,
            "agent_name": "pippit_nest_agent",
        }
    )
    if PIPPIT_HOME_URL.endswith("?") or PIPPIT_HOME_URL.endswith("&"):
        return f"{PIPPIT_HOME_URL}{params}"
    separator = "&" if "?" in PIPPIT_HOME_URL else "?"
    return f"{PIPPIT_HOME_URL}{separator}{params}"


def extract_entries_from_run(run: dict) -> list:
    matched = []
    for entry in run.get("entry_list") or []:
        item = {}
        message = entry.get("message")
        artifact = entry.get("artifact")
        if message:
            item["id"] = message.get("message_id", "")
            item["role"] = message.get("role", "")
            item["content"] = as_list(message.get("content", []))
            client_tool_calls = as_list(message.get("client_tool_calls", []))
            if client_tool_calls:
                item["content"].extend(client_tool_calls)
        if artifact:
            item["id"] = artifact.get("artifact_id", "")
            item["role"] = artifact.get("role", "")
            item["content"] = as_list(artifact.get("content", []))
        if item:
            matched.append(item)
    return matched


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]
