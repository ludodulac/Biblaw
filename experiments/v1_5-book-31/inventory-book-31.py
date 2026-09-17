#!/usr/bin/env python3
import json
from pathlib import Path

BASE = "ffefe0f92fca0d8580ed84332f8c2d6a5d621b1b"
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/documentary-extractions/psalms/book-31"
EXPECTED = list(range(188, 206))

# Diagnostic references only: no consolidation, no family, no relation nature.
# Each group names a local documentary zone where residual autonomy deserves review.
DENSE_ZONES = [
    {"psalm":188,"refs":["subject-001","subject-002","subject-004","subject-005","subject-011","subject-014","subject-027"],"question":"Église / hiérarchie / corps de l’Église / dirigeants / Nation / structures / fonction : distinguer institutions, fonctions et architecture commune sans fusion préalable."},
    {"psalm":190,"refs":["subject-002","subject-003","subject-005","subject-007","subject-008","subject-010"],"question":"pensée / structure subtile / origine / mondes derrière / maîtrise / discernement : plusieurs branches peuvent dépendre du tronc pensée tout en conservant des opérations documentaires propres."},
    {"psalm":191,"refs":["subject-001","subject-002","subject-003","subject-011","subject-010","subject-004","subject-013"],"question":"Ange / rencontre / vivre avec / alliance / homme-Ange / tradition / transformation : séparer étapes, relation, cadre et transformation."},
    {"psalm":193,"refs":["subject-004","subject-005","subject-006","subject-007","subject-008","subject-011","subject-012"],"question":"pensée / mondes subtils / énergie créatrice / canalisation / corps catalyseur / prêtres et rois / gouverner : chaîne causale dense, sans présumer que ses maillons sont fusionnables."},
    {"psalm":203,"refs":["subject-001","subject-002","subject-003","subject-004","subject-005","subject-006","subject-007","subject-008"],"question":"zone initiale du psaume à relire comme architecture locale avant tout accès transverse ; le script vérifie les références mais ne les requalifie pas."},
    {"psalm":205,"refs":["subject-001","subject-002","subject-003","subject-004","subject-005","subject-006"],"question":"zone initiale du psaume à soumettre au même test d’autonomie résiduelle, sans inférer de famille à partir du lexique."}
]

# Recurrences are observations to inspect later, never families.
RECURRENCE_LABELS = [
    "homme", "Dieu", "âme", "corps", "pensée", "Lumière", "terre",
    "Nation Essénienne", "sainte assemblée", "Église", "religion",
    "transformation", "discipline", "conscience", "Bien commun"
]

def load():
    rows=[]
    for n in EXPECTED:
        p=DATA/f"psalm-{n}.json"
        if not p.exists(): raise SystemExit(f"missing {p}")
        d=json.loads(p.read_text(encoding="utf-8"))
        assert d["protocolVersion"] == "1.5"
        assert d["source"]["recordId"] == f"book-31-psalm-{n}"
        subjects=d.get("subjects",[])
        ids=[s["localId"] for s in subjects]
        assert len(ids)==len(set(ids))
        rows.append((n,d,subjects))
    return rows

def ref_exists(rows, psalm, local_id):
    d=next(d for n,d,s in rows if n==psalm)
    return any(s["localId"]==local_id for s in d["subjects"])

def main():
    rows=load()
    counts={str(n):len(s) for n,d,s in rows}
    for z in DENSE_ZONES:
        for r in z["refs"]:
            assert ref_exists(rows,z["psalm"],r), (z["psalm"],r)
    rec=[]
    for label in RECURRENCE_LABELS:
        hits=[]
        needle=label.casefold()
        for n,d,subjects in rows:
            for s in subjects:
                if needle in s.get("localSubject","").casefold():
                    hits.append({"recordId":d["source"]["recordId"],"localId":s["localId"]})
        psalms=sorted({int(h["recordId"].rsplit("-",1)[1]) for h in hits})
        if len(psalms)>=2:
            rec.append({"observedLabel":label,"psalms":psalms,"refs":hits,
                        "status":"RECURRENCE-TO-REVIEW-NOT-A-FAMILY"})
    out={
      "recordType":"experimental-v1.5-book-31-inventory",
      "baseCommit":BASE,
      "scope":{"book":31,"title":"La nouvelle Pâque","psalms":[188,205],"expectedFiles":18},
      "controls":{"files":len(rows),"continuous": [n for n,_,_ in rows]==EXPECTED,
                  "noPrimaryMutation":"This script is read-only over V1.5 primaries.",
                  "noImportedBook44Families":True},
      "subjectCounts":counts,
      "totalSubjects":sum(counts.values()),
      "minimum":{"count":min(counts.values()),"psalms":[int(k) for k,v in counts.items() if v==min(counts.values())]},
      "maximum":{"count":max(counts.values()),"psalms":[int(k) for k,v in counts.items() if v==max(counts.values())]},
      "diagnostic":{"localDensityZones":DENSE_ZONES,
                    "residualAutonomyTest":"Remove the supposed parent/trunk context: does the referenced subject still carry a sufficiently determined documentary matter of its own? No merge is performed here.",
                    "transverseRecurrences":rec,
                    "distinction":{"localDensity":"multiple matters or branches concentrated inside one psalm","transversality":"a documented matter or angle recurring across several psalms"}},
      "prohibitions":["no family","no attachment","no DIRECT/FONCTIONNEL","no consolidation rationale","no alias","no merge","no navigation"]
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
