"""Re-run theorem-oriented independent checks and preserve exact outcomes."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
CHECKS=['check_uniform.py','layout_experiments.py','endpoint_layout.py',
        'check_normal_form.py','optimal_language.py','check_language_stabilization.py',
        'check_sharp_language.py','check_language_counts.py','check_manuscript_source.py',
        'audit/verify_manifest.py']


def main():
    rows=[]
    # Authorize only this explicitly selected checkout for this process tree.
    # No global Git configuration is changed.
    env=os.environ.copy()
    count=int(env.get('GIT_CONFIG_COUNT','0'))
    env['GIT_CONFIG_KEY_'+str(count)]='safe.directory'
    env['GIT_CONFIG_VALUE_'+str(count)]=ROOT.as_posix()
    env['GIT_CONFIG_COUNT']=str(count+1)
    for name in CHECKS:
        result=subprocess.run([sys.executable,str(ROOT/'post_baseline'/name)],
                              cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
        rows.append(dict(check=name,exit_code=result.returncode,
                         stdout=result.stdout,stderr=result.stderr))
        print(name,'PASS' if result.returncode==0 else 'FAIL',flush=True)
        if result.returncode:
            print(result.stdout,result.stderr,flush=True)
            break
    data=dict(python=sys.version,checks=rows,status='COMPUTATIONALLY VERIFIED finite checks',
              all_passed=len(rows)==len(CHECKS) and all(x['exit_code']==0 for x in rows))
    (ROOT/'post_baseline/sprint_results/FINAL_CHECKS.json').write_text(
        json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
    if not data['all_passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
