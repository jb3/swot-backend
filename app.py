"""Entry point for Swot application."""

from backend.config import CONFIG
from backend.route_manager import RouteManager

manager = RouteManager()

if CONFIG.host.migrate_on_startup:
    from alembic.command import upgrade
    from alembic.config import Config
    import os

    config_dir = os.path.dirname(os.path.realpath(__file__))

    config_file = os.path.join(config_dir, "alembic.ini")

    config = Config(file_=config_file)

    upgrade(config, "head")

if __name__ == "__main__":
    if CONFIG.host.DEBUG:
        manager.run()

app = manager.app
