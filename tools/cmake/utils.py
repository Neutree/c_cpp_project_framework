import time
import re
import os
import subprocess

def check_all_submodule(sdk_path):
    if (not os.path.exists(os.path.join(sdk_path, ".gitmodules"))) or (not os.path.exists(os.path.join(sdk_path, ".git"))):
        return True, ""
    with open(os.path.join(sdk_path, ".gitmodules")) as f:
        content = f.read()
        m = re.findall(r'path = (.*)', content)
        if not m:
            return True, ""
        for path in m:
            full_path = os.path.join(sdk_path, path)
            err_msg = "Submodule {} not exists, please run `git submodule update --init --recursive` to init all submodules".format(path)
            if (not os.path.exists(full_path)):
                print("-- {} not exists".format(full_path))
                return False, err_msg
            files = os.listdir(full_path)
            if ".git" not in files:
                print("-- {}/.git not exists".format(full_path))
                return False, err_msg
            visible_files = []
            for name in files:
                if not name.startswith("."):
                    visible_files.append(name)
            if len(visible_files) == 0:
                print("-- {} no files".format(full_path))
                return False, err_msg
        # check if submodule version is the same as should be
        cmd = ["git", "submodule", "status"]
        p = subprocess.Popen(cmd, cwd=sdk_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate("")
        res = p.returncode
        if res != 0:
            print("-- git submodule status failed")
            return False, err
        try:
            output = output.decode(encoding="utf-8" if os.name == "nt" else "utf-8")
        except Exception:
            output = output.decode(encoding="gbk" if os.name == "nt" else "utf-8")
        lines = output.split("\n")
        for line in lines:
            if line.startswith("+"):
                print("\n============================================")
                print("-- [Warning]\n!! Submodule [{}] have changes, it maybe cause problems\nif you don't know what this means, please execute:\n    git submodule update --init --recursive`\nto update submodule !".format(line.split(" ")[1]))
                print("============================================\n")
                time.sleep(1)
            elif line.startswith("-"):
                return False, "Submodule {} not exists, please run `git submodule update --init --recursive` to init all submodules".format(line.split(" ")[1])

    return True, ""
