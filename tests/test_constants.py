import numpy as np
from galois import FieldArray
from rijndael_statter import EXTENTION_FIELD, XY_MULT_MATRIX, INVERSE_XY_MULT_MATRIX, XZ_MULT_MATRIX, \
    INVERSE_XZ_MULT_MATRIX, YZ_MULT_MATRIX, INVERSE_YZ_MULT_MATRIX, S_BOX, INVERSE_S_BOX


IDENTITY_MATRIX: FieldArray = EXTENTION_FIELD(
    (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
)

def test_xy_mult_matracies() -> None:
    assert np.all(np.equal(IDENTITY_MATRIX, XY_MULT_MATRIX @ INVERSE_XY_MULT_MATRIX))


def test_xz_mult_matracies() -> None:
    assert np.all(np.equal(IDENTITY_MATRIX, XZ_MULT_MATRIX @ INVERSE_XZ_MULT_MATRIX))


def test_yz_mult_matracies() -> None:
    assert np.all(np.equal(IDENTITY_MATRIX, YZ_MULT_MATRIX @ INVERSE_YZ_MULT_MATRIX))


def test_s_boxes() -> None:
    for location, value in np.ndenumerate(S_BOX):
        assert INVERSE_S_BOX[value] == location[0]