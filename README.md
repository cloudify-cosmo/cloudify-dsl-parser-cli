


# This component is not officially supported by GigaSpaces and should not be used

This component is not officially supported by GigaSpaces and should not be used

The dsl parser API this project uses does not provide any backwards compatibility guarantees

# cloudify-dsl-parser-cli

a cli wrapper for cloudify-dsl-parser


## A word about list-operations

the list-operations command will install the plugins specified in the plugin yaml.

we recommend you activate it each time in a new virtualenv which you should later delete.

## How to install

clone and run

```
pip install  -rdev-requirements.txt . --no-deps
```

# How to run the cli

 - use a virtualenv
 - clone the repository
 - run `pip install -r dev-requirements.txt .` - this will install your dependencies and the cli

now if you run `cfy-dsl-parser` you will see it is installed

to configure the composer to use this parser, just point to the virtual environment.

