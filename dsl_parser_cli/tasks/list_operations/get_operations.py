"""
This POC shows how to get cloudify plugin operations

To run this POC you need to do the following

1. Get a virtualenv with cloudify-plugins-common
   installed - plugins may reference this
2. Get a plugin's source and put it relative to this
   source at folder X (see what X is below)
3. Add __init__.py files to make directories into packages
"""

import tempfile
import shutil
import os
from subprocess import Popen, PIPE

import cloudify.decorators

import plugin_installer

from get_package_name import get_package_name

operations = []


def op_hook(func, **kwargs):
    op_name = func.func_name
    op_module = func.__module__
    operations.append({'module': op_module,
                       'name': op_name,
                       'args': func.func_code.co_varnames})

cloudify.decorators.operation = op_hook


def extract_module_paths(plugin_name):

    # print('getting paths for ' + plugin_name)

    module_paths = []
    p = Popen(['pip', 'show', '-f', plugin_name],
              stdin=PIPE,
              stdout=PIPE,
              stderr=PIPE)
    output, err = p.communicate()
    files = output.splitlines()
    for module in files:
        if module.endswith('.py') and '__init__' not in module:
            # the files paths are relative to the package __init__.py file.
            module_paths.append(module.replace('../', '')
                                .replace('/', '.').replace('.py', '').strip())
    return module_paths


def get_for_package(package_name):
    global operations
    operations = []
    modules_paths = extract_module_paths(package_name)

    for path in modules_paths:
        try:
            __import__(path)
        except:
            pass
    return operations


def get_for_plugin(plugin_data):
    if 'source' not in plugin_data:
        raise Exception('invalid plugin_data. source is missing')
    plugin_source = plugin_data['source']
    plugin_dir = tempfile.mkdtemp()
    try:
        package_name = get_package_name(plugin_source, plugin_dir)
        plugin_installer.install(plugin_dir, plugin_data)
        return get_for_package(package_name)
    finally:
        if plugin_dir and os.path.exists(plugin_dir):
            shutil.rmtree(plugin_dir)
