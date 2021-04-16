# -*- coding: utf-8 -*-
# app.py

from flask import Flask, render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, SelectField, \
    StringField, TextAreaField, SubmitField
from wtforms import validators
from pymongo import MongoClient
from wtforms.validators import DataRequired
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



#globalvar = []
#globalvarn = []

class Biblio_int_libri(Form):
    id_biblib = StringField("Id",
        validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
    )
    titolo = StringField("Titolo",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    anno = StringField("Anno",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    numero_pagine = StringField("Numero pagine",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    citta = StringField("Citta",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    casa_editrice = StringField("Casa editrice",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    collana = StringField("Collana",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    n_collana = StringField("N collana",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    autore_nome_cognome = StringField("Autore nome cognome",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Descrizione_interna_id = StringField("Descrizione interna id",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
    )


class Annotazioni_testo(Form):
    Id_auto_inc = StringField("Id auto inc",
        validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
    )
    Id_AT = StringField("Id",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    intervallo_carte = StringField("Intervallo carte",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Datazione = StringField("Datazione",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Contenuto = StringField("Contenuto",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Posizione = StringField("Posizione",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Tipologia_scrittura = StringField("Tipologia scrittura",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )

class AnnotazioniMarg(Form):
    Id_auto_inc = StringField("Id auto inc",
        validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
    )
    Id_anno = StringField("ID annotazioni marginali",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    intervallo_carte = StringField("Intervallo carte",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Datazione = StringField("Datazione",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Contenuto = StringField("Contenuto",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Posizione = StringField("Posizione",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Tipologia_scrittura = StringField("Tipologia scrittura",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
            validators=[ validators.Length(max=500)],render_kw={'class':"form-control",}
        )

class Copisti(Form):
    """Subform.

    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    id_cop = StringField("Id copisti",
                         validators=[validators.Length(max=500)], render_kw={'class': "form-control"}
                         )
    intervallo_carte = StringField("Intervallo carte",
                                   validators=[validators.Length(max=500)], render_kw={'class': "form-control"}
                                   )
    datazione = StringField("Datazione",
                            validators=[validators.Length(max=500)], render_kw={'class': "form-control"}
                            )
    tipologia_scrittura = StringField("Tipologia scrittura",
                                      validators=[validators.Length(max=500)], render_kw={'class': "form-control"}
                                      )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
                                                validators=[validators.Length(max=500)], render_kw={'class': "form-control"}
                                                )


class DescInt(Form):
    """Subform.

    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    autore = StringField("Autore",
                         validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                         )
    titolo = StringField("Titolo",
                         validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                         )
    descid = StringField("ID descrizione interna",
                         validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                         )
    incipit = StringField("Incipit",
                          validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                          )
    explicit = StringField("Explicit",
                           validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                           )
    carte = StringField("Carte",
                        validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                        )
    rubrica = StringField("Rubrica",
                          validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                          )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
                                                validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                                                )
    Descrizione_interna_id = StringField("Descrizione interna id",
                                         validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                                         )

class DescEst(Form):
    Segnatura = StringField("Segnatura",
                            validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                            )
    datazione = StringField("Datazione",
                            validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                            )
    tipo_di_supporto_e_qualita = StringField("Tipo di supporto e qualita",
                                             validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                                             )
    consistenza = StringField("Consistenza",
                              validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                              )
    numerazione_carte = StringField("Numerazione carte",
                                    validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                                    )
    carte_di_guardia = StringField("Carte di guardia",
                                   validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                                   )
    prospetto_fascicolazione = StringField("Prospetto fascicolazione",
                                           validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                                           )
    arrangiamento_fogli_gregory = StringField("Arrangiamento fogli gregory",
                                              validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                                              )
    dimensioni = StringField("Dimensioni",
                             validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                             )
    rigatura = StringField("Rigatura",
                           validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                           )
    foratura = StringField("Foratura",
                           validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                           )
    legatura = StringField("Legatura",
                           validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                           )
    utenti_email = StringField("Utenti email",
                               validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                               )
    Descrizione_Esterna_Segnatura = StringField("Descrizione esterna segnatura",
                                                validators=[validators.Length(max=500)], render_kw={'class': "form-control", }
                                                )
class MainForm(FlaskForm):
    """Parent form."""
    descrizione_esterna = FieldList(
        FormField(DescEst),
        min_entries=1,
        max_entries=20
    )
  
    descrizione_interna = FieldList(
        FormField(DescInt),
        min_entries=1,
        max_entries=20
    )

    copisti = FieldList(
        FormField(Copisti),
        min_entries=1,
        max_entries=40
    )

    annotazioni_marginali = FieldList(
        FormField(AnnotazioniMarg),
        min_entries=1,
        max_entries=40
    )

    annotazioni_testo = FieldList(
        FormField(Annotazioni_testo),
        min_entries=1,
        max_entries=40
    )

     
    biblio_int_libri = FieldList(
        FormField(Biblio_int_libri),
        min_entries=1,
        max_entries=40
    )


class NewRecord(FlaskForm):
    segnatura_idx = StringField('Segnatura ID', validators=[DataRequired()],render_kw={'class': "form-control", "aria-describedby":"emailHelp", "placeholder":"Per esempio XXVII_A" })


# Create models
db = SQLAlchemy()


class Race(db.Model):
    """Stores races."""
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)


class Lap(db.Model):
    """Stores laps of a race."""
    __tablename__ = 'laps'

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'))

    runner_name = db.Column(db.String(100))
    lap_time = db.Column(db.Integer)
    category = db.Column(db.String(4))
    notes = db.Column(db.String(255))

    # Relationship
    race = db.relationship(
        'Race',
        backref=db.backref('laps', lazy='dynamic', collection_class=list)
    )


# Initialize app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'sosecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config["WTF_CSRF_ENABLED"] = False
db.init_app(app)
db.create_all(app=app)


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
    template_form4 = Annotazioni_testo(prefix='annotazioni_testo-_-')
    template_form5 = Biblio_int_libri(prefix='biblio_int_libri-_-')
    template_form6 = DescEst(prefix='descrizione_esterna-_-')   

    if form.validate_on_submit():
        # Create race
        #new_race = Race()
        print("Entrato")
        data_dict = form.data
        if 'csrf_token' in data_dict.keys():
            del data_dict['csrf_token']
            print("Deleted csrf")
        data_dict['last_modified'] = datetime.datetime.utcnow()
        #client.capitolare.codici.insert_one(data_dict)
        if varx is None:
            client.capitolare.codici.insert_one(data_dict)
            varx = client.capitolare.codici.find_one({'segnatura_idx': segnatura})
        else:
            client.capitolare.codici.update_one({'_id': varx['_id']},{'$set':data_dict}, upsert=False)
            #TO DO: Avoid query
            varx = client.capitolare.codici.find_one({'segnatura_idx': segnatura})

        #db.session.add(new_race)

        # for lap in form.laps.data:
        #    new_lap = Lap(**lap)

        # Add to race
        #    new_race.laps.append(new_lap)

        # db.session.commit()
        print("Valido")

    if varx is not None:
        form.process(data=varx)

    return render_template(
        'index.html',
        form=form,
        _template=template_form,
        _template2=template_form2,
        _template3=template_form3,
        _template4=template_form4,
        _template5=template_form5,
        _template6=template_form6 #descirizione esterna
    )


@app.route('/lineeguidacatalog')
def lineeguidacat():
    """Show the details of a race."""

    return render_template(
        'lineeguidacatalog.html'
    )


if __name__ == '__main__':
    app.run()
