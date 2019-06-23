#
# @file from https://github.com/Neutree/c_cpp_project_framework
# @author neucrack
#

import argparse
import os, sys, time, re, shutil
import subprocess
from multiprocessing import cpu_count


parser = argparse.ArgumentParser(description='build tool', prog=os.path.basename(sys.argv[0]))

parser.add_argument('--toolchain',
                        help='toolchain path ( absolute path )',
                        default="")

parser.add_argument('--toolchain-prefix',
                        help='toolchain prefix(e.g. mips-elf-',
                        default="")
cmd_help ='''project command'''
parser.add_argument("cmd",
                    help=cmd_help,
                    choices=["build", "clean", "distclean", "clean_conf"]
                    )

args = parser.parse_args()

cwd = sys.path[0]
os.chdir(cwd)

config_filename = ".config.mk"
config_content_old = ""

if not os.path.exists("CMakeLists.txt") or  not os.path.exists("main"):
    print("please run me at project folder!")
    exit(1)
if os.path.exists(config_filename):
    with open(config_filename) as f:
        config_content_old = f.read()
header = "# Generated by config.py, DO NOT edit!\n\n"
config_content = header
if args.toolchain.strip() != "":
    if not os.path.exists(args.toolchain):
        print("config toolchain path error:", args.toolchain)
        exit(1)
    args.toolchain = args.toolchain.strip().replace("\\","/")
    config_content += 'CONFIG_TOOLCHAIN_PATH="'+args.toolchain+'"\n'
if args.toolchain_prefix.strip() != "":
    args.toolchain_prefix = args.toolchain_prefix.strip().replace("\\","/")
    config_content += 'CONFIG_TOOLCHAIN_PREFIX="'+args.toolchain_prefix+'"\n'
config_content += '\n'
if config_content != config_content_old:
    with open(config_filename, "w") as f:
        f.write(config_content)
    if os.path.exists("build/config/global_config.mk"):
        os.remove("build/config/global_config.mk")
    print("generate config file at: {}".format(config_filename))


if args.cmd == "build":
    print("build now")
    time_start = time.time()
    if not os.path.exists("build"):
        os.mkdir("build")
    os.chdir("build")
    try:
        subprocess.run(["cmake", "-G", "Unix Makefiles", ".."])
    except Exception as e:
        print("cmake Error:{}".format(e))
        exit(1)
    try:
        subprocess.run(["make", "-j{}".format(cpu_count())])
    except Exception as e:
        print("make Error:{}".format(e))
        exit(1)

    time_end = time.time()
    print("==================================")
    print("build end, time last:%.2fs" %(time_end-time_start))
    print("==================================")

elif args.cmd == "clean":
    print("clean now")
    if os.path.exists("build"):
        os.chdir("build")
        try:
            subprocess.run(["make", "clean"])
        except Exception as e:
            print("make Error:{}".format(e))
            exit(1)
    print("clean complete")
elif args.cmd == "distclean":
    print("clean now")
    if os.path.exists("build"):
        shutil.rmtree("build")
    print("clean complete")
elif args.cmd == "clean_conf":
    print("clean now")
    if os.path.exists(config_filename):
        os.remove(config_filename)
    if os.path.exists("build/config/"):
        shutil.rmtree("build/config")
    print("clean complete")
elif args.cmd == "menuconfig":
    time_start = time.time()
    if not os.path.exists("build"):
        os.mkdir("build")
    os.chdir("build")
    if not os.path.exists("build/Makefile"):
        try:
            subprocess.run(["cmake", ".."])
        except Exception as e:
            print("cmake Error:{}".format(e))
            exit(1)
    try:
        subprocess.run(["make", "menuconfig"])
    except Exception as e:
        print("make menucconfig Error:{}".format(e))
        exit(1)
else:
    print("Error: Unknown command")
    exit(1)
