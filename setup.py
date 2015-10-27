from setuptools import setup, find_packages 
from codecs import open  # To use a consistent encoding
import os

here = os.path.abspath(os.path.dirname(__file__))

#Get the long description from the relevant file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='umpyre',
    packages=find_packages(),
    version='0.0.1',
    description='Fun with sabermetrics in python',
    long_description=long_description,    
    url='https://github.com/dustinstansbury/umpyre',
    author='Dustin Stansbury',
    author_email='dustin.stansburay@gmail.com.com',
    keywords='baseball,sabermetrics,python',

    install_requires=['numpy>=1.6.1',
                      'scipy>=0.9'
                      'pandas',
                      'scikit-learn',
                      'ipython',
                      'MySQL-python',
                      'statsmodels',
                      'beautifulsoup4',
                      'dateutils',
                      'seaborn',
                      'progressbar',
                      'lxml'],
)