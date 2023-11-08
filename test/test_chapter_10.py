from qiskit.quantum_info import Pauli

from chapter_10 import compute_syndromes
from chapter_10_sage import transform_check_matrix, generators_to_check_matrix, \
    generators_steane_code_repr, generators_steane_code_standard_repr


def test_compute_syndromes():
    # Five qubit code:
    g1 = Pauli("XZZXI")
    g2 = Pauli("IXZZX")
    g3 = Pauli("XIXZZ")
    g4 = Pauli("ZXIXZ")

    generators = [g1, g2, g3, g4]

    syndromes = compute_syndromes(generators)

    assert syndromes == {
        "XIIII": "0001",
        "IIZII": "0010",
        "IIIIX": "0011",
        "IIIIZ": "0100",
        "IZIII": "0101",
        "IIIXI": "0110",
        "IIIIY": "0111",
        "IXIII": "1000",
        "IIIZI": "1001",
        "ZIIII": "1010",
        "YIIII": "1011",
        "IIXII": "1100",
        "IYIII": "1101",
        "IIYII": "1110",
        "IIIYI": "1111",
    }


def test_transform_check_matrix():
    cm = generators_to_check_matrix(generators_steane_code_repr())
    cm1 = transform_check_matrix(cm, [
        # procedure according to book:
        ["swap qubits", 0, 3],
        ["swap qubits", 2, 3],
        ["swap qubits", 5, 6],
        ["add row", 5, 3], # target, source
        ["add row", 5, 4],
        ["add row", 3, 5],
        ["add row", 4, 5],
    ])

    assert cm1 == generators_to_check_matrix(generators_steane_code_standard_repr())
