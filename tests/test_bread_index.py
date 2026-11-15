"""Regression checks for the documentary 'Le pain dans la Bible' navigation."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "bread-public.json"
CORPUS = ROOT / "data" / "corpus" / "books"


class BreadIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_part_categories_have_documentary_entries(self):
        self.assertEqual(self.data["schemaVersion"], 1)
        self.assertGreaterEqual(len(self.data["parts"]), 6)
        part_ids = [part["id"] for part in self.data["parts"]]
        self.assertEqual(len(part_ids), len(set(part_ids)))
        for part in self.data["parts"]:
            self.assertTrue(part["label"] and part["intro"])
            self.assertTrue(part["entries"])
            for entry in part["entries"]:
                self.assertTrue(entry["title"] and entry["summary"])
                self.assertTrue(entry["references"])

    def test_every_reference_exists_in_the_canonical_psalm_and_verse(self):
        cache = {}
        for part in self.data["parts"]:
            for entry in part["entries"]:
                for reference in entry["references"]:
                    record_id = reference["recordId"]
                    match = re.fullmatch(r"(book-\d{2})-(psalm-\d{3})", record_id)
                    self.assertIsNotNone(match, record_id)
                    path = CORPUS / match.group(1) / (match.group(2) + ".json")
                    self.assertTrue(path.is_file(), str(path))
                    if path not in cache:
                        cache[path] = json.loads(path.read_text(encoding="utf-8"))
                    psalm = cache[path]
                    self.assertEqual(psalm["id"], record_id)
                    self.assertEqual(psalm["recordType"], "psalm")
                    valid_verses = {verse["number"] for verse in psalm["verses"]}
                    for number in reference["verses"]:
                        self.assertIn(number, valid_verses, f"{record_id} v.{number}")

    def test_page_and_reader_hooks_are_present(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "js" / "biblaw.js").read_text(encoding="utf-8")
        for element_id in ("breadToggle", "breadLibrary", "breadCategories",
                           "breadBack", "breadReferences", "breadMethod"):
            self.assertEqual(html.count(f'id="{element_id}"'), 1)
        self.assertIn('js/biblaw-bread.js?v=002', html)
        self.assertIn('css/biblaw-bread.css?v=002', html)
        self.assertIn("BiblawBread?.open()", app)
        self.assertIn("BiblawBread?.setCorpusLoading(ensureCorpusReady)", app)
        self.assertIn("BiblawBread?.restoreAfterPsalm()", app)
        self.assertIn("sourceParams.get('rubrique')==='pain'", app)
        self.assertIn("window.location?.hash==='#breadLibrary'", app)
        self.assertIn('js/biblaw.js?v=146', html)


    def test_bread_assets_are_in_pages_deploy_allow_list(self):
        builder = (ROOT / "scripts" / "build_pages_site.py").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        for path in ("css/biblaw-bread.css", "js/biblaw-bread.js", "data/bread-public.json"):
            self.assertIn(f'"{path}"', builder)
            self.assertIn(f"test -f _site/{path}", workflow)



if __name__ == "__main__":
    unittest.main()
