#!/usr/bin/env python3
"""
NTFS $MFT Record Parser — Inspired by WitherOrNot/ntfstool
Decodes Master File Table binary records for forensic analysis.
"""

import struct
import json

def parse_mft_header(record_bytes: bytes):
    if len(record_bytes) < 48:
        return {"error": "Buffer too short for MFT record"}
    magic = record_bytes[:4]
    if magic != b'FILE':
        return {"error": "Invalid MFT signature, expected 'FILE'"}

    update_seq_offset, update_seq_size = struct.unpack('<HH', record_bytes[4:8])
    logfile_seq = struct.unpack('<Q', record_bytes[8:16])[0]
    seq_number = struct.unpack('<H', record_bytes[16:18])[0]
    hard_link_count = struct.unpack('<H', record_bytes[18:20])[0]
    first_attr_offset = struct.unpack('<H', record_bytes[20:22])[0]
    flags = struct.unpack('<H', record_bytes[22:24])[0]

    return {
        "magic": "FILE",
        "is_in_use": bool(flags & 0x01),
        "is_directory": bool(flags & 0x02),
        "sequence_number": seq_number,
        "hard_links": hard_link_count,
        "first_attribute_offset": first_attr_offset,
        "logfile_sequence": logfile_seq
    }

if __name__ == "__main__":
    # Sample valid MFT record header
    sample = b'FILE\x30\x00\x03\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x38\x00\x01\x00' + b'\x00'*28
    print(json.dumps(parse_mft_header(sample), indent=2))
