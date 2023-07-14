from sage.all import matrix, i

from utils_sage import Id, X, Y, Z, H


def test_pauli_matrices():
    # Basic algebraic identities:
    assert Id == matrix.identity(2)
    assert X**2 == Y**2 == Z**2 == -i*X*Y*Z == Id
    assert H.H == H
    assert H*X*H == Z
