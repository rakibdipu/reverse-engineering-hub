#!/usr/bin/env python3
"""
Unity Harmony IL Code Patcher Visualizer — Inspired by WitherOrNot/MuseDashDLCUnlock
Demonstrates runtime IL instruction replacement (e.g. ldc.i4.1 + ret).
"""

import json

OPCODES = {
    "ldc.i4.0": 0x16,  # load false (0)
    "ldc.i4.1": 0x17,  # load true (1)
    "ret":      0x2A   # return
}

def simulate_harmony_postfix(method_name: str):
    """Replaces method body to always return true (purchased/unlocked)"""
    return {
        "target_method": method_name,
        "original_behavior": "CheckServerEntitlement() -> bool",
        "patched_il_bytes": [OPCODES["ldc.i4.1"], OPCODES["ret"]],
        "patched_asm": ["ldc.i4.1", "ret"],
        "result": "Always returns True without modifying assembly on disk"
    }

if __name__ == "__main__":
    patch = simulate_harmony_postfix("IsDlcPurchased")
    print(json.dumps(patch, indent=2))
