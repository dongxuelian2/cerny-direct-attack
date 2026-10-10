"""Verify the citation-only paper change and current release bytes.

No historic 61/97-file QA or mathematical audit is rerun/overwritten.
"""
from pathlib import Path
import hashlib,json,re,sys,zipfile
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));import build_release

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    old=json.loads((ROOT/'_qa/reference_variant_before.json').read_text(encoding='utf-8'))
    for name in ('main.tex','references.bib'):
        data=(ROOT/name).read_bytes()
        assert data.count(b'Shortest Reset Words}')==1
        reverse=data.replace(b'Shortest Reset Words}',b'Shortest Reset Word}')
        assert hashlib.sha256(reverse).hexdigest()==old['accepted_artifact_sha256'][name]
    assert not re.search('Warning|Overfull|Underfull|undefined|Error',(ROOT/'main.log').read_text(errors='replace'))
    pdf=PdfReader(ROOT/'main.pdf');assert len(pdf.pages)==7
    assert pdf.metadata.title=='Sharpness of the Avoid-or-Compress Bound for Reachable Images'
    for i,(page,previous) in enumerate(zip(pdf.pages,old['pdf_page_texts']),1):
        now=' '.join(page.extract_text().split())
        prior=' '.join(previous.split()).replace('Shortest Reset Word','Shortest Reset Words')
        assert now==prior,('Unexpected PDF content change',i)
        assert (ROOT/'_qa'/f'reference-variant-page-{i}.png').is_file()
    tex=(ROOT/'main.tex').read_text(encoding='utf-8');bib=(ROOT/'references.bib').read_text(encoding='utf-8')
    assert set(re.findall(r'\\bibitem\{([^}]+)\}',tex))==set(re.findall(r'@\w+\{([^,]+),',bib))
    expected=set(build_release.BASE+build_release.EXTRA);assert len(expected)==109
    actual={p.relative_to(ROOT/'reproducibility').as_posix() for p in (ROOT/'reproducibility').rglob('*') if p.is_file()}
    assert actual==expected
    unchanged=[];changed=[]
    for name,digest in old['accepted_checksums'].items():
        (unchanged if sha(ROOT/name)==digest else changed).append(name)
    allowed={'main.tex','main.pdf','references.bib','LITERATURE_NOVELTY_AUDIT.md','VALIDATION.json',
        'SOURCE_PROVENANCE.json','release/arxiv-source.zip','release/submission-bundle.zip'}
    if '--archives' not in sys.argv:
        assert set(changed)<=allowed
        validation=json.loads((ROOT/'VALIDATION.json').read_text(encoding='utf-8'))
        validation['date']='2026-10-09'
        validation['bibliography_title_variant_alignment']=dict(key='szykula2018',
            uses_article_pdf_plural_title=True,publisher_singular_variant_preserved_in_audit=True,
            source_diff_is_title_only=True,pdf_text_diff_is_title_only=True,
            pdf_pages=7,latex_warnings=0,all_current_pdf_pages_visually_reviewed=True,
            mathematical_claims_parameters_and_supplement_unchanged=True)
        (ROOT/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
        print('7 pages, zero warnings, source/PDF text differ only in citation title; 109 supplement files unchanged')
        return
    assert set(changed)==allowed,(changed,allowed)
    assert sha(ROOT/'release/reproducibility.zip')==old['accepted_artifact_sha256']['release/reproducibility.zip']
    for name in expected:
        assert sha(ROOT/'reproducibility'/name)==old['accepted_checksums']['reproducibility/'+name]
    for archive,entries in [('arxiv-source.zip',{'main.tex','references.bib','anc/reproducibility.zip'}),('reproducibility.zip',expected)]:
        with zipfile.ZipFile(ROOT/'release'/archive) as z:
            assert z.testzip() is None and set(z.namelist())==entries
            for entry in entries:
                path=(ROOT/entry if entry!='anc/reproducibility.zip' else ROOT/'release/reproducibility.zip') if archive=='arxiv-source.zip' else ROOT/'reproducibility'/entry
                assert z.read(entry)==path.read_bytes()
    with zipfile.ZipFile(ROOT/'release/submission-bundle.zip') as z:
        assert z.testzip() is None and len(z.namelist())==119
        for name in z.namelist(): assert z.read(name)==(ROOT/name).read_bytes(),name
    checks=0
    for table,base in [(ROOT/'SHA256SUMS.txt',ROOT),(ROOT/'release/ARCHIVE_SHA256SUMS.txt',ROOT/'release')]:
        for line in table.read_text().splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
    assert checks==121
    result=dict(status='pass',date='2026-10-09',source_diff_is_title_only=True,pdf_text_diff_is_title_only=True,
        pdf_pages=7,latex_warnings=0,visually_reviewed_current_pages=7,
        mathematical_claims_and_parameters_unchanged=True,supplement_files_unchanged=109,
        reproducibility_archive_byte_identical=True,current_checksum_entries_verified=checks,
        changed_previously_checksummed_files=sorted(changed),
        accepted_artifact_sha256={name:sha(ROOT/name) for name in old['accepted_artifact_sha256']},
        source_sha256={Path(__file__).name:sha(Path(__file__))},
        limits='Citation title variant alignment only; PDF plural and publisher metadata singular are both valid titles for the same DOI.')
    (ROOT/'_qa/reference_variant_release_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
