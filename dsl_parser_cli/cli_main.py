import logging
import argparse
import cli_actions
import cli_logger

# http://stackoverflow.com/questions/17626694/remove-python-userwarning
import warnings
warnings.filterwarnings("ignore")


def _parse():
    parser = argparse.ArgumentParser(prog='cfy-dsl-parser',
                                     description='Process some integers.')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "a" command
    parser_validate = subparsers.add_parser('validate',
                                            help='validate help')
    parser_validate.add_argument('-p', '--blueprint-path',
                                 dest='blueprint_path',
                                 help='the path to blueprint yaml file',
                                 required=True)
    parser_validate.set_defaults(func=cli_actions.validate)

    parser_list_operations = subparsers.add_parser('list-operations',
                                                   help='list operations'
                                                        'for plugin')
    parser_list_operations.add_argument('--plugin-url',
                                        dest='plugin_url',
                                        help='url for plugin yaml',
                                        required=True)
    parser_list_operations.set_defaults(func=cli_actions.list_operations)

    parser_plugin_extract = subparsers.add_parser('plugin-extract',
                                                  help='extracts plugin to a '
                                                       'dest directory')
    parser_plugin_extract.add_argument('--dest-dir',
                                       dest='dest_dir',
                                       help='url for plugin source',
                                       required=True)
    parser_plugin_extract.add_argument('--plugin-source-url',
                                       dest='plugin_source_url',
                                       help='url. value of plugin source',
                                       required=True)
    parser_plugin_extract.set_defaults(func=cli_actions.plugin_extract)
    return parser.parse_args()


def main():
    cli_logger.init()
    args = _parse()
    args.func(args)


if __name__ == '__main__':
    main()
