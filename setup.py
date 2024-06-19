from setuptools import setup, find_packages

setup(
    name='pycan',
    version='0.1.0',
    author='Yanujz',
    author_email='yanujz@live.it',
    description='A Python module for implementing a UDS + ISO-TP stack for automotive diagnostics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Yanujz/pycan',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
