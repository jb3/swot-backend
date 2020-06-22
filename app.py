"""Entry point for Swot application."""

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand, upgrade

from backend.config import CONFIG
from backend.route_manager import RouteManager

manager = RouteManager()

migrate = Migrate(manager.app, manager.app.db)

cli = Manager(manager.app)
cli.add_command("db", MigrateCommand)
cli.add_command(
    "runserver",
    Server(
        host=CONFIG.host.host, port=CONFIG.host.port
    ),
)

if CONFIG.host.migrate_on_startup:
    with manager.app.app_context():
        upgrade()

app = manager.app

if __name__ == "__main__":
    cli.run()
