from sage.all import matrix, i, sqrt

from utils_sage import Id, X, Y, Z, H, S, P0, P1, CX, CY, CZ, kron, sgn, delta, eps, inner


def test_pauli_matrices():
    # Basic algebraic identities:
    assert Id == matrix.identity(2)
    assert Z == matrix.diagonal([1, -1])

    assert H.H == H
    assert H*H == Id
    assert H == (X + Z) / sqrt(2)
    assert X == H*Z*H

    assert X**2 == Y**2 == Z**2 == -i*X*Y*Z == Id


def test_phase_gate():
    assert S**2 == Z
    assert S * X * S.H == Y


def test_projections():
    assert P0 == matrix([[1, 0], [0, 0]])
    assert P1 == matrix([[0, 0], [0, 1]])


def test_controlled_paulis():
    assert CZ == matrix.diagonal([1, 1, 1, -1])
    assert CX == kron(Id, H) * CZ * kron(Id, H)
    assert CY == kron(Id, S) * CX * kron(Id, S.H)


def test_kronecker_delta():
    assert delta(0, 0) == 1
    assert delta(1, 1) == 1
    assert delta(1, 0) == 0
    assert delta(0, 1) == 0


def test_levi_civita():
    assert eps(0, 1, 2) == 1
    assert eps(2, 0, 1) == 1
    assert eps(1, 2, 0) == 1

    assert eps(0, 2, 1) == -1
    assert eps(1, 0, 2) == -1
    assert eps(2, 1, 0) == -1

    assert eps(0, 0, 0) == 0
    assert eps(1, 1, 1) == 0
    assert eps(2, 2, 2) == 0

    assert eps(1, 0, 0) == 0
    assert eps(0, 1, 0) == 0
    assert eps(0, 0, 1) == 0

    assert eps(2, 0, 0) == 0
    assert eps(0, 2, 0) == 0
    assert eps(0, 0, 2) == 0

    assert eps(0, 1, 1) == 0
    assert eps(1, 0, 1) == 0
    assert eps(1, 1, 0) == 0

    assert eps(2, 1, 1) == 0
    assert eps(1, 2, 1) == 0
    assert eps(1, 1, 2) == 0

    assert eps(0, 2, 2) == 0
    assert eps(2, 0, 2) == 0
    assert eps(2, 2, 0) == 0

    assert eps(1, 2, 2) == 0
    assert eps(2, 1, 2) == 0
    assert eps(2, 2, 1) == 0


def test_sgn():
    assert sgn(0) == 0
    assert sgn(6) == 1
    assert sgn(-3) == -1


def test_inner():
    assert inner(X, X) == 2
    assert inner(X + Y, Z) == 0
    assert inner(X + 2*Z + 3*Id, 5*X + 100*Y + Z + 3*Id) == 32
