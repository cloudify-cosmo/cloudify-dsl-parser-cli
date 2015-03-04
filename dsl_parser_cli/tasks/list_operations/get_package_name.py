"""
hack-ish script to extract the name field from a python package
should be called with the directory containing setup.py as the first argument
"""

import setuptools
import sys
from os import path
import pip
import tempfile
import shutil
import os
import pipes
from subprocess import Popen, PIPE

result = None


def parse_pip_version(pip_version=None):
    """
        :return: (major,minor,micro) pip version
    """
    if not pip_version:
        try:
            pip_version = pip.__version__
        except AttributeError as e:
            raise Exception('Failed to get pip version: ', str(e))

    if not pip_version:
        raise Exception('Failed to get pip version')

    if not isinstance(pip_version, basestring):
        raise Exception('Invalid pip version: {0} is not a string'
                        .format(pip_version))

    if not pip_version.__contains__("."):
        raise Exception('Unknown formatting of pip version: "{0}", ' +
                        'expected dot-delimited numbers (e.g. ' +
                        '"1.5.4", "6.0")'.format(pip_version))

    version_parts = pip_version.split('.')
    major = version_parts[0]
    minor = version_parts[1]
    micro = ''
    if len(version_parts) > 2:
        micro = version_parts[2]

    if not str(major).isdigit():
        raise Exception('Invalid pip version: "{0}", major version ' +
                        'is "{1}" while expected to be a number'
                        .format(pip_version, major))

    if not str(minor).isdigit():
        raise Exception('Invalid pip version: "{0}", minor version ' +
                        'is "{1}" while expected to be a number'
                        .format(pip_version, minor))

    return major, minor, micro


def is_pip6_or_higher(pip_version=None):
    """
        :return: True iff pip is of version 6+
    """
    major, minor, micro = parse_pip_version(pip_version)

    if int(major) >= 6:
        return True
    else:
        return False


# based on https://github.com/cloudify-cosmo/cloudify-manager/blob/master/plugins/plugin-installer/plugin_installer/tasks.py  # noqa
def download_plugin(plugin_url):
    """

        :param plugin_url: url to download
        :return: directory where extracted plugin can be found
    """
    plugin_dir = tempfile.mkdtemp()
    download_args = ['cfy-dsl-parser',
                     'plugin-extract',
                     '--plugin-source-url',
                     pipes.quote(plugin_url),
                     '--dest-dir',
                     pipes.quote(plugin_dir)]
    p = Popen(download_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        raise Exception('error when download. [{0}] , [{1}]'
                        .format(output, err))
    return plugin_dir


def extract_plugin_dir(plugin_url, plugin_dir):
    """

        :param plugin_url: what to extract
        :param plugin_dir: where to extract
        :return: directory where plugin is extracted to
    """
    try:
        # check pip version and unpack plugin_url accordingly
        if is_pip6_or_higher():
            pip.download.unpack_url(link=pip.index.Link(plugin_url),
                                    location=plugin_dir,
                                    download_dir=None,
                                    only_download=False)
        else:
            req_set = pip.req.RequirementSet(build_dir=None,
                                             src_dir=None,
                                             download_dir=None)
            req_set.unpack_url(link=pip.index.Link(plugin_url),
                               location=plugin_dir,
                               download_dir=None,
                               only_download=False)

    except Exception as e:
        if plugin_dir and os.path.exists(plugin_dir):
            shutil.rmtree(plugin_dir)
        raise Exception('Failed to download and unpack plugin from ' +
                        '{0}: {1}'.format(plugin_url, str(e)))

    return plugin_dir


def get_package_name(plugin_url):
    """
        :param plugin_url: plugin url
        :return: the plugin's package name
    """
    root_dir = download_plugin(plugin_url)

    # patch for setuptools.py that prints the package name
    # to stdout (also supports pbr packages)
    def patch_setup(name=None, pbr=False, *args, **kwargs):
        if pbr:
            import ConfigParser
            config = ConfigParser.ConfigParser()
            config.read(path.join(root_dir, 'setup.cfg'))
            name = config.get('metadata', 'name')
        if name is None:
            sys.stderr.write('Failed finding extracting package name for'
                             ' package located at: {0}'.format(root_dir))
            sys.exit(1)
        global result
        result = name
        # sys.stdout.write(name)
    # monkey patch setuptools.setup
    # backup = setuptools.setup
    setuptools.setup = patch_setup
    # Make sure our setup.py is first in path
    # sys.path.insert(0, root_dir)
    # # The line below is important
    # import setup  # NOQA
    execfile(root_dir + '/setup.py')
    # setuptools.setup = backup
    shutil.rmtree(root_dir)
    return result
