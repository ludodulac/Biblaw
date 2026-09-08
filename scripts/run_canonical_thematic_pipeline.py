#!/usr/bin/env python3
"""Run the canonical thematic rebuild in a deterministic, regression-safe order.

Documentary PDF repairs are applied before semantic indexing. Deep indexing passes are then replayed
from books 1 through 44. The indexing passes are descriptive research aids; they do not assert an
exclusive interpretation of the Psalms.

Historical Book 17 pilot extraction artefacts are normalized at the production boundary before
browser artefacts are built. The compact thematic runtime is built from validated sources, validates
its candidate before atomic replacement, and is then independently revalidated as the production
artifact. Generated search/catalog artefacts are followed by production-boundary integrity audits so
a successful canonical rebuild cannot silently publish stale or legacy attachment relationships.

Timing output is diagnostic only: it is never persisted into generated artefacts and therefore does
not affect reproducibility. Only completion scripts proven to read shared inputs and write disjoint
book ranges are run concurrently; their captured logs are replayed in deterministic script order.
"""
from __future__ import annotations
import subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TIMINGS=[]

def run(script):
    print(f'\n=== {script} ===',flush=True)
    started=time.perf_counter()
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
    elapsed=time.perf_counter()-started
    TIMINGS.append((script,elapsed))
    print(f'--- timing {script}: {elapsed:.3f}s',flush=True)

def _run_captured(script):
    started=time.perf_counter()
    proc=subprocess.run(
        [sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,text=True,
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
    )
    return script,time.perf_counter()-started,proc.returncode,proc.stdout

def run_parallel(scripts):
    """Run independent disjoint-output generators concurrently, with deterministic log replay."""
    scripts=list(scripts)
    group_started=time.perf_counter()
    with ThreadPoolExecutor(max_workers=len(scripts)) as pool:
        results=list(pool.map(_run_captured,scripts))
    for script,elapsed,returncode,output in results:
        print(f'\n=== {script} [parallel] ===',flush=True)
        if output:
            print(output,end='' if output.endswith('\n') else '\n',flush=True)
        TIMINGS.append((script,elapsed))
        print(f'--- timing {script}: {elapsed:.3f}s',flush=True)
        if returncode:
            raise subprocess.CalledProcessError(returncode,[sys.executable,str(ROOT/'scripts'/script)])
    print(f'--- timing parallel completion group: {time.perf_counter()-group_started:.3f}s',flush=True)

def repair_documentary_boundaries():
    print('\n=== audited PDF documentary repairs ===',flush=True)
    started=time.perf_counter()
    import repair_known_pdf_psalm_anomalies as repair
    for case in repair.CASES:
        repair.extract_case(case)
    repair.repair_book44_final_psalm()
    elapsed=time.perf_counter()-started
    TIMINGS.append(('audited PDF documentary repairs',elapsed))
    print(f'--- timing audited PDF documentary repairs: {elapsed:.3f}s',flush=True)
    run('repair_book23_psalm128_numbering.py')
    run('repair_book32_psalm182.py')

def print_timing_summary(total):
    print('\n=== canonical pipeline timings ===',flush=True)
    for name,elapsed in sorted(TIMINGS,key=lambda item:(-item[1],item[0]))[:12]:
        print(f'{elapsed:8.3f}s  {name}',flush=True)
    print(f'{total:8.3f}s  TOTAL canonical pipeline',flush=True)

def main():
    pipeline_started=time.perf_counter()
    repair_documentary_boundaries()
    run('normalize_book17_production_attachments.py')
    run('deepen_books01_02_semantic_evidence.py'); run('finalize_books01_02_semantic.py')
    run('deepen_books03_05_semantic_evidence.py'); run('finalize_books03_05_semantic.py')
    run('deepen_books06_08_semantic_evidence.py'); run('finalize_books06_08_semantic.py')
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
    run_parallel((
        'complete_books24_26_thematic.py',
        'complete_books27_30_thematic.py',
        'complete_books31_40_thematic.py',
        'complete_books41_44_thematic.py',
    ))
    run('deepen_book23_semantic_part1.py'); run('deepen_books23_25_semantic_evidence.py'); run('finalize_books23_25_semantic.py')
    for lo,hi in ((26,28),(29,31),(32,34),(35,37),(38,40),(41,43)):
        run(f'deepen_books{lo}_{hi}_semantic_evidence.py'); run(f'finalize_books{lo}_{hi}_semantic.py')
    run('deepen_book44_semantic_evidence.py'); run('finalize_book44_semantic.py')
    run('sync_thematic_documentary_status.py'); run('normalize_thematic_metadata.py'); run('build_book_contexts.py'); run('validate_thematic_index.py'); run('build_thematic_directory.py'); run('build_public_theme_directory.py'); run('audit_thematic_search_quality.py'); run('build_thematic_search_index.py'); run('validate_thematic_search_index.py'); run('build_thematic_connections.py'); run('validate_thematic_connections.py'); run('build_thematic_search_runtime.py'); run('validate_thematic_search_runtime.py'); run('build_browser_search_catalog.py'); run('audit_corpus_attachments.py'); run('audit_legacy_psalm_references.py')
    print_timing_summary(time.perf_counter()-pipeline_started)
if __name__=='__main__': main()
