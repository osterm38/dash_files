from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[
        "settings.toml",
        ".secrets.toml",
        ".env",
    ],                                 # path/glob
    environments=True,                 # activate layered environments
    envvar_prefix="MYAPP",             # `export MYAPP_FOO=bar`
    env_switcher="MYAPP_MODE",         # `export MYAPP_MODE=production`
    load_dotenv=True,                  # read a .env file
)
