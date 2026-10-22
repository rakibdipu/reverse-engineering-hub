#!/usr/bin/env python3
"""
QEMU Command Generator & Runner — Inspired by WitherOrNot/qemui
Generates optimized QEMU virtual machine arguments.
"""

import json

def build_qemu_cmd(vm_name: str, ram_mb: int = 4096, cores: int = 4, disk_path: str = "disk.qcow2"):
    cmd = [
        "qemu-system-x86_64",
        "-name", vm_name,
        "-m", str(ram_mb),
        "-smp", f"cores={cores}",
        "-enable-kvm",
        "-cpu", "host",
        "-drive", f"file={disk_path},format=qcow2,if=virtio",
        "-netdev", "user,id=net0,hostfwd=tcp::2222-:22",
        "-device", "virtio-net-pci,netdev=net0",
        "-vga", "virtio",
        "-display", "gtk,gl=on"
    ]
    return {
        "vm_name": vm_name,
        "command_list": cmd,
        "command_string": " ".join(cmd)
    }

if __name__ == "__main__":
    print(json.dumps(build_qemu_cmd("ReverseEngLab"), indent=2))
