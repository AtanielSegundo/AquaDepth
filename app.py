from flask import Flask
from typing import Literal,List,Union

class ApiInterface:
    def __init__(self,mode:Literal["server","dev"]="server") -> None:
        if mode == "server":
            self.api = Flask("AquaDepth Api")
        elif "dev":
            pass
    @Flask.route("/<name>")
    def hello_world(name:str,*args):
        return f"<b>hello {name}<\b> and {args}"

if __name__ == "__main__":
    import argparse
    from utils.generics import verify_path,config_log
    parser = argparse.ArgumentParser(
             description='Aqua Depth Arguments',
             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--mode",metavar="Mode",nargs="?",
                        default="server")
    parser.add_argument("--test",action="store_true",default=False)
    parser.add_argument("--logpath",metavar="Path",
                        type=str,default="logs/aqua.log")
    args = parser.parse_args()

    log_path = args.logpath 
    if verify_path(log_path):
        logger = config_log(save_path=log_path)
    else:
        from os.path import dirname
        from os import mkdir
        if verify_path(dir_name:=dirname(log_path)):
            logger = config_log(save_path=log_path)
        else:
            mkdir(dir_name)
            logger = config_log(save_path=log_path)
    
    
    