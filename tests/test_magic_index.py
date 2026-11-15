"""Ensure every editorial magic subject uses real Psalm verses."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MagicIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = json.loads((ROOT / "data/magic-curated.json").read_text(encoding="utf-8"))

    def test_editorial_subjects_have_canonical_references(self):
        parts = self.guide["parts"]
        self.assertEqual(self.guide["schemaVersion"], 1)
        self.assertGreaterEqual(len(parts), 8)
        self.assertEqual(len({part["id"] for part in parts}), len(parts))
        cache = {}
        count = 0
        for part in parts:
            self.assertTrue(part["label"] and part["intro"])
            self.assertTrue(part["entries"])
            for entry in part["entries"]:
                self.assertTrue(entry["title"] and entry["summary"])
                self.assertTrue(entry["references"])
                for ref in entry["references"]:
                    rid = ref["recordId"]
                    book, psalm = rid.split("-psalm-")
                    path = ROOT / "data/corpus/books" / book / ("psalm-" + psalm + ".json")
                    self.assertTrue(path.is_file(), rid)
                    if path not in cache:
                        cache[path] = json.loads(path.read_text(encoding="utf-8"))
                    document = cache[path]
                    self.assertEqual(document["recordType"], "psalm")
                    self.assertEqual(document["id"], rid)
                    actual = {v["number"] for v in document["verses"]}
                    for number in ref["verses"]:
                        self.assertIn(number, actual, f"{rid} verse {number}")
                        count += 1
        self.assertGreaterEqual(count, 130)

    def test_public_pages_must_publish_all_magic_assets(self):
        builder = (ROOT / "scripts/build_pages_site.py").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "js/biblaw.js").read_text(encoding="utf-8")
        for path in ("js/biblaw-magic.js", "css/biblaw-magic.css"):
            self.assertIn(f'"{path}"', builder)
        self.assertIn('generate_public_magic(magic_public)', builder)
        self.assertIn('data/magic-public.json', builder)
        for path in ("js/biblaw-magic.js", "css/biblaw-magic.css",
                     "data/magic-public.json"):
            self.assertIn(f"test -f _site/{path}", workflow)
        self.assertIn('id="magicToggle"', html)
        self.assertIn('id="magicLibrary"', html)
        self.assertIn('js/biblaw-magic.js?v=001', html)
        self.assertIn('BiblawMagic?.open()', app)
        self.assertIn("sourceParams.get('rubrique')==='magie'", app)


if __name__ == "__main__":
    unittest.main()
