import pytest
from qiskit import transpile
from qiskit_aer import AerSimulator

from chapter_5 import (find_factor, get_maximizing_keys, intlogx, is_power,
                       make_order_finding_phase_estimation, quantum_add)


@pytest.mark.parametrize("a,b,size,expected", {
    (1, 2, 4, 3),
    (0, 0, 4, 0),
    (1, 0, 4, 1),
    (5, 10, 4, 15),
    (100, 50, 8, 150),
})
def test_quantum_addition(a, b, size, expected):
    assert quantum_add(a, b, size=size) == expected


@pytest.mark.parametrize("a,b,modulus,expected", {
    (2, 1, 10, 3),
    (0, 2, 10, 2),
    (5, 6, 7, 4),
    (7, 7, 8, 6),
    (7, 19, 21, 5),
    (67, 83, 85, 65),
})
def test_modular_quantum_addition(a, b, modulus, expected):
    assert quantum_add(a, b, modulus=modulus) == expected


@pytest.mark.slow
@pytest.mark.parametrize("a,modulus,maximizing_bits", {
    # Remark: Theoretically, if the order is a power of 2 the results should be *clean* in
    # the sense that only the below mentioned strings get non-zero counts. In practice
    # this does not seem to be the case. Maybe the reason is the small angle problem in
    # the Fourier transform. Also note that we do addition in Fourier space (which might
    # worsen the problem).

    # The order is r = 2, so s/r in {0, 0.5}
    (3, 8, ('00000000', '10000000')),
    # The order is r = 4, so s/r in {0, 0.25, 0.5, 0.75}:
    (7, 15, ('0000000000', '0100000000', '1000000000', '1100000000')),
})
def test_phase_estimation(a, modulus, maximizing_bits):
    # Setting eps=1.0 is theoretically justified since the fractions are exactly
    # representable in binary. So setting it to a smaller value won't help (at least this
    # is not backed by the analysis from the book).
    qc = make_order_finding_phase_estimation(a, modulus, eps=1.0)

    sim = AerSimulator()
    qc_obj = transpile(qc, sim)
    counts = sim.run(qc_obj).result().get_counts()

    num = len(maximizing_bits)
    result = get_maximizing_keys(counts, num)

    assert result == maximizing_bits


@pytest.mark.parametrize("N, base, offset, exponent, expected", {
    (7, 2, 0, 1, 2),
    (8, 2, 0, 1, 3),
    (100, 2, 90, 1, 3),
    (1024, 2, 512, 1, 9),
    (1023, 2, 512, 1, 8),
    (1024, 2, 16, 2, 4),
    (1023, 2, 16, 2, 3),
    (1000, 3, 1, 3, 2),
    (999, 3, 1, 3, 1),
})
def test_intlogx(N, base, offset, exponent, expected):
    assert intlogx(N, base, offset, exponent) == expected


@pytest.mark.parametrize("N", {
    # These numbers are *probably* all prime (https://bigprimes.org/):
    7,
    17,
    87803,
    63677916755048130433,
    3653830433690631231215033779172394321457504060347295936059433436653593414026691052633975151578907267,
    # Roughly 1000 bits:
    694132660957031113047665284378532956251732011797289589969556436434735219310464570922895568634461408873887848260360545569006450572256819756449202403712996238839577863592506729956934258640602885447906264615930253012437897772899559071819968673582797974093477640282435584546082331225516832102340474835529,
    # Products of two primes:
    2341121591 * 3536648897,
    33318506043084601978901983513127189439078469098941 * 57666386236412678991478313909997305232366971065901,
    # Roughly 1000 bits:
    267235751626887712762234547639051825020255990491073909324282238093658784919122126843094712258943571265478372330167756989106909834248894847222757028093 * 442119851295683804328228639966196873910083006543457611240362529682859193457180901378680312821415860447501430305027501449183718893689426744660311637941,
})
def test_is_power_negative(N):
    assert is_power(N) is None


@pytest.mark.parametrize("a,b", {
    # In all cases a**b is roughly a 1000 bit number
    (2, 1000),
    (5, 431),
    (29, 207),
    (5441, 83),
    (1576052117, 37),
    (7513950727, 31),
    (173566555901126500012468354357, 13),
})
def test_is_power_positive(a, b):
    x, k = is_power(a ** b)
    assert x ** k == a ** b


@pytest.mark.parametrize("N,factor", {
    # special case: even numbers
    (2, 2),
    (8, 2),
    (10385820, 2),
    # powers:
    (3**17, 3),
    (5**9, 5),
    (19**3, 19),
})
def test_find_factor_trivial_cases(N, factor):
    # sometimes find_factor finds a larger factor:
    assert find_factor(N) % factor == 0


@pytest.mark.slow
@pytest.mark.parametrize("N,factors,cheat_code", {
    # The cheat_code guarantees that we only have to run the circuit once
    (15, (3, 5), 7),  # smallest possible non-trivial case (already takes long)
})
def test_find_factor_non_trivial_cases(N, factors, cheat_code):
    assert find_factor(N, randrange=lambda *_: cheat_code) in factors
