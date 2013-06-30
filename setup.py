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
