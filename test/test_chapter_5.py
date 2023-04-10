import pytest

from chapter_5 import quantum_add


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
