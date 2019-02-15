import os, json, requests
import io
import pandas as pd

fields = [
    "file_name",
    "cases.submitter_id",
    "cases.diagnoses.days_to_death",
    "cases.diagnoses.vital_status"
    ]
fields = ",".join(fields)

cases_endpt = "https://api.gdc.cancer.gov/files"

with open("filter-RNAseq.json", 'r') as f:
        filters = json.load(f)

params = {
    "filters": json.dumps(filters),
    "fields": fields,
    "format": "TSV",
    "size": "10000" #HACK: modificar si los casos superan los hints
    }

response = requests.get(cases_endpt, params = params)
df = pd.read_csv(io.StringIO(response.text), sep='\t', header=0)
df = df.sort_values('file_name')
df.reset_index(inplace = True) 
print df
df.to_csv("DeadOrAlive.tsv", sep='\t')
