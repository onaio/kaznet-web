"""
Setup.py for Kaznet
"""
from setuptools import setup, find_packages

setup(
    name='kaznet',
    version="1.0.0",
    description='Tasking application built on top of Onadata',
    license='Apache 2.0',
    author='Ona Systems Inc',
    author_email='tech@ona.io',
    url='https://github.com/onaio/kaznet-web',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'Django >= 2, < 2.1',
        'djangorestframework',
        'psycopg2-binary',
        'django-prices',
        'django-phonenumber-field',
        'phonenumberslite',
        'django-allauth',
        'requests',
        'celery',
        'django-cors-headers',
        'whitenoise',
        'djangorestframework-jsonapi',
        'geopy',
        'django-filter < 2',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 2',
    ],
)
