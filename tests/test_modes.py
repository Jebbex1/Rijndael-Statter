import random
from rijndael3d.modes.ecb import ecb_encrypt, ecb_decrypt
from rijndael3d.modes.cbc import cbc_encrypt, cbc_decrypt
from rijndael3d.modes.ctr import ctr_encrypt, ctr_decrypt


def test_circular_ecb() -> None:
    key = random.randbytes(64)
    plaintext = random.randbytes(256)
    
    encrypted = ecb_encrypt(plaintext, key)
    assert len(encrypted) >= len(plaintext)
    
    decrypted = ecb_decrypt(encrypted, key)
    
    assert plaintext == decrypted


def test_circular_cbc() -> None:
    key = random.randbytes(64)
    plaintext = random.randbytes(256)
    iv = random.randbytes(64)
    
    encrypted = cbc_encrypt(plaintext, key, iv)
    assert len(encrypted) >= len(plaintext)
    
    decrypted = cbc_decrypt(encrypted, key, iv)
    
    assert plaintext == decrypted


def test_circular_ctr() -> None:
    key = random.randbytes(64)
    plaintext = random.randbytes(256)
    iv = random.randint(0, 2**512-1).to_bytes(64)
    
    encrypted = ctr_encrypt(plaintext, key, iv)
    assert len(encrypted) >= len(plaintext)
    
    decrypted = ctr_decrypt(encrypted, key, iv)
    
    assert plaintext == decrypted
    