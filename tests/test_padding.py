import random
from rijndael3d.padding import generate_suffix, pad, unpad


def test_generate_suffix() -> None:
    test_key = random.randbytes(64)
    
    suffix = generate_suffix(random.randint(1, 64), test_key)
    assert suffix.rfind(b"\x00") == 0


def test_circular_padding() -> None:
    test_key = random.randbytes(64)

    # normal case
    test_plaintext = random.randbytes(70)
    padded = pad(test_plaintext, test_key)
    assert padded.rfind(b"\x00") >= len(padded)-64
    assert test_plaintext == unpad(padded)
    
    # edge case where the block length is already a 64 multiple
    test_plaintext = random.randbytes(64)
    padded = pad(test_plaintext, test_key)
    assert padded.rfind(b"\x00") >= len(padded)-64
    assert test_plaintext == unpad(padded)
