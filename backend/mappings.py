"""
Map blueprints to their mount path.

The name of the blueprint must line up with the name of the directory within
the routes directory.
"""

MAPPINGS = {
  "api": {
    "users": "users"
  },
  "/": "pages"
}
