#!/usr/bin/env python3
"""Run the canonical thematic rebuild in a deterministic, regression-safe order.

Documentary PDF repairs are applied before semantic indexing. Deep indexing passes are then replayed
from books 9 through 44. The indexing passes are descriptive research aids; they do not assert an
exclusive interpretation of the Psalms.
"""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(script):
    print(f'\n=== {script} ===',flush=True)
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)

def repair_documentary_boundaries():
    print('\n=== audited PDF documentary repairs ===',flush=True)
    import repair_known_pdf_psalm_anomalies as repair
    for case in repair.CASES:
        repair.extract_case(case)
    repair.repair_book44_final_psalm()
    run('repair_book23_psalm128_numbering.py')
    run('repair_book32_psalm182.py')

def main():
    repair_documentary_boundaries()
    run('deepen_books09_11_semantic_evidence.py'); run('finalize_books09_11_semantic.py')
    run('deepen_books12_14_semantic_evidence.py'); run('finalize_books12_14_semantic.py')
    run('complete_book17_thematic.py'); run('deepen_books15_17_semantic_evidence.py'); run('finalize_books15_17_semantic.py')
    run('complete_books18_20_thematic.py')
    run('deepen_book18_semantic.py'); run('deepen_book18_semantic_part2.py')
    for n in range(1,7): run(f'deepen_book19_semantic_part{n}.py')
    for n in range(1,7): run(f'deepen_book20_semantic_part{n}.py')
    run('ground_books18_20_semantic_evidence.py'); run('finalize_book18_semantic.py'); run('finalize_book19_semantic.py'); run('finalize_book20_semantic.py')
    run('complete_books21_23_thematic.py')
    for n in range(1,9): run(f'deepen_book21_semantic_part{n}.py')
    run('ground_book21_semantic_evidence.py'); run('finalize_book21_semantic.py')
    for n in range(1,8): run(f'deepen_book22_semantic_part{n}.py')
    run('ground_book22_semantic_evidence.py'); run('finalize_book22_semantic.py')
    run('complete_books24_26_thematic.py'); run('complete_books27_30_thematic.py'); run('complete_books31_40_thematic.py'); run('complete_books41_44_thematic.py')
    run('deepen_book23_semantic_part1.py'); run('deepen_books23_25_semantic_evidence.py'); run('finalize_books23_25_semantic.py')
    for lo,hi in ((26,28),(29,31),(32,34),(35,37),(38,40),(41,43)):
        run(f'deepen_books{lo}_{hi}_semantic_evidence.py'); run(f'finalize_books{lo}_{hi}_semantic.py')
    run('deepen_book44_semantic_evidence.py'); run('finalize_book44_semantic.py')
    run('sync_thematic_documentary_status.py'); run('normalize_thematic_metadata.py'); run('build_book_contexts.py'); run('validate_thematic_index.py'); run('build_thematic_directory.py')
if __name__=='__main__': main()
