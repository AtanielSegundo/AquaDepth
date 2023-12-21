from flask import Flask,jsonify,render_template,request
from flask_dropzone import Dropzone
from os.path import join
def server(**args):
    logger = args["logger"]
    name = args["name"]
    port = args["port"]
    host = args["host"]
    
    api = Flask(name)
    api.config.update(
    UPLOADED_PATH="data",
    DROPZONE_MAX_FILE_SIZE = 60 ,
    DROPZONE_TIMEOUT = 5*60*1000,    
    DROPZONE_DEFAULT_MESSAGE = "<p>Arraste e solte imagens das marcas de calado do navio</p>")

    dropzone = Dropzone(api)
    
    
    @api.route('/upload', methods=['GET','POST'])
    def upload_file():
        if 'file' in request.files:
            file = request.files['file']
            file.save(join(api.config['UPLOADED_PATH'],file.filename))
        return "successful_upload"

    @api.route("/static")
    def static_image():
        return render_template("static_image.html")
        

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
        home_url = host+":"+str(port)
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