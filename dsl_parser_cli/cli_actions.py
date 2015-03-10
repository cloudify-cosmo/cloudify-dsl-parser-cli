import sys

import requests
import json
import yaml


from dsl_parser import parser

from dsl_parser_cli import cli_logger
from dsl_parser_cli.tasks.list_operations.get_operations \
    import get_for_plugin
from dsl_parser_cli.tasks.list_operations.get_package_name \
    import extract_plugin_dir


"""
    This module is a collection of actions this module exposes.

    If exposed by a cli, this module defines the subcommands
"""


def validate(args):
    """
    Validates a blueprint using the official dsl parser

    Example:

        validate(dict( path = '/path/to/blueprint' ) )

    Attributes:

        args (dict): a dict of arguments

    Returns:
        None
    """
    try:
        parser.parse_from_path(args.blueprint_path)
    except Exception as e:
        cli_logger.error(e)


def plugin_extract(args):
    try:
        extract_plugin_dir(plugin_url=args.plugin_source_url,
                           plugin_dir=args.dest_dir)
    except:
        cli_logger.exception('unable to extract plugin to dir [{0}]'
                             .format(args.dest_dir))
        sys.exit(1)


def list_operations(args):
    try:
        blueprint_yaml = requests.get(url=args.blueprint_url).text
        blueprint_data = yaml.load(stream=blueprint_yaml)
        results = [{'plugin_name': plugin_name,
                    'operations': get_for_plugin(plugin_data=plugin_data)}
                   for plugin_name, plugin_data
                   in blueprint_data.get('plugins', {}).items()]
        cli_logger.info(json.dumps(results))
    except:
        cli_logger.exception('unable to list operations on plugin')
        sys.exit(1)
