from Bio import Entrez
import gget


Entrez.email = "kallefruitema@gmail.com"

a = gget.ref("panthera_pardus")
print(a)


id = 'ENSPPRT00000008335.1'
x = Entrez.efetch(db='gene', id=id, rettype='gb', retmode='text')
print(x.read())

print("="*50)

c = gget.search(id,"panthera_pardus")
print(c)

print("="*50)

z = gget.seq(id)
print(z)
# git config --global user.email "you@example.com"
# git config --global user.name "Your Name"