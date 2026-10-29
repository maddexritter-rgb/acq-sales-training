"""Portable library structure, retrieval, and installation regressions. Fictional probes."""
import importlib.util,json,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];skill=root/'skills/sales-call-audit';lib=skill/'brand/alex/library'
spec=importlib.util.spec_from_file_location('retrieval',skill/'scripts/find_coaching.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cards=json.loads((lib/'cards.json').read_text());assert len(cards)==100
assert len({c['id'] for c in cards})==len(cards)
coverage={s['source_id']:s for s in json.loads((lib/'coverage.json').read_text())['sources']}
for c in cards:
    for key in ('title','trigger','action','suggested_dialogue','branches','practice','do_not_apply'):assert c[key].strip(),(c['id'],key)
    page=(lib/(c['module']+'.md')).read_text()
    assert '## '+c['id']+' — ' in page
    for key in ('trigger','action','suggested_dialogue','branches','practice','do_not_apply'):assert c[key] in page,(c['id'],key)
    for a in c['sources']:assert 1<=a['start_line']<=a['end_line']<=coverage[a['source_id']]['line_count']
probes=[
 ('buyer corrected diagnosis reports already arrive','DIS06'),
 ('connection cutting out repeatedly repeat question','CTX05'),
 ('contradictory service information previous rep different offer','OFF09'),
 ('assistant will pay later promised payment not confirmed','CLS04'),
 ('genuine budget outside available resources','MON02'),
 ('partner joint decision authority','TIM06'),
 ('enterprise procurement security legal review','TIM09'),
 ('no show missed meeting','OPS05'),
 ('learner practice one buyer turn wait','MGR02'),
 ('invented tone confidence transcript without audio','DEL01'),
 ('current desired state obstacle','DIS04'),
 ('renewal cancellation guarantee conditions exclusions','MON06')]
for q,want in probes:
    found=[c['id'] for c in m.rank(cards,q,limit=5)]
    assert want in found,(q,want,found)
assert m.rank(cards,'zzzzzxnonexistent')==[]
assert all(c['module']=='02-discovery' for c in m.rank(cards,'buyer problem',module='02-discovery'))
with tempfile.TemporaryDirectory() as td:
    for host,dot in [('codex','.agents'),('claude','.claude')]:
        subprocess.run([sys.executable,str(skill/'scripts/install_skill.py'),host,'--project',td],check=True,capture_output=True)
        installed=Path(td)/dot/'skills/sales-call-audit'
        p=subprocess.run([sys.executable,str(installed/'scripts/find_coaching.py'),'--id','DIS06'],check=True,capture_output=True,text=True)
        assert json.loads(p.stdout)[0]['id']=='DIS06'
print('100 cards, Markdown/data parity, valid source ranges, 12 retrieval probes, empty/filter behavior, both installed retrieval paths: PASS')
