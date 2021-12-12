import  datetime
import calendar

def convertdate(text):
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return datetime.date(year, month, day)

    dictmes = {'gennaio': 1,
    'febbraio': 2,
    'marzo': 3,
    'aprile': 4,
    'maggio': 5,
    'giugno': 6,
    'luglio': 7,
    'agosto': 8,
    'settembre': 9,
    'ottobre': 10,
    'novembre': 11,
    'dicembre': 12}

    convdict = {'N': 0,
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
    'XI': 11,
    'XII': 12,
    'XIII': 13,
    'XIV': 14,
    'XV': 15,
    'XVI': 16,
    'XVII': 17,
    'XVIII': 18,
    'XIX': 19,
    'XX': 20,
    'XXI':21}

    letconv = {"in.":[0,-90],
                "ex.":[90,0],
                "med.":[25,-25],
                "metà":[25,-25],
                "1.metà":[0,-50],
                "2.metà":[50,0],
                "1.quarto":[0,-75],
                "2.quarto":[25,-50],
                "3.quarto":[50,-25],
                "4.quarto":[70,0]}
    notes = ""
    if text.isdigit():
        # 1234
        final = int(text)+1
        return "%s-01-01"%text.zfill(4),"%s-01-01"%str(final).zfill(4),notes

    splitted = text.split(" ")  
    modi,modf = 0,0
    if splitted[0].lower() in dictmes.keys():
        # Agosto 453
        date = datetime.datetime(int(splitted[1]),dictmes[splitted[0].lower()],1,0,0,0)
        fdate = add_months(date,1)
        notes = " ".join(splitted[2:])
        return date.strftime("%Y-%m-%d"),fdate.strftime("%Y-%m-%d"),notes
    
    if splitted[1].lower() in dictmes.keys():
        # 12 Dicembre 1234
        date = datetime.datetime(int(splitted[2]),dictmes[splitted[1].lower()],int(splitted[0]),0,0,0)
        fdate = date + datetime.timedelta(days=1)
        notes = " ".join(splitted[3:])
        return date.strftime("%Y-%m-%d"),fdate.strftime("%Y-%m-%d"),notes

    if "-" in splitted[0]:
        # 1809-12-2
        y,m,d = splitted[0].split("-")
        date = datetime.datetime(int(y),int(m),int(d),0,0,0)
        fdate = date + datetime.timedelta(days=1)
        notes = " ".join(splitted[1:])
        return date.strftime("%Y-%m-%d"),fdate.strftime("%Y-%m-%d"),notes

    # if "/" in splitted[1]:
    #     versione MANUS
    #     # sec. XI/XII
    #     st,fn = splitted[1].split("/")
    #     final = convdict[fn]
    #     starting = convdict[st]
    #     print(starting*100+91,final*100+10)
    #     notes = " ".join(splitted[1:])
    #     return "%s-01-01"%(starting*100+91),"%s-01-01"%(final*100+10),notes
 
    if "/" in text:
        # "saec. XIII ex./XIV in."
        # sec. XI/XII
        notes = ""
        st,fn = text.split("/")
        stsp = st.split(" ")
        fnsp = fn.split(" ")
        initsec = convdict[stsp[1]] - 1
        finsec = convdict[fnsp[0]]
        ij = 0
        ig = 0
        if len(stsp) > 2:
            ij = letconv[stsp[2]][0]
            #print(ij)
        if len(fnsp) > 1:
            if fnsp[1] in letconv.keys():
                ig = letconv[fnsp[1]][1]
                notes = " ".join(fnsp[2:])
            if fnsp[1].strip('.') in letconv.keys():
                ig = letconv[fnsp[1].strip('.')][1]
                notes = " ".join(fnsp[2:])
        #print(initsec*100+ij,finsec*100+ig)
        return "%s-01-01"%str(initsec*100+ij).zfill(4),"%s-01-01"%str(finsec*100+ig).zfill(4),notes
    
    if splitted[1] in convdict.keys():
        century = splitted[1]
    else:
        print("Secolo non identificato")
    if len(splitted) > 2:
        if splitted[2] in letconv.keys():
            modi,modf = letconv[splitted[2]]

    final = convdict[century]
    starting = final -1
    notes = " ".join(splitted[3:])
    #print(starting*100+1+modi,final*100+modf)
    return "%s-01-01"%str(starting*100+1+modi).zfill(4),"%s-01-01"%str(final*100+modf).zfill(4),notes


convertdate("14 Dicembre 534") == ('0534-12-14', '0534-12-15','')
convertdate("Agosto 1891 (non ci sono note)") == ('1891-08-01', '1891-09-01', '(non ci sono note)')
convertdate("14 Dicembre 534 (come desunto dal testo)")
convertdate("sec. XII ex.")
convertdate("sec. XII 1.metà")
convertdate("sec. XII med.")
convertdate("sec. XII in.")
convertdate("sec. XII in.")
convertdate("sec. XII ex.")
convertdate("sec. XII med.")
convertdate("sec. XII metà")
convertdate("sec. XII 1.metà")
convertdate("sec. XII 2.metà")
convertdate("sec. XII 1.quarto")
convertdate("sec. XII 2.quarto")
convertdate("sec. XII 3.quarto")
convertdate("sec. XII 4.quarto")
convertdate("sec. XII 4.quarto.")
convertdate("sec. XII/XIII")
convertdate("sec. XII 1.metà/XIV 2.quarto")

