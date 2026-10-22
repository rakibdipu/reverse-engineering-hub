#!/usr/bin/env python3
"""
XenonRecomp XEX Inspector & ABI Bridge — Inspired by WitherOrNot/XenonRecomp-XEO3
Inspects Xbox 360 binary signatures for Microsoft XEO3 static recompilation.
"""

import struct
import json

PPC_TO_X64_REG_MAP = {
    "r1": "rsp",    # Stack pointer
    "r3": "rax",    # Return value / Param 1
    "r4": "rdx",    # Param 2
    "r5": "rcx",    # Param 3
    "r6": "r8",     # Param 4
    "r7": "r9",     # Param 5
    "r12": "r11",   # Scratch register
}

def analyze_xex_header(sample_bytes: bytes):
    if len(sample_bytes) < 4:
        return {"error": "Invalid file size"}
    magic = sample_bytes[:4]
    return {
        "magic": magic.decode(errors='ignore'),
        "is_valid_xex": magic in [b'XEX1', b'XEX2', b'XEX-'],
        "abi_register_bridge": PPC_TO_X64_REG_MAP,
        "supported_target": "Microsoft XEO3 Backward Compatibility Engine"
    }

if __name__ == "__main__":
    sample = b'XEX2\x00\x00\x00\x01'
    print(json.dumps(analyze_xex_header(sample), indent=2))
