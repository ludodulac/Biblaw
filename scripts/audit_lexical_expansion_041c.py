#!/usr/bin/env python3
"""041C audit of the checked-in, generated browser morphology runtime."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
runtime=json.loads((ROOT/"data/lexical-expansion-runtime.json").read_text(encoding="utf8"))
assert runtime["v"]==1
assert runtime["m"]=="4fc815cbf17aecdf1b47f6bbc263489a460fd8d11ae17e6b522336c72bd0e333"
groups=runtime["g"];assert groups and all(len(g)>=2 and g==sorted(set(g)) for g in groups)
forms=[f for g in groups for f in g]
assert len(forms)==len(set(forms))
assert all(f and " " not in f for f in forms)
assert not ({"empli","dote","travers","etre","avoir"}&set(forms))
for left,right in (("pain","pains"),("maison","maisons"),("aimer","aimons"),("chanter","chante"),("garder","gardera"),("parler","parlons")):
    assert any(left in g and right in g for g in groups),(left,right)
html=(ROOT/"index.html").read_text(encoding="utf8")
js=(ROOT/"js/biblaw.js").read_text(encoding="utf8")
assert 'id="exactExpansionOption"' in html and 'id="includeWordForms"' in html
assert "data/lexical-expansion-runtime.json" in js
assert "const available=Boolean(key&&expansions.length);" in js
assert "const exactItems=matches(query);" in js
assert "mergeExpansionMatches(exactItems,query);" in js
assert "checkbox.checked=false" in js
assert "state.mode==='exact'&&$('includeWordForms')?.checked" in js
assert "fallbackExpansion" not in js
print("041C lexical runtime contract PASS",len(groups),"groups",len(forms),"anchors")
