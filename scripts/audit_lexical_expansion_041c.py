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
# Historical production safeguards preserved for the 041C runtime format.
# The old s/i/n/pf fields described the superseded 028/019 generator and have
# no equivalent in the Morphalou-only 041C artifact: do not invent their values.
# Source integrity remains checked by the pinned Morphalou SHA above.
RUNTIME = ROOT / "data/lexical-expansion-runtime.json"
assert set(runtime) == {"g", "m", "v"}, "unexpected runtime schema"
assert RUNTIME.stat().st_size < 200_000, "oversized lexical sidecar"
assert all(isinstance(g, list) and len(g) >= 2 for g in groups)
assert all(isinstance(f, str) and f and not f.isspace() and " " not in f for f in forms)
assert "prendre" in forms and "prendront" in next(g for g in groups if "prendre" in g)
assert 'Occurrences exactes' in html
assert 'function singleWordQueryKey' in js
assert 'function expansionFormsFor' in js
assert 'function mergeExpansionMatches' in js
assert "return render([],[],{textualCount:textual.length,unresolvedTheme:true,textualAvailable:Boolean(textual.length)})" in js
assert 'data-show-text-search' in js
assert '>THÈME</button>' in html and '>MOTS</button>' in html
assert html.index('id="modeThemes"') < html.index('id="secondaryTools"')
assert html.index('id="modeExact"') < html.index('id="secondaryTools"')
assert html.index('id="results"') < html.index('id="exactExpansionOption"'), "morphology moved into advanced options after results"
print("041C lexical runtime contract PASS",len(groups),"groups",len(forms),"anchors")
