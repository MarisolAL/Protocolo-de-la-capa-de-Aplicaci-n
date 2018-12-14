PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
CREATE TABLE usuarios (
  id                INTEGER PRIMARY KEY,
  intentos_disp     INTEGER
 );

--Las imagenes de los pokemones
--estaran en la base en forma de la ruta de la imagen
CREATE TABLE pokemon(
  id  INTEGER PRIMARY KEY,
  nombre TEXT,
  imagen TEXT
);
 CREATE TABLE tiene_pok(
  id_usuario INTEGER REFERENCES usuarios(id),
  id_pokemon INTEGER REFERENCES pokemon(id),
  PRIMARY KEY(id_usuario, id_pokemon)
);
INSERT INTO usuarios VALUES (1,10);
INSERT INTO usuarios VALUES (2,10);
INSERT INTO usuarios VALUES (3,10);
INSERT INTO usuarios VALUES (4,10);
INSERT INTO usuarios VALUES (5,10);
INSERT INTO usuarios VALUES (6,9);
INSERT INTO usuarios VALUES (7,10);
INSERT INTO usuarios VALUES (8,13);
INSERT INTO usuarios VALUES (9,10);
INSERT INTO usuarios VALUES (10,10);
INSERT INTO pokemon VALUES(1,"Abel","img/Abel.png");
INSERT INTO pokemon VALUES(2,"Alm","img/Alm.png");
INSERT INTO pokemon VALUES(3,"Ares","img/Ares.png");
INSERT INTO pokemon VALUES(4,"Arvis","img/Arvis.png");
INSERT INTO pokemon VALUES(5,"Berkut","img/Berkut.png");
INSERT INTO pokemon VALUES(6,"Camila","img/Camila.png");
INSERT INTO pokemon VALUES(7,"Camus","img/Camus.png");
INSERT INTO pokemon VALUES(8,"Catria","img/Catria.png");
INSERT INTO pokemon VALUES(9,"Celica poseida","img/CelicaPoseida.png");
INSERT INTO pokemon VALUES(10,"Cherche","img/Cherche.png");
INSERT INTO pokemon VALUES(11,"Chrom","img/Chrom.png");
INSERT INTO pokemon VALUES(12,"Chrom","img/ChromC.png");
INSERT INTO pokemon VALUES(13,"Chrom","img/ChromN.png");
INSERT INTO pokemon VALUES(14,"Chrom","img/ChromS.png");
INSERT INTO pokemon VALUES(15,"Clarisse","img/Clarisse.png");
INSERT INTO pokemon VALUES(16,"Corrin","img/Corrin.png");
INSERT INTO pokemon VALUES(17,"Corrin","img/CorrinM.png");
INSERT INTO pokemon VALUES(18,"Dorcas","img/Dorcas.png");
INSERT INTO pokemon VALUES(19,"Eir","img/Eir.png");
INSERT INTO pokemon VALUES(20,"Eirika","img/Eirika.png");
INSERT INTO pokemon VALUES(21,"Eldigan","img/Eldigan.png");
INSERT INTO pokemon VALUES(22,"Elise","img/Elise.png");
INSERT INTO pokemon VALUES(23,"Eliwood","img/Eliwood.png");
INSERT INTO pokemon VALUES(24,"Ephraim","img/Ephraim.png");
INSERT INTO pokemon VALUES(25,"Ethlyn","img/Ethlyn.png");
INSERT INTO pokemon VALUES(26,"Felicia","img/Felicia.png");
INSERT INTO pokemon VALUES(27,"Finn","img/Finn.png");
INSERT INTO pokemon VALUES(28,"Fjorm","img/Fjorm.png");
INSERT INTO pokemon VALUES(29,"Frederick","img/Frederick.png");
INSERT INTO pokemon VALUES(30,"Gaius","img/Gaius.png");
INSERT INTO pokemon VALUES(31,"Gerome","img/Gerome.png");
INSERT INTO pokemon VALUES(32,"Gordin","img/Gordin.png");
INSERT INTO pokemon VALUES(33,"Hana","img/Hana.png");
INSERT INTO pokemon VALUES(34,"Hardin","img/Hardin.png");
INSERT INTO pokemon VALUES(35,"Hector","img/Hector.png");
INSERT INTO pokemon VALUES(36,"Ike","img/Ike.png");
INSERT INTO pokemon VALUES(37,"Inigo","img/Inigo.png");
INSERT INTO pokemon VALUES(38,"Innes","img/Innes.png");
INSERT INTO pokemon VALUES(39,"Jeorge","img/Jeorge.png");
INSERT INTO pokemon VALUES(40,"Joshua","img/Joshua.png");
INSERT INTO pokemon VALUES(41,"Kagero","img/Kagero.png");
INSERT INTO pokemon VALUES(42,"Laegjarn","img/Laegjarn.png");
INSERT INTO pokemon VALUES(43,"Lene","img/Lene.png");
INSERT INTO pokemon VALUES(44,"Leon","img/Leon.png");
INSERT INTO pokemon VALUES(45,"Libra","img/Libra.png");
INSERT INTO pokemon VALUES(46,"Lilina","img/Lilina.png");
INSERT INTO pokemon VALUES(47,"Lissa","img/Lissa.png");
INSERT INTO pokemon VALUES(48,"Lon'qu","img/Lonqu.png");
INSERT INTO pokemon VALUES(49,"Lucina","img/Lucina.png");
INSERT INTO pokemon VALUES(50,"Lucius","img/Lucius.png");
INSERT INTO pokemon VALUES(51,"Lute","img/Lute.png");
INSERT INTO pokemon VALUES(52,"Lyn","img/Lyn.png");
INSERT INTO pokemon VALUES(53,"Lyon","img/Lyon.png");
INSERT INTO pokemon VALUES(54,"Marisa","img/Marisa.png");
INSERT INTO pokemon VALUES(55,"Marth","img/Marth.png");
INSERT INTO pokemon VALUES(56,"Micaiah","img/Micaiah.png");
INSERT INTO pokemon VALUES(57,"Navarre","img/Navarre.png");
INSERT INTO pokemon VALUES(58,"Owain","img/Owain.png");
INSERT INTO pokemon VALUES(59,"Palla","img/Palla.png");
INSERT INTO pokemon VALUES(60,"Robin poseido","img/RobinMPoseido.png");
INSERT INTO pokemon VALUES(61,"Robin poseida","img/RobinSPoseido.png");
INSERT INTO pokemon VALUES(62,"Roy","img/Roy.png");
INSERT INTO pokemon VALUES(63,"Seth","img/Seth.png");
INSERT INTO pokemon VALUES(64,"Tiki","img/Tiki.png");
COMMIT;
