from flask import Flask
from typing import Literal,List,Union,Callable,Tuple
from logging import Logger

class ApiInterface:
    def __init__(self,logger:Logger,mode:Literal["server","dev"]="server",
                host:str=None,name:str="AquaDepth Api") -> None:
        self.host   = host
        self.logger = logger
        self.name   = name 
        self._load_configs_(mode)
        
        if mode == "server":
            from api import server
            self.debug = False
            self.api:Flask = \
            server(name=self.name,logger=self.logger)     
        
        elif mode == "dev":
            from api import dev
            self.debug = True
            self.api:Flask = \
            dev(name=self.name,logger=self.logger)     
            
    def _load_configs_(self,mode:str):
        import json
        try:
            with open(f"configs/{mode}.json") as jp:                
                temp_dict:dict =  json.load(jp)
        except Exception as e:
            self.logger.error(f"Cant Load {mode}.json | Error : {e}")
        else:
            for key,item in temp_dict.items():
                setattr(self,key,item)
                self.logger.info(f"{key} : {item} | Set")

    def run(self):
        self.api.run(self.host,debug=self.debug)

if __name__ == "__main__":
    import argparse
    from utils.generics import verify_path,config_log
    parser = argparse.ArgumentParser(
             description='Aqua Depth Arguments',
             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--mode",nargs="?",default="server")
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
    api = ApiInterface(logger=logger,mode=mode)
    
    api.run()