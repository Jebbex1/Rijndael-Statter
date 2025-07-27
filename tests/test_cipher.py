import numpy as np
import random
from rijndael3d.cipher import perform_round, perform_inverse_round, encrypt_block, decrypt_block
from rijndael3d.block import export_to_bytes
from rijndael3d.debug_operations import get_random_block


def test_circular_perform_round() -> None:
    b = get_random_block()
    b_start_copy = b.copy()
    key = np.asarray([random.randint(0, 255) for _ in range(64)], dtype=np.uint8).reshape((4, 4, 4))

    perform_round(b, key)
    perform_inverse_round(b, key)
    
    assert export_to_bytes(b) == export_to_bytes(b_start_copy)


def test_circular_block_encryption() -> None:
    key = b"".join([random.randint(0, 255).to_bytes(1) for _ in range(64)])
    plaintext = b"".join([random.randint(0, 255).to_bytes(1) for _ in range(64)])

    ciphertext = encrypt_block(plaintext, key)

    decrypted_ciphertext = decrypt_block(ciphertext, key)
    assert decrypted_ciphertext == plaintext
