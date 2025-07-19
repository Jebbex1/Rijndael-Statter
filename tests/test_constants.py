import numpy as np
from r3d.constants import XY_MULT_MATRIX, INVERSE_XY_MULT_MATRIX, XZ_MULT_MATRIX, \
    INVERSE_XZ_MULT_MATRIX, YZ_MULT_MATRIX, INVERSE_YZ_MULT_MATRIX, S_BOX, INVERSE_S_BOX
from r3d.gf_arithmetic import multiply_mats


IDENTITY_MATRIX: np.ndarray = np.asarray(
    (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    ),
    dtype=np.uint8
)


def test_xy_mult_matrices() -> None:
    assert np.all(np.equal(IDENTITY_MATRIX, multiply_mats(XY_MULT_MATRIX, INVERSE_XY_MULT_MATRIX)))


def test_xz_mult_matrices() -> None:
    assert np.all(np.equal(IDENTITY_MATRIX, multiply_mats(XZ_MULT_MATRIX, INVERSE_XZ_MULT_MATRIX)))


def test_yz_mult_matrices() -> None:
    assert np.all(np.equal(IDENTITY_MATRIX, multiply_mats(YZ_MULT_MATRIX, INVERSE_YZ_MULT_MATRIX)))


def test_s_boxes() -> None:
    for location, value in np.ndenumerate(S_BOX):
        assert INVERSE_S_BOX[value] == location[0]