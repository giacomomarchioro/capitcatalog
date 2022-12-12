from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, SelectMultipleField, SelectField, \
    StringField, TextAreaField, SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired,Regexp


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
    tipologia_di_elemento = SelectField(u'Tipologia', choices=[
        ('Annotazione','Annotazione'),
        ('Timbro', 'Timbro'),
        ('Sigillo', 'Sigillo'),
        ('Etichetta', 'Etichetta'),
        ('Stemma', 'Stemma'),],
        render_kw={'class': "form-control", })
    
    Datazione = StringField("Datazione",
            validators=[ ],render_kw={'class':"form-control",}
        )
    trascrizione_datazione =  StringField("Trascrizione datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    note_datazione =  StringField("Note datazione",
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
    tipologia = SelectField(u'ID_descrizione_esterna',
                            choices=[
                            ('Postilla o annotazione','Postilla o annotazione'),
                            ('Scrittura avventizia', 'Scrittura avventizia'),
                            ],validate_choice=False,render_kw={'class': "form-control", })

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
    note_datazione =  StringField("Note datazione",
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
    note_datazione =  StringField("Note datazione",
                            validators=[], render_kw={'class': "form-control", }
                            ) 
    tipologia_scrittura = SelectField(u'Tipologia', choices=[
        ('Capitale Romana','Capitale Romana'),
        ('Corsiva Romana','Corsiva Romana'),
        ('Onciale', 'Onciale'),
        ('Semi-onciale', 'Semi-onciale'),
        ('Insulare', 'Insulare'),
        ('Visigotica', 'Visigotica'),
        ('Beneventana', 'Beneventana'),
        ('Carolina', 'Carolina'),
        ('Gotica', 'Gotica'),
        ('Umanistica', 'Umanistica')
        ],
        render_kw={'class': "form-control", })
    note_sulla_scrittura =  StringField("Note sulla scrittura",
                            validators=[], render_kw={'class': "form-control", }
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

    # da eliminare
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

    lacunoso = BooleanField(u'Lacunoso:')

    mutilo = BooleanField(u'Mutilo:')

    Descrizione_Esterna_Segnatura = SelectField(u'ID_descrizione_esterna', choices=[('Non assegnato', 'Non assegnato')],validate_choice=False,render_kw={'class': "form-control id-componente", })
    
    Descrizione_interna_id = StringField("Descrizione interna ID",
                                        #validators=[Regexp('^[1-9]\d*(\.[1-9]\d*)*$',message='ID non valido')],
                                        render_kw={'class': "form-control id-textual-unit",
                                        'required pattern':"^[1-9]\d*(\.[1-9]\d*)*$"
                                        }
                                         )
    ref_parte = SelectField(u'ID_descrizione_esterna', choices=[('Non assegnato', 'Non assegnato')],validate_choice=False,render_kw={'class': "form-control ref-parte", })


class DescEst(Form):
    Segnatura = StringField("Segnatura",
                            validators=[], render_kw={'class': "form-control", }
                            )
    #scriptio = SelectField(u"Scriptio", choices=[('superior', 'superior'),('inferior', 'inferior') ],render_kw={'class': "form-control", })

    ref_parte = SelectField(u'ID_descrizione_esterna', choices=[('Non assegnato', 'Non assegnato')],validate_choice=False,render_kw={'class': "form-control ref-parte", })

    tipologia = SelectField(u"Tipologia", choices=[('Unità codicologica', 'Unità codicologica'),('Unità palinsesto', 'Unità palinsesto'),('Frammento manoscritto', 'Frammento manoscritto'),('Frammento a stampa', 'Frammento a stampa') ],render_kw={'class': "form-control", })

    caratteri_utilizzati = SelectMultipleField(u"Caratteri utilizzati", choices=[('Alfabeto greco', 'Alfabeto greco'),('Alfabeto latino', 'Alfabeto latino'),('Notazione musicale', 'Notazione musicale')],render_kw={'class': "form-control", })

    forma = SelectField(u"Forma", choices=[('rilegato', 'rilegato'),('fascicoli', 'fascicoli'),('fogli sciolti', 'fogli sciolti'),('rotolo', 'rotolo') ],render_kw={'class': "form-control", })

    datazione = StringField("Datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    note_datazione =  StringField("Note datazione",
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
    note_sul_luogo =  StringField("Note sul luogo",
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
                                                validators=[], render_kw={'class': "form-control id-componente", }
                                                )
    numero_di_fascicolo = StringField("Numero di fascicolo",
                            validators=[], render_kw={'class': "form-control", }
                            )
    decorazioni = StringField("Decorazioni",
                        validators=[], render_kw={'class': "form-control", }
                        )
    filigrana = StringField(u"Filigrana",render_kw={'class': "form-control", })
    
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
                           validators=[], render_kw={'class': "form-control id-parte", })
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
    altezza_mm = StringField("Altezza (mm):",
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
    altezza_mm = StringField("Altezza (mm):",
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
class Illustrazioni(FlaskForm):
    """Parent form."""
    tipologia = SelectField(u'Tipologia', choices=[
        ('Antiporta','Antiporta'),
        ('Illustrazioni a piena pagina','Illustrazioni a piena pagina'),
        ('Illustrazioni a vignetta','Illustrazioni a vignetta'),
        ('Illustrazioni senza cornice','Illustrazioni senza cornice'),
        ('Iniziali semplici','Iniziali semplici'),
        ('Iniziali filigranate','Iniziali filigranate'),
        ('INIZIALI ORNATE.fitomorfe','INIZIALI ORNATE.fitomorfe'),
        ('INIZIALI ORNATE.zoomorfe','INIZIALI ORNATE.zoomorfe'),
        ('INIZIALI ORNATE.antropomorfe','INIZIALI ORNATE.antropomorfe'),
        ('INIZIALI ORNATE.bianchi girari','INIZIALI ORNATE.bianchi girari'),
        ('INIZIALI FIGURATE','INIZIALI FIGURATE'),
        ('INIZIALI ISTORIATE','INIZIALI ISTORIATE'),
        ('FREGI','FREGI'),
        ('DISEGNI','DISEGNI'),
        ('SEGNI DI PARAGRAFO','SEGNI DI PARAGRAFO'),
        ('Richiami di fascicolo ornati','Richiami di fascicolo ornati'),
        ('Stemmi e armi araldiche','Stemmi e armi araldiche'),
    ],render_kw={'class': "form-control-x", })
    ids = StringField("Ids",validators=[], render_kw={'type': "hidden"})
    manifest_index =  IntegerField("manifest_index",
                        validators=[], render_kw={'class': "form-control-x","id":"vai","size":"3","placeholder":"0" })
    pagina_incipit = BooleanField("Pagina d'incipit")
    identificativo = StringField("identificativo",
                        validators=[], render_kw={'class': "form-control-x", })
    carta_scelta  = StringField("Carta scelta",
                        validators=[], render_kw={'class': "form-control-x", })
    locus  = StringField("Locus",
                        validators=[], render_kw={'class': "form-control-x", })
    link_immagine  = StringField("link_immagine",
                        validators=[], render_kw={'class': "form-control-x","id":"link-immagine" })
    area_posizionamento  = StringField("area_posizionamento",
                        validators=[], render_kw={'class': "form-control-x", })
    datazione = StringField("Datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    note_datazione =  StringField("Note datazione",
                            validators=[], render_kw={'class': "form-control", }
                            )
    non_prima =  StringField("Non prima",
                            validators=[], render_kw={'class': "form-control"}
                            )
    non_dopo =  StringField("Non dopo",
                            validators=[], render_kw={'class': "form-control"}
                            )
    autore_ambito = StringField("Autore ambito",
                        validators=[], render_kw={'class': "form-control-x"})
    
    tecnica_esecutiva = SelectField(u'Tipologia', choices=[('Penna', 'Penna'),('Pennello', 'Penello')],render_kw={'class': "form-control-x", })
    ampiezza_mm = StringField("ampiezza_mm",
                        validators=[], render_kw={'class': "form-control-x"})
    altezza_mm = StringField("altezza_mm",
                        validators=[], render_kw={'class': "form-control-x"})
    oro = BooleanField("Oro")
    azzurro = BooleanField("Azzurro")
    descrizione = StringField("descrizione",
                        validators=[], render_kw={'class': "form-control-x"})
    wikidata = StringField("wikidata",
                        validators=[], render_kw={'class': "form-control-x"})
    iconoclass = StringField("iconoclass",
                        validators=[], render_kw={'class': "form-control-x"})

## FORMS authority records
class AuthoirityRecord(FlaskForm):
    """Parent form."""
    idauthority = StringField("idauthority",
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
    tipologia = SelectField(u'Tipologia', choices=[('Titolo', 'Titolo'),
                                                   ('Segnatura', 'Segnatura'),
                                                   ('Collocazione', 'Collocazione'),
                                                   ('Conosciuto come', 'Conosciuto come'),
                                                   ('Numero di inventario','Numero di inventario')
                                                    ],
                                                    render_kw={'class': "form-control", })
   
    descrizione = StringField("Descrizione",validators=[])
    in_uso = BooleanField("In uso")
    datazione = StringField("Datazione",validators=[])
    used_not_before = StringField("Utilizzata non prima:",validators=[])
    used_not_after = StringField("Utilizzata non dopo:",validators=[])

## FORMS for tagging the text
class TagTesto(FlaskForm):
    """Parent form.""" 
    autore_mittente = StringField("Autore o mittente:",validators=[])
    commentatore = StringField("Commentatore:",validators=[])
    dedicatario = StringField("Dedicatario:",validators=[])
    destinatario = StringField("Destinatario:",validators=[])
    epitomatore = StringField("Epitomatore:",validators=[])
    glossatore = StringField("Glossatore:",validators=[])
    annotatore = StringField("Annotatore:",validators=[])
    traduttore_adattatore = StringField("Traduttore Adattatore:",validators=[])
    copista = StringField("Copista:",validators=[])
    opera_identificata = StringField("Opera identificata:",validators=[])
    bibliografia = StringField("Bibliografia:",validators=[])

class TagManufatto(FlaskForm):
    """Parent form.""" 
    autore_mittente = StringField("Autore o mittente:",validators=[])
    commentatore = StringField("Commentatore:",validators=[])
    possessore = StringField("Possessore:",validators=[])
    committente = StringField("Committente:",validators=[])
    dedicatario = StringField("Dedicatario:",validators=[])
    destinatario = StringField("Destinatario:",validators=[])
    epitomatore = StringField("Epitomatore:",validators=[])
    glossatore = StringField("Glossatore:",validators=[])
    annotatore = StringField("Annotatore:",validators=[])
    traduttore_adattatore = StringField("Traduttore Adattatore:",validators=[])
    copista = StringField("Copista:",validators=[])
    opera_identificata = StringField("Opera identificata:",validators=[])
    luogo = StringField("Luogo:",validators=[])
    miniatore = StringField("Miniatore:",validators=[])
    editore =  StringField("Editore:",validators=[])




