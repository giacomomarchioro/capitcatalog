# -*- coding: utf-8 -*-
# app.py

from sys import prefix
from flask import Flask, render_template,url_for, request, redirect,jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from databasecredential import connectionstring
from werkzeug.datastructures import MultiDict
import json
import datetime
import ast
from bson.objectid import ObjectId
from converter import convertdate
# pprint library is used to make the output look more pretty
from pprint import pprint
import re
from bson.json_util import dumps
import forms


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(connectionstring)
#db=client.admin
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)


#var = client.capitolare.codici.find_one({segnatura_idx: 'm0257_0'}) 

def convertdatesafe(date):
    try:
        return convertdate(date)
    except:
        return ("","","")


def sort_dec_int(var):
	try:
		var['descrizione_interna'] = sorted(var['descrizione_interna'], key= lambda s: list(map(int, s['Descrizione_interna_id'].split('.'))))
	except ValueError:
		return "Errorre ID descrizione interna"

def sort_copisti(var):
	try:
		var['copisti'] = sorted(var['copisti'], key= lambda s: s['id_cop'])
	except ValueError:
		return "Errorre ID descrizione coppisti"

def sort_annotazioni(var):
	try:
		var['annotazioni_marginali'] = sorted(var['annotazioni_marginali'], key= lambda s: s['Id_anno'])
	except ValueError:
		return "Errorre ID descrizione annotazioni"

def sort_storia(var):
	try:
		var['storia_del_manoscritto'] = sorted(var['storia_del_manoscritto'], key= lambda s: s['Id_AT'])
	except ValueError:
		return "Errorre ID storia del manoscritto."

def sort_DescEst(var):
	try:
		var['descrizione_esterna'] = sorted(var['descrizione_esterna'], key= lambda s: s['Descrizione_Esterna_Segnatura'])
	except ValueError:
		return "Errorre Descrizione Esterna non disponibile."

# Initialize app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'sose1231crext'


@app.route('/', methods=['GET', 'POST'])
def index():
    varx = client.capitolare.codici.find({'version': 1})
    form = forms.NewRecord()
    stato = ""
    if form.validate_on_submit():
        #import pdb; pdb.set_trace()
        notvalidchr = "~:/?#[]@!$&'()*+,;= "
        if any((c in notvalidchr) for c in form.segnatura_idx.data):
            stato = ["alert alert-danger","I seguenti caratteri (~:/?#[]@!$&'()*+,;=) e gli spazi non possono essere usati nell'ID"]
            return render_template(
                'homepage.html',varx=varx, form=form, stato=stato)

        test = client.capitolare.codici.find({'version': 1,
        'segnatura_idx':form.segnatura_idx.data})
        
        if test.count() > 0:
            stato = ["alert alert-danger","ID già usato!"]
        
        else:
            data_dict = {}
            data_dict['created'] = datetime.datetime.utcnow()
            data_dict['last_modified'] = datetime.datetime.utcnow()
            data_dict['segnatura_idx'] = form.segnatura_idx.data
            data_dict['status'] = "appena creato"
            data_dict['version'] = 1
            client.capitolare.codici.insert_one(data_dict)
            access_url = url_for('insertfield', segnatura=form.segnatura_idx.data)
            stato = ["alert alert-success",
            "Nuovo record inserito con successo! Accedilo al seguente <a href='%s'> link </a>linkattraverso la tabella principale" %access_url]

        form.segnatura_idx.data
        print(form.data)
        #return redirect('/success')
    return render_template(
        'homepage.html',varx=varx, form=form, stato=stato)

@app.route('/insertfield/<segnatura>', methods=['GET', 'POST'])
def insertfield(segnatura):
    varx = client.capitolare.codici.find_one({'segnatura_idx': segnatura})
    #import pdb; pdb.set_trace()
    #form = MainForm(MultiDict(varx))
    form = forms.MainForm()
    #form.populate_obj(varx)
    template_formP = forms.Parte(prefix='parte-_-')
    template_form = forms.DescInt(prefix='descrizione_interna-_-')
    template_form2 = forms.Copisti(prefix='copisti-_-')
    template_form3 = forms.AnnotazioniMarg(prefix='annotazioni_marginali-_-')
    template_form4 = forms.Storia_del_manoscritto(prefix='storia_del_manoscritto-_-')
    if varx is not None:
        if varx['status'] != 'appena creato':
            descrizioni_esterne_id = [(i['Descrizione_Esterna_Segnatura'],i['Descrizione_Esterna_Segnatura']) for i in varx['descrizione_esterna']]
            descrizioni_esterne_id =  list(reversed(descrizioni_esterne_id))
            descrizioni_esterne_id2 = descrizioni_esterne_id + [('altro','altro')]
            if descrizioni_esterne_id[0] != ("",""): 
                template_form.Descrizione_Esterna_Segnatura.choices = descrizioni_esterne_id
                template_form2.Descrizione_Esterna_Segnatura.choices = descrizioni_esterne_id
                template_form3.Descrizione_Esterna_Segnatura.choices = descrizioni_esterne_id
                template_form4.Descrizione_Esterna_Segnatura.choices = descrizioni_esterne_id2


    template_form5 = forms.Facsimile(prefix='facsimile-_-')
    template_form6 = forms.DescEst(prefix='descrizione_esterna-_-')
    log = "n.d."   
    if form.validate_on_submit():
        # Create race
        #new_race = Race()
        #import pdb; pdb.set_trace()
        print("Entrato")
        data_dict = form.data
        if 'csrf_token' in data_dict.keys():
            del data_dict['csrf_token']
            print("Deleted csrf")
        data_dict['last_modified'] = datetime.datetime.now()
        #client.capitolare.codici.insert_one(data_dict)
        sort_copisti(data_dict)
        sort_storia(data_dict)
        sort_annotazioni(data_dict)
        sort_dec_int(data_dict)
        sort_DescEst(data_dict)
        for anno in data_dict['annotazioni_marginali']:
            if anno['Datazione'] != "" and (anno['non_dopo'] == "" or anno['non_prima'] == ""):
                anno['non_prima'],anno['non_dopo'],_ = convertdatesafe(anno['Datazione'])
        for st in data_dict['storia_del_manoscritto']:
            if st['Datazione'] != ""  and (st['non_dopo'] == "" or st['non_prima'] == ""):
                st['non_prima'],st['non_dopo'],_ = convertdatesafe(st['Datazione'])
        for de in data_dict['descrizione_esterna']:
            if de['datazione'] != ""  and (de['non_dopo'] == "" or de['non_prima'] == ""):
                de['non_prima'],de['non_dopo'],_ = convertdatesafe(de['datazione'])
        for cop in data_dict['copisti']:
            if cop['datazione'] != ""  and (cop['non_dopo'] == "" or cop['non_prima'] == ""):
                cop['non_prima'],cop['non_dopo'],_ = convertdatesafe(cop['datazione'])

        if varx is None:
            client.capitolare.codici.insert_one(data_dict)
            varx = client.capitolare.codici.find_one({'segnatura_idx': segnatura})
        else:
            client.capitolare.codici.update_one({'_id': varx['_id']},{'$set':data_dict}, upsert=False)
            #TO DO: Avoid query
            log = datetime.datetime.now().strftime("%H:%M:%S")
            varx = client.capitolare.codici.find_one({'segnatura_idx': segnatura})

    if varx is not None:
        #import pdb; pdb.set_trace()
        if varx['status'] != 'appena creato':
            form.process(data=varx)
            # we dynamically add the choices
            if descrizioni_esterne_id[0] != ("",""): 
                for sm in form.storia_del_manoscritto:
                    sm.Descrizione_Esterna_Segnatura.choices = descrizioni_esterne_id2
                for am in form.annotazioni_marginali:
                    am.Descrizione_Esterna_Segnatura.choices = descrizioni_esterne_id
                for cp in form.copisti:
                    cp.Descrizione_Esterna_Segnatura.choices = descrizioni_esterne_id
                for di in form.descrizione_interna:
                    di.Descrizione_Esterna_Segnatura.choices = descrizioni_esterne_id

        #import pdb; pdb.set_trace()
    return render_template(
        'index.html',
        form=form,
        _templateP=template_formP,
        _template=template_form,
        _template2=template_form2,
        _template3=template_form3,
        _template4=template_form4,
        _template5=template_form5,
        _template6=template_form6, #descirizione esterna
        log=log,
        segnatura=segnatura 
    )




@app.route('/insertaltidentifier/<segnatura>', methods=['GET', 'POST'])
def insertaltidentifier(segnatura):     
    el_id = request.args.get('id',None)
    remove = request.args.get('remove',None)
    altids = client.capitolare.identificativi.find({'segnatura_idx': segnatura})
    varx = None
    mod = False
    print(remove)
    if el_id is not None and remove is None:
        print("Modifica")
        mod = True
        varx = client.capitolare.identificativi.find_one({"_id": ObjectId(el_id)})
         
    form = forms.altIdentifier()
    log = "n.d." 
    if form.validate_on_submit():
        print("Entrato")
        data_dict = form.data
        if 'csrf_token' in data_dict.keys():
            del data_dict['csrf_token']
            print("Deleted csrf")
        data_dict['last_modified'] = datetime.datetime.now()
        data_dict['segnatura_idx'] = segnatura

        if varx is None:
            client.capitolare.identificativi.insert_one(data_dict)
        else:
            client.capitolare.identificativi.update_one({'_id': varx['_id']},{'$set':data_dict}, upsert=False)
            #TO DO: Avoid query
            log = datetime.datetime.now().strftime("%H:%M:%S")
            varx = client.capitolare.identificativi.find_one({"_id": ObjectId(el_id)})

    else:
        print("Non valido")

    if varx is not None:
        form.process(data=varx)
    #import pdb; pdb.set_trace()
    return render_template(
        'insertaltidentifier.html',
        form=form,
        log=log,
        segnatura=segnatura,
        altids=altids,
        mod=mod
    )

@app.route('/deletealtidentifier/<segnatura>', methods=['GET', 'POST'])
def deletealtidentifier(segnatura):     
    el_id = request.args.get('id',None)
    print("cancellato")
    client.capitolare.identificativi.remove({"_id": ObjectId(el_id)})
    return redirect("/insertaltidentifier/%s" %segnatura)

@app.route('/getnameauthoritydb')
def getnameauthoritydb():
    namelist = client.capitolare.nameauthority.find()
    offset = request.args.get('offset',None)
    data = json.loads(dumps(list(namelist)))
    return {'data': data}

@app.route('/nameauthority', methods=['GET', 'POST'])
def nameauthority():
    namelist = client.capitolare.nameauthority.find()
    form = forms.AuthoirityRecord()
    stato = ""
    varx = None
    mod = False
    el_id = request.args.get('id',None)
    emojidict  = {  "Ente":"🏛️",
                    "Persona":"👤",
                    "Famiglia":"👥",
                    "Luogo":"🗺️",
                    "Opera":"📖"}
    if el_id is not None:
        print("Modifica")
        mod = True
        varx = client.capitolare.nameauthority.find_one({"_id": ObjectId(el_id)})
    if form.validate_on_submit():
        #import pdb; pdb.set_trace()
        notvalidchr = "~:/?#[]@!$&'()*+;="
        #if any((c in notvalidchr) for c in form.identificativo.data):
        #    stato = ["alert alert-danger","I seguenti caratteri (~:/?#[]@!$&'()*+;=) non possono essere usati nell'ID"]
        #    return render_template(
        #        'nameauthority.html',namelist=namelist, form=form, stato=stato,mod=mod,emojidict=emojidict)

    
        data_dict = form.data
        if 'csrf_token' in data_dict.keys():
            del data_dict['csrf_token']
        data_dict['created'] = datetime.datetime.utcnow()
        data_dict['last_modified'] = datetime.datetime.utcnow()
        data_dict['version'] = 1
        #access_url = url_for('insertfield', segnatura=form.segnatura_idx.data)
        stato = ["alert alert-success",
        "Nuovo record inserito con successo! Accedilo al seguente <a href=''> link </a>linkattraverso la tabella principale"]
    #return redirect('/success')
        if varx is None:
            if data_dict['idauthority'] == "":
                ids = client.capitolare.nameauthority.distinct('idauthority')
                newid = 0
                while "L"+str(newid).zfill(5)  in ids:
                    newid +=1
                data_dict['idauthority'] = "L"+str(newid).zfill(5)

            client.capitolare.nameauthority.insert_one(data_dict)
        else:
            client.capitolare.nameauthority.update_one({'_id': varx['_id']},{'$set':data_dict}, upsert=False)
            #TO DO: Avoid query
            log = datetime.datetime.now().strftime("%H:%M:%S")
            varx = client.capitolare.nameauthority.find_one({"_id": ObjectId(el_id)})
    if varx is not None:
        form.process(data=varx)

  
    return render_template(
        'nameauthority.html',namelist=namelist, form=form, stato=stato,mod=mod,emojidict=emojidict)

@app.route('/deletename', methods=['GET', 'POST'])
def deletename():     
    el_id = request.args.get('id',None)
    print("cancellato")
    client.capitolare.nameauthority.remove({"_id": ObjectId(el_id)})
    return redirect("/nameauthority")

@app.route('/lineeguidacatalog')
def lineeguidacat():
    """Show the details of a race."""

    return render_template(
        'lineeguidacatalog.html'
    )

@app.route('/cercaenti/<jsonformat>/')
def cercaente(jsonformat):
    q = request.args.get('q',None)
    regx = re.compile(q, re.IGNORECASE)
    query = {"$and" : [{"tipologia":"Ente"},
                    {"$or":[{"identificativo": regx},
                            {"altre_forme": regx}]}]}
    enti = client.capitolare.nameauthority.find(query)
    datadict = dict()
    datadict['results'] = []
    if jsonformat == "keyvalue":
        for ente in enti: 
            dataentity = dict()
            dataentity['value'] = ente['identificativo']
            dataentity['key'] = ente['idauthority']
            datadict['results'].append(dataentity)

    response = jsonify(datadict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/cercapersona/<jsonformat>/')
def cercapersona(jsonformat):
    q = request.args.get('q',None)
    regx = re.compile(q, re.IGNORECASE)
    query = {"$and" : [{"tipologia":"Persona"},
                    {"$or":[{"identificativo": regx},
                            {"altre_forme": regx}]}]}
    persone = client.capitolare.nameauthority.find(query)
    datadict = dict()
    datadict['results'] = []
    if jsonformat == "keyvalue":
        for persona in persone: 
            dataentity = dict()
            dataentity['value'] = persona['identificativo']
            dataentity['key'] = persona['idauthority']
            datadict['results'].append(dataentity)

    response = jsonify(datadict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/cercaopera/<jsonformat>/')
def cercaopera(jsonformat):
    q = request.args.get('q',None)
    regx = re.compile(q, re.IGNORECASE)
    query = {"$and" : [{"tipologia":"Opera"},
                    {"$or":[{"identificativo": regx},
                            {"altre_forme": regx}]}]}
    opere = client.capitolare.nameauthority.find(query)
    datadict = dict()
    datadict['results'] = []
    if jsonformat == "keyvalue":
        for opera in opere: 
            dataentity = dict()
            dataentity['value'] = opera['identificativo']
            dataentity['key'] = opera['idauthority']
            datadict['results'].append(dataentity)

    response = jsonify(datadict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/cercaentifamiglieopersone/<jsonformat>/')
def cercaentifamiglieopersone(jsonformat):
    q = request.args.get('q',None)
    regx = re.compile(q, re.IGNORECASE)
    query = {"$and" : [{"$or":[{"tipologia":"Persona"},{"tipologia":"Famiglia"},{"tipologia":"Ente"}]},
                       {"$or":[{"identificativo": regx},
                            {"altre_forme": regx}]}]}
    entifamiglieopersone = client.capitolare.nameauthority.find(query)
    datadict = dict()
    datadict['results'] = []
    if jsonformat == "keyvalue":
        for i in entifamiglieopersone: 
            dataentity = dict()
            dataentity['value'] = i['identificativo']
            dataentity['key'] = i['idauthority']
            datadict['results'].append(dataentity)

    response = jsonify(datadict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/cercaluogo/<jsonformat>/')
def cercaluogo(jsonformat):
    q = request.args.get('q',None)
    regx = re.compile(q, re.IGNORECASE)
    query = {"$and" : [{"tipologia":"Luogo"},
                    {"$or":[{"identificativo": regx},
                            {"altre_forme": regx}]}]}
    luoghi = client.capitolare.nameauthority.find(query)
    datadict = dict()
    datadict['results'] = []
    if jsonformat == "keyvalue":
        for luogo in luoghi: 
            dataentity = dict()
            dataentity['value'] = luogo['identificativo']
            dataentity['key'] = luogo['idauthority']
            datadict['results'].append(dataentity)

    response = jsonify(datadict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/tagtesto/<segnatura>/<componente>/<idint>', methods=['GET', 'POST'])
def tagtesto(segnatura,componente,idint):
    # http://localhost:5000/tagtesto/mtesto/test/1-2?l=2r-57v

    form = forms.TagTesto()
    l = request.args.get('l',None)
    stato = ""
    query = { "$and" : [ {"segnatura":segnatura},{"componente":componente},{"idint":idint}]}
    varx = client.capitolare.riferimenti.find_one(query)
    mod = False
    el_id = request.args.get('id',None)
    def parseresult(field):
        ids = []
        string = form.data[field]
        if string != "":
            ids = [ i['key'] for i in  ast.literal_eval(string)]
        return ids

    if form.validate_on_submit():
        data_dict = form.data
        data_dict['tipologia'] = 'testo'
        data_dict['segnatura'] = segnatura
        data_dict['componente'] = componente
        data_dict['idint'] = idint
        data_dict['locus'] = l
        data_dict['autore_mittente_ids'] = parseresult('autore_mittente')
        data_dict['commentatore_ids'] = parseresult('commentatore')
        data_dict['dedicatario_ids'] = parseresult('dedicatario')
        data_dict['destinatario_ids'] = parseresult('destinatario')
        data_dict['epitomatore_ids'] = parseresult('epitomatore')
        data_dict['glossatore_ids'] = parseresult('glossatore')
        data_dict['traduttore_adattatore_ids'] = parseresult('traduttore_adattatore')
        data_dict['copista_ids'] = parseresult('copista')
        if 'csrf_token' in data_dict.keys():
            del data_dict['csrf_token']
        if varx is None:
            client.capitolare.riferimenti.insert_one(data_dict)
            varx = client.capitolare.riferimenti.find_one(query)
        else:
            client.capitolare.riferimenti.update_one({'_id': varx['_id']},{'$set':data_dict}, upsert=False)
            #TO DO: Avoid query
            log = datetime.datetime.now().strftime("%H:%M:%S")
            varx = client.capitolare.riferimenti.find_one(query)
    #breakpoint()
    if varx is not None:
        form.process(data=varx)
    return render_template('tagtesto.html',
                            form=form,
                            segnatura=segnatura,
                            componente=componente,
                            idint=idint,
                            locus=l)

@app.route('/tagmanufatto/<segnatura>', methods=['GET', 'POST'])
def tagmanufatto(segnatura):
    # http://localhost:5000/tagtesto/mtesto/test/1-2?l=2r-57v

    form = forms.TagManufatto()
    stato = ""
    componente = request.args.get('componente',"-")
    parte = request.args.get('parte',"-")
    query = { "$and" : [ {"segnatura":segnatura},{"componente":componente},{"parte":parte}]}
    varx = client.capitolare.riferimenti.find_one(query)
    mod = False
    def parseresult(field):
        ids = []
        string = form.data[field]
        if string != "":
            ids = [ i['key'] for i in  ast.literal_eval(string)]
        return ids

    if form.validate_on_submit():
        data_dict = form.data
        data_dict['tipologia'] = 'manufatto'
        data_dict['segnatura'] = segnatura
        data_dict['componente'] = componente
        data_dict['parte'] = parte
        data_dict['idint'] = "-"
        data_dict['locus'] = "-"
        data_dict['possessore_ids'] = parseresult('possessore')
        data_dict['committente_ids'] = parseresult('committente')
        data_dict['luogo_ids'] = parseresult('luogo')
        data_dict['autore_mittente_ids'] = parseresult('autore_mittente')
        data_dict['commentatore_ids'] = parseresult('commentatore')
        data_dict['dedicatario_ids'] = parseresult('dedicatario')
        data_dict['destinatario_ids'] = parseresult('destinatario')
        data_dict['epitomatore_ids'] = parseresult('epitomatore')
        data_dict['glossatore_ids'] = parseresult('glossatore')
        data_dict['traduttore_adattatore_ids'] = parseresult('traduttore_adattatore')
        data_dict['copista_ids'] = parseresult('copista')
        if 'csrf_token' in data_dict.keys():
            del data_dict['csrf_token']
        if varx is None:
            client.capitolare.riferimenti.insert_one(data_dict)
            varx = client.capitolare.riferimenti.find_one(query)
        else:
            client.capitolare.riferimenti.update_one({'_id': varx['_id']},{'$set':data_dict}, upsert=False)
            #TO DO: Avoid query
            log = datetime.datetime.now().strftime("%H:%M:%S")
            varx = client.capitolare.riferimenti.find_one(query)
    #breakpoint()
    if varx is not None:
        form.process(data=varx)
    return render_template('TagManufatto.html',
                            form=form,
                            segnatura=segnatura)

@app.route('/indiceillustrazioni/<segnatura>', methods=['GET', 'POST'])
def indiceillustrazioni(segnatura):
    # http://127.0.0.1:5432/indiceillustrazioni/testillu?id=1231
    # http://127.0.0.1:5432/indiceillustrazioni/teste
    # {segnatura_idx:"testillu",illustrazioni: { $elemMatch:{ids:1231}}}
    form = forms.Illustrazioni()
    stato = ""
    componente = "-"
    el_id = request.args.get('id',None)
    query = {"segnatura_idx":segnatura}
    # trovo la segnatura QUESTA DEVE ESSERE PRESENTA DALL'INIZIO
    varx = client.capitolare.indiceillustrazioni.find_one({"segnatura_idx":segnatura})
    if varx is None:
        abort(400,"Inserire una segnatura valida")
    if el_id is not None:
        # se specifico un id, trovo all'interno della segnatura l'illustrazione
        elData = next((item for item in varx['illustrazioni'] if item["ids"] == el_id), None)
    if 'illustrazioni' in varx:
        illustrazioni = varx['illustrazioni']
    else:
        illustrazioni = []
    #breakpoint()
    if form.validate_on_submit():
        # quando invio il form avrò i dati della singola illustrazione
        data_dict = form.data
        # genero un ids univoco se non prsente
        if data_dict['ids'] == "":
            ids = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            data_dict['ids'] = ids
        # converto la datazione
        if data_dict['datazione'] != "" and (data_dict['non_dopo'] == "" or data_dict['non_prima'] == ""):
                data_dict['non_prima'],data_dict['non_dopo'],_ = convertdatesafe(data_dict['datazione'])
        # elimino il CSRF
        if 'csrf_token' in data_dict.keys():
            del data_dict['csrf_token']
        # CASO 1: nuovo record
        if el_id is None:
            client.capitolare.indiceillustrazioni.update(query, {'$push': {'illustrazioni': data_dict}})
            illustrazioni.append(data_dict)
        # CASO 2: update vecchio record
        """         db["my_collection"].update(
                { "_id": ObjectId(document_id) },
                { "$set": { 'documents.'+str(doc_index)+'.content' : new_content_B}}
            )db.POST_COMMENT.update(
                {
                    "_id": ObjectId("5ec424a1ed1af85a50855964"),
                    "bucket.commentId": "5eaf258bb80a1f03cd97a3ad_lepf4f"
                },
                {
                    $set: {
                        "bucket.$.text": "Comment text changed",
                        "bucket.$.createdDate": ISODate("2015-12-11T14:12:00.000+0000")
                    }
                }
            )
         """

        # if varx is None:
        #     newrecord = {'segnatura_idx': segnatura,
        #         'illustrazioni':[data_dict]}
        #     client.capitolare.indiceillustrazioni.insert_one(newrecord)
        #     varx = client.capitolare.indiceillustrazioni.find_one(query)
        # else:
        #     updateq = {'_id': varx['_id'],
        #                'illustrazioni': {'$elemMatch':{ids:data_dict['ids']}}}
        #     client.capitolare.indiceillustrazioni.update_one(updateq,{'$set':data_dict}, upsert=False)
        #     #TO DO: Avoid query
        #     log = datetime.datetime.now().strftime("%H:%M:%S")
        #     varx = client.capitolare.indiceillustrazioni.find_one(query)
    #breakpoint()
    if el_id is not None:
        form.process(data=elData)
    #breakpoint()

    return render_template('formdecorazioni.html',
                            form=form,
                            segnatura=segnatura,
                            illustrazioni=illustrazioni,
                            manifest=varx['manifest'])

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/iiifjcrop')
def iiifjcrop():
    return render_template('microvisualizzatoremanifest.html')

if __name__ == '__main__':
    app.run(debug=True, port=5432)

