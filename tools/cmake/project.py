#
# @file from https://github.com/Neutree/c_cpp_project_framework
# @author neucrack
# @license MIT
#


import argparse
import os, sys, time, re, shutil
import subprocess
from multiprocessing import cpu_count

if not os.path.exists("CMakeLists.txt") or  not os.path.exists("main"):
    print("please run me at project folder!")
    exit(1)

try:
    # sdk_path from project's project.py
    sdk_path = sdk_path
except Exception:
    sdk_path = os.path.abspath("../../")
project_path = sys.path[0]
project_name = ""
project_cmake_path = project_path+"/CMakeLists.txt"
project_cmake_content = ""
with open(project_cmake_path) as f:
    project_cmake_content = f.read()
match = re.findall(r"set\(PROJECT_NAME (.*)\)", project_cmake_content)
if len(match) != 0:
    project_name = match[0]
    if("project_dir_name" in project_name):
        project_name = os.path.basename(project_path)
    print("-- project name: {}".format(project_name))
if project_name == "":
    print("[ERROR] Can not find project name in {}, not set(PROJECT_NAME {})".format(project_cmake_path, "${project_name}"))
    exit(1)

# find extra tools
tools_dir = os.path.join(sdk_path, "tools")
sys.path.insert(1, tools_dir)
# find all .py files in tools dir
extra_tools_names = []
parsers = []
extra_tools = {}
for name in os.listdir(tools_dir):
    if name.endswith(".py"):
        extra_tools_names.append(name[:-3])
# import all tools
for name in extra_tools_names:
    # import from tool file
    tool = __import__(name)
    hasattr(tool, "parser") and parsers.append(tool.parser)
    if hasattr(tool, "cmds"):
        extra_tools[tool.__name__] = {
            "tool": tool,
            "cmds": tool.cmds,
        }

project_parser = argparse.ArgumentParser(description='build tool, e.g. `python project.py build`', prog="project.py", parents=parsers)

project_parser.add_argument('--toolchain',
                        help='toolchain path ( absolute path )',
                        metavar='PATH',
                        default="")

project_parser.add_argument('--toolchain-prefix',
                        help='toolchain prefix(e.g. mips-elf-',
                        metavar='PREFIX',
                        default="")
project_parser.add_argument('--config_file',
                        help='config file path, e.g. config_defaultd.mk',
                        metavar='PATH',
                        default="{}/config_defaults.mk".format(project_path))
project_parser.add_argument('--verbose',
                        help='for build command, execute `cmake -build . --verbose` to compile',
                        action="store_true",
                        default=False)
project_parser.add_argument('-G', '--generator', default="", help="project type to generate, supported type on your platform see `cmake --help`")
project_parser.add_argument('--release', action="store_true", default=False, help="release mode, default is debug mode")
project_parser.add_argument('--build-type', default=None, help="build type, [Debug, Release, MinRelSize, RelWithDebInfo], you can also set build type by CMAKE_BUILD_TYPE environment variable")

cmd_help ='''
project command:

config:     config toolchain path
clean_conf: clean toolchain path config
menuconfig: open menuconfig pannel, a visual config pannel
build:      start compile project, temp files in `build` dir, dist files in `dist` dir
rebuild:    update cmakefiles and build, if new file added, shoud use this command
clean:      clean build files, won't clean configuration
distclean:  clean all build files and configuration except configuration configed by config conmand
flash:      burn firmware to board's flash
'''

cmd_choices = ["config", "build", "rebuild", "menuconfig", "clean", "distclean", "clean_conf"]
for k, v in extra_tools.items():
    cmd_choices.extend(v["cmds"])
cmd_choices = list(set(cmd_choices))
project_parser.add_argument("cmd",
                    help=cmd_help,
                    choices=cmd_choices
                    )

project_args = project_parser.parse_args()

cwd = sys.path[0]
os.chdir(cwd)

config_filename = ".config.mk"

def load_config_mk(path):
    configs = {}
    if os.path.exists(config_filename):
        with open(config_filename) as f:
            content = f.read()
            lines = content.split("\n")
            for line in lines:
                line = line.strip()
                if (not line) or line.startswith("#"):
                    continue
                k, v = line.split("=")
                if v.startswith('"') and v.endswith('"'):
                    v = v[1:-1]
                elif v in ["y", "n"]:
                    v = True if v == "y" else False
                else:
                    try:
                        if v.startswith("0x"):
                            v = int(v, 16)
                        else:
                            v = int(v)
                    except:
                        pass
                configs[k] = v
    return configs

def dump_config_mk(configs, path):
    with open(config_filename, "w") as f:
        for k, v in configs.items():
            if isinstance(v, bool):
                v = "y" if v else "n"
            elif isinstance(v, int):
                v = str(v)
            elif isinstance(v, str):
                v = '"' + v + '"'
            f.write("{}={}\n".format(k, v))

def get_config_files(config_file, sdk_path, project_path):
    files = []
    config_mk = os.path.join(project_path, ".config.mk")
    config_default = os.path.join(project_path, "config_defaults.mk")
    if config_file and os.path.exists(config_file):
        files.append(config_file)
    elif os.path.exists(config_default):
        files.append(config_default)
    if os.path.exists(config_mk):
        files.append(config_mk)
    return files

configs = load_config_mk(config_filename)
configs_old = configs.copy()

header = "# Generated by config.py, DO NOT edit!\n\n"
config_content = header
if project_args.generator.strip():
    configs["CONFIG_CMAKE_GENERATOR"] = project_args.generator
if project_args.toolchain.strip() != "":
    if not os.path.exists(project_args.toolchain):
        print("[ERROR] config toolchain path error:", project_args.toolchain)
        exit(1)
    project_args.toolchain = project_args.toolchain.strip().replace("\\","/")
    configs["CONFIG_TOOLCHAIN_PATH"] = project_args.toolchain
if project_args.toolchain_prefix.strip() != "":
    project_args.toolchain_prefix = project_args.toolchain_prefix.strip().replace("\\","/")
    configs["CONFIG_TOOLCHAIN_PREFIX"] = project_args.toolchain_prefix
if "CONFIG_CMAKE_GENERATOR" not in configs or not configs["CONFIG_CMAKE_GENERATOR"]:
    configs["CONFIG_CMAKE_GENERATOR"] = "Unix Makefiles"
    print('no generator set, will use "Unix Makefiles" as default')
if configs != configs_old:
    dump_config_mk(configs, config_filename)
    if os.path.exists("build/config/global_config.mk"):
        os.remove("build/config/global_config.mk")
    print("generate config file at: {}".format(config_filename))

if project_args.build_type:
    build_type = project_args.build_type
elif project_args.release:
    build_type = "MinSizeRel"
elif "CMAKE_BUILD_TYPE" in os.environ:
    build_type = os.environ["CMAKE_BUILD_TYPE"]
else:
    build_type = "Debug"
thread_num = cpu_count()
print("-- CPU count: {}".format(thread_num))
# config
if project_args.cmd == "config":
    print("config complete")
# rebuild / build
elif project_args.cmd == "build" or project_args.cmd == "rebuild":
    print("build now")
    time_start = time.time()
    if not os.path.exists("build"):
        os.mkdir("build")
    os.chdir("build")
    if not os.path.exists("Makefile") or project_args.cmd == "rebuild":
        if not os.path.isabs(project_args.config_file):
            project_args.config_file = os.path.join(project_path, project_args.config_file)
        config_path = os.path.abspath(project_args.config_file)
        if not os.path.exists(config_path):
            print("config file path error:{}".format(config_path))
            exit(1)
        print("-- build type: {}".format(build_type))
        res = subprocess.call(["cmake", "-G", configs["CONFIG_CMAKE_GENERATOR"],
                               "-DCMAKE_BUILD_TYPE={}".format(build_type),
                               "-DDEFAULT_CONFIG_FILE={}".format(config_path),  ".."])
        if res != 0:
            exit(1)
    if project_args.verbose:
        if configs["CONFIG_CMAKE_GENERATOR"] == "Unix Makefiles":
            res = subprocess.call(["cmake", "--build", ".", "--target", "all", "--", "VERBOSE=1"])
        elif configs["CONFIG_CMAKE_GENERATOR"] == "Ninja":
            res = subprocess.call(["cmake", "--build", ".", "--target", "all", "--", "-v"])
        else:
            res = subprocess.call(["cmake", "--build", ".", "--target", "all"])
    else:
        if configs["CONFIG_CMAKE_GENERATOR"] in ["Unix Makefiles", "Ninja"]:
            res = subprocess.call(["cmake", "--build", ".", "--target", "all", "--", "-j{}".format(thread_num)])
        else:
            res = subprocess.call(["cmake", "--build", ".", "--target", "all"])
    if res != 0:
        exit(1)

    time_end = time.time()
    print("==================================")
    print("build end, time last:%.2fs" %(time_end-time_start))
    print("==================================")
# clean
elif project_args.cmd == "clean":
    print("clean now")
    if os.path.exists("build"):
        os.chdir("build")
        p =subprocess.Popen(["cmake", "--build", ".", "--target", "clean"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate("")
        res = p.returncode
        if res == 0:
            print(output.decode(encoding="gbk" if os.name == "nt" else "utf-8"))
    print("clean complete")
# distclean    
elif project_args.cmd == "distclean":
    print("clean now")
    if os.path.exists("build"):
        os.chdir("build")
        p =subprocess.Popen(["cmake", "--build", ".", "--target", "clean"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate("")
        res = p.returncode
        if res == 0:
            print(output.decode(encoding="gbk" if os.name == "nt" else "utf-8"))
        os.chdir("..")
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    print("clean complete")
# menuconfig
elif project_args.cmd == "menuconfig":
    time_start = time.time()
    if not os.path.exists("build"):
        os.mkdir("build")
    os.chdir("build")
    binary_path = os.path.abspath(os.getcwd())
    if not os.path.exists("build/config/global_config.mk"):
        if not os.path.isabs(project_args.config_file):
            project_args.config_file = os.path.join(project_path, project_args.config_file)
        config_path = os.path.abspath(project_args.config_file)
        if not os.path.exists(config_path):
            print("config file path error:{}".format(config_path))
            exit(1)
        res = subprocess.call(["cmake", "-G", configs["CONFIG_CMAKE_GENERATOR"], 
                               "-DCMAKE_BUILD_TYPE={}".format(build_type),
                               "-DDEFAULT_CONFIG_FILE={}".format(config_path),  ".."])
        if res != 0:
            exit(1)
    # res = subprocess.call(["cmake", "--build", ".", "--parallel", "1", "--target", "menuconfig"])
    # when use Ninja, menuconfig will not work, so use python script instead, need help here, PR is welcome
    tool_path = os.path.join(sdk_path, "tools/kconfig/genconfig.py")
    if not os.path.exists(tool_path):
        print("[ERROR] kconfig tool not found:", tool_path)
        exit(1)
    # get default files
    config_files = get_config_files(project_args.config_file, sdk_path, project_path)
    cmd = [sys.executable, tool_path, "--kconfig", os.path.join(sdk_path, "Kconfig")]
    for path in config_files:
        cmd.extend(["--defaults", path])
    cmd.extend(["--menuconfig", "True", "--env", "SDK_PATH={}".format(sdk_path),
                                        "--env", "PROJECT_PATH={}".format(project_path),
                                        "--env", "BUILD_TYPE={}".format(build_type)])
    cmd.extend(["--output", "makefile", os.path.join(binary_path, "config", "global_config.mk")])
    cmd.extend(["--output", "cmake", os.path.join(binary_path, "config", "global_config.cmake")])
    cmd.extend(["--output", "header", os.path.join(binary_path, "config", "global_config.h")])
    res = subprocess.call(cmd)
    if res != 0:
        exit(1)
# clean_conf
elif project_args.cmd == "clean_conf":
    print("clean now")
    # clean cmake config files
    if os.path.exists(config_filename):
        os.remove(config_filename)
    if os.path.exists("build/config/"):
        shutil.rmtree("build/config")
    # clean extra tools config file
    for k, v in extra_tools.items():
        if project_args.cmd in v["cmds"]:
            vars = {
                "project_path": project_path,
                "project_name": project_name,
                "sdk_path": sdk_path,
                "build_type": build_type,
                "project_parser": project_parser,
                "project_args": project_args,
                "configs": configs,
            }
            print("-- call tool <{}>'s clean_conf cmd".format(k))
            v["tool"].main(vars)
    print("clean complete")
# extra tools
elif project_args.cmd in cmd_choices:
    for k, v in extra_tools.items():
        if project_args.cmd in v["cmds"]:
            tool = v["tool"]
            vars = {
                "project_path": project_path,
                "project_name": project_name,
                "sdk_path": sdk_path,
                "build_type": build_type,
                "project_parser": project_parser,
                "project_args": project_args,
                "configs": configs,
            }
            print("\n-------- {} start ---------".format(project_args.cmd))
            ret = tool.main(vars)
            print("-------- {} end ---------".format(project_args.cmd))
            exit(ret)
else:
    print("Error: Unknown command")
    exit(1)

