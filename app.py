from flask import Flask

api = Flask("AquaDepth Api")

@api.route("/<name>")
def hello_world(name:str,*args):
    return f"<b>hello {name}<\b> and {args}"
