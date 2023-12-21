from flask import Flask,jsonify,render_template,request
def server(**args):
    logger = args["logger"]
    name = args["name"]
    port = args["port"]
    host = args["host"]
    api = Flask(name)
    
    @api.route('/static', methods=['POST'])
    def upload_file():
        if 'file' in request.files:
            file = request.files['file']
            # Here you should save the file
            # file.save(path_to_save_file)
            return 'File uploaded successfully'

    return 'No file uploaded'
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