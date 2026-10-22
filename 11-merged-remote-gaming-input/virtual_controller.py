#!/usr/bin/env python3
"""
Virtual Remote Gaming & Emulation Controller
Maps touch input & LeanKeyboard keys to virtual gamepad / QEMU
"""

class VirtualController:
    def __init__(self):
        self.button_map = {
            'KEY_UP': 'DPAD_UP',
            'KEY_DOWN': 'DPAD_DOWN',
            'KEY_ENTER': 'BUTTON_A',
            'KEY_BACK': 'BUTTON_B'
        }
        print('🎮 Virtual Controller initialized')

    def send_input(self, raw_key):
        mapped = self.button_map.get(raw_key, 'UNKNOWN')
        print(f'Input: {raw_key} -> Gamepad: {mapped}')
        return mapped

if __name__ == '__main__':
    c = VirtualController()
    c.send_input('KEY_ENTER')
