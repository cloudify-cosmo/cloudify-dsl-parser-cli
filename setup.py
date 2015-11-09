########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


from setuptools import setup, find_packages


install_requires = [
    'cloudify-dsl-parser==3.3rc1',
    'cloudify-plugins-common==3.3rc1',

]

try:
    from collections import OrderedDict  # NOQA
except ImportError, e:
    install_requires.append('ordereddict==1.1')


setup(
    name='cloudify-dsl-parser-cli',
    version='0.1',
    author='Gigaspaces',
    author_email='cosmo-admin@gigaspaces.com',
    packages=find_packages(),
    license='LICENSE',
    description='Cloudify DSL parser command line',
    entry_points={
        'console_scripts': [
            'cfy-dsl-parser = dsl_parser_cli.cli_main:main'
        ]
    },
    zip_safe=False,
    install_requires=install_requires
)
