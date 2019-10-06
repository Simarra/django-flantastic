"""
Download hudge geocoded file and only keep bakeries.
It also remove unwanted fields.
"""

import pandas as pd
import wget
import tempfile
import os.path

CSV_LINK = "http://data.cquest.org/geo_sirene/last/etablissements_actifs.csv.gz"
CHUNK_SIZE = 2000
COMPRESSION = "gzip"
TMP_DIR = tempfile.gettempdir()
TMP_FILE = TMP_DIR + os.sep + 'etablissements_actifs.csv.gz'

NAF_COL = 'apet700'
NAF_CODES = ("1071C", "1071D")
COLS_TO_KEEP = ['siren', 'codpos', 'libcom',  'enseigne',  'apet700', 'libapet',  'nomen_long', 'sigle', 'nom', 'prenom', 'civilite',  'vmaj', 'vmaj1', 'vmaj2', 'vmaj3', 'datemaj', 'latitude', 'longitude', 'geo_score', 'geo_type', 'geo_adresse', 'geo_id', 'geo_ligne', 'geo_l4', 'geo_l5']

chunks = []

if not os.path.isfile(TMP_FILE): 
    wget.download(CSV_LINK, TMP_FILE )

for gm_chunk in pd.read_csv(TMP_FILE, chunksize=CHUNK_SIZE, compression=COMPRESSION, usecols=COLS_TO_KEEP):
    tmp_res = gm_chunk[gm_chunk[NAF_COL].isin(NAF_CODES)]
    tmp_res.enseigne.fillna(tmp_res.l1_normalisee, inplace=True)
    chunks.append(tmp_res)

pd_result = pd.concat(chunks)
pd_result.to_csv('myres.csv')


