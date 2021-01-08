from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='xinaprocessor',
    version='0.1.0',
    install_requires=required,
    tests_require=['pytest'],
    author="Xina AI",
    description="Arabic processing library",
    packages=find_packages(include=['xinaprocessor'])
)
