
from itertools import cycle

rows = []
ante_elements = 2
count=0
period=1290
fogli_guardia_ante=2
fogli=34
fogli_guardia_post=2
post_elements=2

# Parte	Componenti	descrizione	Elemento	sottoelemento	Numerazione_a	Titolo	Livello titolo	non_prima	non_dopo	varianti	materiale	fori_di_preparazione	peli_residui	aree_di_scalfo_residue	illustrazione	foratura	rigatura	filigrana	fascicolazione	lato_foglio palinsesto	colore	spessore note_conservative	ampiezza_mm	altezza_mm			

sides = cycle(('r','v'))
parchmentsides = cycle(('c','p'))
papersides = cycle(('a','b'))
parchmentsidesgregory = cycle(('c','p','p','c'))

# sesterno 6 foglio 12 pagine
#1,1,2,2,2,2,1,1,3,3,4,4,4,4,3,3
import math
numerobifogli = 3
current = 0.5
posizionefasc = 1
fascicolo = 1
numerofogli = 50
for i in range(numerofogli):
    print(math.ceil(current),current,posizionefasc)
    if posizionefasc < numerobifogli*2:
        current +=0.5
    if posizionefasc > numerobifogli*2:
        current -=0.5
    posizionefasc +=1
    if posizionefasc == numerobifogli*4+1:
        posizionefasc = 1
        fascicolo +=1
        current += numerobifogli + 0.5

def generaindicebifoglio(numerobifogli):
    current = 0.5
    posizionefasc = 1
    fascicolo = 1
    while True:
        yield math.ceil(current)
        if posizionefasc < numerobifogli*2:
            current +=0.5
        if posizionefasc > numerobifogli*2:
            current -=0.5
        posizionefasc +=1
        if posizionefasc == numerobifogli*4+1:
            posizionefasc = 1
            fascicolo +=1
            current += numerobifogli + 0.5



for i in ante_elements:
    rows.append([count,i,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
    count += 1
for i in range(fogli_guardia_ante*2):
    side = next(sides) 
    sd = "g%s%s"%(i+1,side)
    rows.append([count,sd,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
    count += 1
for i in range(fogli):
    side = next(sides) 
    sd = "%s%s"%(i+1,side)
    rows.append([count,sd,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
    count += 1
    side = next(sides)
    sd = "%s%s"%(i+1,side)
    rows.append([count,sd,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
    count += 1
for i in range(fogli_guardia_post*2):
    side = next(sides) 
    sd = "g%s%s"%(i+1,side)
    rows.append([count,sd,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
    count += 1
for i in post_elements:
    rows.append([count,i,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
    count += 1