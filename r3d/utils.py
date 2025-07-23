def partition_text_to_blocks(source: bytes) -> list[bytes]:
    assert len(source)%64 == 0, "Can only partition multiples of 64."

    blocks = []
    for start in range(0, len(source), 64):
        blocks.append(source[start:start+64])

    return blocks


def xor_block_bytes(b1: bytes, b2: bytes) -> bytes:
    assert len(b1) == len(b2) == 64, "Blocks are of incorrect length."
    return (int(b1.hex(), 16) ^ int(b2.hex(), 16)).to_bytes(64)
