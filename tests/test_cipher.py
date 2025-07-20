import numpy as np
import random
from r3d.cipher import perform_round, perform_inverse_round, encrypt_block, decrypt_block
from r3d.block import get_ordered_block, export_to_bytes


def test_circular_perform_round() -> None:
    for _ in range(100):
        b = get_ordered_block()
        b_start_copy = b.copy()
        test_key = np.asarray([random.randint(0, 255) for _ in range(64)], dtype=np.uint8).reshape((4, 4, 4))

        assert export_to_bytes(b) == export_to_bytes(b_start_copy)

        perform_round(b, test_key)
        assert export_to_bytes(b) != export_to_bytes(b_start_copy)

        perform_inverse_round(b, test_key)
        assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_circular_block_encryption() -> None:
    test_key = b"".join([random.randint(0, 255).to_bytes(1) for _ in range(64)])
    plaintext = b"".join([random.randint(0, 255).to_bytes(1) for _ in range(64)])

    ciphertext = encrypt_block(plaintext, test_key)

    decrypted_ciphertext = decrypt_block(ciphertext, test_key)
    assert decrypted_ciphertext == plaintext
