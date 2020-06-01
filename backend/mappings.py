"""
Map blueprints to their mount path.

The name of the blueprint must line up with the name of the directory within
the routes directory.
"""

# The format is mountpath: pythonmodule
# or alternatively a dictionary combining these
# so "api": {"users": "users"} will mount /api/users
# to the "users" Python module
MAPPINGS = {
    # API endpoints
    "api": {"users": "users", "/": "index"},
    # Staticish pages
    "/": "pages",
    # User management pages
    "users": "users",
    "teacher": "teacher",
}
