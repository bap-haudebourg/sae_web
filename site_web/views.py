from .app import app, mkpath, db
from flask import render_template, url_for , redirect, request,  flash
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, BooleanField, SubmitField, HiddenField, DateField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@login_required
def home():
    return render_template('home.html', utilisateur = current_user)

class LoginForm(FlaskForm):
    login = StringField('Login')
    password = PasswordField('Mot de passe')

class ReservationForm(FlaskForm):
    idEvent = HiddenField('idEvent', validators=[DataRequired()])
    idSpec = HiddenField('idSpec', validators=[DataRequired()])
    dureeRes = SelectField('Durée de la réservation', choices=[(1, 'Une Journée'), (2, 'Deux jours'), (3, 'La totalité du festival')])
    prixRes = HiddenField('Prix de la réservation', validators=[DataRequired()])

class InscriptionForm(FlaskForm):
    nomSpec = StringField('Nom', validators=[DataRequired()])
    prenomSpec = StringField('Prénom', validators=[DataRequired()])
    ddnSpec = DateField('Date de naissance',format='%Y-%m-%d', validators=[DataRequired()])
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    
class RechercheGroupeForm(FlaskForm):
    nomGr = StringField('Nom du groupe')
    nomStyle = StringField('Nom du style')

class RechercheConcertForm(FlaskForm):
    nomConcert = StringField('Nom du concert')
    nomStyle = StringField('Nom du style')
    
class RechercheEvenementForm(FlaskForm):
    nomEvent = StringField('Nom de l\'événement')
    
class AjouterGroupe(FlaskForm):
    nomGr = StringField('Nom du groupe', validators=[DataRequired()])
    descGr = StringField('Description du groupe', validators=[DataRequired()])
    nomStyle = StringField('Nom du style', validators=[DataRequired()])
    
class AjouterArtiste(FlaskForm):
    nomArt = StringField('Nom de l\'artiste', validators=[DataRequired()])
    prenomArt = StringField('Prénom de l\'artiste', validators=[DataRequired()])
    ddnArt = DateField('Date de naissance',format='%Y-%m-%d', validators=[DataRequired()])
    nomInstr = StringField('Nom de l\'instrument', validators=[DataRequired()])

class AjouterConcert(FlaskForm):
    nomConcert = StringField('Nom du concert', validators=[DataRequired()])
    dateConcert = DateField('Date du concert',format='%Y-%m-%d', validators=[DataRequired()])
    nomLieu = StringField('Nom du lieu', validators=[DataRequired()])
    prixConcert = IntegerField('Prix du concert', validators=[DataRequired()])
    nomGr = StringField('Nom du groupe', validators=[DataRequired()])
    nomStyle = StringField('Nom du style', validators=[DataRequired()])
    
class AjouterArtisteGroupe(FlaskForm):
    id = HiddenField('id', validators=[DataRequired()])
    nomGr = StringField('Nom du groupe', validators=[DataRequired()])
    nomArt = StringField('Nom de l\'artiste', validators=[DataRequired()])
    prenomArt = StringField('Prénom de l\'artiste', validators=[DataRequired()])
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if request.form['button'] == 'Connexion':
            util = Utilisateur.query.filter_by(login=form.login.data).first()
            if util is not None and util.password == sha256(form.password.data.encode()).hexdigest():
                login_user(util)
                return redirect(url_for('home'))
            else:
                flash('Mauvais login ou mot de passe')
        else:
            return redirect(url_for('inscription'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    if request.method == 'POST':
        spec = Spectateur()
        spec.nomSpec = form.nomSpec.data
        spec.prenomSpec = form.prenomSpec.data
        spec.ddnSpec = form.ddnSpec.data
        db.session.add(spec)
        db.session.commit()
        util = Utilisateur()
        util.idSpec = Spectateur.query.filter_by(nomSpec=form.nomSpec.data).first().idSpec
        util.idRole = 1
        util.login = form.login.data
        util.password = sha256(form.password.data.encode()).hexdigest()
        db.session.add(util)
        db.session.commit()
        login_user(util)
        return redirect(url_for('home'))
    return render_template('inscription.html', form=form)


@app.route('/concert/<id>/reservation', methods=['GET', 'POST'])
@login_required
def reservation(id):
    form = ReservationForm()
    concert = Concert.query.filter_by(idCo=id).first()
    evenement = Evenement.query.filter_by(idCo=id).first()
    evenement.nomLieu = Lieu.query.filter_by(idLieu=evenement.idLieu).first().nomLieu
    groupe = Groupe.query.filter_by(idGr=evenement.idGr).first()
    style = Style.query.filter_by(idStyle=groupe.idStyle).first()
    form.idEvent.data = evenement.idEvent
    form.idSpec.data = current_user.idSpec
    form.prixRes.data = evenement.prix
    if request.method == 'POST':
        res = Reservation()
        res.idSpec = form.idSpec.data
        res.idEvent = form.idEvent.data
        res.dureeReservation = form.dureeRes.choices[int(form.dureeRes.data)-1][1]
        res.prixReservation = form.prixRes.data
        resa = Reservation.query.filter_by(idSpec=res.idSpec).filter_by(idEvent=res.idEvent).first()
        if not resa:
            db.session.add(res)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('reservation.html', utilisateur = current_user, concert=concert, groupe=groupe, style=style, evenement=evenement, form=form)

@app.route('/planning')
@login_required
def planning():
    reservations = Reservation.query.filter_by(idSpec=current_user.idSpec).all()
    dates = {}
    for res in reservations:
        evenement = Evenement.query.filter_by(idEvent=res.idEvent).first()
        co = Concert.query.filter_by(idCo=evenement.idCo).first()
        co.date = Evenement.query.filter_by(idEvent=evenement.idEvent).first().dateEvent
        date = co.date.strftime('%d/%m/%Y')
        co.date = co.date.strftime('%H:%M:%S')
        if not date in dates:
            dates[date] = []
        dates[date].append(co)
    return render_template('planning.html', utilisateur = current_user, dates=dates)

@app.route('/rechercher_concert', methods=['GET', 'POST'])
@login_required
def rechercher_concert():
    form = RechercheConcertForm()
    nomConcert = ''
    nomStyle = ''
    idStyle = None
    if request.method == 'POST':
        if form.nomConcert.data != '':
            nomConcert = form.nomConcert.data
        if form.nomStyle.data != '':
            nomStyle = form.nomStyle.data
            idStyle = Style.query.filter_by(nomStyle=nomStyle).first().idStyle
    if idStyle:
        if nomConcert:
            groupe = Groupe.query.filter_by(idStyle=idStyle).all()
            concerts = []
            for g in groupe:
                evenement = Evenement.query.filter_by(idGr=g.idGr).first()
                if evenement:
                    concerts.append(Concert.query.filter(Concert.idCo==evenement.idCo, Concert.nomCo.like(f"%{nomConcert}%")).first())            
        else:
            groupe = Groupe.query.filter_by(idStyle=idStyle).all()
            concerts = []
            for g in groupe:
                evenement = Evenement.query.filter_by(idGr=g.idGr).first()
                if evenement:
                    concerts.append(Concert.query.filter_by(idCo=evenement.idCo).first())                
    else:
        if nomConcert:
            concerts = Concert.query.filter(Concert.nomCo.like(f"%{nomConcert}%")).all()
        else:
            concerts = Concert.query.all()
    for co in concerts:
        evenement = Evenement.query.filter_by(idCo=co.idCo).first().idGr
        co.nomGr = Groupe.query.filter_by(idGr=evenement).first().nomGr
        groupe = Groupe.query.filter_by(idGr=evenement).first()
        co.nomStyle = Style.query.filter_by(idStyle=groupe.idStyle).first().nomStyle  
    return render_template('rechercher_concert.html', utilisateur = current_user, form=form, concerts=concerts, nomConcert=nomConcert, nomStyle=nomStyle)

@app.route('/recherche_groupe', methods=['GET', 'POST'])
@login_required
def rechercher_groupe():
    form = RechercheGroupeForm()
    nomGr = ''
    nomStyle = ''
    idStyle = None
    if request.method == 'POST':
        if form.nomGr.data != '':
            nomGr = form.nomGr.data
        if form.nomStyle.data != '':
            nomStyle = form.nomStyle.data
            idStyle = Style.query.filter_by(nomStyle=nomStyle).first().idStyle
    if idStyle:
        if nomGr:
            groupes = Groupe.query.filter_by(nomGr=nomGr).filter_by(idStyle=idStyle).all()
        else:
            groupes = Groupe.query.filter_by(idStyle=idStyle).all()
    else:
        if nomGr:
            groupes = Groupe.query.filter_by(nomGr=nomGr).all()
        else:
            groupes = Groupe.query.all()
    for g in groupes:
        g.nomStyle = Style.query.filter_by(idStyle=g.idStyle).first().nomStyle
    return render_template('rechercher_groupe.html', utilisateur = current_user, groupes=groupes, form=form, nomGr=nomGr, nomStyle=nomStyle)

@app.route('/groupe/<id>', methods=['GET', 'POST'])
@login_required
def groupe(id):
    groupe = Groupe.query.filter_by(idGr=id).first()
    style = Style.query.filter_by(idStyle=groupe.idStyle).first()
    comp_groupe = Composition_Groupe.query.filter_by(idGr=id).all()
    artistes = []
    for art in comp_groupe:
        artiste = Artiste.query.filter_by(idArt=art.idArt).first()
        artiste.nomInstr = Instrument.query.filter_by(idInstr=artiste.idInstr).first().nomInstr
        artistes.append(artiste)
    return render_template('groupe.html', utilisateur = current_user, groupe=groupe, artistes=artistes, style=style)  

@app.route('/artiste/<id>', methods=['GET', 'POST'])
@login_required
def artiste(id):
    artiste = Artiste.query.filter_by(idArt=id).first()
    instrument = Instrument.query.filter_by(idInstr=artiste.idInstr).first()
    groupe = Composition_Groupe.query.filter_by(idArt=id).all()
    groupes = []
    for g in groupe:
        groupes.append(Groupe.query.filter_by(idGr=g.idGr).first())
    return render_template('artiste.html', utilisateur = current_user, artiste=artiste, instrument=instrument, groupes=groupes)

@app.route('/concert/<id>', methods=['GET', 'POST'])
@login_required
def concert(id):
    concert = Concert.query.filter_by(idCo=id).first()
    evenement = Evenement.query.filter_by(idCo=id).first()
    evenement.nomLieu = Lieu.query.filter_by(idLieu=evenement.idLieu).first().nomLieu
    groupe = Groupe.query.filter_by(idGr=evenement.idGr).first()
    style = Style.query.filter_by(idStyle=groupe.idStyle).first()
    return render_template('concert.html', utilisateur = current_user, concert=concert, groupe=groupe, style=style, evenement=evenement)

@app.route('/ajouter_groupe', methods=['GET', 'POST'])
@login_required
def ajouter_groupe():
    form = AjouterGroupe()
    if request.method == 'POST':
        groupe = Groupe()
        groupe.nomGr = form.nomGr.data
        groupe.descGr = form.descGr.data
        groupe.idStyle = Style.query.filter_by(nomStyle=form.nomStyle.data).first().idStyle
        db.session.add(groupe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ajouter_groupe.html', utilisateur = current_user, form=form)

@app.route('/ajouter_artiste', methods=['GET', 'POST'])
@login_required
def ajouter_artiste():
    form = AjouterArtiste()
    if request.method == 'POST':
        artiste = Artiste()
        artiste.nomArt = form.nomArt.data
        artiste.prenomArt = form.prenomArt.data
        artiste.ddnArt = form.ddnArt.data
        artiste.idInstr = Instrument.query.filter_by(nomInstr=form.nomInstr.data).first().idInstr
        db.session.add(artiste)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ajouter_artiste.html', utilisateur = current_user, form=form)

@app.route('/ajouter_concert', methods=['GET', 'POST'])
@login_required
def ajouter_concert():
    form = AjouterConcert()
    if request.method == 'POST':
        concert = Concert()
        concert.nomCo = form.nomConcert.data
        concert.prix = form.prixConcert.data
        db.session.add(concert)
        db.session.commit()
        evenement = Evenement()
        evenement.idCo = Concert.query.filter_by(nomCo=form.nomConcert.data).first().idCo
        evenement.idGr = Groupe.query.filter_by(nomGr=form.nomGr.data).first().idGr
        evenement.idLieu = Lieu.query.filter_by(nomLieu=form.nomLieu.data).first().idLieu
        evenement.dateEvent = form.dateConcert.data
        db.session.add(evenement)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ajouter_concert.html', utilisateur = current_user, form=form)

@app.route('/ajouter_artiste_groupe', methods=['GET', 'POST'])
@login_required
def ajouter_artiste_groupe():
    form = AjouterArtisteGroupe()
    if request.method == 'POST':
        comp_groupe = Composition_Groupe()
        comp_groupe.idGr = Groupe.query.filter_by(nomGr=form.nomGr.data).first().idGr
        comp_groupe.idArt = Artiste.query.filter_by(nomArt=form.nomArt.data).first().idArt
        db.session.add(comp_groupe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ajouter_artiste_groupe.html', utilisateur = current_user, form=form)

@app.route('/admin_ajouter')
@login_required
def admin_ajouter():
    return render_template('admin_ajouter.html', utilisateur = current_user)

@app.route('/favoris')
@login_required
def favoris():
    fav = Groupe_Favoris.query.filter_by(idSpec=current_user.idSpec).all()
    groupes = []
    for f in fav:
        g=Groupe.query.filter_by(idGr=f.idGr).first()
        g.nomStyle = Style.query.filter_by(idStyle=g.idStyle).first().nomStyle
        groupes.append(g)   
    return render_template('favoris.html', utilisateur = current_user, groupes=groupes)

@app.route('/ajouter_favoris/<id>', methods=['GET', 'POST'])
@login_required
def ajouter_favoris(id):
    fav = Groupe_Favoris()
    fav.idSpec = current_user.idSpec
    fav.idGr = id
    db.session.add(fav)
    db.session.commit()
    return redirect(url_for('favoris'))

@app.route('/rechercher_evenement', methods=['GET', 'POST'])
@login_required
def rechercher_evenement():
    form = RechercheEvenementForm()
    nomEvent = ''
    if request.method == 'POST':
        if form.nomEvent.data != '':
            nomEvent = form.nomEvent.data
    if nomEvent:
        evenements = Evenement.query.filter(Evenement.nomEvent.like(f"%{nomEvent}%")).all()
    else:
        evenements = Evenement.query.all()
    for e in evenements:
        e.nomGr = Groupe.query.filter_by(idGr=e.idGr).first().nomGr
        e.nomLieu = Lieu.query.filter_by(idLieu=e.idLieu).first().nomLieu
        if e.idCo:
            e.nomCo = Concert.query.filter_by(idCo=e.idCo).first().nomCo
        else:
            e.nomCo = ""
    return render_template('rechercher_evenement.html', utilisateur = current_user, form=form, evenements=evenements, nomEvent=nomEvent)