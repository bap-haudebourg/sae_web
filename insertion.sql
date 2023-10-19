INSERT INTO SPECTATEUR(nomSpec,prenomSpec,ddnSpec) VALUES('NOM', 'prenom', STR_TO_DATE("24/09/1998", "%d/%m/%Y")),
('NOM', 'prenom', STR_TO_DATE("24/09/1998", "%d/%m/%Y")),('NOM', 'prenom', STR_TO_DATE("24/09/1998", "%d/%m/%Y")),
('NOM', 'prenom', STR_TO_DATE("24/09/1998", "%d/%m/%Y")),('NOM', 'prenom', STR_TO_DATE("24/09/1998", "%d/%m/%Y")),
('NOM', 'prenom', STR_TO_DATE("24/09/1998", "%d/%m/%Y")),('NOM', 'prenom', STR_TO_DATE("24/09/1998", "%d/%m/%Y"));

INSERT INTO ARTISTE(nomArt,prenomArt,instrumentArt) VALUES('NOM', 'prenom', 'guitare'),('NOM', 'prenom', 'guitare'),
('NOM', 'prenom', 'violon'),('NOM', 'prenom', 'flute'),('NOM', 'prenom', 'guitare'),('NOM', 'prenom', 'saxophone');


INSERT INTO STYLE(nomStyle,descStyle) VALUES('Electronique',''), ('Techno','' ),('Jungle',''), ('idm','');

INSERT INTO GROUPE(nomGr,descGr,lienresGr,lienvidGr) VALUES('Groupe1','GR1','',''),('Groupe2','GR2','',''),('Groupe3','GR3','',''),
('Groupe4','GR4','',''),('Groupe5','GR5','',''),('Groupe6','GR6','','');

INSERT INTO CONCERT(nomCo,debutCo,finCo,tempsMont,tempsDemont,nbHerbergCo) VALUES();

INSERT INTO GROUPE_FAVORIS(idGr,idSpec) VALUES(1, 1);

INSERT INTO COMPOSITION_GROUPE(idGr,idArt) VALUES(1, 1),(1,2),(1,3),(1,4),(1,5),(1,6);

INSERT INTO EVENEMENT(idGr,idEvent,nomEvent,prix,publicAutorise) VALUES();

INSERT INTO RESERVATION(idSpec,idCo,dureeReservation,prixReservation) VALUES();