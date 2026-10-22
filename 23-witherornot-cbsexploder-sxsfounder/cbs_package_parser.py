#!/usr/bin/env python3
"""
Windows CBS Package & MUM Manifest Parser — Inspired by WitherOrNot/cbsexploder
Inspects Component-Based Servicing metadata and assemblies.
"""

import xml.etree.ElementTree as ET
import json

SAMPLE_MUM = """<?xml version="1.0" encoding="utf-8"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v3" manifestVersion="1.0">
  <assemblyIdentity name="Package_for_RollupFix" version="10.0.19041.1" processorArchitecture="amd64" language="neutral" buildType="release" publicKeyToken="31bf3856ad364e35"/>
  <package identifier="KB5005565" releaseType="Update">
    <update name="5005565-1_neutral_GDR">
      <packageExtended declare="true" restart="possible"/>
    </update>
  </package>
</assembly>
"""

def parse_mum(xml_string: str):
    root = ET.fromstring(xml_string)
    ns = {'asm': 'urn:schemas-microsoft-com:asm.v3'}
    identity = root.find('asm:assemblyIdentity', ns)
    package = root.find('asm:package', ns)

    return {
        "package_name": identity.attrib.get('name') if identity is not None else "Unknown",
        "version": identity.attrib.get('version') if identity is not None else "Unknown",
        "arch": identity.attrib.get('processorArchitecture') if identity is not None else "Unknown",
        "update_id": package.attrib.get('identifier') if package is not None else "Unknown",
        "parser_status": "Success"
    }

if __name__ == "__main__":
    print(json.dumps(parse_mum(SAMPLE_MUM), indent=2))
