# Rijnd3D
R3D (short for Rijndael 3D, pronounced as the color Red) is my work-in-progress extension of the Rijndael cipher that works in 512-bit 4x4x4 blocks of bytes. This module uses new layer-based permutation algorithms together with modified versions of regular Rijndael components to utilize the 3 dimensional structure of blocks.
This module is programmed in pure Python, it implements finite-field arithmetic in GF(2<sup>8</sup>) and is boosted by the [`numba`](https://numba.pydata.org/) module where possible.

## Cipher Specifications
- Key: 512-bit
- Block size: 512 bits
- Number of rounds per-block: 16

## Installation and Usage
As of writing this readme, the module is not yet finished and ready for deployment. When it is, there will be an official release to PyPI.