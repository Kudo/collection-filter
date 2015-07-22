import setuptools
import io

setuptools.setup(
    name='collection-filter',
    version='0.1',
    description=(
        'A small list/dict DSL query filter ' +
        'specific for RESTful API partial response.'
    ),
    author='Kudo Chien',
    author_email='ckchien@gmail.com',
    url='https://github.com/kudo/python-collection-filter',
    license='MIT',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    packages = ['collection_filter'],
    test_suite = 'tests',
    install_requires = ['jsonpath-rw'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
