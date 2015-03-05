import os

from subprocess import Popen, PIPE


def install(plugin_dir, plugin_data):
    print('installing..')
    """
        installs the plugin. yaml looks like this
        <pre>
         puppet:
             executor: host_agent
             source: my_cloudify_plugins/puppet-plugin
             install_arguments: -r requirements.txt
         </pre>
        :param package: package to install
        :return: None
    """
    # the reason why we are not using pip programmatically
    # is that it prints to output even with '-q' flag.
    previous_cwd = os.getcwd()
    try:
        # install_arguments require us to change directory.
        # -r requirements.txt only works if install on .
        os.chdir(plugin_dir)
        args = plugin_data.get('install_arguments', '-q')
        install_args = ['pip', 'install', '.']
        install_args.extend(args.split(' '))
        p = Popen(install_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if p.returncode != 0:
            raise Exception('error when download. [{0}] , [{1}]'
                            .format(output, err))
    finally:
        os.chdir(previous_cwd)
