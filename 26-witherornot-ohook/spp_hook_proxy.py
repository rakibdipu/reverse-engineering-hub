#!/usr/bin/env python3
"""
SPP COM Interface Proxy Interceptor — Inspired by WitherOrNot/ohook
Simulates Software Protection Platform DLL proxy routing.
"""

import json

SPP_VTABLE = [
    {"index": 0, "method": "QueryInterface"},
    {"index": 1, "method": "AddRef"},
    {"index": 2, "method": "Release"},
    {"index": 3, "method": "SLGetLicensingStatusInformation", "hooked": True, "forced_return": "LICENSED (0x01)"},
    {"index": 4, "method": "SLGetPolicyInformationDWORD", "hooked": True, "forced_return": "GRACE_PERIOD_PERPETUAL"}
]

def get_proxy_status():
    return {
        "architecture": "DLL Proxy (version.dll / slc.dll)",
        "target_process": "SppExtComObj.exe / WINWORD.EXE",
        "hook_strategy": "VTable interception with perpetual license response",
        "intercepted_methods": SPP_VTABLE
    }

if __name__ == "__main__":
    print(json.dumps(get_proxy_status(), indent=2))
