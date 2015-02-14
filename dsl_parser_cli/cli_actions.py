from dsl_parser import parser
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
        parser.parse_from_path(args.path)
    except Exception as e:
        print(e)
