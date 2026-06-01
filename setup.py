"""
CB PMR Logbook - Setup.py pro PyInstaller distribuci
"""

from setuptools import setup
from setuptools.command.build_py import build_py
import os

# Přečteme requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='CB-PMR-Logbook',
    version='1.0.0',
    description='Profesionální deník pro CB a PMR radioamatéry',
    author='PC-RADIO-LOGBOOK',
    author_email='',
    url='https://github.com/MERC63AMG/PC-RADIO-LOGBOOK',
    py_modules=['main'],
    entry_points={
        'gui_scripts': [
            'cb-pmr-logbook=main:main',
        ],
    },
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Czech',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Communications :: Ham Radio',
    ],
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
)
