from setuptools import setup

setup(
    name='satosa_static_ds',
    py_modules=['satosa_static_ds'],
    entry_points={
    'console_scripts': ['satosa_static_ds = satosa_static_ds:main', ],},
)

#    data_files=['happy_birthday-art.txt'],
#    'console_scripts': ['sunet_wallet = wallet:main', ],},
#    long_description=open('README.rst').read(),
