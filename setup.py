from setuptools import find_packages, setup

setup(
    name='puro',
    version='0.0.1',
    description='Highly configurable data streams',
    url='https://github.com/jvtm/puro',
    author='Jyrki Muukkonen',
    author_email='jvtm@kruu.org',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='data streams json',
    packages=find_packages(exclude=['docs', 'tests']),
    # NOTE: for now all used helper modules as strict requirements
    # this might change later on, and introducing 'full' + 'test' flavors
    install_requires=['jmespath', 'jsonschema', 'kmatch'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-asyncio'],
    },
)
