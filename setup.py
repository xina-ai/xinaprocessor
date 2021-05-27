from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xinaprocessor',
    version='0.4',
    install_requires=required,
    tests_require=['pytest'],
    author="Xina AI",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/xina-ai/xinaprocessor',
    description="Xina processing library",
    packages=find_packages(include=['xinaprocessor'])
)
