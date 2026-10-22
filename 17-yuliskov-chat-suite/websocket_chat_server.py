#!/usr/bin/env python3
"""
Unified Chat Server — Merging yuliskov's MyChatClient, MyChatService & MyAuthService
"""

import json
import time

class SimpleChatServer:
    def __init__(self):
        self.users = {}
        self.messages = []

    def authenticate_user(self, username, password):
        if len(username) >= 3 and len(password) >= 4:
            token = f"JWT_{username}_{int(time.time())}"
            self.users[username] = {"token": token, "joined": time.time()}
            return {"status": "authenticated", "token": token, "user": username}
        return {"status": "error", "message": "Invalid credentials"}

    def broadcast_message(self, token, message_text):
        sender = next((u for u, data in self.users.items() if data["token"] == token), None)
        if not sender:
            return {"status": "unauthorized"}
        msg = {
            "id": len(self.messages) + 1,
            "sender": sender,
            "content": message_text,
            "timestamp": time.time()
        }
        self.messages.append(msg)
        return {"status": "sent", "message": msg}

if __name__ == "__main__":
    chat = SimpleChatServer()
    auth = chat.authenticate_user("rakib", "secret123")
    print("Auth Result:", json.dumps(auth, indent=2))
    send = chat.broadcast_message(auth["token"], "Hello from unified Chat Suite!")
    print("Broadcast Message:", json.dumps(send, indent=2))
