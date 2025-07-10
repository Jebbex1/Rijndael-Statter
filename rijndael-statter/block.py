import numpy as np
from galois import GF, Poly


PRIME_FIELD = GF(2)        # finite field for the coefficients of every polynomial
EXTENTION_FIELD = GF(2**8) # finite field for the irreducible polynomial


class Block:
    def __init__(self, source_bytes: bytes) -> None:
        if not len(source_bytes) == 64:
            raise ValueError(f"Blocks are of length 64 bytes (512 bits) only, supplied length of {len(source_bytes)}")
        
        self.poly_block = np.ndarray(dtype=Poly, shape=(64, 1, 1))

        for i in range(64):
            self.poly_block[i] = Poly.Int(source_bytes[i], PRIME_FIELD)
        
        self.poly_block = self.poly_block.reshape((4, 4, 4))


    @classmethod
    def from_poly_block(cls, poly_block: np.ndarray):
        obj = object.__new__(cls)
        obj.poly_block = np.copy(poly_block)
        return obj
    

    def __str__(self) -> str:
        return self.poly_block.__str__()
    

    def __add__(self, b: 'Block'):
        return Block.from_poly_block(self.poly_block + b.poly_block)
