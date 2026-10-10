"""One-time reference-title variant alignment, with pre-edit provenance.

DROPS metadata uses singular Word; the article PDF uses plural Words.
This changes the chosen citation-title convention, not a theorem or DOI.
"""
from pathlib import Path
import hashlib,json
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    previous=json.loads((ROOT/'investigation/AUXILIARY_AUDIT_20261009_18.json').read_text())
    for name,digest in previous['accepted_artifact_sha256'].items(): assert sha(ROOT/name)==digest
    files={}
    for table,base in [(ROOT/'SHA256SUMS.txt',ROOT),(ROOT/'release/ARCHIVE_SHA256SUMS.txt',ROOT/'release')]:
        for line in table.read_text().splitlines():
            digest,name=line.split('  ',1); assert sha(base/name)==digest
            files[str((base/name).relative_to(ROOT)).replace('\\','/')]=digest
    assert len(files)==121
    before=dict(status='pre_edit_verified',accepted_checksums=files,
        accepted_artifact_sha256=previous['accepted_artifact_sha256'],
        pdf_page_texts=[p.extract_text() for p in PdfReader(ROOT/'main.pdf').pages],
        chosen_convention='Article PDF plural Reset Words; publisher metadata singular Reset Word is a valid variant',
        primary_pdf='https://drops.dagstuhl.de/storage/00lipics/lipics-vol096-stacs2018/LIPIcs.STACS.2018.56/LIPIcs.STACS.2018.56.pdf',
        publisher_record='https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2018.56')
    (ROOT/'_qa/reference_variant_before.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
    for name in ('main.tex','references.bib'):
        path=ROOT/name; data=path.read_bytes()
        assert data.count(b'Shortest Reset Word}')==1
        data=data.replace(b'Shortest Reset Word}',b'Shortest Reset Words}')
        path.write_bytes(data)
    path=ROOT/'LITERATURE_NOVELTY_AUDIT.md';text=path.read_text(encoding='utf-8')
    old="The bibliography uses the publisher's canonical STACS title in the singular, *Shortest Reset Word*. The PDF heading and arXiv title use the plural; this title variation does not denote a different result. The MFCS author name is Vojtěch Vorel; all diacritics are encoded in LaTeX/BibTeX."
    new="Rechecked on 9 October 2026: the DROPS publisher record and exported BibTeX use the singular, *Shortest Reset Word*, whereas the article PDF heading and arXiv title use the plural, *Shortest Reset Words*. The manuscript and its BibTeX now consistently follow the article PDF's plural title. Both title variants identify the same DOI; the singular publisher metadata is not treated as an error. The MFCS author name is Vojtěch Vorel; all diacritics are encoded in LaTeX/BibTeX."
    assert text.count(old)==1; path.write_text(text.replace(old,new),encoding='utf-8')
    path=ROOT/'SOURCE_PROVENANCE.json';data=json.loads(path.read_text(encoding='utf-8'))
    data['bibliography_title_variant_alignment']=dict(date='2026-10-09',key='szykula2018',
        title_used='Improving the Upper Bound on the Length of the Shortest Reset Words',
        convention=before['chosen_convention'],primary_pdf=before['primary_pdf'],publisher_record=before['publisher_record'],
        mathematical_source_unchanged=True,doi='10.4230/LIPIcs.STACS.2018.56')
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('121 pre-edit hashes verified; citation title aligned with article PDF; no mathematical edits')

if __name__=='__main__':main()
