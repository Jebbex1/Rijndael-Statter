import random
from r3d.modes.ecb import ecb_encrypt, ecb_decrypt
from r3d.modes.cbc import cbc_encrypt, cbc_decrypt


def test_circular_ecb() -> None:
    test_key = random.randbytes(64)
    test_plaintext = random.randbytes(246)
    
    encrypted = ecb_encrypt(test_plaintext, test_key)
    assert len(encrypted) >= len(test_plaintext)
    
    decrypted = ecb_decrypt(encrypted, test_key)
    
    assert test_plaintext == decrypted


def test_circular_cbc() -> None:
    test_key = random.randbytes(64)
    test_plaintext = random.randbytes(259)
    
    encrypted = cbc_encrypt(test_plaintext, test_key)
    assert len(encrypted) >= len(test_plaintext)
    
    decrypted = cbc_decrypt(encrypted, test_key)
    
    assert test_plaintext == decrypted
    