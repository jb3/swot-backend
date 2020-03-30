"""Entry point for Swot application."""

from backend.route_manager import RouteManager
from backend.config import CONFIG

manager = RouteManager()

if __name__ == "__main__":
    if CONFIG.host.DEBUG:
        manager.run()

app = manager.app
