#!/usr/bin/env python3
"""Real Chromium smoke test of grammar selection and semantic regression."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parents[1]
runtime = json.loads((ROOT / "data/linguistic-grammar-browser-runtime.json").read_text())
analyses = runtime["forms"][0]["analyses"]
assert {x["partOfSpeech"]:x["occurrenceCount"] for x in analyses} == {"NOUN":22,"VERB":70}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto("http://127.0.0.1:8765/index.html", wait_until="networkidle", timeout=60000)
    page.locator("#modeExact").click()
    page.locator("#query").fill("garde")
    page.locator("#searchButton").click()
    page.locator("[data-grammar-index]").first.wait_for()
    assert page.locator("[data-grammar-index]").count() == 2
    assert page.locator("[data-grammar-index]").nth(0).inner_text().lower().find("nom") >= 0
    page.locator("[data-grammar-index]").nth(0).click()
    assert "22 occurrences" in page.locator("#resultCount").inner_text()
    assert page.locator("[data-semantic-sense-id]").count() == 0
    assert page.locator("#ambiguityPanel").is_hidden()
    page.locator("#query").fill("autre")
    page.locator("#query").fill("garde")
    page.locator("#searchButton").click()
    page.locator("[data-grammar-index]").last.click()
    assert "70 occurrences" in page.locator("#resultCount").inner_text()
    assert page.locator("[data-semantic-sense-id]").count() == 0
    page.locator("#query").fill("bien")
    page.locator("#searchButton").click()
    page.locator("[data-semantic-sense-id]").first.wait_for()
    assert page.locator("[data-semantic-sense-id]").count() >= 2
    page.locator("[data-semantic-sense-id]").first.click()
    assert page.locator("#resultCount").inner_text()
    page.locator("#query").fill("éléphant")
    page.locator("#searchButton").click()
    assert page.locator("[data-grammar-index]").count() == 0
    assert errors == [], errors
    print("CHROMIUM_GRAMMAR_AND_BIEN=PASS")
    browser.close()
