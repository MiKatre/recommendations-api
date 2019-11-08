import urllib.request
import zipfile
from fastai.collab import Path

def download_ml100k():
  url = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'
  path = Path('app/data/')

  path.mkdir(parents=True, exist_ok=True)
  dest_zip = path/'ml-100k.zip'
  dest_unzip = path/'ml-100k'

  if not dest_unzip.exists():
    print('Downloading and extracting files...')
    urllib.request.urlretrieve(url, dest_zip)

    with zipfile.ZipFile(path/'ml-100k.zip', 'r') as ref:
      ref.extractall(path)

    print('Removing zip file...')
    dest_zip.unlink()
    print('Done !')

  else:
    print('Files already downloaded...')

  path = dest_unzip
  return path

def download_ml20m():
  url = 'http://files.grouplens.org/datasets/movielens/ml-20m.zip'
  path = Path('app/data/')

  path.mkdir(parents=True, exist_ok=True)
  dest_zip = path/'ml-20m.zip'
  dest_unzip = path/'ml-20m'

  if not dest_unzip.exists():
    print('Downloading and extracting files...')
    urllib.request.urlretrieve(url, dest_zip)

    with zipfile.ZipFile(path/'ml-20m.zip', 'r') as ref:
      ref.extractall(path)

    print('Removing zip file...')
    dest_zip.unlink()
    print('Done !')

  else:
    print('Files already downloaded...')

  path = dest_unzip
  return path


def build_dataset():
  return 'mixed pandas dataframe'