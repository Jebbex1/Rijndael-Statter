import numpy as np
from rijndael_statter import Block, get_ordered_block


def test_repr_compiling() -> None:
    b = get_ordered_block()
    b.xy_layered_repr()
    b.xz_layered_repr()
    b.yz_layered_repr()


def test_circular_shift_rows() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_byte_block(b)

    assert np.all(np.equal(b, b_start_copy))

    b.shift_rows()
    assert np.any(np.not_equal(b, b_start_copy))

    b.inverse_shift_rows()
    assert np.all(np.equal(b, b_start_copy))


def test_circular_rotate_elements() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_byte_block(b)

    assert np.all(np.equal(b, b_start_copy))

    b.rotate_elements()
    assert np.any(np.not_equal(b, b_start_copy))

    b.inverse_rotate_elements()
    assert np.all(np.equal(b, b_start_copy))


def test_circular_spin_rings() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_byte_block(b)

    assert np.all(np.equal(b, b_start_copy))

    b.spin_rings()
    assert np.any(np.not_equal(b, b_start_copy))

    b.inverse_spin_rings()
    assert np.all(np.equal(b, b_start_copy))


def test_circular_sub_bytes() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_byte_block(b)

    assert np.all(np.equal(b, b_start_copy))

    b.sub_bytes()
    assert np.any(np.not_equal(b, b_start_copy))

    b.inverse_sub_bytes()
    assert np.all(np.equal(b, b_start_copy))


def test_circular_mix_xy_columns() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_byte_block(b)

    assert np.all(np.equal(b, b_start_copy))

    b.mix_xy_columns()
    assert np.any(np.not_equal(b, b_start_copy))

    b.inverse_mix_xy_columns()
    assert np.all(np.equal(b, b_start_copy))



def test_circular_mix_xz_columns() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_byte_block(b)

    assert np.all(np.equal(b, b_start_copy))

    b.mix_xz_columns()
    assert np.any(np.not_equal(b, b_start_copy))

    b.inverse_mix_xz_columns()
    assert np.all(np.equal(b, b_start_copy))



def test_circular_mix_yz_columns() -> None:
    b = get_ordered_block()
    b_start_copy = Block.from_byte_block(b)

    assert np.all(np.equal(b, b_start_copy))

    b.mix_yz_columns()
    assert np.any(np.not_equal(b, b_start_copy))

    b.inverse_mix_yz_columns()
    assert np.all(np.equal(b, b_start_copy))
