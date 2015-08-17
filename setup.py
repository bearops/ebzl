from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession
from os import path


requirements = [str(ir.req)
                for ir in parse_requirements('./requirements/requirements.txt',
                                             session=PipSession())]

setup(
    name="ebzl",
    version="0.9",
    description="AWS ElasticBeanstalk management helper",
    url="http://github.com/bearops/ebzl",
    author='Wojciech Gaca',
    author_email='gaca@dubizzle.com',
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0"
    ],
    keywords=("aws amazon web services elastic beanstalk "
              "eb application environment"),
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ebzl = ebzl.ebzl:main'
        ]
    }
)
