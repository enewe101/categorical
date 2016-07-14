import numpy as np
from collections import Counter
from categorical import Categorical
from unittest import TestCase, main


class TestMultinomialSampler(TestCase):

	def test_multinomial_sampler(self):
		counts = range(1,6)
		sampler = Categorical(counts)

		# Test asking for a single sample (where no shape tuple supplied)
		single_sample = sampler.sample()
		self.assertTrue(type(single_sample) is np.int64)

		# Test asking for an array of samples (by passing a shape tuple)
		shape = (2,3,5)
		array_sample = sampler.sample(shape)
		self.assertTrue(type(array_sample) is np.ndarray)
		self.assertTrue(array_sample.shape == shape)


	def test_multinomial_sampler_stats(self):
		'''
		This tests that the sampler really does produce results whose
		statistics match those requested by the counts vector
		'''
		# Seed numpy's random function to make the test reproducible
		np.random.seed(1)

		# Make a sampler with probabilities proportional to counts
		counts = range(1,6)
		sampler = Categorical(counts)

		# Draw one hundred thousand samples, then total up the fraction of
		# each outcome obseved
		counter = Counter(sampler.sample((100000,)))
		total = float(sum(counter.values()))
		found_normalized = [
			counter[i] / total for i in range(len(counts))
		]

		# Make an list of the expected fractions by which each outcome
		# should be observed, in the limit of infinite sample
		total_in_expected = float(sum(counts))
		expected_normalized = [
			c / total_in_expected for c in counts
		]

		# Check if each outcome was observed with a fraction that is within
		# 0.005 of the expected fraction
		close = [
			abs(f - e) < 0.005
			for f,e in zip(found_normalized, expected_normalized)
		]
		self.assertTrue(all(close))


if __name__=='__main__':
	main()
