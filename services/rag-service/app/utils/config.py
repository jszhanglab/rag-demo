# rag-service/app/utils/config.py
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import json
import toml

#----- Monorepo Root Path Helpers --------------------

def find_repo_root(start: Path) -> Path:
    p = start
    # root dirictory's parent is itself
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    raise RuntimeError("Repo root not found")

# current directory
HERE = Path(__file__).resolve()
REPO_ROOT = find_repo_root(HERE)

#----- Centralized Route Configuration Loading ---------------------
# fetches common API routes defined in the shared package
API_ROUTES_PATH = REPO_ROOT / "packages" / "common" / "apiRoutes.json"

# load apiRoutes.json
with open(API_ROUTES_PATH, "r", encoding="utf-8") as f:
    API_ROUTES = json.load(f)


#----- Dynamic Application Configuration ------------
# fetches project metadata from pyproject.toml
PYPROJECT_TOML_PATH = REPO_ROOT / "services" / "rag-service" / "pyproject.toml"

try:
    with open(PYPROJECT_TOML_PATH, "r") as f:
        pyproject_data = toml.load(f)
        PROJECT_METADATA = pyproject_data.get('project', {})
except FileNotFoundError:
    PROJECT_METADATA = {}

class Settings(BaseSettings):
    # model_config is used for telling Pydantic where to find the .env file.
    # Pydantic will automatically load and cast variables from the .env file.
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / "services" / "rag-service" / "config" / ".env",
        extra='ignore' # ignore configuration variables not defined in the model
    )
    PROJECT_NAME: str = PROJECT_METADATA.get("name")
    PROJECT_VERSION: str = PROJECT_METADATA.get("version")
    PROJECT_DESCRIPTION: str = PROJECT_METADATA.get("description")
    # CORS configuration be loaded from .env or environment variables automatically by Pydantic
    CORS_ORIGINS: List[str] = []

    #TODO
    #VECTOR_DB_URL:  
    #LLM_MODEL_NAME: 

settings = Settings()    