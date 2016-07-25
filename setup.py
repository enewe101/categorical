"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='categorical',

    # Versions should comply with PEP440.  For a discussion on 
	# single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.4',

    description='Fast on-demand sampling from categorical distributions',
    long_description='''
Categorical Sampler
-----

Install from pip: `pip install categorical-sampler`

Let&rsquo;s generate a probability distribution to get us started.  First, sample a bunch of random numbers to determine probability &ldquo;scores&rdquo;.


    >>> from random import random
    >>> k = 10**6
    >>> scores = [random() for i in range(k)]
    >>> total = sum(scores)
    >>> probabilities = [s / total for s in scores]


We've normalized the scores to sum to 1, i.e. make
them into proper probabilities, but actually the categorical sampler will do that for us, so it&rsquo;s not necessary:

    >>> from categorical import Categorical as C
    >>> my_sampler = C(scores)
    >>> print my_sampler.sample()
    487702

Comparing to numpy, assuming we draw 1000 individual samples *individually*:


    >>> from numpy.random import choice
    >>> import time
    >>> 
    >>> def time_numpy():
    >>>     start = time.time()
    >>>     for i in range(1000):
    >>>         choice(k, p=probabilities)
    >>>     print time.time() - start
    >>> 
    >>> def time_my_alias():
    >>>     start = time.time()
    >>>     for i in range(1000):
    >>>         my_sampler.sample()
    >>>     print time.time() - start
    >>> 
    >>> time_numpy()
    31.0555009842
    >>> time_my_alias()
    0.0127031803131

Get the actual probability of a given outcome:

    >>> my_sampler.get_probability(487702)
    1.0911282101090306e-06 

	''',

    # The project's main homepage.
    url='https://github.com/enewe101/categorical',

    # Author details
    author='Edward Newell',
    author_email='edward.newell@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, 
		# ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='sample sampler sampling categorical multinomial discrete distribution statistics probability random',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

	install_requires=['numpy'],
)
