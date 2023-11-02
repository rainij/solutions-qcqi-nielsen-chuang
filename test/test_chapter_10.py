from qiskit.quantum_info import Pauli

from chapter_10 import compute_syndromes


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
