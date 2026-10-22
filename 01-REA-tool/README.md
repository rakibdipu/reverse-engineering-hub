# 🔍 Project 01: REA — Reverse Engineer Anything

> **AI Coding Agents + Ghidra + IDA Pro = Automated Binary Reverse Engineering**

---

## 👤 Upstream Creator & Attribution
* **Original Author / Inspiration:** [@morluto](https://github.com/morluto/rea)
* **Upstream Repository:** [https://github.com/morluto/rea](https://github.com/morluto/rea)
* **Credit & License:** All original architectural concepts belong to @morluto. This repository provides an upgraded, documented, and runnable standalone implementation.

---

## 🚀 How We Made It Better / Merged Innovations
- Standalone Python MCP server implementation with direct headless Ghidra and IDA Pro bridge.
- Adds automated string extraction, cryptographic constant hunting (AES S-Box, MD5, RSA), and import table resolution.
- Out-of-the-box configuration template for both Claude Code and Cursor IDE.

---

## 📖 What is REA?

**REA (Reverse Engineer Anything)** is an open-source tool that:
- Connects **Claude Code** and **Cursor** AI coding assistants
- Integrates with **Ghidra** (NSA's free software reverse engineering suite) and **IDA Pro** (industry-standard disassembler)
- Inspects and analyzes compiled binaries without requiring original source code

## 🔗 References

- **Original Repository:** [https://github.com/morluto/rea](https://github.com/morluto/rea)
- **News Coverage:** [CyberSecurityNews Article](https://cybersecuritynews.com/reverse-engineer-anything-tool/)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              REA Tool Architecture                   │
│                                                     │
│  ┌─────────────┐    MCP     ┌──────────────────┐   │
│  │  AI Agent   │ ─────────► │   RE Backend     │   │
│  │             │            │                  │   │
│  │ Claude Code │◄────────── │ ┌──────────────┐ │   │
│  │  or Cursor  │  Results   │ │   Ghidra     │ │   │
│  └─────────────┘            │ │   (Free)     │ │   │
│                             │ └──────────────┘ │   │
│                             │ ┌──────────────┐ │   │
│                             │ │   IDA Pro    │ │   │
│                             │ │  (Premium)   │ │   │
│                             │ └──────────────┘ │   │
│                             │ ┌──────────────┐ │   │
│                             │ │   Hopper     │ │   │
│                             │ │  (macOS/Lin) │ │   │
│                             │ └──────────────┘ │   │
│                             └──────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## ⚙️ How REA Works

REA operates in three primary phases:

### Step 1: Disassembly & Headless Analysis
```bash
# Analyze executable headless using Ghidra
ghidra-headless /project -import target.exe -postScript REAScript.java
```

### Step 2: MCP Bridge (Connecting AI to Ghidra)
```python
# REA MCP Server exposes tools to the AI agent
@mcp.tool()
def analyze_function(address: str) -> str:
    """Retrieves decompiled C pseudocode of a function from Ghidra"""
    return ghidra.decompile(address)

@mcp.tool()
def list_imports(binary_path: str) -> list:
    """Lists imported DLL functions for Windows PE binaries"""
    return ghidra.get_imports(binary_path)

@mcp.tool()
def find_strings(pattern: str) -> list:
    """Searches for embedded strings (URLs, API keys, credentials)"""
    return ghidra.search_strings(pattern)
```

### Step 3: AI Synthesis & Automated Explanations
```
AI Agent (Claude/Cursor) ──► Calls MCP Tool ──► Ghidra/IDA ──► Returns Data ──► AI Explains in Plain English
```

## 🛠️ Installation & Setup

### Requirements

```bash
# 1. Install Ghidra
wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.1.2_build/ghidra_11.1.2_PUBLIC_20240709.zip
unzip ghidra_11.1.2_PUBLIC_20240709.zip

# 2. OpenJDK 17
sudo apt install openjdk-17-jdk

# 3. Python MCP Bridge
pip install mcp ghidra-bridge requests
```

### Configuring Claude Code / Cursor MCP

```json
// Add to .cursor/mcp.json or claude_desktop_config.json:
{
  "mcpServers": {
    "rea": {
      "command": "python3",
      "args": ["rea_mcp_server.py"],
      "env": {
        "GHIDRA_PATH": "/opt/ghidra",
        "IDA_PATH": "/opt/ida"
      }
    }
  }
}
```

## 🎯 Practical Use Cases

| Domain | REA Capability |
|---|---|
| **Malware Triage** | Dissect suspicious PE/ELF executables and identify API call chains |
| **Protocol Reversing** | Extract proprietary network protocols and packet structures |
| **CTF Challenges** | Automate binary analysis and decompile challenge targets |
| **Vulnerability Research** | Discover buffer overflows, memory corruptions, and unsafe APIs |
| **Firmware Audits** | Analyze IoT and embedded firmware binaries |

---

## ⚠️ Legal Notice

> Use this tool strictly on authorized targets, proprietary code you own, or open-source challenges. Comply with all local cybersecurity legislation and responsible vulnerability disclosure policies.