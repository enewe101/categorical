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


