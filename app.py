from flask import Flask
from typing import Literal,List,Union,Callable,Tuple
from logging import Logger

class ApiInterface:
    def __init__(self,logger:Logger,mode:Literal["server","dev"]="server",
                host:str=None,port:int=5000,name:str="AquaDepth Api") -> None:
        
        self.logger = logger
        if host != None or name != "AquaDepth Api" or port != 5000:
            self.host   = host
            self.name   = name
            self.port   = port  
        else:
            self._load_configs_(mode)
        
        if mode == "server":
            from api import server
            self.debug = False
            self.api:Flask = \
            server(name=self.name,host=self.host,
                   logger=self.logger,port=self.port)     
        
        elif mode == "dev":
            from api import dev
            self.debug = True
            self.api:Flask = \
            dev(name=self.name,host=self.host,
                logger=self.logger,port=self.port)     
            
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
        self.api.run(self.host,debug=self.debug,port=self.port)

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