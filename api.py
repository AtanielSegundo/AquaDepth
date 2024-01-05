from flask import Flask,jsonify,render_template,request
from flask_dropzone import Dropzone
from os.path import join
from os import remove,listdir
from typing import Literal,List,Union,Callable,Tuple
from logging import Logger
from time import sleep 

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
            self.debug = False
            self.api:Flask = \
            server(name=self.name,host=self.host,
                   logger=self.logger,port=self.port)     
        
        elif mode == "dev":
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

def server(**args):
    logger = args["logger"]
    name = args["name"]
    port = args["port"]
    host = args["host"]
    home_url = host+":"+str(port)
    api = Flask(name)
    api.__setattr__("images_list_to_process",{"new":[],"old":[]})
    api.config.update(
    UPLOADED_PATH="data",
    DROPZONE_MAX_FILE_SIZE = 60 ,
    DROPZONE_TIMEOUT = 5*60*1000,    
    DROPZONE_DEFAULT_MESSAGE = "<p>Arraste e solte imagens das marcas de calado do navio</p>")
    
    for file in listdir(folder:=api.config["UPLOADED_PATH"]):
        remove(join(folder,file))
    dropzone = Dropzone(api)

    @api.route('/upload', methods=['GET','POST'])
    def upload_file():
        if 'file' in request.files:
            file = request.files['file']
            api.images_list_to_process["new"].append(file.filename)
            file.save(join(api.config['UPLOADED_PATH'],file.filename))
        return "successful_upload"

    @api.route("/static")
    def static_image():
        return render_template("static_image.html")
    
    @api.route("/test")
    def test():
        return render_template("home.html")

    @api.route("/process")
    def process():
        for i in range(10):
            sleep(1)
        for old_image in api.images_list_to_process["old"]:
            try:
                remove(join(api.config['UPLOADED_PATH'],old_image))
                logger.info(old_image + "removed")
            except Exception as e: 
                logger.error(f"error {e} removing {old_image}")
        response = {i:"OK" for i in api.images_list_to_process["new"]}
        api.images_list_to_process["old"] = api.images_list_to_process["new"].copy()
        api.images_list_to_process["new"] = []
        return response
    
    @api.route("/log/json")
    def get_log_json():
        path = logger.__dict__["handlers"][0].baseFilename
        temp_dict = {}
        with open(path,"r") as logfile:
            logfile_lines = logfile.readlines()
            count = 1
            for line in logfile_lines:
                temp_dict[count] = line.strip()
                count+=1
        return temp_dict
    
    @api.route("/log/raw")
    def get_log_raw():
        path = logger.__dict__["handlers"][0].baseFilename
        logfile_str = str()
        with open(path,"r") as logfile:
            logfile_arr = logfile.readlines()
        for entry in logfile_arr:
            logfile_str+="<b>"+entry+"</b><br>"

        return logfile_str
    
    @api.route("/")
    def home():
        return render_template("index.html")

    @api.errorhandler(404)
    def page_not_found(error):
        return render_template("error_404.html")

    return api
    
    
    

def dev(**args):
    name = args["name"]
    logger = args["logger"]
    port = args["port"]

    api = Flask("dev_"+name)
    
    @api.route("/log/json")
    def get_log_json():
        path = logger.__dict__["handlers"][0].baseFilename
        temp_dict = {}
        with open(path,"r") as logfile:
            logfile_lines = logfile.readlines()
            count = 1
            for line in logfile_lines:
                temp_dict["entry_"+str(count)] = line
                count+=1
        return temp_dict
    
    @api.route("/log/raw")
    def get_log_raw():
        path = logger.__dict__["handlers"][0].baseFilename
        logfile_str = str()
        with open(path,"r") as logfile:
            logfile_arr = logfile.readlines()
        for entry in logfile_arr:
            logfile_str+="<b>"+entry+"</b><br>"

        return logfile_str
    
    @api.route("/")
    def home():
        return "<head>On going</head>" 

    @api.errorhandler(404)
    def page_not_found(error):
        return render_template("error_404.html")
    
    return api