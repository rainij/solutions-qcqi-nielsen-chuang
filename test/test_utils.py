from sage.all import matrix, i, sqrt

from utils_sage import Id, X, Y, Z, H, S, P0, P1, CX, CY, CZ, kron


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
