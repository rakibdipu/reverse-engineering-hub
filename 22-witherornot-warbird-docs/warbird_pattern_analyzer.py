#!/usr/bin/env python3
"""
Warbird Entropy & Obfuscation Scanner — Inspired by WitherOrNot/warbird-docs
Detects high-entropy code sections characteristic of Microsoft Warbird obfuscation.
"""

import math
import json

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

def inspect_section(name: str, section_bytes: bytes):
    entropy = calculate_entropy(section_bytes)
    is_obfuscated = entropy > 7.2  # Typical threshold for encrypted/compressed code
    return {
        "section": name,
        "size_bytes": len(section_bytes),
        "entropy": round(entropy, 3),
        "warbird_characteristics": {
            "encrypted": is_obfuscated,
            "suspicious_entropy": is_obfuscated,
            "verdict": "Likely Warbird Obfuscated/Packed" if is_obfuscated else "Standard Native Code"
        }
    }

if __name__ == "__main__":
    sample = bytes([i % 256 for i in range(1024)])
    print(json.dumps(inspect_section(".text", sample), indent=2))
