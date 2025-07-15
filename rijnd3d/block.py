import numpy as np
from .constants import S_BOX, INVERSE_S_BOX, EXTENTION_FIELD, XY_MULT_MATRIX, INVERSE_XY_MULT_MATRIX, XZ_MULT_MATRIX, \
    INVERSE_XZ_MULT_MATRIX, YZ_MULT_MATRIX, INVERSE_YZ_MULT_MATRIX
from numba import jit


def get_ordered_block():
    return Block(b"".join(i.to_bytes(1) for i in range(64)))


class Block(np.ndarray):
    def __new__(cls, source_bytes: bytes) -> 'Block':
        if not len(source_bytes) == 64:
            raise ValueError(f"Blocks are of length 64 bytes (512 bits) only, supplied length of {len(source_bytes)}")
        
        byte_block = np.ndarray(dtype=np.uint8, shape=(64, 1, 1)).view(cls)

        for i in range(64):
            byte_block[i] = source_bytes[i]
        
        byte_block = byte_block.reshape((4, 4, 4)).view(cls)

        return byte_block


    @classmethod
    def from_byte_block(cls, src_block: 'Block') -> 'Block':
        obj = src_block.copy()
        return obj
    

    def xy_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, byte in np.ndenumerate(self):
            # loc for location, in format x,y,z
            int_block[loc[2]][loc[0]][loc[1]] = byte  # convert to to view layers in the wanted plane 
        return int_block.__str__()


    def xz_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, byte in np.ndenumerate(self):
            # loc for location, in format x,y,z
            int_block[loc[1]][loc[0]][loc[2]] = byte  # convert to to view layers in the wanted plane
        return int_block.__str__()


    def yz_layered_repr(self) -> str:
        int_block = np.ndarray(dtype=np.uint8, shape=(4, 4, 4))
        for loc, byte in np.ndenumerate(self):
            # loc for location, in format x,y,z
            int_block[loc] = byte  # convert to to view layers in the wanted plane 
        return int_block.__str__()


    @jit(nopython=True, nogil=True, cache=True)
    def shift_rows(self) -> None:  # XY layer permutation
        for z in range(0, 4):
            self[1][0][z], self[1][1][z], self[1][2][z], self[1][3][z] = \
                self[1][1][z], self[1][2][z], self[1][3][z], self[1][0][z]  # row 2
            self[2][0][z], self[2][1][z], self[2][2][z], self[2][3][z] = \
                self[2][2][z], self[2][3][z], self[2][0][z], self[2][1][z]  # row 3
            self[3][0][z], self[3][1][z], self[3][2][z], self[3][3][z] = \
                self[3][3][z], self[3][0][z], self[3][1][z], self[3][2][z]  # row 4
    

    @jit(nopython=True, nogil=True, cache=True)
    def inverse_shift_rows(self) -> None:  # XY layer permutation
        for z in range(0, 4):
            self[1][0][z], self[1][1][z], self[1][2][z], self[1][3][z] = \
                self[1][3][z], self[1][0][z], self[1][1][z], self[1][2][z]  # row 2
            self[2][0][z], self[2][1][z], self[2][2][z], self[2][3][z] = \
                self[2][2][z], self[2][3][z], self[2][0][z], self[2][1][z]  # row 3
            self[3][0][z], self[3][1][z], self[3][2][z], self[3][3][z] = \
                self[3][1][z], self[3][2][z], self[3][3][z], self[3][0][z]  # row 4


    @jit(nopython=True, nogil=True, cache=True)
    def rotate_elements(self) -> None:  # XZ layer permumtation
        for y in range(0, 4):
            self[0][y][1], self[0][y][3], self[2][y][3], self[2][y][1] = \
                self[2][y][1], self[0][y][1], self[0][y][3], self[2][y][3]  # group 2
            self[1][y][1], self[1][y][3], self[3][y][3], self[3][y][1] = \
                self[3][y][3], self[3][y][1], self[1][y][1], self[1][y][3]  # group 3
            self[1][y][0], self[1][y][2], self[3][y][2], self[3][y][0] = \
                self[1][y][2], self[3][y][2], self[3][y][0], self[1][y][0]  # group 4
    

    @jit(nopython=True, nogil=True, cache=True)
    def inverse_rotate_elements(self) -> None:  # XZ layer permutation
        for y in range(0, 4):
            self[0][y][1], self[0][y][3], self[2][y][3], self[2][y][1] = \
                self[0][y][3], self[2][y][3], self[2][y][1], self[0][y][1]  # group 2
            self[1][y][1], self[1][y][3], self[3][y][3], self[3][y][1] = \
                self[3][y][3], self[3][y][1], self[1][y][1], self[1][y][3]  # group 3
            self[1][y][0], self[1][y][2], self[3][y][2], self[3][y][0] = \
                self[3][y][0], self[1][y][0], self[1][y][2], self[3][y][2]  # group 4
    

    @jit(nopython=True, nogil=True, cache=True)
    def spin_rings(self) -> None:  # YZ layer permutation
        for x in range(0, 4):
            self[x][1][2], self[x][2][1] = self[x][2][1], self[x][1][2]  # ring 2
            self[x][1][1], self[x][2][2] = self[x][2][2], self[x][1][1]  # ring 3
            self[x][0][0], self[x][0][3], self[x][3][0], self[x][3][3] = \
                self[x][0][3], self[x][3][3], self[x][0][0], self[x][3][0]  # ring 1
            self[x][0][2], self[x][2][3], self[x][3][1], self[x][1][0] = \
                self[x][1][0], self[x][0][2], self[x][2][3], self[x][3][1]  # ring 4
            self[x][0][1], self[x][1][3], self[x][3][2], self[x][2][0] = \
                self[x][2][0], self[x][0][1], self[x][1][3], self[x][3][2]  # ring 5
            

    @jit(nopython=True, nogil=True, cache=True)
    def inverse_spin_rings(self) -> None:
        for x in range(0, 4):
            self[x][1][2], self[x][2][1] = self[x][2][1], self[x][1][2]  # ring 2
            self[x][1][1], self[x][2][2] = self[x][2][2], self[x][1][1]  # ring 3
            self[x][0][0], self[x][0][3], self[x][3][0], self[x][3][3] = \
                self[x][3][0], self[x][0][0], self[x][3][3], self[x][0][3]  # ring 1
            self[x][0][2], self[x][2][3], self[x][3][1], self[x][1][0] = \
                self[x][2][3], self[x][3][1], self[x][1][0], self[x][0][2]  # ring 4
            self[x][0][1], self[x][1][3], self[x][3][2], self[x][2][0] = \
                self[x][1][3], self[x][3][2], self[x][2][0], self[x][0][1]  # ring 5


    @jit(nopython=True, nogil=True, cache=True)
    def sub_bytes(self) -> None:
        for loc, byte in np.ndenumerate(self):
            self[loc] = S_BOX[byte]

    
    @jit(nopython=True, nogil=True, cache=True)
    def inverse_sub_bytes(self) -> None:
        for loc, byte in np.ndenumerate(self):
            self[loc] = INVERSE_S_BOX[byte]
    

    def mix_xy_columns(self) -> None:
        for z in range(0, 4):
            self[slice(0, 4)][slice(0, 4)][z] = \
                (XY_MULT_MATRIX @ EXTENTION_FIELD(self[slice(0, 4)][slice(0, 4)][z]))
    

    def inverse_mix_xy_columns(self) -> None:
        for z in range(0, 4):
            self[slice(0, 4)][slice(0, 4)][z] = \
                (INVERSE_XY_MULT_MATRIX @ EXTENTION_FIELD(self[slice(0, 4)][slice(0, 4)][z]))


    def mix_xz_columns(self) -> None:
        for y in range(0, 4):
            self[slice(0, 4)][y][slice(0, 4)] = \
                (XZ_MULT_MATRIX @ EXTENTION_FIELD(self[slice(0, 4)][y][slice(0, 4)]))
    

    def inverse_mix_xz_columns(self) -> None:
        for y in range(0, 4):
            self[slice(0, 4)][y][slice(0, 4)] = \
                (INVERSE_XZ_MULT_MATRIX @ EXTENTION_FIELD(self[slice(0, 4)][y][slice(0, 4)]))
    

    def mix_yz_columns(self) -> None:
        for x in range(0, 4):
            self[x][slice(0, 4)][slice(0, 4)] = \
                (YZ_MULT_MATRIX @ EXTENTION_FIELD(self[x][slice(0, 4)][slice(0, 4)]))
    

    def inverse_mix_yz_columns(self) -> None:
        for x in range(0, 4):
            self[x][slice(0, 4)][slice(0, 4)] = \
                (INVERSE_YZ_MULT_MATRIX @ EXTENTION_FIELD(self[x][slice(0, 4)][slice(0, 4)]))