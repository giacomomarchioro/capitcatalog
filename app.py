# -*- coding: utf-8 -*-
# app.py

from flask import Flask, render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, SelectField, \
    StringField, TextAreaField, SubmitField 
from wtforms import validators
from pymongo import MongoClient
from wtforms.validators import DataRequired,Regexp
from databasecredential import connectionstring
from werkzeug.datastructures import MultiDict
import json
import datetime
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(connectionstring)
db=client.admin
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)


#var = client.capitolare.codici.find_one({"segnatura_idx":"XXVII"}) 

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

#globalvar = []
#globalvarn = []

class Biblio_int_libri(Form):
    id_biblib = StringField("Id",
        validators=[ ],render_kw={'class':"form-control",}
    )
    titolo = StringField("Titolo",
            render_kw={'class':"form-control",}
        )
    anno = StringField("Anno",
            validators=[ ],render_kw={'class':"form-control",}
        )
    numero_pagine = StringField("Numero pagine",
            validators=[ ],render_kw={'class':"form-control",}
        )
    citta = StringField("Citta",
            validators=[ ],render_kw={'class':"form-control",}
        )
    casa_editrice = StringField("Casa editrice",
            validators=[ ],render_kw={'class':"form-control",}
        )
    collana = StringField("Collana",
            validators=[ ],render_kw={'class':"form-control",}
        )
    n_collana = StringField("N collana",
            validators=[ ],render_kw={'class':"form-control",}
        )
    autore_nome_cognome = StringField("Autore nome cognome",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Descrizione_interna_id = StringField("Descrizione interna id",
            validators=[ ],render_kw={'class':"form-control",}
    )


class Storia_del_manoscritto(Form):
    Id_auto_inc = StringField("Id auto inc",
        validators=[ ],render_kw={'class':"form-control",}
    )
    Id_AT = StringField("Id",
            validators=[ ],render_kw={'class':"form-control",}
        )
    intervallo_carte = StringField("Intervallo carte",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Datazione = StringField("Datazione",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Contenuto = StringField("Contenuto",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Posizione = StringField("Posizione",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Tipologia_scrittura = StringField("Tipologia scrittura",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
            validators=[ ],render_kw={'class':"form-control",}
        )
    link_img = StringField("Link immagine:",
            validators=[ ],render_kw={'class':"form-control",}
        )
    
    link_ROI = StringField("Link regione dell'immagine:",
            validators=[ ],render_kw={'class':"form-control",}
        )

class AnnotazioniMarg(Form):
    Id_auto_inc = StringField("Id auto inc",
        validators=[ ],render_kw={'class':"form-control",}
    )
    Id_anno = StringField("ID annotazioni marginali",
            validators=[ ],render_kw={'class':"form-control",}
        )
    intervallo_carte = StringField("Intervallo carte",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Datazione = StringField("Datazione",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Contenuto = StringField("Contenuto",
            render_kw={'class':"form-control",}
        )
    Posizione = StringField("Posizione",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Tipologia_scrittura = StringField("Tipologia scrittura",
            validators=[ ],render_kw={'class':"form-control",}
        )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
            validators=[ ],render_kw={'class':"form-control",}
        )

    link_img = StringField("Link immagine:",
            validators=[ ],render_kw={'class':"form-control",
            'pattern':"^http:\/\/lezioni\.meneghetti\.univr\.it\/UVjs\/\?manifest=?.*" }
        )
    
    link_ROI = StringField("Link regione dell'immagine:",
            validators=[ ],render_kw={'class':"form-control",
            'pattern':"^http:\/\/lezioni\.meneghetti\.univr\.it\/\/imageapi\/.*" }
        )

class Copisti(Form):
    """Subform.

    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    id_cop = StringField("Id copisti",
                         validators=[], render_kw={'class': "form-control"}
                         )
    intervallo_carte = StringField("Intervallo carte",
                                   validators=[], render_kw={'class': "form-control"}
                                   )
    datazione = StringField("Datazione",
                            validators=[], render_kw={'class': "form-control"}
                            )
    tipologia_scrittura = StringField("Tipologia scrittura",
                                      validators=[], render_kw={'class': "form-control"}
                                      )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
                                                validators=[], render_kw={'class': "form-control"}
                                                )


class DescInt(Form):
    """Subform.

    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    autore = StringField("Autore",
                         validators=[], render_kw={'class': "form-control", }
                         )
    titolo = StringField("Titolo",
                         validators=[], render_kw={'class': "form-control", }
                         )
    descid = StringField("ID descrizione interna padre",
                         #validators=[Regexp('^[1-9]\d*(\.[1-9]\d*)*$',message='ID non valido')],
                         render_kw={'class': "form-control",
                         'required pattern':"^[1-9]\d*(\.[1-9]\d*)*$"
                                        }
                         )
    incipit = StringField("Incipit",validators=[],
                          render_kw={'class': "form-control", }
                          )
    incipit_url = StringField("Incipit URL", render_kw={'class': "form-control",
    'pattern':"^http:\/\/lezioni\.meneghetti\.univr\.it\/UVjs\/\?manifest=?.*" }
    )
    explicit = StringField("Explicit",validators=[],
                            render_kw={'class': "form-control", }
                           )
    carte = StringField("Carte",
                        validators=[], render_kw={'class': "form-control", }
                        )
    rubrica = StringField("Rubrica",
                          render_kw={'class': "form-control", }
                          )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
                                                validators=[], render_kw={'class': "form-control", }
                                                )
    Descrizione_interna_id = StringField("Descrizione interna ID",
                                        #validators=[Regexp('^[1-9]\d*(\.[1-9]\d*)*$',message='ID non valido')],
                                        render_kw={'class': "form-control",
                                        'required pattern':"^[1-9]\d*(\.[1-9]\d*)*$"
                                        }
                                         )

class DescEst(Form):
    Segnatura = StringField("Segnatura",
                            validators=[], render_kw={'class': "form-control", }
                            )
    datazione = StringField("Datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    tipo_di_supporto_e_qualita = StringField("Tipo di supporto e qualita",
                                             validators=[], render_kw={'class': "form-control", }
                                             )
    consistenza = StringField("Consistenza",
                              validators=[], render_kw={'class': "form-control", }
                              )
    numerazione_carte = StringField("Numerazione carte",
                                    validators=[], render_kw={'class': "form-control", }
                                    )
    carte_di_guardia = StringField("Carte di guardia",
                                   validators=[], render_kw={'class': "form-control", }
                                   )
    prospetto_fascicolazione = StringField("Prospetto fascicolazione",
                                           validators=[], render_kw={'class': "form-control", }
                                           )
    arrangiamento_fogli_gregory = StringField("Arrangiamento fogli gregory",
                                              validators=[], render_kw={'class': "form-control", }
                                              )
    dimensioni = StringField("Dimensioni",
                             validators=[], render_kw={'class': "form-control", }
                             )
    rigatura = StringField("Rigatura",
                           validators=[], render_kw={'class': "form-control", }
                           )
    foratura = StringField("Foratura",
                           validators=[], render_kw={'class': "form-control", }
                           )
    legatura = StringField("Legatura",
                           validators=[], render_kw={'class': "form-control", }
                           )
    utenti_email = StringField("Autore scheda",
                               validators=[], render_kw={'class': "form-control", }
                               )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
                                                validators=[], render_kw={'class': "form-control", }
                                                )
    numero_di_fascicolo = StringField("Numero di fascicolo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    decorazioni = StringField("Decorazioni",
                        validators=[], render_kw={'class': "form-control", }
                        )
    filigrana = StringField("Filigrana",
                        validators=[], render_kw={'class': "form-control", }
                        )
    orchid = StringField("Orch.ID.",
                    validators=[],
                    render_kw={'class': "form-control",
                         'required pattern':"^https:\/\/orcid\.org\/.*"
                                        }
                         )
    

class MainForm(FlaskForm):
    """Parent form."""
 
    status = SelectField(u'Stato', choices=[('In lavorazione', 'In lavorazione'),('Concluso', 'concluso'), ('Abbandonato', 'abbandonato'),('Presentabile', 'presentabile'), ],render_kw={'class': "form-control", })

    manifest = StringField("Manifest:",
                            validators=[], render_kw={'class': "form-control", }
                            )
    immagine_banner = StringField("Banner:",
                            validators=[], render_kw={'class': "form-control",
                            'pattern':"^http:\/\/lezioni\.meneghetti\.univr\.it\/\/imageapi\/.*" }
                            )
    immagine_dorso = StringField("Dorso:",
                            validators=[], render_kw={'class': "form-control",
                            'pattern':"^http:\/\/lezioni\.meneghetti\.univr\.it\/\/imageapi\/.*" }
                            )
    immagine_esemplificativa = StringField("Immagine esemplificativa:",
                            validators=[], render_kw={'class': "form-control",
                            'pattern':"^http:\/\/lezioni\.meneghetti\.univr\.it\/\/imageapi\/.*" }
                            )

    sommario_desc = TextAreaField("Sommario:",
                            validators=[], render_kw={'class': "form-control",'rows':"4" }
                            )
                            

    descrizione_esterna = FieldList(
        FormField(DescEst),
        min_entries=1,
        max_entries=200
    )
  
    descrizione_interna = FieldList(
        FormField(DescInt),
        min_entries=1,
        max_entries=500
    )

    copisti = FieldList(
        FormField(Copisti),
        min_entries=1,
        max_entries=200
    )

    annotazioni_marginali = FieldList(
        FormField(AnnotazioniMarg),
        min_entries=1,
        max_entries=200
    )

    storia_del_manoscritto = FieldList(
        FormField(Storia_del_manoscritto),
        min_entries=1,
        max_entries=200
    )

     
    biblio_int_libri = FieldList(
        FormField(Biblio_int_libri),
        min_entries=1,
        max_entries=200
    )


class NewRecord(FlaskForm):
    segnatura_idx = StringField('Segnatura ID', validators=[DataRequired()],render_kw={'class': "form-control", "aria-describedby":"emailHelp", "placeholder":"Per esempio m0037_0" })




# Initialize app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'sose1231crext'


@app.route('/', methods=['GET', 'POST'])
def index():
    varx = client.capitolare.codici.find({'version': 1})
    form = NewRecord()
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
    
    #form = MainForm(MultiDict(varx))
    form = MainForm()
    #form.populate_obj(varx)
    template_form = DescInt(prefix='descrizione_interna-_-')
    template_form2 = Copisti(prefix='copisti-_-')
    template_form3 = AnnotazioniMarg(prefix='annotazioni_marginali-_-')
    template_form4 = Storia_del_manoscritto(prefix='storia_del_manoscritto-_-')
    template_form5 = Biblio_int_libri(prefix='biblio_int_libri-_-')
    template_form6 = DescEst(prefix='descrizione_esterna-_-')
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

        if varx is None:
            client.capitolare.codici.insert_one(data_dict)
            varx = client.capitolare.codici.find_one({'segnatura_idx': segnatura})
        else:
            client.capitolare.codici.update_one({'_id': varx['_id']},{'$set':data_dict}, upsert=False)
            #TO DO: Avoid query
            log = datetime.datetime.now().strftime("%H:%M:%S")
            varx = client.capitolare.codici.find_one({'segnatura_idx': segnatura})

    else:

        #db.session.add(new_race)

        # for lap in form.laps.data:
        #    new_lap = Lap(**lap)

        # Add to race
        #    new_race.laps.append(new_lap)

        # db.session.commit()
        #import pdb; pdb.set_trace()
        print("Non valido")

    if varx is not None:
        form.process(data=varx)
    #import pdb; pdb.set_trace()
    return render_template(
        'index.html',
        form=form,
        _template=template_form,
        _template2=template_form2,
        _template3=template_form3,
        _template4=template_form4,
        _template5=template_form5,
        _template6=template_form6, #descirizione esterna
        log=log,
        segnatura=segnatura 
    )


@app.route('/lineeguidacatalog')
def lineeguidacat():
    """Show the details of a race."""

    return render_template(
        'lineeguidacatalog.html'
    )

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/iiifjcrop')
def iiifjcrop():
    return render_template('microvisualizzatoremanifest.html')

if __name__ == '__main__':
    app.run()
