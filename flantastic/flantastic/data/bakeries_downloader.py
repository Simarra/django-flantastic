"""
Download hudge geocoded file and only keep bakeries.
It also remove unwanted fields.
"""

import pandas as pd
import wget
import tempfile
import os.path
from .definitions import (CHUNK_SIZE, COLS_TO_KEEP, COMPRESSION,
                          CSV_LINK, NAF_CODES, NAF_COL, TMP_CSV,
                          TMP_DIR, TMP_GZ_FILE)

chunks = []

if not os.path.isfile(TMP_CSV):

    # DOWNLOAD FILE
    if not os.path.isfile(TMP_GZ_FILE):
        wget.download(CSV_LINK, TMP_GZ_FILE)

    # GENERATE A CSV WITH BAKERIES ONLY
    for gm_chunk in pd.read_csv(TMP_GZ_FILE,
                                chunksize=CHUNK_SIZE,
                                compression=COMPRESSION,
                                usecols=COLS_TO_KEEP):
        tmp_res = gm_chunk[gm_chunk[NAF_COL].isin(NAF_CODES)]
        tmp_res.enseigne.fillna(tmp_res.l1_normalisee, inplace=True)
        chunks.append(tmp_res)

    pd_result = pd.concat(chunks)
    pd_result.to_csv(TMP_CSV)
