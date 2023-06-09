import os
import sys
import urllib.request
import urllib.error


def install_evo(cfg):
    base_path = cfg.basic_config.base_path
    pw = cfg.basic_config.pw
    version_num = cfg.evo

    os.chdir(cfg.basic_config.base_path)

    # install EVO for map evaluation
    try:
        os.system(pw.sudo() + "rm -rf ./thirdparty/evo")
        os.chdir("./thirdparty")

        try:
            urllib.request.urlretrieve(
                "https://github.com/MichaelGrupp/evo/archive/refs/tags/v" + version_num + ".zip",
                "./evo.zip")
        except urllib.error.HTTPError as e:
            raise Exception("EVO: cloning failed")

        os.system("unzip ./evo.zip -d .")
        os.rename("evo-" + version_num, "evo")
        os.system(pw.sudo() + "rm -rf ./evo.zip")

    except Exception as e:
        print("")
        sys.exit(e)

    os.chdir(cfg.basic_config.base_path)
    os.system("chmod u+x ./thirdparty/install_evo.sh")
    os.system("./thirdparty/install_evo.sh")