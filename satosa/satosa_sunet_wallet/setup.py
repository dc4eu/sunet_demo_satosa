from setuptools import setup

setup(
    name='satosa_sunet_wallet',
    py_modules=['satosa_sunet_wallet'],
    entry_points={
    'console_scripts': ['satosa_sunet_wallet = satosa_sunet_wallet:main', ],},
)

#    data_files=['happy_birthday-art.txt'],
#    'console_scripts': ['sunet_wallet = wallet:main', ],},
#    long_description=open('README.rst').read(),
