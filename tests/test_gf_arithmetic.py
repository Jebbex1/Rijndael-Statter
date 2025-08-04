from galois import Poly, FieldArray, GF
import random
import numpy as np
from rijndael3d.gf_arithmetic import gf_multiply, multiply_mats, gf_2_512_multiply_bytes
    

WORKING_FIELD = GF(2**8)
GCM_FIELD =     GF(2**512, irreducible_poly=((1 << 512) | (1 << 8) | (1 << 5) | (1 << 2) | 1))


IDENTITY_MATRIX: FieldArray = WORKING_FIELD(
    (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
)


MAT1: FieldArray = WORKING_FIELD(
    (
        (2, 3, 1, 1),
        (1, 2, 3, 1),
        (1, 1, 2, 3),
        (3, 1, 1, 2),
    )
)


INVERSE_MAT1: FieldArray = WORKING_FIELD(
    (
        (14, 11, 13,  9),
        ( 9, 14, 11, 13),
        (13,  9, 14, 11),
        (11, 13,  9, 14),
    )
)


def test_gf_multiply() -> None:
    for _ in range(64):
        r1 = random.randint(0, 255)
        r2 = random.randint(0, 255)
        out1 = gf_multiply(r1, r2)
        out2 = (Poly.Int(r1, WORKING_FIELD) * Poly.Int(r2, WORKING_FIELD))
        assert out1 == out2


def test_gf_2_512_multiply_bytes() -> None:
    for _ in range(64):
        r1 = random.randint(0, (2**512)-1)
        r2 = random.randint(0, (2**512)-1)
        out1 = int.from_bytes(gf_2_512_multiply_bytes(r1.to_bytes(64), r2.to_bytes(64)))
        out2 = (Poly.Int(r1, GCM_FIELD) * Poly.Int(r2, GCM_FIELD))
        assert out1 == out2


def test_multiply_mats() -> None:
    assert np.all(np.equal(IDENTITY_MATRIX, multiply_mats(MAT1, INVERSE_MAT1)))
