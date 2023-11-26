import sys
from os.path import abspath,join,basename
from os import system
from os import name as version

argv = sys.argv
sys.path.append("..")

if len(argv) > 1:
    path = None
    for idx,arg in enumerate(argv):
        if arg == "--source":
            path = argv[idx+1]
        elif arg == '--require':
            require = argv[idx+1]
    
    venv_name = basename(path)
    dir_path = path
    sys_ext = None
    #windows case
    if version == "nt":
        alias = "py"
        path = abspath(join(path,"Scripts/activate.bat"))
        sys_ext = "bat"
        folder_name = "Scripts"
    #linux case
    else:
        alias = "python"
        path = abspath(join(path,"bin/activate"))
        sys_ext = "sh"
        folder_name = "bin"

    print(folder_name)
    py_path = abspath(join(dir_path,f"{folder_name}/first.py"))
    with open(py_path,"w") as p:
        makefile = f"with open('{venv_name}/{folder_name}/.inited','w') as i:\n\t\ti.write('inited')\n\t\ti.close()"
        p.write(f"import os\nimport sys\nif os.path.exists('{venv_name}/{folder_name}/.inited'):\n\tsys.exit(0)\nelse:\n\tos.system('pip install -r {require}')\n\t{makefile}\n\tsys.exit(1)")
        p.close()

    with open(path,"a") as p:
        p.write(f"\n {alias} {dir_path}/{folder_name}/first.py\n")

        if sys_ext == "bat":
            p.write(f"if %errorlevel% equ 1 (\n\tdeactivate\n)")
        elif sys_ext == "sh":
            p.write("if [ $? -eq 1 ]; then\n\tdeactivate\nfi\n")
        p.close()

    with open(f"activate_{venv_name}.{sys_ext}","w") as p:
        if sys_ext == "bat":
            activate_name = f"activate.{sys_ext}"
            meta = f'{folder_name}/{activate_name}'
            p.write(f"{abspath(join(dir_path,meta))}")
            p.close()
        elif sys_ext == "sh":
            meta = f'{folder_name}/activate'
            p.write(f"source {venv_name}/{folder_name}/activate")
            p.close()

    if sys_ext == "sh":
        system(f"chmod +x ./activate_{venv_name}.{sys_ext}")
