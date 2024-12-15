import main
from urllib.request import urlretrieve
from urllib.error import URLError

http = "https://arxiv.org/pdf"

id_arxiv = str(input("ID or link: "))

if id_arxiv.startswith("http") or id_arxiv.startswith("https") or id_arxiv.startswith("arxiv.org"):
    link = id_arxiv
elif id_arxiv.startswith("arXiv:"):
    id_arxiv = id_arxiv[6:]
    link = '/'.join([http,id_arxiv])
else:
    link = '/'.join([http,id_arxiv])

sep = '\\'
try:
    file,_= urlretrieve(link)
except URLError:
    try:
        file,_= urlretrieve(link+'.pdf')
    except:
        print("There has been a problem finding the site. Try again with the URL from your web browser.")
except:
    print("There has been a problem. Try to insert the URL from the web browser.")
name=file.split(sep)[-1]
main.QRArxiv(file,sep=sep,shortname='.'.join((name,'pdf')),id_arxiv=id_arxiv)
print("The file {} is ready to eat.".format(name))
