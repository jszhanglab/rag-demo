# rag-service/app/utils/config.py
from pathlib import Path
import json

def find_repo_root(start: Path) -> Path:
    """
    从 start 目录往上查找，直到发现含有 .git 的目录为止。
    适用于 monorepo。
    """
    p = start
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    raise RuntimeError("Repo root not found — ensure you're inside the rag-demo project")

# 当前文件：rag-demo/services/rag-service/app/utils/config.py
HERE = Path(__file__).resolve()
REPO_ROOT = find_repo_root(HERE)

API_ROUTES_PATH = REPO_ROOT / "packages" / "common" / "apiRoutes.json"

# 加载 JSON
with open(API_ROUTES_PATH, "r", encoding="utf-8") as f:
    API_ROUTES = json.load(f)
