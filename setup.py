#
# Copyright 2013 Sam Kleinman (tychoish)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import taskn

from setuptools import setup
from sys import version_info

with open('requirements.txt') as f:
    REQUIRES = f.read().splitlines()

if version_info < (2, 7):
    # no argparse in 2.6 standard
    REQUIRES.append('argparse')

setup(
    name='taskn',
    maintainer='tychoish',
    maintainer_email='sam@tychoish.com',
    description='A note taking addition to taskwarrior',
    version=taskn.__version__,
    license='Apache',
    url='http://cyborginstitute.org/projects/taskn',
    packages=['taskn'],
    install_requires=REQUIRES,
    test_suite=None,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'console_scripts': [
            'taskn = taskn.note:main',
            'tasknadm = taskn.admin:main',
            ],
        }
    )
