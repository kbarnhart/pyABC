import scipy as sp
from pyabc import (PercentileDistanceFunction,
                   MinMaxDistanceFunction,
                   PNormDistance)


class MockABC:
    def __init__(self, samples):
        self.samples = samples

    def sample_from_prior(self):
        return self.samples


def test_single_parameter():
    dist_f = MinMaxDistanceFunction(measures_to_use=["a"])
    abc = MockABC([{"a": -3}, {"a": 3}, {"a": 10}])
    dist_f.initialize(0, abc.sample_from_prior())
    d = dist_f(0, {"a": 1}, {"a": 2})
    assert 1/13 == d


def test_two_parameters_but_only_one_used():
    dist_f = MinMaxDistanceFunction(measures_to_use=["a"])
    abc = MockABC([{"a": -3, "b": 2}, {"a": 3, "b": 3}, {"a": 10, "b": 4}])
    dist_f.initialize(0, abc.sample_from_prior())
    d = dist_f(0, {"a": 1, "b": 10}, {"a": 2, "b": 12})
    assert 1/13 == d


def test_two_parameters_and_two_used():
    dist_f = MinMaxDistanceFunction(measures_to_use=["a", "b"])
    abc = MockABC([{"a": -3, "b": 2}, {"a": 3, "b": 3}, {"a": 10, "b": 4}])
    dist_f.initialize(0, abc.sample_from_prior())
    d = dist_f(0, {"a": 1, "b": 10}, {"a": 2, "b": 12})
    assert 1/13 + 2/2 == d


def test_single_parameter_percentile():
    dist_f = PercentileDistanceFunction(measures_to_use=["a"])
    abc = MockABC([{"a": -3}, {"a": 3}, {"a": 10}])
    dist_f.initialize(0, abc.sample_from_prior())
    d = dist_f(0, {"a": 1}, {"a": 2})
    expected = (
        1 / (sp.percentile([-3, 3, 10], 80) - sp.percentile([-3, 3, 10], 20))
    )
    assert expected == d


def test_pnormdistance():
    abc = MockABC([{'s1': -1, 's2': -1, 's3': -1},
                   {'s1': -1, 's2': 0, 's3': 1}])

    # first test that for PNormDistance, the weights stay constant
    dist_f = PNormDistance(p=2)
    dist_f.initialize(0, abc.sample_from_prior())

    # call distance function, also to initialize w
    d = dist_f(0, abc.sample_from_prior()[0], abc.sample_from_prior()[1])
    expected = pow(1**2+2**2, 1/2)
    assert expected == d

    assert sum(abs(a-b) for a, b in
               zip(list(dist_f.w[0].values()), [1, 1, 1])) < 0.01

    # TODO: Also create test for AdaptivePNormDistance
