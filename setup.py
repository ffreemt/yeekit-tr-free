r'''
"yeekitone translate"
'''
# pylint: disable=invalid-name
from pathlib import Path
import re

from setuptools import setup, find_packages

name = """yeekit-tr-free"""
# description = ' '.join(name.split('-'))
description = name.replace('-tr-', ' translate for ')
dir_name, = find_packages()
curr_dir = Path(__file__).parent

version, = re.findall(r"\n__version__\W*=\W*'([^']+)'", open(f'{dir_name}/__init__.py').read())
targz = 'v_' + version.replace('.', '') + '.tar.gz'
install_requires = [
    'requests',
    'jmespath',
    'pytest',
    'coloredlogs',
    'ratelimit',
]

README_rst = f'{curr_dir}/README.md'
long_description = open(README_rst, encoding='utf-8').read() if Path(README_rst).exists() else ''

setup(
    name=name,
    packages=find_packages(),
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['machine translation', 'free', 'scraping', ],
    author="mikeee",
    url=f'http://github.com/ffreemt/{name}',
    download_url='https://github.com/ffreemt/yeekit-tr-free/archive/' + targz,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT License',
)
