import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import zipfile
import shutil

def download(remote, local):
    r = requests.get(remote)
    open(local, 'wb').write(r.content)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def create_hq(capitulo):
    download_path = "download/"
    hqs_path = "hqs/"

    if capitulo < 10:
        name = "000" + str(capitulo)

    elif capitulo < 100:
        name = "00" + str(capitulo)

    elif capitulo < 1000:
        name = "0" + str(capitulo)
    else:
        name = str(capitulo)
    
    if os.path.isdir(download_path):
        shutil.rmtree(download_path)


    if not os.path.isdir(download_path):
        os.makedirs(download_path)
    if not os.path.isdir(hqs_path):
        os.makedirs(hqs_path)

    r = requests.get("https://www.hqbr.com.br/hqs/Hellblazer/capitulo/"+str(capitulo)+"/leitor/0#1")
    soup = BeautifulSoup(r.content)

    all_images = (soup.find_all('script')[4].text.split('pages = [')[1].split(']')[0].split(","))

    for i in all_images:
        i = i.replace('"', '')
        path_remote = "https://www.hqbr.com.br" + i
        path_local = download_path + i.split("/")[-1]
        print("\t\t",path_remote,flush=True)
        download(path_remote, path_local)

    zipf = zipfile.ZipFile(hqs_path+'Hellblazer(BR)'+name +
                           '.cbr', 'w', zipfile.ZIP_DEFLATED)
    zipdir(download_path, zipf)
    zipf.close()
    shutil.rmtree(download_path)

for i in list(range(237, 238)):
    try:
        create_hq(i)
    except:
        print("ERROR: " + str(i))
    