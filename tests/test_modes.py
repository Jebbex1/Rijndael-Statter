import random
from rijndael3d.modes.ecb import ecb_encrypt, ecb_decrypt
from rijndael3d.modes.cbc import cbc_encrypt, cbc_decrypt
from rijndael3d.modes.ctr import ctr_encrypt, ctr_decrypt
from rijndael3d.modes.gcm import gcm_encrypt, gcm_decrypt
from rijndael3d.utils     import xor_bytes


def test_circular_ecb() -> None:
    key = random.randbytes(64)
    plaintext = random.randbytes(256)
    
    encrypted = ecb_encrypt(plaintext, key)    
    decrypted = ecb_decrypt(encrypted, key)
    
    assert plaintext == decrypted


def test_circular_cbc() -> None:
    key = random.randbytes(64)
    plaintext = random.randbytes(256)
    iv = random.randbytes(64)
    
    encrypted = cbc_encrypt(plaintext, key, iv)    
    decrypted = cbc_decrypt(encrypted, key, iv)
    
    assert plaintext == decrypted


def test_circular_ctr() -> None:
    key = random.randbytes(64)
    plaintext = random.randbytes(256)
    iv = random.randint(0, 2**512-1).to_bytes(64)
    
    encrypted = ctr_encrypt(plaintext, key, iv)    
    decrypted = ctr_decrypt(encrypted, key, iv)
    
    assert plaintext == decrypted
    
    
def test_circular_gcm() -> None:
    key = random.randbytes(64)
    plaintext = random.randbytes(256)
    iv = random.randint(0, 2**512-1).to_bytes(64)
    aad = random.randbytes(400)
    
    encrypted, tag = gcm_encrypt(plaintext, key, iv, aad)   
     
    # Normal case of decryption where nothing was changed
    try:
        decrypted = gcm_decrypt(encrypted, key, iv, tag, aad)
    except ValueError:
        raise AssertionError("GCM failed tag check where no data was changed.")  
      
    assert plaintext == decrypted
    

def test_gcm_auth() -> None:
    key = random.randbytes(64)
    plaintext = random.randbytes(256)
    iv = random.randint(0, 2**512-1).to_bytes(64)
    aad = random.randbytes(400)
    
    encrypted, tag = gcm_encrypt(plaintext, key, iv, aad)
    
    # Changed ciphertext
    try:
        # Flip the last bit
        gcm_decrypt(encrypted[:-1]+(1^encrypted[-1]).to_bytes(1), key, iv, tag, aad)
    except ValueError:
        pass  # should have been raised - test successful
    else:
        raise AssertionError("GCM succeeded tag check where ciphertext was changed.")

    # Changed iv
    try:
        # Flip the last bit
        gcm_decrypt(encrypted, key, iv[:-1]+(1^iv[-1]).to_bytes(1), tag, aad)
    except ValueError:
        pass  # should have been raised - test successful
    else:
        raise AssertionError("GCM succeeded tag check where iv was changed.")

    # Changed tag
    try:
        # Flip the last bit
        gcm_decrypt(encrypted, key, iv, tag[:-1]+(1^tag[-1]).to_bytes(1), aad)
    except ValueError:
        pass  # should have been raised - test successful
    else:
        raise AssertionError("GCM succeeded tag check where tag was changed.")

    # Changed aad
    try:
        # Flip the last bit
        gcm_decrypt(encrypted, key, iv, tag, aad[:-1]+(1^aad[-1]).to_bytes(1))
    except ValueError:
        pass  # should have been raised - test successful
    else:
        raise AssertionError("GCM succeeded tag check where aad was changed.")

    # Changed key
    try:
        # Flip the last bit
        gcm_decrypt(encrypted, key[:-1]+(1^key[-1]).to_bytes(1), iv, tag, aad)
    except ValueError:
        pass  # should have been raised - test successful
    else:
        raise AssertionError("GCM succeeded tag check where key was changed.")
