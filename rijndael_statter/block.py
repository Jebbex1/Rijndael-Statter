import numpy as np
from galois import GF, Poly


PRIME_FIELD = GF(2)        # finite field for the coefficients of every polynomial
EXTENTION_FIELD = GF(2**8) # finite field for the irreducible polynomial


def get_ordered_block() -> 'Block':
    return Block(b"".join(i.to_bytes(1) for i in range(64)))


class Block:
    def __init__(self, source_bytes: bytes) -> None:
        if not len(source_bytes) == 64:
            raise ValueError(f"Blocks are of length 64 bytes (512 bits) only, supplied length of {len(source_bytes)}")
        
        self.poly_block = np.ndarray(dtype=Poly, shape=(64, 1, 1))

        for i in range(64):
            self.poly_block[i] = Poly.Int(source_bytes[i], PRIME_FIELD)
        
        self.poly_block = self.poly_block.reshape((4, 4, 4))


    @classmethod
    def from_poly_block(cls, poly_block: np.ndarray) -> 'Block':
        obj = object.__new__(cls)
        obj.poly_block = np.copy(poly_block)
        return obj


    def __str__(self) -> str:
        return self.poly_block.__str__()
    

    def __add__(self, b: 'Block') -> 'Block':
        return Block.from_poly_block(self.poly_block + b.poly_block)
    

    def xy_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, poly in np.ndenumerate(self.poly_block):
            # loc for location, in format x,y,z
            int_block[loc[2]][loc[0]][loc[1]] = poly._integer  # convert to to view layers in the wanted plane 
        return int_block.__str__()


    def xz_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, poly in np.ndenumerate(self.poly_block):
            # loc for location, in format x,y,z
            int_block[loc[1]][loc[0]][loc[2]] = poly._integer  # convert to to view layers in the wanted plane
        return int_block.__str__()


    def yz_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, poly in np.ndenumerate(self.poly_block):
            # loc for location, in format x,y,z
            int_block[loc] = poly._integer  # convert to to view layers in the wanted plane 
        return int_block.__str__()


    def shift_rows(self) -> None:  # XY layer permutation
        p_block = self.poly_block
        for z in range(0, 4):
            p_block[1][0][z], p_block[1][1][z], p_block[1][2][z], p_block[1][3][z] = \
                p_block[1][1][z], p_block[1][2][z], p_block[1][3][z], p_block[1][0][z]  # row 2
            p_block[2][0][z], p_block[2][1][z], p_block[2][2][z], p_block[2][3][z] = \
                p_block[2][2][z], p_block[2][3][z], p_block[2][0][z], p_block[2][1][z]  # row 3
            p_block[3][0][z], p_block[3][1][z], p_block[3][2][z], p_block[3][3][z] = \
                p_block[3][3][z], p_block[3][0][z], p_block[3][1][z], p_block[3][2][z]  # row 4
    

    def inverse_shift_rows(self) -> None:  # XY layer permutation
        p_block = self.poly_block
        for z in range(0, 4):
            p_block[1][0][z], p_block[1][1][z], p_block[1][2][z], p_block[1][3][z] = \
                p_block[1][3][z], p_block[1][0][z], p_block[1][1][z], p_block[1][2][z]  # row 2
            p_block[2][0][z], p_block[2][1][z], p_block[2][2][z], p_block[2][3][z] = \
                p_block[2][2][z], p_block[2][3][z], p_block[2][0][z], p_block[2][1][z]  # row 3
            p_block[3][0][z], p_block[3][1][z], p_block[3][2][z], p_block[3][3][z] = \
                p_block[3][1][z], p_block[3][2][z], p_block[3][3][z], p_block[3][0][z]  # row 4


    def rotate_elements(self) -> None:  # XZ layer permumtation
        p_block = self.poly_block
        for y in range(0, 4):
            p_block[0][y][1], p_block[0][y][3], p_block[2][y][3], p_block[2][y][1] = \
                p_block[2][y][1], p_block[0][y][1], p_block[0][y][3], p_block[2][y][3]  # group 2
            p_block[1][y][1], p_block[1][y][3], p_block[3][y][3], p_block[3][y][1] = \
                p_block[3][y][3], p_block[3][y][1], p_block[1][y][1], p_block[1][y][3]  # group 3
            p_block[1][y][0], p_block[1][y][2], p_block[3][y][2], p_block[3][y][0] = \
                p_block[1][y][2], p_block[3][y][2], p_block[3][y][0], p_block[1][y][0]  # group 4
    

    def inverse_rotate_elements(self) -> None:  # XZ layer permutation
        p_block = self.poly_block
        for y in range(0, 4):
            p_block[0][y][1], p_block[0][y][3], p_block[2][y][3], p_block[2][y][1] = \
                p_block[0][y][3], p_block[2][y][3], p_block[2][y][1], p_block[0][y][1]  # group 2
            p_block[1][y][1], p_block[1][y][3], p_block[3][y][3], p_block[3][y][1] = \
                p_block[3][y][3], p_block[3][y][1], p_block[1][y][1], p_block[1][y][3]  # group 3
            p_block[1][y][0], p_block[1][y][2], p_block[3][y][2], p_block[3][y][0] = \
                p_block[3][y][0], p_block[1][y][0], p_block[1][y][2], p_block[3][y][2]  # group 4
    

    def spin_rings(self) -> None:  # YZ layer permutation
        p_block = self.poly_block
        for x in range(0, 4):
            p_block[x][1][2], p_block[x][2][1] = p_block[x][2][1], p_block[x][1][2]  # ring 2
            p_block[x][1][1], p_block[x][2][2] = p_block[x][2][2], p_block[x][1][1]  # ring 3
            p_block[x][0][0], p_block[x][0][3], p_block[x][3][0], p_block[x][3][3] = \
                p_block[x][0][3], p_block[x][3][3], p_block[x][0][0], p_block[x][3][0]  # ring 1
            p_block[x][0][2], p_block[x][2][3], p_block[x][3][1], p_block[x][1][0] = \
                p_block[x][1][0], p_block[x][0][2], p_block[x][2][3], p_block[x][3][1]  # ring 4
            p_block[x][0][1], p_block[x][1][3], p_block[x][3][2], p_block[x][2][0] = \
                p_block[x][2][0], p_block[x][0][1], p_block[x][1][3], p_block[x][3][2]  # ring 5
            

    def inverse_spin_rings(self) -> None:
        p_block = self.poly_block
        for x in range(0, 4):
            p_block[x][1][2], p_block[x][2][1] = p_block[x][2][1], p_block[x][1][2]  # ring 2
            p_block[x][1][1], p_block[x][2][2] = p_block[x][2][2], p_block[x][1][1]  # ring 3
            p_block[x][0][0], p_block[x][0][3], p_block[x][3][0], p_block[x][3][3] = \
                p_block[x][3][0], p_block[x][0][0], p_block[x][3][3], p_block[x][0][3]  # ring 1
            p_block[x][0][2], p_block[x][2][3], p_block[x][3][1], p_block[x][1][0] = \
                p_block[x][2][3], p_block[x][3][1], p_block[x][1][0], p_block[x][0][2]  # ring 4
            p_block[x][0][1], p_block[x][1][3], p_block[x][3][2], p_block[x][2][0] = \
                p_block[x][1][3], p_block[x][3][2], p_block[x][2][0], p_block[x][0][1]  # ring 5
