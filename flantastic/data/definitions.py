import os
import tempfile

CSV_LINK = "http://data.cquest.org/geo_sirene/" + \
"last/etablissements_actifs.csv.gz"
CHUNK_SIZE = 2000
COMPRESSION = "gzip"
TMP_DIR = tempfile.gettempdir()
TMP_GZ_FILE = TMP_DIR + os.sep + 'etablissements_actifs.csv.gz'
TMP_CSV = TMP_DIR + os.sep + 'bakeries.csv'

NAF_COL = 'apet700'
NAF_CODES = ("1071C", "1071D")
COLS_TO_KEEP = ['siren',
                'codpos',
                'libcom',
                'enseigne',
                'apet700',
                'libapet',
                'nomen_long',
                'sigle', 'nom',
                'prenom',
                'civilite',
                'vmaj',
                'vmaj1',
                'vmaj2',
                'vmaj3',
                'datemaj',
                'latitude',
                'longitude',
                'geo_score',
                'geo_type',
                'geo_adresse',
                'geo_id',
                'geo_ligne',
                'geo_l4',
                'l1_normalisee',
                'geo_l5']
DELIMITER = ","
