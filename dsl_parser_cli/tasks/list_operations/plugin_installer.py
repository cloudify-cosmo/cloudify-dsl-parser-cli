from subprocess import Popen, PIPE
import pipes


def install(package):
    """
        installs the plugin
        :param package: package to install
        :return: None
    """
    # the reason why we are not using pip programmatically
    # is that it prints to output even with '-q' flag.

    install_args = ['pip', 'install', pipes.quote(package), '-q']
    p = Popen(install_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        raise Exception('error when download. [{0}] , [{1}]'
                        .format(output, err))
