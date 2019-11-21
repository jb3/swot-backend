from flask import request, jsonify
from backend.route import Route

class PostTest(Route):
    name = "index"
    path = "/"

    def get(self):
        return "Index for Post API"
