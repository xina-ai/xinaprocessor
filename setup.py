from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='xinaprocessor',
    version='0.1.1',
    install_requires=required,
    tests_require=['pytest'],
    author="Xina AI",
    url='https://github.com/xina-ai/xinaprocessor',
    description="Arabic processing library",
    packages=find_packages(include=['xinaprocessor'])
)
