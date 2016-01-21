#!/usr/bin/env python
"""
sentry-pubuim
============

An extension for `Sentry <https://getsentry.com>`_ which posts notifications
to `Pubuim <https://pubu.im/>`_.

:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=7.0.0',
]

setup(
    name='sentry-pubuim',
    version='0.0.4',
    author='minbaby.zhang',
    author_email='minbaby.zhang@behinders.com',
    url='https://github.com/minbaby/sentry-pubuim',
    description='A Sentry extension which posts notifications to Pubuim (https://pubu.im/).',
    long_description=open('README.rst').read(),
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'pubuim = sentry_pubuim',
        ],
        'sentry.plugins': [
            'pubuim = sentry_pubuim.plugin:PubuimPlugin',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
