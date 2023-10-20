delimiter |
create or replace trigger maxPreInscription before insert on PREINSCRIPTION_EVENEMENT for each row
begin;
  declare mes varchar(100);
  declare maxInscription int;
  declare inscription int;
    if (select publicAutorise from EVENEMENT where idGr = new.idGr and idEvent = new.idEvent) then
      select nbPreinscription into maxInscription from EVENEMENT where idGr = new.idGr and idEvent = new.idEvent;
      select COUNT(*) into inscription from PREINSCRIPTION_EVENEMENT where idGr = new.idGr and idEvent =new.idEvent;
      if (inscription+1)>maxInscription then
        set mes = concat("nombre de préinscription deja complète ", new.idGr ," ", new.idEvent);
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
      end if;
    end if;
  end |
  delimiter ;

create or replace trigger supperpositionHeure before insert on EVENEMENT for each row
begin
  declare mes varchar(100);
  declare debut datetime;
  declare fin datetime;
  declare fini boolean DEFAULt false; 
  declare lesDate cursor for select dateEvent,dureEvent from EVENEMENT where DATE(dateEvent) = DATE(new.dateEvent);
  declare continue handler for not found set fini = true;
  open lesDate;
  while not fini do
    fetch lesDate into debut,fin;
    if not fini then
      if time(debut) < time(new.dateEvent) + time(new.dureeEvent) && time(debut) + time(fin) > time(new.dateEvent) then
        set mes = concat("Heure de début en conflit avec un autre événement ", new.idGr ," ", new.idEvent);
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
      end if;
      if time(debut) < time(new.dateEvent) && time(debut) + time(fin) > time(new.dateEvent) || time(debut) < time(new.dateEvent) && time(debut) + time(fin) > time(new.dateEvent) +time(new.dureeEvent) then
        set mes = concat("Heure de fin en conflit avec un autre événement ", new.idGr ," ", new.idEvent);
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
      end if;
    end if;
  end while;
end;
delimiter ;
  end while;
end;
delimiter ;