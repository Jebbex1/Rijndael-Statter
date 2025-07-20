import numpy as np
import random
from r3d.block import get_ordered_block, sub_bytes, shift_rows, mix_xy_columns, rotate_elements, \
    mix_yz_columns, add_round_key, inverse_mix_xy_columns, inverse_mix_xz_columns, inverse_mix_yz_columns, \
    inverse_rotate_elements, inverse_shift_rows, inverse_spin_rings, inverse_sub_bytes, mix_xz_columns, \
    xy_layered_repr, xz_layered_repr, yz_layered_repr, block_from_bytes, export_to_bytes, spin_rings
from r3d.cipher import perform_round, perform_inverse_round


def test_repr_compiling() -> None:
    b = get_ordered_block()
    xy_layered_repr(b)
    xz_layered_repr(b)
    yz_layered_repr(b)


def test_circular_shift_rows() -> None:
    b = get_ordered_block()
    b_start_copy = b.copy()

    assert export_to_bytes(b) == export_to_bytes(b_start_copy)

    shift_rows(b)
    assert export_to_bytes(b) != export_to_bytes(b_start_copy)

    inverse_shift_rows(b)
    assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_circular_rotate_elements() -> None:
    b = get_ordered_block()
    b_start_copy = b.copy()

    assert export_to_bytes(b) == export_to_bytes(b_start_copy)

    rotate_elements(b)
    assert export_to_bytes(b) != export_to_bytes(b_start_copy)

    inverse_rotate_elements(b)
    assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_circular_spin_rings() -> None:
    b = get_ordered_block()
    b_start_copy = b.copy()

    assert export_to_bytes(b) == export_to_bytes(b_start_copy)

    spin_rings(b)
    assert export_to_bytes(b) != export_to_bytes(b_start_copy)

    inverse_spin_rings(b)
    assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_circular_sub_bytes() -> None:
    b = get_ordered_block()
    b_start_copy = b.copy()

    assert export_to_bytes(b) == export_to_bytes(b_start_copy)

    sub_bytes(b)
    assert export_to_bytes(b) != export_to_bytes(b_start_copy)

    inverse_sub_bytes(b)
    assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_circular_mix_xy_columns() -> None:
    b = get_ordered_block()
    b_start_copy = b.copy()

    assert export_to_bytes(b) == export_to_bytes(b_start_copy)

    mix_xy_columns(b)
    assert export_to_bytes(b) != export_to_bytes(b_start_copy)

    inverse_mix_xy_columns(b)
    assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_circular_mix_xz_columns() -> None:
    b = get_ordered_block()
    b_start_copy = b.copy()

    assert export_to_bytes(b) == export_to_bytes(b_start_copy)

    mix_xz_columns(b)
    assert export_to_bytes(b) != export_to_bytes(b_start_copy)

    inverse_mix_xz_columns(b)
    assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_circular_mix_yz_columns() -> None:
    b = get_ordered_block()
    b_start_copy = b.copy()

    assert export_to_bytes(b) == export_to_bytes(b_start_copy)

    mix_yz_columns(b)
    assert export_to_bytes(b) != export_to_bytes(b_start_copy)

    inverse_mix_yz_columns(b)
    assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_add_round_key():
    for _ in range(64):
        b = get_ordered_block()
        test_key = np.asarray([random.randint(0, 255) for _ in range(64)], dtype=np.uint8).reshape((4, 4, 4))
        
        add_round_key(b, test_key)
        
        for location, value in np.ndenumerate(b):
            assert value == b[location]


def test_circular_perform_round() -> None:
    for _ in range(64):
        b = get_ordered_block()
        b_start_copy = b.copy()
        test_key = np.asarray([random.randint(0, 255) for _ in range(64)], dtype=np.uint8).reshape((4, 4, 4))

        assert export_to_bytes(b) == export_to_bytes(b_start_copy)

        perform_round(b, test_key)
        assert export_to_bytes(b) != export_to_bytes(b_start_copy)

        perform_inverse_round(b, test_key)
        assert export_to_bytes(b) == export_to_bytes(b_start_copy)
