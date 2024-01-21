from .app import db, login_manager
from flask_login import UserMixin, current_user
from sqlalchemy import func

class Spectateur(UserMixin, db.Model):
    idSpec = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomSpec = db.Column(db.String(30))
    prenomSpec = db.Column(db.String(30))
    ddnSpec = db.Column(db.Date)

class Artiste(db.Model):
    idArt = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomArt = db.Column(db.String(30))
    prenomArt = db.Column(db.String(30))
    ddnArt = db.Column(db.Date)
    idInstr = db.Column(db.Integer)
    
class Instrument(db.Model):
    idInstr = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomInstr = db.Column(db.String(30))
    
class Style(db.Model):
    idStyle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomStyle = db.Column(db.String(30))
    descStyle = db.Column(db.String(30))
    
class Sous_Style(db.Model):
    idsStyle = db.Column(db.Integer)
    nomsStyle = db.Column(db.String(30))
    descsStyle = db.Column(db.String(30))
    idStyle = db.Column(db.Integer, primary_key=True)
    
class Groupe(db.Model):
    idGr = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomGr = db.Column(db.String(30))
    descGr = db.Column(db.String(30))
    idStyle = db.Column(db.Integer)

class Hebergement(db.Model):
    idHeb = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomHeb = db.Column(db.String(30))
    descHeb = db.Column(db.String(30))
    prixHeb = db.Column(db.Integer)
    nbPlaceHeb = db.Column(db.Integer)

class Occupation_Hebergement(db.Model):
    idHeb = db.Column(db.Integer, primary_key=True)
    idGr = db.Column(db.Integer, primary_key=True)
    nbPlaceOcc = db.Column(db.Integer)
    dateOcc = db.Column(db.Date, primary_key=True)

class Reseau_Social_Groupe(db.Model):
    idRes = db.Column(db.Integer, primary_key=True)
    nomRes = db.Column(db.String(30))
    lienRes = db.Column(db.String(30))
    idGr = db.Column(db.Integer, primary_key=True)

class Photo_Groupe(db.Model):
    idPh = db.Column(db.Integer, primary_key=True)
    nomPh = db.Column(db.String(30))
    imagePh = db.Column(db.LargeBinary)
    idGr = db.Column(db.Integer, primary_key=True)
    
class Video_Groupe(db.Model):
    idVid = db.Column(db.Integer, primary_key=True)
    nomVid = db.Column(db.String(30))
    lienVid = db.Column(db.String(30))
    idGr = db.Column(db.Integer, primary_key=True)
    
class Lieu(db.Model):
    idLieu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomLieu = db.Column(db.String(30))
    
class Concert(db.Model):
    idCo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomCo = db.Column(db.String(30))
    debutCo = db.Column(db.Integer)
    finCo = db.Column(db.Integer)
    tempsMont = db.Column(db.Float)
    tempsDemont = db.Column(db.Float)
    nbHebergCo = db.Column(db.Integer)
    
class Groupe_Favoris(db.Model):
    idGr = db.Column(db.Integer, primary_key=True)
    idSpec = db.Column(db.Integer, primary_key=True)
    
class Composition_Groupe(db.Model):
    idGr = db.Column(db.Integer, primary_key=True)
    idArt = db.Column(db.Integer, primary_key=True)
    
class Evenement(db.Model):
    idGr = db.Column(db.Integer, primary_key=True)
    idEvent = db.Column(db.Integer, primary_key=True)
    idCo = db.Column(db.Integer, default=None)
    idLieu = db.Column(db.Integer)
    nomEvent = db.Column(db.String(30))
    prix = db.Column(db.Integer, default=0)
    dateEvent = db.Column(db.DateTime)
    dureeEvent = db.Column(db.Time)
    publicAutorise = db.Column(db.Boolean, default=True)
    nbPreinscription = db.Column(db.Integer)
    
class Preinscription_Evenement(db.Model):
    idEvent = db.Column(db.Integer, primary_key=True)
    idSpec = db.Column(db.Integer, primary_key=True)
    
class Reservation(db.Model):
    idSpec = db.Column(db.Integer, primary_key=True)
    idEvent = db.Column(db.Integer, primary_key=True)
    dureeReservation = db.Column(db.Enum('Une Journée','Deux jours', 'La totalité du festival'))
    prixReservation = db.Column(db.Integer)
    
class Role(db.Model):
    idRole = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomRole = db.Column(db.String(30))

class Utilisateur(db.Model):
    idSpec = db.Column(db.Integer, primary_key=True)
    idRole = db.Column(db.Integer)
    login = db.Column(db.String(30))
    password = db.Column(db.String(30))
    
    def get_id(self):
        return str(self.idSpec)
    
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

@login_manager.user_loader
def load_user(username):
    return Utilisateur.query.get(username)