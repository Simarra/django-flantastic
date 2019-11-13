"""
Download hudge geocoded file and only keep bakeries.
It also remove unwanted fields.
"""

from tqdm import tqdm
import logging
import pandas as pd
import tempfile
import os.path
from flantastic.data.definitions import (CHUNK_SIZE, COLS_TO_KEEP, COMPRESSION,
                          CSV_LINK, NAF_CODES, NAF_COL, TMP_CSV,
                          TMP_DIR, TMP_GZ_FILE)
import requests

logger = logging.getLogger(__name__)

def _download_file(url, local_filename):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=8192), desc="downloadig geosirene"): 
                if chunk: 
                    f.write(chunk)
    logger.info("Geosirene downloaded")



def download_bakeries():
    chunks = []

    if not os.path.isfile(TMP_CSV):

        # DOWNLOAD FILE
        if not os.path.isfile(TMP_GZ_FILE):
            _download_file(CSV_LINK, TMP_GZ_FILE)

        # GENERATE A CSV WITH BAKERIES ONLY
        for gm_chunk in tqdm(pd.read_csv(TMP_GZ_FILE,
                                    chunksize=CHUNK_SIZE,
                                    compression=COMPRESSION,
                                    usecols=COLS_TO_KEEP), desc="processing geosirene"):

            # get only bakeries
            tmp_res = gm_chunk[gm_chunk[NAF_COL].isin(NAF_CODES)]
            # DELETE GEOSCORE 0
            tmp_res = tmp_res[tmp_res.geo_score != float(0)]
            # do names
            tmp_res.enseigne.fillna(tmp_res.l1_normalisee, inplace=True)
            chunks.append(tmp_res)

        pd_result = pd.concat(chunks)
        pd_result.to_csv(TMP_CSV)
