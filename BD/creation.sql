DROP TABLE IF EXISTS RESERVATION;
DROP TABLE IF EXISTS GROUPE_FAVORIS;
DROP TABLE IF EXISTS PREINSCRIPTION_EVENEMENT;
DROP TABLE IF EXISTS EVENEMENT;
DROP TABLE IF EXISTS COMPOSITION_GROUPE;
DROP TABLE IF EXISTS SPECTATEUR;
DROP TABLE IF EXISTS ARTISTE;
DROP TABLE IF EXISTS STYLE;
DROP TABLE IF EXISTS GROUPE;
DROP TABLE IF EXISTS CONCERT;
DROP TABLE IF EXISTS LIEU;

CREATE TABLE SPECTATEUR (
    idSpec int PRIMARY KEY AUTO_INCREMENT,
    nomSpec varchar(30),
    prenomSpec varchar(30),
    ddnSpec date
);

CREATE TABLE ARTISTE (
    idArt int PRIMARY KEY AUTO_INCREMENT,
    nomArt varchar(30),
    prenomArt varchar(30),
    instrumentArt varchar(30)
);

CREATE TABLE STYLE (
    idStyle int PRIMARY KEY AUTO_INCREMENT,
    nomStyle varchar(30),
    descStyle varchar(30)
);

CREATE TABLE GROUPE (
    idGr int PRIMARY KEY AUTO_INCREMENT,
    nomGr varchar(30),
    descGr varchar(30),
    lienresGr varchar(30),
    lienvidGr varchar(30)
);

CREATE TABLE LIEU (
    idLieu int PRIMARY KEY AUTO_INCREMENT,
    nomLieu varchar(30),
    villeLieu varchar(30)
);

CREATE TABLE CONCERT (
    idCo int PRIMARY KEY AUTO_INCREMENT,
    nomCo varchar(30),
    debutCo int,
    finCo int,
    tempsMont decimal(12,2),
    tempsDemont decimal(12,2),
    nbHerbergCo int
);

CREATE TABLE GROUPE_FAVORIS (
    idGr int,
    idSpec int,
    PRIMARY KEY(idGr, idSpec)
);
CREATE TABLE COMPOSITION_GROUPE (
    idGr int,
    idArt int,
    PRIMARY KEY(idGr, idArt)
);

CREATE TABLE EVENEMENT (
    idGr int,
    idEvent int,
    idCo int DEFAULT NULL,
    idLieu int,
    nomEvent varchar(30),
    prix int DEFAULT 0,
    dateEvent datetime,
    dureeEvent TIME,
    publicAutorise BOOLEAN DEFAULT TRUE,
    nbPreinscription int,
    PRIMARY KEY (idGr,idEvent)
);

CREATE TABLE PREINSCRIPTION_EVENEMENT ( 
    idGr int,
    idEvent int,
    idSpec int,
    PRIMARY KEY (idGr,idEvent, idSpec)
);

CREATE TABLE RESERVATION (
    idSpec int,
    idCo int,
    dureeReservation ENUM('Une Journée','Deux jours', 'La totalité du festival'),
    prixReservation int,
    PRIMARY KEY (idSpec,idCo)
);


ALTER TABLE RESERVATION ADD FOREIGN KEY ( idSpec ) REFERENCES SPECTATEUR ( idSpec ) ;
ALTER TABLE RESERVATION ADD FOREIGN KEY ( idCo ) REFERENCES CONCERT ( idCo ) ;
ALTER TABLE COMPOSITION_GROUPE ADD FOREIGN KEY ( idGr ) REFERENCES GROUPE ( idGr ) ;
ALTER TABLE COMPOSITION_GROUPE ADD FOREIGN KEY ( idArt ) REFERENCES ARTISTE ( idArt ) ;
ALTER TABLE GROUPE_FAVORIS ADD FOREIGN KEY ( idGr ) REFERENCES GROUPE ( idGr ) ;
ALTER TABLE GROUPE_FAVORIS ADD FOREIGN KEY ( idSpec ) REFERENCES SPECTATEUR ( idSpec ) ;
ALTER TABLE EVENEMENT ADD FOREIGN KEY ( idLieu ) REFERENCES LIEU ( idLieu ) ;
ALTER TABLE EVENEMENT ADD FOREIGN KEY ( idGr ) REFERENCES GROUPE ( idGr ) ;
ALTER TABLE PREINSCRIPTION_EVENEMENT ADD FOREIGN KEY ( idGr,idEvent ) REFERENCES EVENEMENT ( idGr,idEvent ) ;
ALTER TABLE PREINSCRIPTION_EVENEMENT ADD FOREIGN KEY ( idSpec ) REFERENCES SPECTATEUR ( idSpec ) ;
