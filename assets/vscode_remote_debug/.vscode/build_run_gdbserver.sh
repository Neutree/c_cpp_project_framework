#/bin/bash

set -e

##################### config #####################
project_path=$(pwd)/../examples/demo1
program_path=${project_path}/build/demo1
target_ip=rock-5b.local
target_port=9000
target_user=root
##################################################

## build first
cd ${project_path}
# python project.py --toolchain "" --toolchain-prefix aarch64-linux-gnu- config
python project.py rebuild

# kill gdbserver first if it is running
ssh ${target_user}@${target_ip} "killall gdbserver > /dev/null 2>&1 || true"

## copy to target
scp ${program_path} ${target_user}@${target_ip}:~/dbg_program.bin

## run gdbserver
ssh ${target_user}@${target_ip} "gdbserver :${target_port} ~/dbg_program.bin"


## now you can run debug in vscode


