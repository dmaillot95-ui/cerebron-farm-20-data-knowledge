import json, os
from pathlib import Path
from hf_gradio import gradio_client

role=os.environ['ROLE']
model=os.environ['MODEL']
focus=os.environ.get('FOCUS','data and knowledge systems')
mission=Path('mission/DATA-KNOWLEDGE-MISSION.md').read_text()
prompt=f'''You are {role} in CEREBRON Farm 20 Data Knowledge.
Focus: {focus}
Mission rules:\n{mission}
Return a concise structured analysis with: INPUT ASSUMPTIONS, METHOD, CLAIMS, EVIDENCE/PROVENANCE REQUIREMENTS, CONTRADICTIONS, UNKNOWNS, FAILURE MODES, RECOMMENDATIONS, VERDICT.
Do not treat generated text as evidence.'''
Path('results').mkdir(exist_ok=True)
out={'role':role,'model':model,'focus':focus,'status':'failed'}
try:
    client=gradio_client.Client(model)
    result=client.predict(message=prompt, api_name='/chat')
    out.update(status='success', result=result)
except Exception as e:
    out['error']=repr(e)
Path(f'results/{role}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
