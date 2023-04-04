import math
from fractions import Fraction
from numbers import Number

import pytest

from continued_fractions import compute_cfrac, eval_cfrac, get_convergent


# Irrational numbers are ok if we do not require to high accuracy
@pytest.mark.parametrize("inp,n,cfrac", [
    (math.sqrt(2), 12, [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]),
    (math.pi, 11, [3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3]),
    (0.5 + 0.5*math.sqrt(5), 20, [1]*20),  # golden ratio
    (1.5, 5, [1, 2]),  # this is a rational which should be ok
    # input contains already a continued fraction:
    ([3, 7, 15.996594406684103], 11, [3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3]),
])
def test_compute_and_eval_cfrac(inp, n, cfrac):
    eps = 1e-6
    assert compute_cfrac(inp, n, skip_remainder=True) == cfrac
    if isinstance(inp, Number):
        assert abs(eval_cfrac(*cfrac) - inp) < eps


@pytest.mark.xfail(reason="Implementation can't really handle *strongly rational* floats.")
@pytest.mark.parametrize("inp,n,cfrac", [
    (1.75, 5, [1, 1, 3]),
    (0b1011 / 2**4, 10, [0, 1, 2, 5]),
    (0b0011 / 2**4, 10, [0, 5, 3]),
    (0b0110 / 2**4, 10, [0, 2, 1, 1, 1]),
    (0b1011_1110 / 2**8, 10, [0, 1, 2, 1, 7, 3, 1]),
    (0b0110_1111_1001 / 2**12, 15, [0, 2, 3, 2, 1, 1, 5, 1, 1, 2, 3]),
    (0b1111_0000_1001_1101/2**16, 15, [0, 1, 15, 1, 1, 1, 3, 5, 1, 3, 1, 11]),
    ([1, 1+1/3], 5, [1, 1, 3]),
])
def test_compute_and_eval_cfrac_fails(inp, n, cfrac):
    assert compute_cfrac(inp, n, skip_remainder=True) == cfrac


@pytest.mark.parametrize("value,limit_denominator,convergent", [
    (Fraction(7, 4), 4, Fraction(7, 4)),
    (Fraction(7, 4), 3, Fraction(2, 1)),
    (Fraction(11, 16), 10, Fraction(2, 3)),
    (Fraction(3, 16), 10, Fraction(1, 5)),
    (Fraction(3, 8), 4, Fraction(1, 3)),
    (Fraction(95, 128), 50, Fraction(23, 31)),
    (Fraction(1785, 4096), 1207, Fraction(526, 1207)),
    (Fraction(61597, 65536), 5556, Fraction(4144, 4409)),
    (Fraction(1180885736762579530678647, 1208925819614629174706176),
     39794478752901109512,
     Fraction(8591994396922615953, 8796010947596302489)),
])
def test_get_convergent(value, limit_denominator, convergent):
    assert get_convergent(value, limit_denominator) == convergent
