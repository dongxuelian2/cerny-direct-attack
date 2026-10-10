"""Build the minimal current manuscript and complete proof supplement."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SUPP=ROOT/'reproducibility'
INV=ROOT/'investigation'
EXTRA=['CODIMENSION_THREE_PROOF.md', 'CODIMENSION_THREE_UPPER_PROOF.md', 'EARLY_PAIR_TYPES.md', 'MATCHING_EARLY_EXCLUSION.md', 'PATH2_EARLY_EXCLUSION.md', 'PATH3_EARLY_EXCLUSION.md', 'SHORT_PAIR_STRUCTURE.md', 'TRIANGLE_EARLY_EXCLUSION.md', 'TRIANGLE_MIXING_CASE_A.md', 'TWO_BLOCK_PROOF.md', 'TYPE4_EARLY_EXCLUSION.md', 'TYPE5_EARLY_EXCLUSION.md', 'TYPE6_EARLY_EXCLUSION.md', 'TYPE7_EARLY_EXCLUSION.md', 'audit_matching_cube.py', 'audit_matching_distances.cpp', 'audit_path2_actions.cpp', 'audit_path2_domains.py', 'audit_path3_closed_T.cpp', 'audit_path3_closed_T_domains.py', 'audit_path3_mixing.cpp', 'audit_path3_mixing.py', 'audit_path3_no_T.cpp', 'audit_path3_no_T.py', 'audit_triangle_actions.cpp', 'audit_triangle_mixing.py', 'audit_type4_actions.cpp', 'audit_type4_domains.py', 'audit_type6_breakers.cpp', 'audit_type6_closed_II.cpp', 'audit_type6_domains.py', 'audit_type7_actions.cpp', 'audit_type7_breakers.cpp', 'audit_type7_domains.py', 'check_codimension_three.py', 'check_codimension_three_upper.py', 'check_matching_cube.py', 'check_two_block.py', 'check_type5_exclusion.py', 'codimension_three.py', 'codimension_three_audit.json', 'codimension_three_upper_audit.json', 'early_alphabet_pool_n6.json', 'early_alphabet_pool_n7.json', 'early_pair_alphabet_pool.py', 'formula_certificates.json', 'frontier_audit.json', 'frontier_certificates.json', 'matching_cube_audit.json', 'matching_cube_check.json', 'matching_cube_profiles.cpp', 'matching_cube_profiles.json', 'matching_distance_audit.json', 'path2_actions_independent.json', 'path2_domain_audit.json', 'path2_reduced_actions.json', 'path2_reduced_actions.py', 'path3_closed_T_actions.json', 'path3_closed_T_actions.py', 'path3_closed_T_audit.json', 'path3_closed_T_independent.json', 'path3_mixing_actions.json', 'path3_mixing_actions.py', 'path3_mixing_audit.json', 'path3_mixing_independent.json', 'path3_no_T_audit.json', 'path3_no_T_independent.json', 'triangle_actions_independent.json', 'triangle_mixing_audit.json', 'triangle_reduced_actions.json', 'triangle_reduced_actions.py', 'two_block_audit.json', 'two_block_certificates.json', 'two_block_family.py', 'type4_actions_independent.json', 'type4_domain_audit.json', 'type4_reduced_actions.json', 'type4_reduced_actions.py', 'type5_exclusion_audit.json', 'type6_breaker_independent.json', 'type6_closed_II_actions.json', 'type6_closed_II_actions.py', 'type6_closed_II_independent.json', 'type6_domain_audit.json', 'type7_actions_independent.json', 'type7_breaker_independent.json', 'type7_domain_audit.json', 'type7_reduced_actions.json', 'type7_reduced_actions.py', 'verify_certificates.py', 'verify_frontier.py']
EXTRA += ['COFINAL_PROOF.md', 'DEFECT_TWO_PROOF.md', 'cofinal_family.py', 'check_cofinal.py', 'check_boundary.py', 'cofinal_audit.json', 'boundary_audit.json', 'defect_two.py', 'check_defect_two.py', 'defect_two_audit.json', 'defect_one_audit.json', 'subset_bfs.py']
BASE=['generator.py', 'checker.py', 'data/certificates.json', 'data/verification.json', 'README.md', 'LICENSE']
OBSOLETE=['BINARY_OBSTRUCTION_PROOF.md', 'EXTENDED_BINARY_OBSTRUCTION_PROOF.md', 'ZERO_STATE_CUT.md', 'audit_extended_widths.cpp', 'audit_inverse_enumeration.py', 'audit_inverse_fibers.cpp', 'audit_inverse_fibers.py', 'binary_obstruction_audit.json', 'binary_obstruction_witness.json', 'check_binary_obstruction.py', 'check_extended_obstruction.py', 'check_n13_obstruction.py', 'compression_decision.cpp', 'compression_decision_extended.cpp', 'compression_decision_extended_independent.cpp', 'compression_decision_independent.cpp', 'compression_decision_inverse.cpp', 'compression_decision_inverse_zero.cpp', 'compression_decision_inverse_zero_fibers.cpp', 'decision_independent_n11.json', 'decision_independent_n5.json', 'decision_independent_n6.json', 'decision_independent_n7.json', 'decision_independent_n8.json', 'decision_independent_n9.json', 'decision_n11.json', 'decision_n5.json', 'decision_n6.json', 'decision_n7.json', 'decision_n8.json', 'decision_n9.json', 'extended_n12.json', 'extended_obstruction_audit.json', 'extended_width_audit.json', 'inverse_control_n5.json', 'inverse_enumeration_audit.json', 'inverse_fibers_audit.json', 'inverse_n12.json', 'inverse_zero_n13.json', 'inverse_zero_n13_fibers.json', 'n13_obstruction_audit.json']
README='# Supplement to Sharpness of the Avoid-or-Compress Bound for Reachable Images\n\nPython >=3.10 (standard library) and a C++17 compiler suffice. Keep assertions enabled; do not use Python -O or C++ -DNDEBUG.\n\n## Complete uniform compression proof (Theorem 6)\n\nRead CODIMENSION_THREE_UPPER_PROOF.md first; its twelve proof notes contain the full symbolic reductions and all case analyses. The upper is for arbitrary finite alphabets, strong connectivity and synchronization, n>=6; image reachability is not needed. It implies F_bin(n,n-3,r)=F(n,n-3,r)=min(n-r,9), n>=5, 1<=r<n-3, with the separately checked lower witnesses.\n\n    python -B check_codimension_three_upper.py --rerun --compiler clang++ --build-dir ../upper-build\n\nThis rebuilds the two complete nonidentity letter pools at n=6,7, sixteen uniform action domains and the matching cube, every independent C++ projection, the two full-row breaker audits through n=9, and all finite symbolic-domain controls. The matching check covers 30,240 distance vectors. Finite state-count controls support the symbolic proof; fresh-label projections are complete for every n. The artificial matching-chain and actual five-state boundary controls distinguish projected exit from compression. --build-dir holds only regenerated binaries and temporary profiles; it should be outside this supplementary directory.\n\nWithout --rerun the command checks all saved independent profiles, underlying-row closure flags, vectors, component reports and current source hashes. The source hashes in the new report are computed afresh; they are provenance, not a proof that an old source is unchanged. Release SHA256SUMS.txt binds the shipped bytes. Compiler wall time is not proof data.\n\n## Uniform lower constructions\n\n    python -B generator.py\n    python -B checker.py\n    python -B check_cofinal.py\n    python -B check_boundary.py\n    python -B check_defect_two.py\n    python -B check_codimension_three.py\n    python -B two_block_family.py\n    python -B check_two_block.py\n\nThe face/larger-gap generator and checker do not import each other: 437 instances through n=1025, 381 face and 56 larger-gap cases, ordinary subset BFS, matrix identity, strong connectivity and original-letter reaching/attaining/reset words. The codimension-three checker tests 180 instances through n=24. The two-block checker tests 221 instances through n=65: 216 use subset BFS and five use full pair-potential/cell-delay certificates. CODIMENSION_THREE_PROOF.md and TWO_BLOCK_PROOF.md give their uniform mathematical proofs. The cofinal checker tests 316 instances through n=39; the M=2g boundary checker tests 33 through n=30. The codimension-one and -two checker tests 378 and 300 instances through n=30. COFINAL_PROOF.md and DEFECT_TWO_PROOF.md give the complete uniform proofs, also included in the manuscript. The two-block upper 3m-1 is only claimed as a local construction value; exact maxima follow when q<=3m-1 meets the known upper q.\n\n## Finite exact frontier\n\n    python -B verify_certificates.py\n    python -B verify_frontier.py\n\nThe first checks all 165 triples through n=10. The second checks 290 literal binary witnesses: all 286 triples through n=12, (13,8,1), and (13,10,r), r=1,2,3. All 290 parameters are exact for both alphabet classes. The complete finite frontier ends at n=12. Other n=13 parameters are not classified by that file. The uniform codimension-three proof replaces the former binary-only covers; those completed historical computations are preserved outside the release and are unnecessary here.\n\nThe conjectured formula min(n-r,binom(n-s+2,2)) is refuted at every n>=11, s=n-3, 1<=r<=n-10, where both maxima are nine rather than ten. This remains a partial answer to Open Problem 4. No alphabet separation or all-parameter replacement formula is claimed. The determined region is m=0 (value one), 1<=m<=3 (value min(n-r,3m)), and m>=4 with n-r<=3m-1 (value n-r). Only the region m>=4, n-r>=3m remains unclassified as a whole; (13,9,1) is still in [11,12].\n\n## Exact contents\n\nThere are 109 files, all directly used by the current paper or its independent proof audits: source, proof notes, certificates and reports, this README and the upstream software LICENSE. No executables, solver dependencies, search logs, checkpoints or unrelated results enter the package. Reports regenerated by --rerun differ only in current-run provenance fields where specified; all mathematical profile/vector/count fields must coincide. The release builder lists every file explicitly.\n'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stage():
    intended=SUPP.resolve()
    for name in OBSOLETE:
        path=(SUPP/name).resolve()
        assert path.parent==intended
        if path.exists():path.unlink()
    for name in EXTRA:shutil.copyfile(INV/name,SUPP/name)
    (SUPP/'README.md').write_text(README,encoding='utf-8')
    actual={p.relative_to(SUPP).as_posix() for p in SUPP.rglob('*') if p.is_file()}
    assert actual==set(BASE+EXTRA),actual^set(BASE+EXTRA)

def archive(path, items):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for path_in, name in sorted(items, key=lambda item: item[1]):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 8, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(info, path_in.read_bytes())
    with zipfile.ZipFile(path) as check:
        assert check.testzip() is None
        assert check.namelist() == sorted(name for _, name in items)

def pack():
    release = ROOT / "release"
    release.mkdir(exist_ok=True)
    supp = [(SUPP / name, name) for name in BASE + EXTRA]
    source = [(ROOT / name, name) for name in ("main.tex", "references.bib")]
    docs = ["main.tex", "main.pdf", "references.bib", "README.md",
            "LITERATURE_NOVELTY_AUDIT.md", "PROOF_AUDIT.md",
            "VALIDATION.json", "SOURCE_PROVENANCE.json", "build_release.py"]
    components = [(ROOT / name, name) for name in docs] + [
        (p, "reproducibility/" + name) for p, name in supp]
    (ROOT / "SHA256SUMS.txt").write_text(
        "".join(f"{digest(p)}  {name}\n" for p, name in sorted(components, key=lambda z: z[1])),
        encoding="utf-8")
    bundle = components + [(ROOT / "SHA256SUMS.txt", "SHA256SUMS.txt")]
    archive(release / "reproducibility.zip", supp)
    source.append((release / "reproducibility.zip", "anc/reproducibility.zip"))
    archive(release / "arxiv-source.zip", source)
    archive(release / "submission-bundle.zip", bundle)
    names = ["arxiv-source.zip", "reproducibility.zip", "submission-bundle.zip"]
    (release / "ARCHIVE_SHA256SUMS.txt").write_text(
        "".join(f"{digest(release / name)}  {name}\n" for name in names),
        encoding="utf-8")
    print(json.dumps(dict(source_files=len(source), supplementary_files=len(supp),
                          bundle_files=len(bundle), hashes_written=True)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", action="store_true")
    args = parser.parse_args()
    if args.stage:
        stage()
    else:
        pack()
