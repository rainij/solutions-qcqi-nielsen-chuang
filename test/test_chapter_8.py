from sage.all import SR, sqrt, matrix, vector

from utils_sage import Id, X, Y, Z, P0
from chapter_8_sage import p, g, affine, toPauli, make_qop1d_matrix_4d, op835, rho_prime_835, chi_835, chi_835_2


def test_toPauli():
    assert toPauli(Id) == [1, 0, 0, 0]
    assert toPauli(X)  == [0, 1, 0, 0]
    assert toPauli(Y)  == [0, 0, 1, 0]
    assert toPauli(Z)  == [0, 0, 0, 1]

    assert toPauli(X+2*Y+3*Z) == [0, 1, 2, 3]


def test_affine_bitflip():
    E0 = sqrt(p) * Id
    E1 = sqrt(1-p) * X

    M, c = affine(*[toPauli(E) for E in [E0, E1]])

    assert M == matrix.diagonal([1, 2*p-1, 2*p-1])
    assert c == vector([0, 0, 0])

    # Represantation as linear map RR^4 to RR^4:
    M4 = make_qop1d_matrix_4d([E0, E1])
    assert M4 == matrix.diagonal([1, 1, 2*p-1, 2*p-1])


def test_affine_amplitude_damping():
    E0 = matrix.diagonal([1, sqrt(1-g)])
    E1 = matrix([[0, sqrt(g)], [0, 0]])

    M, c = affine(*[toPauli(E) for E in [E0, E1]])
    M = M.expand()

    assert M == matrix.diagonal([sqrt(1-g), sqrt(1-g), 1-g])
    assert c == vector([0, 0, g])

    # Represantation as linear map RR^4 to RR^4:
    M4 = make_qop1d_matrix_4d([E0, E1])
    assert M4 == matrix([
        [1,         0,         0,   0],
        [0, sqrt(1-g),         0,   0],
        [0,         0, sqrt(1-g),   0],
        [g,         0,         0, 1-g],
    ])


def test_exercise_835():
    rho = [P0, P0*X, X*P0, X*P0*X]
    assert op835(rho[0]) == rho_prime_835[0]
    assert op835(rho[1]) == rho_prime_835[1]
    assert op835(rho[2]) == rho_prime_835[2]
    assert op835(rho[3]) == rho_prime_835[3]

    assert chi_835 == chi_835_2
