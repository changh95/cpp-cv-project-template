import os

def create_venv(cfg):
    os.chdir(cfg.basic_config.base_path)

    # Install virtual environment
    os.system(cfg.basic_config.pw.sudo() + "apt-get -y install python3-venv")

    # Installs easydict, numpy, scipy in a virtual environment (.venv)
    os.system("chmod u+x ./thirdparty/create_venv.sh")
    os.system("./thirdparty/create_venv.sh")