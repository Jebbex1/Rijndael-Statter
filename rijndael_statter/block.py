import numpy as np
from .constants import S_BOX, INVERSE_S_BOX

def get_ordered_block() -> 'Block':
    return Block(b"".join(i.to_bytes(1) for i in range(64)))


class Block:
    def __init__(self, source_bytes: bytes) -> None:
        if not len(source_bytes) == 64:
            raise ValueError(f"Blocks are of length 64 bytes (512 bits) only, supplied length of {len(source_bytes)}")
        
        self.byte_block = np.ndarray(dtype=np.uint8, shape=(64, 1, 1))

        for i in range(64):
            self.byte_block[i] = source_bytes[i]
        
        self.byte_block = self.byte_block.reshape((4, 4, 4))


    @classmethod
    def from_byte_block(cls, byte_block: np.ndarray) -> 'Block':
        obj = object.__new__(cls)
        obj.byte_block = np.copy(byte_block)
        return obj


    def __str__(self) -> str:
        return self.byte_block.__str__()
    

    def xy_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, byte in np.ndenumerate(self.byte_block):
            # loc for location, in format x,y,z
            int_block[loc[2]][loc[0]][loc[1]] = byte  # convert to to view layers in the wanted plane 
        return int_block.__str__()


    def xz_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, byte in np.ndenumerate(self.byte_block):
            # loc for location, in format x,y,z
            int_block[loc[1]][loc[0]][loc[2]] = byte  # convert to to view layers in the wanted plane
        return int_block.__str__()


    def yz_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, byte in np.ndenumerate(self.byte_block):
            # loc for location, in format x,y,z
            int_block[loc] = byte  # convert to to view layers in the wanted plane 
        return int_block.__str__()


    def shift_rows(self) -> None:  # XY layer permutation
        p_block = self.byte_block
        for z in range(0, 4):
            p_block[1][0][z], p_block[1][1][z], p_block[1][2][z], p_block[1][3][z] = \
                p_block[1][1][z], p_block[1][2][z], p_block[1][3][z], p_block[1][0][z]  # row 2
            p_block[2][0][z], p_block[2][1][z], p_block[2][2][z], p_block[2][3][z] = \
                p_block[2][2][z], p_block[2][3][z], p_block[2][0][z], p_block[2][1][z]  # row 3
            p_block[3][0][z], p_block[3][1][z], p_block[3][2][z], p_block[3][3][z] = \
                p_block[3][3][z], p_block[3][0][z], p_block[3][1][z], p_block[3][2][z]  # row 4
    

    def inverse_shift_rows(self) -> None:  # XY layer permutation
        p_block = self.byte_block
        for z in range(0, 4):
            p_block[1][0][z], p_block[1][1][z], p_block[1][2][z], p_block[1][3][z] = \
                p_block[1][3][z], p_block[1][0][z], p_block[1][1][z], p_block[1][2][z]  # row 2
            p_block[2][0][z], p_block[2][1][z], p_block[2][2][z], p_block[2][3][z] = \
                p_block[2][2][z], p_block[2][3][z], p_block[2][0][z], p_block[2][1][z]  # row 3
            p_block[3][0][z], p_block[3][1][z], p_block[3][2][z], p_block[3][3][z] = \
                p_block[3][1][z], p_block[3][2][z], p_block[3][3][z], p_block[3][0][z]  # row 4


    def rotate_elements(self) -> None:  # XZ layer permumtation
        p_block = self.byte_block
        for y in range(0, 4):
            p_block[0][y][1], p_block[0][y][3], p_block[2][y][3], p_block[2][y][1] = \
                p_block[2][y][1], p_block[0][y][1], p_block[0][y][3], p_block[2][y][3]  # group 2
            p_block[1][y][1], p_block[1][y][3], p_block[3][y][3], p_block[3][y][1] = \
                p_block[3][y][3], p_block[3][y][1], p_block[1][y][1], p_block[1][y][3]  # group 3
            p_block[1][y][0], p_block[1][y][2], p_block[3][y][2], p_block[3][y][0] = \
                p_block[1][y][2], p_block[3][y][2], p_block[3][y][0], p_block[1][y][0]  # group 4
    

    def inverse_rotate_elements(self) -> None:  # XZ layer permutation
        p_block = self.byte_block
        for y in range(0, 4):
            p_block[0][y][1], p_block[0][y][3], p_block[2][y][3], p_block[2][y][1] = \
                p_block[0][y][3], p_block[2][y][3], p_block[2][y][1], p_block[0][y][1]  # group 2
            p_block[1][y][1], p_block[1][y][3], p_block[3][y][3], p_block[3][y][1] = \
                p_block[3][y][3], p_block[3][y][1], p_block[1][y][1], p_block[1][y][3]  # group 3
            p_block[1][y][0], p_block[1][y][2], p_block[3][y][2], p_block[3][y][0] = \
                p_block[3][y][0], p_block[1][y][0], p_block[1][y][2], p_block[3][y][2]  # group 4
    

    def spin_rings(self) -> None:  # YZ layer permutation
        p_block = self.byte_block
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
        p_block = self.byte_block
        for x in range(0, 4):
            p_block[x][1][2], p_block[x][2][1] = p_block[x][2][1], p_block[x][1][2]  # ring 2
            p_block[x][1][1], p_block[x][2][2] = p_block[x][2][2], p_block[x][1][1]  # ring 3
            p_block[x][0][0], p_block[x][0][3], p_block[x][3][0], p_block[x][3][3] = \
                p_block[x][3][0], p_block[x][0][0], p_block[x][3][3], p_block[x][0][3]  # ring 1
            p_block[x][0][2], p_block[x][2][3], p_block[x][3][1], p_block[x][1][0] = \
                p_block[x][2][3], p_block[x][3][1], p_block[x][1][0], p_block[x][0][2]  # ring 4
            p_block[x][0][1], p_block[x][1][3], p_block[x][3][2], p_block[x][2][0] = \
                p_block[x][1][3], p_block[x][3][2], p_block[x][2][0], p_block[x][0][1]  # ring 5


    def sub_bytes(self) -> None:
        for loc, byte in np.ndenumerate(self.byte_block):
            self.byte_block[loc] = S_BOX[byte]

    
    def inverse_sub_bytes(self) -> None:
        for loc, byte in np.ndenumerate(self.byte_block):
            self.byte_block[loc] = INVERSE_S_BOX[byte]
