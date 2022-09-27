# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

packages = ['anixart']

requires = ['requests']

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('py -m build')
    os.system('py -m twine upload --repository testpypi dist/*')
    os.system('py -m twine upload --repository pypi dist/*')
    sys.exit()

about = {}
with open(os.path.join(here, 'anixart', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'anixart': 'anixart'},
    include_package_data=True,
    install_requires=requires,
    license=about['__license__'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Documentation': 'https://anixart.readthedocs.io/',
        'Source': 'https://github.com/SantaSpeen/anixart',
    },
    python_requires=">=3.7",
)
