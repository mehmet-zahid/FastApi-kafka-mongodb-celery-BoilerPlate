from dotenv import load_dotenv
import os


def check_var_env(var_name: str):
    """this function first check if the env var is set in compose environment,
    if not, it tries to get it from .env file in the root directory. If it's not set,
    it raises ValueError."""

    var = os.getenv(var_name)
    if not var:
        # env_path = str(Path().cwd().parent) + "/.env.local"
        # logger.info(f"Loading .env file from {env_path}")
        load_dotenv(override=True)
        var = os.getenv(var_name)
        if not var:
            raise ValueError(f"{var_name} environment variable not set")
    return var
