#!/usr/bin/env python
#-*- coding = utf-8 -*-

#
# @file from https://github.com/Neutree/c_cpp_project_framework
# @author neucrack
# @license Apache 2.0
#

import sys, os

sdk_env_name = "MY_SDK_PATH"
custom_component_path_name = "CUSTOM_COMPONENTS_PATH"

# get SDK absolute path
sdk_path = os.path.abspath(sys.path[0]+"/../../")
try:
    if os.environ[sdk_env_name] and os.path.exists(os.environ[sdk_env_name]):
        sdk_path = os.environ[sdk_env_name]
except Exception:
    pass
print("-- SDK_PATH:{}".format(sdk_path))

# get custom components path
custom_components_path = None
try:
    if os.environ[custom_component_path_name] and os.path.exists(os.environ[custom_component_path_name]):
        custom_components_path = os.environ[custom_component_path_name]
except Exception:
    pass
print("-- CUSTOM_COMPONENTS_PATH:{}".format(custom_components_path))

# execute project script from SDK
project_file_path = sdk_path+"/tools/cmake/project.py"
with open(project_file_path) as f:
    exec(f.read())

