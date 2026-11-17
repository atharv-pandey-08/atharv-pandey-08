"""Checks the profile README's local images and SVGs. Standard library only.

Run with: python3 -m unittest discover tests
"""

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


class ReadmeTests(unittest.TestCase):
    def test_local_images_exist(self) -> None:
        html = re.findall(r'src="([^"]+)"', README)
        local = [p for p in html if not p.startswith(("http://", "https://"))]
        self.assertTrue(local, "banner must be referenced")
        for rel in local:
            self.assertTrue((ROOT / rel).is_file(), f"missing file: {rel}")

    def test_svgs_are_valid_xml(self) -> None:
        for svg in (ROOT / "docs" / "assets").glob("*.svg"):
            root = ET.parse(svg).getroot()  # raises if the XML is broken
            self.assertTrue(root.tag.endswith("svg"))
            self.assertIn("viewBox", root.attrib)

    def test_private_details_stay_out(self) -> None:
        # The resume's phone number and client details are not for a public page.
        for banned in ("236", "788-9110", "Dentsply", "150K"):
            self.assertNotIn(banned, README)


if __name__ == "__main__":
    unittest.main()
