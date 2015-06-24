from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession
from os import path
here = path.abspath(path.dirname(__file__))

install_reqs = parse_requirements('./requirements/requirements.txt', 
                                  session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="ebzl",
    version="0.0.1",
    install_requires=reqs,
    author='Wojciech Gaca',
    author_email='gaca@dubizzle.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ebzl = ebzl.ebzl:main'
        ]
    }
)
