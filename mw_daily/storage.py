from __future__ import annotations

import json
import base64
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


PROGRESS_PATH = Path(__file__).resolve().parent.parent / "data" / "progress.json"


def github_storage_config() -> dict[str, str] | None:
    try:
        config = st.secrets.get("github_storage", None)
    except StreamlitSecretNotFoundError:
        return None

    if not config or not config.get("token") or not config.get("repo"):
        return None

    return {
        "token": config["token"],
        "repo": config["repo"],
        "branch": config.get("branch", "main"),
        "path": config.get("path", "data/progress.json"),
    }


def github_headers(token: str) -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def show_storage_warning() -> None:
    if st.session_state.get("_mw_daily_storage_warning_shown"):
        return
    st.session_state["_mw_daily_storage_warning_shown"] = True
    st.warning(
        "I couldn't load my saved history from GitHub just now. "
        "The app is still available, but history may be incomplete."
    )


def load_attempts_from_github(config: dict[str, str]) -> list[dict[str, Any]]:
    try:
        response = requests.get(
            f"https://api.github.com/repos/{config['repo']}/contents/{config['path']}",
            headers=github_headers(config["token"]),
            params={"ref": config["branch"]},
            timeout=10,
        )
    except requests.RequestException:
        show_storage_warning()
        return []

    if response.status_code == 404:
        return []
    try:
        response.raise_for_status()
    except requests.RequestException:
        show_storage_warning()
        return []

    payload = response.json()
    content = base64.b64decode(payload["content"]).decode("utf-8")
    return json.loads(content or "[]")


def save_attempts_to_github(config: dict[str, str], attempts: list[dict[str, Any]]) -> None:
    get_response = requests.get(
        f"https://api.github.com/repos/{config['repo']}/contents/{config['path']}",
        headers=github_headers(config["token"]),
        params={"ref": config["branch"]},
        timeout=10,
    )
    sha = None
    if get_response.status_code == 200:
        sha = get_response.json()["sha"]
    elif get_response.status_code != 404:
        get_response.raise_for_status()

    encoded_content = base64.b64encode(
        json.dumps(attempts, indent=2).encode("utf-8")
    ).decode("utf-8")
    payload: dict[str, Any] = {
        "message": "Save MW Daily progress",
        "content": encoded_content,
        "branch": config["branch"],
    }
    if sha:
        payload["sha"] = sha

    put_response = requests.put(
        f"https://api.github.com/repos/{config['repo']}/contents/{config['path']}",
        headers=github_headers(config["token"]),
        json=payload,
        timeout=10,
    )
    put_response.raise_for_status()


def load_attempts() -> list[dict[str, Any]]:
    config = github_storage_config()
    if config:
        return load_attempts_from_github(config)

    if not PROGRESS_PATH.exists():
        return []
    with PROGRESS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_attempt(attempt: dict[str, Any]) -> None:
    config = github_storage_config()
    attempts = load_attempts()
    existing_index = next(
        (
            index
            for index, saved_attempt in enumerate(attempts)
            if saved_attempt["question_id"] == attempt["question_id"]
            and saved_attempt["mode"] == attempt["mode"]
            and saved_attempt["study_date"] == attempt["study_date"]
        ),
        None,
    )

    stamped_attempt = {
        **attempt,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    if existing_index is None:
        attempts.append(stamped_attempt)
    else:
        attempts[existing_index] = stamped_attempt

    if config:
        save_attempts_to_github(config, attempts)
        return

    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_PATH.open("w", encoding="utf-8") as file:
        json.dump(attempts, file, indent=2)
