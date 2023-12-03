from flask import Flask,jsonify,render_template
def server(**args):
    name = args["name"]
    logger = args["logger"]

    api = Flask(name)
    
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
    
    
    

def dev(**args):
    name = args["name"]
    logger = args["logger"]

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
    
    @api.errorhandler(404)
    def page_not_found(error):
        return jsonify({"error": "Página não encontrada"}), 404
    
    return api