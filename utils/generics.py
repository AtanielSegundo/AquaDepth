from typing import Literal

def config_log(save_path:str,with_time=True):
    import logging
    from os.path import exists,basename
    from os import remove

    if exists(save_path):
        remove(save_path)

    if with_time:
        formatter = logging.Formatter(
            "[%(levelname)s] [%(asctime)s] - %(message)s", datefmt="%Y_%m_%d_%H_%M_%S")
    else:
        formatter = logging.Formatter("%(message)s")
    
    file_handler = logging.FileHandler(save_path)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(basename(save_path).split('.')[0])
    logger.setLevel(level=logging.INFO)
    logger.handlers = [file_handler, console_handler]

    return logger

def verify_path(path:str,mode:Literal["dir","file","url"]="file") -> bool:
    if mode == "dir":
        from os.path import isdir
        return True if isdir(path) else False
        
    elif mode == "file":
        from os.path import exists
        return True if exists(path) else False
    
    elif mode == "url":
        pass