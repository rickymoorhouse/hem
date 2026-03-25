import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hemApp",
    author = "Ricky Moorhouse",
    author_email = "hem@rickymoorhouse.uk",
    description = ("HTTP Endpoint Monitor - keeping the loose ends tied up"),
    setup_requires = ['setuptools_scm', 'pytest>=8.0.0', 'pytest-cov>=5.0.0', 'requests-mock>=1.12.0'],
    use_scm_version=True,
    install_requires = ['PyYaml>=6.0.0', 'pike>=0.1.1', 'click>=8.1.0', 'requests>=2.32.0', 'dnspython>=2.6.0', 'pyjwt>=2.9.0'],
    license = "MIT",
    keywords = "monitor, http",
    url = "https://rickymoorhouse.uk/blog/2018/introducing-hem/",
    packages=find_packages(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    test_suite = 'nose.collector',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'hem=hemApp.cli:main',
        ],
    },    
)
