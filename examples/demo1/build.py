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
parser.add_argument("cmd",
                    help="",
                    nargs='?',
                    default=""
                    )

args = parser.parse_args()

cwd = sys.path[0]
os.chdir(cwd)

if args.cmd == "" or args.cmd == "build":
    print("build now")
    time_start = time.time()
    if not os.path.exists("build"):
        os.mkdir("build")
    os.chdir("build")
    try:
        subprocess.run(["cmake", ".."])
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
    shutil.rmtree("build")
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

