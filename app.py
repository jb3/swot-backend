"""Entry point for Swot application."""

from backend.config import CONFIG
from backend.route_manager import RouteManager

manager = RouteManager()

if __name__ == "__main__":
    if CONFIG.host.DEBUG:
        manager.run()

app = manager.app
