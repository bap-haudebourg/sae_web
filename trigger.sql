delimiter |
create or replace trigger maxPreInscription before insert on PREINSCRIPTION_EVENEMENT for each row
begin
  declare mes varchar(100);
  declare maxInscription int,
  declare inscription int,
  if (select publicAutorise from EVENEMENT where idGr = new.idGr and idEvent = new.idEvent) &&(select publicAutorise from EVENEMENT where idGr = new.idGr and idEvent = new.idEvent  )
  select nbPreinscription into maxInscription from EVENEMENT where idGr = new.idGr and idEvent = new.idEvent;
  select COUNT(*) into inscription from PREINSCRIPTION_EVENEMENT where idGr = new.idGr and idEvent =new.idEvent;
  if (inscription+1)>maxInscription then
    set mes = concat("nombre de préinscription deja complète ", new.idGr ," ", new.idEvent);
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  end if;
end |
create or replace trigger 
delimiter ;