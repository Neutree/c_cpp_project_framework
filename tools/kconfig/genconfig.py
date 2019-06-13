from Kconfiglib.menuconfig import menuconfig
from Kconfiglib.kconfiglib import Kconfig
import argparse
import os, sys


def write_config(kconfig, filename):
    print("write config at:", filename)

def write_cmake(kconfig, filename):
    print("write cmake  at:", filename)

def write_header(kconfig, filename):
    print("write header at:", filename)
    kconfig.write_autoconf(filename)

OUTPUT_FORMATS = {"config": write_config,
                  "header": write_header,
                  "cmake": write_cmake
                  }

parser = argparse.ArgumentParser(description='menuconfig tool', prog=os.path.basename(sys.argv[0]))

parser.add_argument('--kconfig',
                    help='KConfig file',
                    default='Kconfig',
                    metavar='FILENAME',
                    required=None)

parser.add_argument('--defaults',
                    help='Optional project defaults file, used if --config file doesn\'t exist. '
                            'Multiple files can be specified using multiple --defaults arguments.',
                    nargs='?',
                    default=[],
                    action='append')

parser.add_argument('--output', nargs=2, action='append',
                        help='Write output file (format and output filename)',
                        metavar=('FORMAT', 'FILENAME'),
                        default=[])

parser.add_argument('--env',
                    action='append',
                    default=[],
                    help='Environment to set when evaluating the config file', 
                    metavar='VAR=VALUE')

parser.add_argument("--menuconfig",
                    help="Open menuconfig GUI interface",
                    choices=["False", "True"],
                    default="False",
                    )

args = parser.parse_args()

for env in args.env:
    env = env.split("=")
    var = env[0]
    value = env[1]
    os.environ[var] = value

out_format = {"config": ".config"}
for fmt, filename in args.output:
    if fmt not in OUTPUT_FORMATS.keys():
        print("Format %s not supported! Known formats:%s" %(fmt, OUTPUT_FORMATS.keys()))
        sys.exit(1)
    out_format[fmt] = filename
    
if out_format["config"] != ".config":
    os.environ["KCONFIG_CONFIG"] = out_format["config"]

kconfig = Kconfig(args.kconfig)

for path in args.defaults:
    if not os.path.exists(path):
        raise ValueError("Path %s not found!" %(path))
    print("load default:", path)
    kconfig.load_config(path, replace=False)


if args.menuconfig == "True":
    menuconfig(kconfig)

# write back

for fmt, filename in out_format.items():
    func = OUTPUT_FORMATS[fmt]
    func(kconfig, filename)


