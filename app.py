from flask import Flask
from typing import Literal,List,Union,Callable,Tuple
from logging import Logger
from api import ApiInterface

if __name__ == "__main__":
    import argparse
    from utils.generics import verify_path,config_log
    parser = argparse.ArgumentParser(
             description='Aqua Depth Arguments',
             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--mode",nargs="?",default="server")
    parser.add_argument("--host",nargs="?",default=None)
    parser.add_argument("--name",nargs="?",default="AquaDepth Api")
    parser.add_argument("--port",nargs="?",default=5000,type=int)
    parser.add_argument("--test",action="store_true",default=False)
    parser.add_argument("--logpath",type=str,default="logs/aqua.log")
    args = parser.parse_args()
    
    log_path = args.logpath 
    mode = args.mode
    logger:Logger = ...
    
    if verify_path(log_path):
        logger = config_log(save_path=log_path)
    else:
        from os.path import dirname
        from os import mkdir
        if verify_path(dir_name:=dirname(log_path),"dir"):
            logger = config_log(save_path=log_path)
        else:
            mkdir(dir_name)
            logger = config_log(save_path=log_path)
    
    if mode not in ["server","dev"]:
        logger.error(f"{mode} not available")
        exit()
    logger.info(f"Log Successfully Made At {log_path}")
    api = ApiInterface(logger=logger,mode=mode,name=args.name,host=args.host,port=args.port)

    api.run()