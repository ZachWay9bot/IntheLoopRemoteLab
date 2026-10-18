from __future__ import annotations

import os


def load_github_token() -> str:
    token = os.getenv("REMOTELAB_GITHUB_TOKEN", "").strip()
    if token:
        return token

    try:
        import keyring
    except ImportError as exc:
        raise RuntimeError(
            "GitHub token missing; set REMOTELAB_GITHUB_TOKEN or install keyring"
        ) from exc

    token = keyring.get_password("RemoteLab-Core", "github-token")
    if not token:
        raise RuntimeError(
            "GitHub token missing from Windows Credential Manager"
        )
    return token
