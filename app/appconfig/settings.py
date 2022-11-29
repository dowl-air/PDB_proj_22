
from pathlib import Path

from konfik import Konfik, DotMap

def get_env_file_config() -> DotMap:
	# Env file project root directory
	BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

	ENV_FILE = BASE_DIR / ".env"

	# Read .env
	konfik = Konfik(ENV_FILE)
	return konfik.config
