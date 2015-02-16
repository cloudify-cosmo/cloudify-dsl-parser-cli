import logging
import argparse
import cli_actions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog='cfy-dsl-parser',description='Process some integers.')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "a" command
parser_validate = subparsers.add_parser('validate',help='validate help')
parser_validate.add_argument('-p','--blueprint-path',dest='path',help='the path to blueprint yaml file')
parser_validate.set_defaults(func=cli_actions.validate)
args = parser.parse_args()

def main():
    args.func(args)


if __name__ == '__main__':
    main()