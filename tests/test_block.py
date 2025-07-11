from rijndael_statter import Block, get_ordered_block, PRIME_FIELD, EXTENTION_FIELD
import numpy as np


def test_circular_shift_rows() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_poly_block(b.poly_block)

    assert np.all(np.equal(b.poly_block, b_start_copy.poly_block))

    b.shift_rows()
    assert np.any(np.not_equal(b.poly_block, b_start_copy.poly_block))

    b.inverse_shift_rows()
    assert np.all(np.equal(b.poly_block, b_start_copy.poly_block))


def test_circular_rotate_elements() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_poly_block(b.poly_block)

    assert np.all(np.equal(b.poly_block, b_start_copy.poly_block))

    b.rotate_elements()
    assert np.any(np.not_equal(b.poly_block, b_start_copy.poly_block))

    b.inverse_rotate_elements()
    assert np.all(np.equal(b.poly_block, b_start_copy.poly_block))


def test_circular_spin_rings() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_poly_block(b.poly_block)

    assert np.all(np.equal(b.poly_block, b_start_copy.poly_block))

    b.spin_rings()
    assert np.any(np.not_equal(b.poly_block, b_start_copy.poly_block))

    b.inverse_spin_rings()
    assert np.all(np.equal(b.poly_block, b_start_copy.poly_block))