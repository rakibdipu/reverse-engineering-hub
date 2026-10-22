#!/usr/bin/env python3
"""
Windows Product Key & Channel Validator — Inspired by WitherOrNot/winkeycheck
Decodes and validates Microsoft 5x5 Product Keys.
"""

import re
import json

KEY_REGEX = re.compile(r'^[B-DF-HJ-NP-TV-Z2-9]{5}(-[B-DF-HJ-NP-TV-Z2-9]{5}){4}$')

GVLK_KEYS = {
    "W269N-WFGWX-YVC9B-4J6C9-T83GX": "Windows 10/11 Pro (GVLK KMS)",
    "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4": "Windows 10/11 Enterprise (GVLK KMS)",
    "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99": "Windows 10/11 Home (GVLK KMS)"
}

def check_product_key(key: str):
    key = key.strip().upper()
    is_valid_format = bool(KEY_REGEX.match(key))
    channel = GVLK_KEYS.get(key, "Custom Retail / OEM / MAK Key")

    return {
        "key": key,
        "valid_format": is_valid_format,
        "identified_edition": channel,
        "validation_method": "Offline Regex & Known GVLK Database"
    }

if __name__ == "__main__":
    test_key = "W269N-WFGWX-YVC9B-4J6C9-T83GX"
    print(json.dumps(check_product_key(test_key), indent=2))
