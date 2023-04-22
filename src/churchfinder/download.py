import os

import requests


def download_pdf_to_file(url, dir, filename):

    r = requests.get(url, stream=True)
    chunk_size = 2000
    if filename is None:
        filename = self.date + ".pdf"

    with open(os.path.join(dir, os.path.join(dir, filename)), "wb") as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
