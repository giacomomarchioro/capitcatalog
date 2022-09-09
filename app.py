# -*- coding: utf-8 -*-
# app.py

from sys import prefix
from flask import Flask, render_template,url_for, request, redirect,jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, SelectMultipleField, SelectField, \
    StringField, TextAreaField, SubmitField,BooleanField
from wtforms import validators
from pymongo import MongoClient
from wtforms.validators import DataRequired,Regexp
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
        

#globalvar = []
#globalvarn = []

class NonValidatingSelectMulipleField(SelectMultipleField):
    def pre_validate(self, form):
        pass 

class Facsimile(Form):
    id_facsimile = StringField("Id", #
        validators=[ ],render_kw={'class':"form-control",}
    )
    tipologia = SelectField(u'Tipologia', choices=[('Edizione a stampa', 'Edizione a stampa'),('Negativo', 'Negativo'), ('Positivo', 'Positivo'),('Riproduzione digitale', 'Riproduzione digitale'), ],render_kw={'class': "form-control", })
    
    descrizione = StringField("Descrizione",#
            validators=[ ],render_kw={'class':"form-control",}
        )
    datazione = StringField("Datazione",#
            validators=[ ],render_kw={'class':"form-control",}
        )
    non_prima = StringField("Non prima:",#
            validators=[ ],render_kw={'class':"form-control",}
        )
    non_dopo = StringField("Non dopo:", #
            validators=[ ],render_kw={'class':"form-control",}
        )
    id_origine = StringField("Sorgente", #
            validators=[ ],default="Originale",render_kw={'class':"form-control",}
        )
    creatore = StringField("Creatore",#
            validators=[ ],render_kw={'class':"form-control",}
        )
    luogo_di_custodia = StringField("Luogo di custodia",#
            validators=[ ],render_kw={'class':"form-control",}
        )
    manifest = StringField("Manifest",
            validators=[ ],render_kw={'class':"form-control",}
        )
    link_online = StringField("Link:",#
            validators=[ ],render_kw={'class':"form-control",}
        )
    completezza = StringField("Completezza",
            validators=[ ],render_kw={'class':"form-control",}
        )
    # parte di riferimento

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
    trascrizione_datazione =  StringField("Trascrizione datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    locus_datazione = StringField("Locus datazione",
                            validators=[], render_kw={'class': "form-control", }
                            ) 
    non_prima =  StringField("Non prima",
                            validators=[], render_kw={'class': "form-control", }
                            )
    non_dopo =  StringField("Non dopo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    trascrizione = StringField("Trascrizione",
                            validators=[], render_kw={'class': "form-control", }
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
    Descrizione_Esterna_Segnatura = SelectField(u'ID_descrizione_esterna', choices=[('Non assegnato', 'Non assegnato')],validate_choice=False,render_kw={'class': "form-control", })
    
    #StringField("Descrizione esterna segnatura",
    #        validators=[ ],render_kw={'class':"form-control",}
    #    )
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
    identificazione = StringField("identificazione",
                         validators=[], render_kw={'class': "form-control"}
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
    trascrizione_datazione =  StringField("Trascrizione datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    locus_datazione = StringField("Locus datazione",
                            validators=[], render_kw={'class': "form-control", }
                            ) 
    non_prima =  StringField("Non prima",
                            validators=[], render_kw={'class': "form-control", }
                            )
    non_dopo =  StringField("Non dopo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    trascrizione = StringField("Trascrizione",
                            validators=[], render_kw={'class': "form-control", }
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
    Descrizione_Esterna_Segnatura = SelectField(u'ID_descrizione_esterna', choices=[('Non assegnato', 'Non assegnato')],validate_choice=False,render_kw={'class': "form-control", })

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
    identificazione = StringField("identificazione",
                         validators=[], render_kw={'class': "form-control"}
                         )
    intervallo_carte = StringField("Intervallo carte",
                                   validators=[], render_kw={'class': "form-control"}
                                   )
    datazione = StringField("Datazione",
                            validators=[], render_kw={'class': "form-control"}
                            )
    non_prima =  StringField("Non prima",
                            validators=[], render_kw={'class': "form-control", }
                            )
    non_dopo =  StringField("Non dopo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    tipologia_scrittura = StringField("Tipologia scrittura",
                                      validators=[], render_kw={'class': "form-control"}
                                      )
    Descrizione_Esterna_Segnatura = NonValidatingSelectMulipleField(u'ID_descrizione_esterna', choices=[('Non assegnato', 'Non assegnato')],validate_choice=False,render_kw={'class': "form-select","multiple":True,"style":"height: 100px"})


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
    lingua = SelectField("Lingua", choices=[('Latino', 'Latino'),('Volgare italiano', 'Volgare italiano'), ('Italiano', 'Italiano'),('Greco antico', 'Greco antico'),('Greco ellenistico (Koinè)', 'Greco ellenistico (Koinè)'),('Ebraico', 'Ebraico'),(r'ge῾ez',r"ge῾ez") ],render_kw={'class': "form-control", })

    descid = StringField("ID descrizione interna padre",
                         #validators=[Regexp('^[1-9]\d*(\.[1-9]\d*)*$',message='ID non valido')],
                         render_kw={'class': "form-control id-father-unit",
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
                        validators=[], render_kw={'class': "form-control locus", }
                        )
    rubrica = StringField("Rubrica",
                          render_kw={'class': "form-control", }
                          )
    tipologia_di_titolo = SelectField(u'Tipologia di testo:', choices=[('Presente originale', 'Presente originale'),('Presente non-originale', 'Presente non-originale'),('Dedotto dal catalogatore', 'Dedotto dal catalogatore'),('Aggiunto dal catalogatore', 'Aggiunto dal catalogatore')],validate_choice=False,render_kw={'class': "form-control", })
    
    tipologia_di_testo = SelectField(u'Tipologia di testo:', choices=[('testo', 'testo'),('proemio/introduzione', 'proemio/introduzione'),('dedica', 'dedica'),('commento', 'commento'),('prologo/conclusione', 'prologo/conclusione'),('sommario', 'sommario')],validate_choice=False,render_kw={'class': "form-control", })

    acefalo = BooleanField(u'Acefalo:')

    mutilo = BooleanField(u'Tipologia di testo:')

    Descrizione_Esterna_Segnatura = SelectField(u'ID_descrizione_esterna', choices=[('Non assegnato', 'Non assegnato')],validate_choice=False,render_kw={'class': "form-control id-componente", })
    
    Descrizione_interna_id = StringField("Descrizione interna ID",
                                        #validators=[Regexp('^[1-9]\d*(\.[1-9]\d*)*$',message='ID non valido')],
                                        render_kw={'class': "form-control id-textual-unit",
                                        'required pattern':"^[1-9]\d*(\.[1-9]\d*)*$"
                                        }
                                         )

class DescEst(Form):
    Segnatura = StringField("Segnatura",
                            validators=[], render_kw={'class': "form-control", }
                            )
    #scriptio = SelectField(u"Scriptio", choices=[('superior', 'superior'),('inferior', 'inferior') ],render_kw={'class': "form-control", })

    tipologia = SelectField(u"Tipologia", choices=[('Unità codicologica', 'Unità codicologica'),('Unità palinsesto', 'Unità palinsesto'),('Frammento manoscritto', 'Frammento manoscritto'),('Frammento a stampa', 'Frammento a stampa') ],render_kw={'class': "form-control", })

    caratteri_utilizzati = SelectMultipleField(u"Caratteri utilizzati", choices=[('Alfabeto greco', 'Alfabeto greco'),('Alfabeto latino', 'Alfabeto latino'),('Notazione musicale', 'Notazione musicale')],render_kw={'class': "form-control", })

    forma = SelectField(u"Forma", choices=[('rilegato', 'rilegato'),('fascicoli', 'fascicoli'),('fogli sciolti', 'fogli sciolti'),('rotolo', 'rotolo') ],render_kw={'class': "form-control", })

    datazione = StringField("Datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    trascrizione_datazione =  StringField("Trascrizione datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    locus_datazione = StringField("Locus datazione",
                            validators=[], render_kw={'class': "form-control", }
                            ) 
    non_prima =  StringField("Non prima",
                            validators=[], render_kw={'class': "form-control", }
                            )
    non_dopo =  StringField("Non dopo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    luogo = StringField("Luogo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    trascrizione_luogo = StringField("Trascrizione luogo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    locus_luogo = StringField("Locus luogo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    link_immagine_luogo = StringField("Link immagine luogo",
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
    filigrana = SelectField(u"Filigrana", choices=[( 'Ravvisabile','ravvisabile'),( 'Non ravvisabile','non ravvisabile') ],render_kw={'class': "form-control", })
    
    orchid = StringField("Orch.ID.",
                    validators=[],
                    render_kw={'class': "form-control",
                         'required pattern':"^https:\/\/orcid\.org\/.*"
                                        }
                         )
    note =  TextAreaField("Note:",
                            validators=[], render_kw={'class': "form-control",'rows':"4" }
                            )

class Parte(Form):
    identificativo_parte = StringField("Identificativo",
                           validators=[], render_kw={'class': "form-control", })
    legatura = StringField("Legatura",
                           validators=[], render_kw={'class': "form-control", })
    carte_di_guardia = StringField("Carte di guardia",
                                   validators=[], render_kw={'class': "form-control", })
    consistenza = StringField("Consistenza",
                              validators=[], render_kw={'class': "form-control", })
    collocazione = StringField("Collocazione",
                              validators=[], render_kw={'class': "form-control", })
    largezza_mm = StringField("Larghezza (mm)",
                            validators=[], render_kw={'class': "form-control"}
                            )
    ampiezza_mm = StringField("Ampiezza (mm):",
                            validators=[], render_kw={'class': "form-control" }
                            )
    profondita_mm = StringField("Profondità (mm):",
                            validators=[], render_kw={'class': "form-control"}
                            )


class MainForm(FlaskForm):
    """Parent form."""
 
    status = SelectField(u'Stato', choices=[('In lavorazione', 'In lavorazione'),('Concluso', 'concluso'), ('Abbandonato', 'abbandonato'),('Presentabile', 'presentabile'), ],render_kw={'class': "form-control", })
    
    segnatura = StringField("Segnatura",
                            validators=[], render_kw={'class': "form-control", }
                            )
    id_segnature_collegate = StringField("Segnature collegate:",
                            validators=[], render_kw={'class': "form-control", }
                            )
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
    largezza_mm = StringField("Larghezza (mm)",
                            validators=[], render_kw={'class': "form-control"}
                            )
    ampiezza_mm = StringField("Ampiezza (mm):",
                            validators=[], render_kw={'class': "form-control" }
                            )
    profondita_mm = StringField("Profondità (mm):",
                            validators=[], render_kw={'class': "form-control"}
                            )
    custodia = SelectField('Custodia', choices=[('No', 'No'),('In cartone', 'In cartone'), ('In pelle ', 'In pelle')],render_kw={'class': "form-control", })

    sommario_desc = TextAreaField("Sommario:",
                            validators=[], render_kw={'class': "form-control",'rows':"4" }
                            )
    storia_desc = TextAreaField("Sommario:",
                            validators=[], render_kw={'class': "form-control",'rows':"4" }
                            )
   
    parte = FieldList(
        FormField(Parte),
        min_entries=1,
        max_entries=200
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

    # the ID must be equal to this:
    facsimile = FieldList(
        FormField(Facsimile),
        min_entries=1,
        max_entries=200
    )


class NewRecord(FlaskForm):
    segnatura_idx = StringField('Segnatura ID', validators=[DataRequired()],render_kw={'class': "form-control", "aria-describedby":"emailHelp", "placeholder":"Per esempio m0037_0" })



## FORMS authority records
class AuthoirityRecord(FlaskForm):
    """Parent form."""
    idauthority = StringField("idauthority",
                        validators=[], render_kw={'class': "form-control-x", })
    identificativo = StringField("identificativo",
                        validators=[], render_kw={'class': "form-control-x", })
    tipologia = SelectField(u'Tipologia', choices=[('Persona', 'Persona'),('Famiglia', 'Famiglia'), ('Ente', 'Ente'),('Luogo', 'Luogo'),('Opera', 'Opera') ],render_kw={'class': "form-control-x", })
    descrizione = StringField("descrizione",
                        validators=[], render_kw={'class': "form-control-x", })
    altre_forme = StringField(" altre_forme",
                        validators=[], render_kw={'class': "form-control-x", })
    non_prima = StringField("non_prima",
                        validators=[], render_kw={'class': "form-control-x", })
    non_dopo = StringField("non_dopo",
                        validators=[], render_kw={'class': "form-control-x", })
    wikidata = StringField("wikidata",
                        validators=[], render_kw={'class': "form-control-x", })
    mirabile = StringField("mirabile",
                        validators=[], render_kw={'class': "form-control-x", })
    SBN_author = StringField("SBN_author",
                        validators=[], render_kw={'class': "form-control-x", })
    reicat_opacSBN = StringField("reicat_opacSBN",
                        validators=[], render_kw={'class': "form-control-x", })

## FORMS for alternative identifiers
class altIdentifier(FlaskForm):
    """Parent form."""
    text = StringField("Testo",
                        validators=[], render_kw={'class': "form-control", })
    tipologia = SelectField(u'Tipologia', choices=[('Titolo', 'Titolo'),('Segnatura', 'Segnatura'), ('Collocazione', 'Collocazione'),('Conosciuto come', 'Conosciuto come'),('Numero di inventario','Numero di inventario') ],render_kw={'class': "form-control", })
   
    descrizione = StringField("Descrizione",
                        validators=[], render_kw={'class': "form-control", })
    datazione = StringField("Datazione",
                        validators=[], render_kw={'class': "form-control", })
    used_not_before = StringField("Utilizzata non prima:",
                    validators=[], render_kw={'class': "form-control", })
    used_not_after = StringField("Utilizzata non dopo:",
                    validators=[], render_kw={'class': "form-control", })

## FORMS for tagging the text
class TagTesto(FlaskForm):
    """Parent form.""" 
    autore_mittente = StringField("Autore o mittente:",validators=[])
    commentatore = StringField("Commentatore:",validators=[])
    dedicatario = StringField("Dedicatario:",validators=[])
    destinatario = StringField("Destinatario:",validators=[])
    epitomatore = StringField("Epitomatore:",validators=[])
    glossatore = StringField("Glossatore:",validators=[])
    traduttore_adattatore = StringField("Traduttore Adattatore:",validators=[])
    copista = StringField("Copista:",validators=[])
    opera_identificata = StringField("Opera identificata:",validators=[])
    bibliografia = StringField("Bibliografia:",validators=[])

class TagSegnatura(FlaskForm):
    """Parent form.""" 
    autore_mittente = StringField("Autore o mittente:",validators=[])
    commentatore = StringField("Commentatore:",validators=[])
    possessore = StringField("Possessore:",validators=[])
    committente = StringField("Committente:",validators=[])
    dedicatario = StringField("Dedicatario:",validators=[])
    destinatario = StringField("Destinatario:",validators=[])
    epitomatore = StringField("Epitomatore:",validators=[])
    glossatore = StringField("Glossatore:",validators=[])
    traduttore_adattatore = StringField("Traduttore Adattatore:",validators=[])
    copista = StringField("Copista:",validators=[])
    opera_identificata = StringField("Opera identificata:",validators=[])
    luogo = StringField("Luogo:",validators=[])




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
    #import pdb; pdb.set_trace()
    #form = MainForm(MultiDict(varx))
    form = MainForm()
    #form.populate_obj(varx)
    template_formP = Parte(prefix='parte-_-')
    template_form = DescInt(prefix='descrizione_interna-_-')
    template_form2 = Copisti(prefix='copisti-_-')
    template_form3 = AnnotazioniMarg(prefix='annotazioni_marginali-_-')
    template_form4 = Storia_del_manoscritto(prefix='storia_del_manoscritto-_-')
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


    template_form5 = Facsimile(prefix='facsimile-_-')
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
         
    form = altIdentifier()
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
    breakpoint()
    data = json.loads(dumps(list(namelist)))
    return {'data': data}

@app.route('/nameauthority', methods=['GET', 'POST'])
def nameauthority():
    namelist = client.capitolare.nameauthority.find()
    form = AuthoirityRecord()
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

@app.route('/tagsegnatura/<segnatura>', methods=['GET', 'POST'])
def tagsegnatura(segnatura):
    # http://localhost:5000/tagtesto/mtesto/test/1-2?l=2r-57v

    form = TagSegnatura()
    stato = ""
    componente = "-tuttelecomponenti-"
    query = { "$and" : [ {"segnatura":segnatura},{"componente":componente}]}
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
        data_dict['segnatura'] = segnatura
        data_dict['componente'] = componente
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
    return render_template('tagsegnatura.html',
                            form=form,
                            segnatura=segnatura)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/iiifjcrop')
def iiifjcrop():
    return render_template('microvisualizzatoremanifest.html')

if __name__ == '__main__':
    app.run(debug=True)

