# 🔍 Project 01: REA — Reverse Engineer Anything

> **AI Coding Agent + Ghidra + IDA Pro = Automated Reverse Engineering**

## 📖 কী এটা?

**REA (Reverse Engineer Anything)** হলো একটি ওপেন-সোর্স টুল যা:
- **Claude Code** এবং **Cursor** AI কোডিং এজেন্টকে সংযুক্ত করে
- **Ghidra** (NSA's free RE tool) এবং **IDA Pro** (industry standard disassembler)-এর সাথে
- যেকোনো binary/executable ফাইলের সোর্স কোড ছাড়াই বিশ্লেষণ করে

## 🔗 রেফারেন্স

- **Original Repo:** https://github.com/morluto/rea
- **News:** https://cybersecuritynews.com/reverse-engineer-anything-tool/

## 🏗️ আর্কিটেকচার

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

## ⚙️ REA কীভাবে কাজ করে?

REA তিনটি ধাপে কাজ করে:

### ধাপ ১: Disassembly (বাইনারি বিশ্লেষণ)
```bash
# Ghidra দিয়ে একটি EXE বিশ্লেষণ
ghidra-headless /project -import target.exe -postScript REAScript.java
```

### ধাপ ২: MCP Bridge (AI সংযোগ)
```python
# REA MCP Server — AI Agent কে টুল দেয়
@mcp.tool()
def analyze_function(address: str) -> str:
    """Ghidra থেকে একটি ফাংশনের ডিকম্পাইলড কোড আনে"""
    return ghidra.decompile(address)

@mcp.tool()
def list_imports(binary_path: str) -> list:
    """বাইনারির সব imported function লিস্ট করে"""
    return ghidra.get_imports(binary_path)

@mcp.tool()
def find_strings(pattern: str) -> list:
    """বাইনারিতে নির্দিষ্ট স্ট্রিং খোঁজে"""
    return ghidra.search_strings(pattern)
```

### ধাপ ৩: AI Analysis (বুদ্ধিমান ব্যাখ্যা)
```
AI Agent (Claude/Cursor) → MCP টুল কল → Ghidra/IDA → ফলাফল → AI ব্যাখ্যা দেয়
```

## 🛠️ ইনস্টলেশন গাইড

### প্রয়োজনীয় সফটওয়্যার

```bash
# 1. Ghidra ইনস্টল করুন (ফ্রি)
wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.1.2_build/ghidra_11.1.2_PUBLIC_20240709.zip
unzip ghidra_11.1.2_PUBLIC_20240709.zip

# 2. Java (Ghidra এর জন্য দরকার)
sudo apt install openjdk-17-jdk

# 3. Python REA Bridge
pip install mcp ghidra-bridge requests

# 4. REA ক্লোন করুন
git clone https://github.com/morluto/rea
cd rea
pip install -e .
```

### Claude Code / Cursor কনফিগার করুন

```json
// .cursor/mcp.json বা claude_code_config.json
{
  "mcpServers": {
    "rea": {
      "command": "python",
      "args": ["-m", "rea.server"],
      "env": {
        "GHIDRA_PATH": "/opt/ghidra",
        "IDA_PATH": "/opt/ida"
      }
    }
  }
}
```

## 📝 ব্যবহারের উদাহরণ

### Claude Code দিয়ে একটি malware বিশ্লেষণ:

```
আপনি Claude Code-কে বলুন:
"target.exe ফাইলটি রিভার্স ইঞ্জিনিয়ার করো। এর main() ফাংশন
থেকে শুরু করে কোন APIs call হচ্ছে এবং কী করছে বলো।"

Claude তখন:
1. analyze_binary("target.exe") কল করবে
2. list_functions() দিয়ে সব ফাংশন দেখবে
3. decompile_function("main") দিয়ে কোড আনবে
4. মানুষের ভাষায় ব্যাখ্যা দেবে
```

## 🎯 ব্যবহারিক প্রয়োগ

| কাজ | REA ব্যবহার |
|-----|-----------|
| Malware বিশ্লেষণ | সন্দেহজনক .exe রিভার্স করুন |
| Protocol RE | বন্ধ সফটওয়্যারের নেটওয়ার্ক প্রোটোকল বের করুন |
| CTF Challenges | Binary exploitation challenge সমাধান |
| Vulnerability Research | বাগ খোঁজা ও রিপোর্ট করা |
| Firmware Analysis | IoT ডিভাইসের ফার্মওয়্যার বিশ্লেষণ |

## ⚠️ আইনি নোট

> শুধুমাত্র **authorized** সফটওয়্যার বা নিজের সফটওয়্যার রিভার্স করুন।
> CTF, security research, malware analysis এই টুলের সঠিক ব্যবহার।
