'''
Enables fast on-demand sampling from a categorical probability distribution
'''

import numpy.random as r
import numpy as np


class Categorical(object):

	def __init__(self, scores):
		if len(scores) < 1:
			raise ValueError('The scores list must have length >= 1')
		self.scores = scores
		self.total = float(sum(scores))
		self.K = len(scores)
		self.setup()


	def get_probability(self, k):
		'''
		Get the actual probability associated to outcome k
		'''
		return self.orig_prob_mass[k]


	def setup(self):
		self.orig_prob_mass = np.zeros(self.K)
		self.mixture_prob_mass = np.zeros(self.K)
		self.mass_reassignments = np.zeros(self.K, dtype=np.int64)
 
		# Sort the data into the outcomes with probabilities
		# that are larger and smaller than 1/K.
		smaller = []
		larger  = []
		for k, score in enumerate(self.scores):
			self.orig_prob_mass[k] = score / self.total
			self.mixture_prob_mass[k] = (self.K*score) / self.total
			if self.mixture_prob_mass[k] < 1.0:
				smaller.append(k)
			else:
				larger.append(k)
 
		# We will have k different slots. Each slot represents 1/K
		# prbability mass, and to each we allocate all of the probability
		# mass from a "small" outcome, plus some probability mass from
		# a "large" outcome (enough to equal the total 1/K).
		# We keep track of the remaining mass left for the larger outcome,
		# allocating the remainder to another slot later.
		# The result is that the kth has some mass allocated to outcome
		# k, and some allocated to another outcome, recorded in J[k].
		# q[k] keeps track of how much mass belongs to outcome k, and 
		# how much belongs to outcome J[k].
		while len(smaller) > 0 and len(larger) > 0:
			small_idx = smaller.pop()
			large_idx = larger.pop()
 
			self.mass_reassignments[small_idx] = large_idx
			self.mixture_prob_mass[large_idx] = (
				self.mixture_prob_mass[large_idx] -
				(1.0 - self.mixture_prob_mass[small_idx])
			)
 
			if self.mixture_prob_mass[large_idx] < 1.0:
				smaller.append(large_idx)
			else:
				larger.append(large_idx)
 

		# Make a sample method, binding some variables, and 
		# vectorising it
		K = self.K
		mixture_prob_mass = self.mixture_prob_mass
		mass_reassignments = self.mass_reassignments
		def _sample(*args):

			# Draw from the overall uniform mixture.
			k = np.random.choice(K)
		 
			# Draw from the binary mixture, either keeping the
			# small one, or choosing the associated larger one.
			if np.random.uniform() < mixture_prob_mass[k]:
				return np.int64(k)
			else:
				return mass_reassignments[k]

		self._sample = _sample
		self._usample = np.vectorize(_sample)

		return self.mass_reassignments, self.mixture_prob_mass


	def sample(self, shape=(), dtype='int64'):

		# Handle the case of a single (non-array) sample
		if len(shape) < 1:
			sample = self._sample()
			if dtype != 'int64':
				sample = getattr(np, dtype)(sample)
			return sample

		# Handle the case of multiple samples returned as an array
		sample = np.fromfunction(self._usample, shape) 
		if dtype != 'int64':
			sample = sample.astype(dtype)
		return sample


