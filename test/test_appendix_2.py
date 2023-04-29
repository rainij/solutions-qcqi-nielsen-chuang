from sympy import eye

from appendix_2 import U_std, s3_perm, s3_std


def test_exercise_A2_17():
    """Test that U_std converts permutation representation into standard representation."""
    assert U_std.H * U_std == eye(3)
    assert len(s3_perm) == len(s3_std) == 6

    for i in range(6):
        print(i)
        G = U_std.H * s3_perm[i] * U_std
        G.col_del(0)
        G.row_del(0)

        assert G == s3_std[i]
