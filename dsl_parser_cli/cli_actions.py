from dsl_parser import parser
import urllib2
import yaml
from lib.list_operations.get_operations import get_for_plugin
from lib.list_operations.get_package_name import extract_plugin_dir
import sys, traceback


"""
    This module is a collection of actions this module exposes.

    If exposed by a cli, this module defines the subcommands
"""

def validate( args ):
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
        print(e)

def plugin_extract( args ):
    try:
        extract_plugin_dir( args.plugin_source_url, args.dest_dir )
    except Exception as e:
        print('unable to extract plugin to dir [{0}]. {1}'.format( args.dest_dir, e))




def list_operations( args ):
    try:
        results = []

        plugins_yaml = urllib2.urlopen(args.plugin_url).read()
        plugins_data = yaml.load( plugins_yaml )
        if 'plugins' not in plugins_data:
            raise Exception('invalid plugin yaml. missing plugins field')

        for plugin_name in plugins_data['plugins']:
            plugin_data = plugins_data['plugins'][plugin_name]
            results.append({ 'plugin_name' : plugin_name, 'operations' : get_for_plugin( plugin_data ) })


        print(results)
    except Exception as e:
        print('unable to list operations on plugin. {0}'.format( e ) )
        traceback.print_exc(file=sys.stdout)