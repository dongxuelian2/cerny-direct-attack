"""Checks for the publication contract and download rejection boundary."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class PublicationTests(unittest.TestCase):
    def test_single_status_and_unique_result_ids(self):
        data=json.loads((ROOT/'results/result_index.json').read_text(encoding='utf-8'))
        rows=data['results']
        self.assertEqual(len(rows),len({r['id'] for r in rows}))
        for row in rows:
            self.assertIn(row['status'],data['statuses'])
            for key in ('name','scope','source','proof_check_status','dependencies','priority'):
                self.assertTrue(row[key],(row['id'],key))
            self.assertTrue((ROOT/row['source']).exists())

    def test_frozen_formal_core_is_separate(self):
        data=json.loads((ROOT/'formal/modules.json').read_text(encoding='utf-8'))
        self.assertEqual(sum(m['stage']=='OpenMath frozen core' for m in data['accepted']),10)
        self.assertEqual(sum(m['stage']=='post-release research' for m in data['accepted']),1)
        self.assertFalse(set(data['excluded']) & {m['source'] for m in data['accepted']})

    def test_hydration_rejects_altered_asset(self):
        with tempfile.TemporaryDirectory() as folder:
            asset=Path(folder)/'altered.zip'
            asset.write_bytes(b'not the checksum-pinned scientific archive')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/hydrate_data.py'),'--asset',str(asset)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('SHA-256 mismatch',result.stderr)


if __name__=='__main__':unittest.main()
