# Copyright 2022 DeepPavlov.ai
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from setuptools import setup, find_packages

from deepgraphs import __author__, __description__, __email__, __keywords__, __license__, __version__

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def readme():
    with open(os.path.join(__location__, 'README.md'), encoding='utf8') as f:
        text = f.read()
    return text


if __name__ == '__main__':
    setup(
        name='deepgraphs',
        packages=find_packages(exclude=('tests', 'docs', 'utils')),
        version=__version__,
        description=__description__,
        long_description=readme(),
        long_description_content_type='text/markdown',
        author=__author__,
        author_email=__email__,
        license=__license__,
        url='https://github.com/deeppavlov/deepgraphs',
        download_url=f'https://github.com/deeppavlov/deepgraphs/archive/{__version__}.tar.gz',
        keywords=__keywords__,
        include_package_data=True,
        extras_require={
            'docs': [
                'sphinx==3.5.4',
                'sphinx_rtd_theme==0.5.2',
                'nbsphinx==0.8.4',
                'ipykernel==5.5.4',
                'jinja2<=3.0.3'
            ]
        }
    )
