import pytest

from qiskit import transpile
from qiskit_aer import AerSimulator

from chapter_5 import quantum_add, make_order_finding_phase_estimation



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


def get_maximizing_bits(counts: dict[str, int], num: int) -> tuple[str]:
    result = sorted(counts.items(), key=lambda a: a[1], reverse=True)[:num]
    result = [a[0] for a in result]
    return tuple(sorted(result))


@pytest.mark.slow
@pytest.mark.parametrize("a,modulus,maximizing_bits", {
    (3, 8, ('00000000', '10000000')),  # the order is r = 2, so s/r in {0, 0.5}
})
def test_phase_estimation(a, modulus, maximizing_bits):
    qc = make_order_finding_phase_estimation(a, modulus, eps=0.5)

    sim = AerSimulator()
    qc_obj = transpile(qc, sim)
    counts = sim.run(qc_obj).result().get_counts()

    num = len(maximizing_bits)
    result = get_maximizing_bits(counts, num)

    assert result == maximizing_bits
