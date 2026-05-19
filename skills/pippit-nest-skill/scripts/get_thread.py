#!/usr/bin/env python3
"""Poll Pippit Nest Agent progress: POST /api/biz/v1/skill/get_thread."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import extract_entries_from_run, get_thread


def main():
    parser = argparse.ArgumentParser(
        description="Fetch messages and artifacts for a Pippit Nest Agent run.",
        epilog="""
Environment:
  PIPPIT_ACCESS_KEY or PippitAccessKey  Optional if a local PippitAccessKey is already saved
  PIPPIT_OPENAPI_BASE or PIPPIT_BASE_URL  Optional, default https://www.pippit.ai

Example:
  python3 get_thread.py --thread-id THREAD_ID --run-id RUN_ID --after-seq 0
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--thread-id", required=True, help="Thread ID returned by submit_run.py")
    parser.add_argument("--run-id", default="", help="Run ID returned by submit_run.py")
    parser.add_argument(
        "--after-seq",
        type=int,
        default=0,
        help="Return entries at or after this sequence cursor. Defaults to 0.",
    )
    args = parser.parse_args()

    run = get_thread(args.thread_id, run_id=args.run_id, after_seq=args.after_seq)
    print(json.dumps({"messages": extract_entries_from_run(run)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
