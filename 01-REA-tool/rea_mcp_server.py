#!/usr/bin/env python3
"""
REA MCP Server — Reverse Engineer Anything
Connects Claude Code / Cursor to Ghidra & IDA Pro via Model Context Protocol

Usage:
    python rea_mcp_server.py --ghidra /opt/ghidra --port 3000

References:
    - https://github.com/morluto/rea
    - https://cybersecuritynews.com/reverse-engineer-anything-tool/
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

# MCP SDK (pip install mcp)
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.types import Tool, TextContent
    HAS_MCP = True
except ImportError:
    print("WARNING: mcp package not installed. Run: pip install mcp")
    HAS_MCP = False


# ─── Configuration ────────────────────────────────────────────────────────────

GHIDRA_PATH = os.environ.get("GHIDRA_PATH", "/opt/ghidra")
IDA_PATH    = os.environ.get("IDA_PATH", "/opt/ida")
WORK_DIR    = Path(tempfile.mkdtemp(prefix="rea_"))

print(f"[REA] Work directory: {WORK_DIR}")
print(f"[REA] Ghidra path: {GHIDRA_PATH}")


# ─── Ghidra Bridge ────────────────────────────────────────────────────────────

class GhidraBridge:
    """Ghidra headless analyzer wrapper"""

    def __init__(self, ghidra_path: str):
        self.ghidra_path = ghidra_path
        self.analyze_headless = os.path.join(ghidra_path, "support", "analyzeHeadless")
        self.project_dir = str(WORK_DIR / "ghidra_project")
        os.makedirs(self.project_dir, exist_ok=True)

    def is_available(self) -> bool:
        return os.path.exists(self.analyze_headless)

    def analyze_binary(self, binary_path: str) -> dict:
        """
        বাইনারি ফাইল লোড করে Ghidra দিয়ে বিশ্লেষণ করে।
        Returns: analysis result dict
        """
        if not self.is_available():
            return {"error": "Ghidra not found. Please install Ghidra and set GHIDRA_PATH"}

        script = self._create_analysis_script()

        cmd = [
            self.analyze_headless,
            self.project_dir, "rea_project",
            "-import", binary_path,
            "-postScript", script,
            "-deleteProject"
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )
            return self._parse_output(result.stdout)
        except subprocess.TimeoutExpired:
            return {"error": "Analysis timed out (120s)"}
        except FileNotFoundError:
            return {"error": f"Ghidra not found at {self.analyze_headless}"}

    def _create_analysis_script(self) -> str:
        """Ghidra Java script তৈরি করে যা ফলাফল JSON-এ দেয়"""
        script_path = str(WORK_DIR / "REAScript.java")
        script_content = '''
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import com.google.gson.*;
import java.util.*;

public class REAScript extends GhidraScript {
    @Override
    public void run() throws Exception {
        JsonObject result = new JsonObject();
        JsonArray functions = new JsonArray();

        FunctionIterator iter = currentProgram.getListing().getFunctions(true);
        while (iter.hasNext() && !monitor.isCancelled()) {
            Function func = iter.next();
            JsonObject f = new JsonObject();
            f.addProperty("name", func.getName());
            f.addProperty("address", func.getEntryPoint().toString());
            f.addProperty("size", func.getBody().getNumAddresses());
            functions.add(f);
        }

        result.add("functions", functions);
        result.addProperty("name", currentProgram.getName());
        result.addProperty("arch", currentProgram.getLanguage().getProcessor().toString());

        println("REA_RESULT:" + result.toString());
    }
}
'''
        with open(script_path, 'w') as f:
            f.write(script_content)
        return script_path

    def _parse_output(self, output: str) -> dict:
        """Ghidra output থেকে JSON ডেটা বের করে"""
        for line in output.split('\n'):
            if line.startswith("REA_RESULT:"):
                try:
                    return json.loads(line[11:])
                except json.JSONDecodeError:
                    pass
        return {"raw_output": output[:2000]}  # ফলাফল না পেলে raw আউটপুট দাও


# ─── MCP Tools Definition ─────────────────────────────────────────────────────

class REAServer:
    """
    REA MCP Server
    AI Agent (Claude Code / Cursor) কে এই টুলগুলো দেওয়া হয়
    """

    def __init__(self):
        self.ghidra = GhidraBridge(GHIDRA_PATH)
        self.loaded_binaries: dict = {}  # cache

    def get_tools(self) -> list:
        """সব available tools এর তালিকা"""
        return [
            {
                "name": "analyze_binary",
                "description": (
                    "একটি binary/executable ফাইল লোড করে Ghidra দিয়ে বিশ্লেষণ করে। "
                    "ফাংশন তালিকা, আর্কিটেকচার, এবং প্রাথমিক তথ্য দেয়।"
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "binary_path": {
                            "type": "string",
                            "description": "বিশ্লেষণ করতে চাওয়া ফাইলের পাথ (যেমন: /tmp/malware.exe)"
                        }
                    },
                    "required": ["binary_path"]
                }
            },
            {
                "name": "list_functions",
                "description": "বাইনারির সব ফাংশনের তালিকা দেয় (নাম + মেমোরি address)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "binary_path": {"type": "string"}
                    },
                    "required": ["binary_path"]
                }
            },
            {
                "name": "decompile_function",
                "description": "একটি নির্দিষ্ট ফাংশনের মেশিন কোড থেকে C-like সোর্স কোড জেনারেট করে",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "binary_path": {"type": "string"},
                        "function_name": {
                            "type": "string",
                            "description": "ফাংশনের নাম বা memory address (যেমন: main বা 0x401000)"
                        }
                    },
                    "required": ["binary_path", "function_name"]
                }
            },
            {
                "name": "find_strings",
                "description": "বাইনারিতে embedded strings খোঁজে (URL, API keys, passwords ইত্যাদি)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "binary_path": {"type": "string"},
                        "min_length": {
                            "type": "integer",
                            "description": "স্ট্রিংয়ের ন্যূনতম দৈর্ঘ্য (ডিফল্ট: 4)",
                            "default": 4
                        }
                    },
                    "required": ["binary_path"]
                }
            },
            {
                "name": "list_imports",
                "description": "বাইনারির সব imported DLL এবং ফাংশন তালিকা দেয় (Windows PE analysis)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "binary_path": {"type": "string"}
                    },
                    "required": ["binary_path"]
                }
            },
            {
                "name": "find_crypto",
                "description": "বাইনারিতে cryptographic constants (AES, RSA, MD5 ইত্যাদি) খোঁজে",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "binary_path": {"type": "string"}
                    },
                    "required": ["binary_path"]
                }
            }
        ]

    def handle_tool_call(self, tool_name: str, arguments: dict) -> str:
        """Tool call প্রসেস করে ফলাফল দেয়"""

        if tool_name == "analyze_binary":
            result = self.ghidra.analyze_binary(arguments["binary_path"])
            return json.dumps(result, indent=2, ensure_ascii=False)

        elif tool_name == "list_functions":
            # Ghidra analysis থেকে ফাংশন লিস্ট বের করো
            result = self.ghidra.analyze_binary(arguments["binary_path"])
            functions = result.get("functions", [])
            return json.dumps({
                "total": len(functions),
                "functions": functions[:50]  # প্রথম ৫০টি দেখাও
            }, indent=2)

        elif tool_name == "decompile_function":
            # TODO: Ghidra decompiler integration
            return json.dumps({
                "function": arguments.get("function_name"),
                "note": "Ghidra decompiler integration — coming soon",
                "hint": "Ghidra-এ manual decompile করতে: Window > Decompiler"
            })

        elif tool_name == "find_strings":
            binary_path = arguments["binary_path"]
            min_len = arguments.get("min_length", 4)

            # strings command ব্যবহার করো (Linux)
            try:
                result = subprocess.run(
                    ["strings", f"-n{min_len}", binary_path],
                    capture_output=True, text=True, timeout=30
                )
                strings = result.stdout.strip().split('\n')
                # Interesting strings filter করো
                interesting = [s for s in strings if any(
                    keyword in s.lower()
                    for keyword in ['http', 'https', 'password', 'key', 'token',
                                    'api', 'user', 'login', 'cmd', 'exec', 'shell']
                )]
                return json.dumps({
                    "total_strings": len(strings),
                    "interesting_strings": interesting[:30],
                    "all_strings_preview": strings[:20]
                }, indent=2)
            except FileNotFoundError:
                return json.dumps({"error": "'strings' command not found. Install binutils."})

        elif tool_name == "list_imports":
            binary_path = arguments["binary_path"]
            try:
                result = subprocess.run(
                    ["objdump", "-p", binary_path],
                    capture_output=True, text=True, timeout=30
                )
                imports = []
                for line in result.stdout.split('\n'):
                    if 'DLL Name:' in line or 'IMPORT' in line.upper():
                        imports.append(line.strip())
                return json.dumps({"imports": imports}, indent=2)
            except FileNotFoundError:
                return json.dumps({"error": "'objdump' not found. Install binutils."})

        elif tool_name == "find_crypto":
            return json.dumps({
                "note": "Crypto detection requires Ghidra plugin 'FindCrypt'",
                "manual_method": "Ghidra → Analysis → One Shot → Find Crypto Constants",
                "known_patterns": {
                    "AES_SBOX": "0x63, 0x7c, 0x77, 0x7b...",
                    "MD5_CONST": "0x67452301, 0xefcdab89...",
                    "RSA_MAGIC": "Look for large prime number constants"
                }
            }, indent=2)

        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def main():
    """REA MCP Server শুরু করো"""
    print("🔍 REA (Reverse Engineer Anything) MCP Server")
    print("=" * 50)

    server = REAServer()

    # Tools দেখাও
    print("\n📋 Available Tools:")
    for tool in server.get_tools():
        print(f"  ✓ {tool['name']}: {tool['description'][:60]}...")

    # Ghidra চেক করো
    if server.ghidra.is_available():
        print(f"\n✅ Ghidra found at: {GHIDRA_PATH}")
    else:
        print(f"\n⚠️  Ghidra NOT found at: {GHIDRA_PATH}")
        print("   Install from: https://ghidra-sre.org/")

    print("\n🚀 Server ready! Configure in Claude Code / Cursor MCP settings.")
    print("\nExample config for .cursor/mcp.json:")
    print(json.dumps({
        "mcpServers": {
            "rea": {
                "command": "python",
                "args": ["rea_mcp_server.py"],
                "env": {"GHIDRA_PATH": "/opt/ghidra"}
            }
        }
    }, indent=2))


if __name__ == "__main__":
    main()
