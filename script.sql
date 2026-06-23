<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> dcc45aed (linux)
-- creer la base de donnee
CREATE DATABASE rh;

-- se connecter a la base de donnee
\c rh

--Pour lister les tables dans la base de donnee
\dt

INSERT INTO api_etatcivil (nom) 
VALUES 
    ('Célibataire'), 
    ('Marié(e)'), 
    ('Divorcé(e)'), 
    ('Veuf/Veuve');

INSERT INTO api_typecontrats ("TypeContrat") 
VALUES 
    ('Salarié'), 
    ('Consultant');

INSERT INTO api_sexes (nom) 
VALUES 
    ('Masculin'), 
    ('Féminin');

INSERT INTO api_modefinancement (nom) 
VALUES 
    ('Fond Mondial'), 
    ('Alliance Gavi'), 
    ('Banque Mondiale/PPSB'), 
    ('Banque Mondiale/PARN');

INSERT INTO api_relations (nom, grade) 
VALUES 
    ('Père', 1), 
    ('Mère', 1), 
    ('Cousin', 2), 
    ('Cousine', 2),
    ('Conjoint(e)', 1),
    ('Frère', 2),
    ('Sœur', 2),
    ('Autre', 3);   


SET client_encoding TO 'UTF8';
SET client_encoding TO 'WIN1252';
SET client_encoding TO 'LATIN1';

INSERT INTO api_services (nom) 
VALUES 
    ('Direction'),
    ('Ressources Humaines'),
    ('Comptabilité et Finances'),
    ('Logistique'),
    ('Informatique / IT'),
    ('Passation de Marchés'),
    ('Suivi et Évaluation'),
    ('Technique / Opérationnel');

INSERT INTO api_postes (nom, grade) 
VALUES 
    ('Coordonnateur de Projet', 1),
    ('Responsable Administratif et Financier', 1),
    ('Chef de Service', 2),
    ('Responsable des Ressources Humaines', 2),
    ('Expert Technique Senior', 2),
    ('Specialiste en Passation de Marches', 2);

INSERT INTO api_role  (name,created_at)  
VALUES
     ('admin',NOW()),
     ('User',NOW()),
     ('Superadmin',NOW());

ajout pour admin direct // ça marche pas:
 SET session_replication_role = 'replica'; 
 SET session_replication_role = 'origin';     

Update role test:
 UPDATE api_login
 SET role_id = 1
 WHERE email_id = 'misaharitsoa@gmail.com';

pour creation admin login json {
    {
    "email": "admin@mail.com",
    "password": "admin",
    "role": 1
}
}

DROP TABLE IF EXISTS api_statut, api_typeconge, api_loginadmin, api_soldeconge, api_conge CASCADE;

INSERT INTO api_statut (id, statut) VALUES
 (1, 'En attente'),
 (2, 'Approuvé'),
 (3, 'Refusé');


INSERT INTO api_typeconge (id, libelle, code, duree_max) VALUES
 (1, 'Congé annuel', 'CA', 30),
 (2, 'Congé maladie', 'CM', 90),
 (3, 'Congé maternité', 'MAT', 120),
 (4, 'Congé paternité', 'PAT', 14),
 (5, 'Congé sans solde', 'CSS', 180),
 (6, 'Congé exceptionnel', 'CE', 5),
 (7, 'RTT', 'RTT', 12);
<<<<<<< HEAD
=======
=======
=======
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> dcc45aed (linux)
>>>>>>> origin/back_test
-- creer la base de donnee
CREATE DATABASE rh;

-- se connecter a la base de donnee
\c rh

--Pour lister les tables dans la base de donnee
\dt

INSERT INTO api_etatcivil (nom) 
VALUES 
    ('Célibataire'), 
    ('Marié(e)'), 
    ('Divorcé(e)'), 
    ('Veuf/Veuve');

INSERT INTO api_typecontrats ("TypeContrat") 
VALUES 
    ('Salarié'), 
    ('Consultant'),
    ('Stage');

INSERT INTO api_sexes (nom) 
VALUES 
    ('Masculin'), 
    ('Féminin');

INSERT INTO api_modefinancement (nom) 
VALUES 
    ('Fond Mondial'), 
    ('Alliance Gavi'), 
    ('Banque Mondiale/PPSB'), 
    ('Banque Mondiale/PARN');

INSERT INTO api_relations (nom, grade) 
VALUES 
    ('Père', 1), 
    ('Mère', 1), 
    ('Cousin', 2), 
    ('Cousine', 2),
    ('Conjoint(e)', 1),
    ('Frère', 2),
    ('Sœur', 2),
    ('Autre', 3);   


SET client_encoding TO 'UTF8';
SET client_encoding TO 'WIN1252';
SET client_encoding TO 'LATIN1';

INSERT INTO api_services (nom) 
VALUES 
    ('Direction'),
    ('Ressources Humaines'),
    ('Comptabilité et Finances'),
    ('Logistique'),
    ('Informatique / IT'),
    ('Passation de Marchés'),
    ('Suivi et Évaluation'),
    ('Technique / Opérationnel');

INSERT INTO api_postes (nom, grade) 
VALUES 
    ('Coordonnateur de Projet', 1),
    ('Responsable Administratif et Financier', 1),
    ('Chef de Service', 2),
    ('Responsable des Ressources Humaines', 2),
    ('Expert Technique Senior', 2),
    ('Specialiste en Passation de Marches', 2);

INSERT INTO api_role  (name,created_at)  
VALUES
     ('admin',NOW()),
     ('User',NOW()),
     ('Superadmin',NOW());

ajout pour admin direct // ça marche pas:
 SET session_replication_role = 'replica'; 
 SET session_replication_role = 'origin';     

Update role test:
 UPDATE api_login
 SET role_id = 1
 WHERE email_id = 'misaharitsoa@gmail.com';

pour creation admin login json {
    {
    "email": "admin@mail.com",
    "password": "admin",
    "role": 1
}
}

DROP TABLE IF EXISTS api_statut, api_typeconge, api_loginadmin, api_soldeconge, api_conge CASCADE;

INSERT INTO api_statut (id, statut) VALUES
 (1, 'En attente'),
 (2, 'Approuvé'),
 (3, 'Refusé');


INSERT INTO api_typeconge (id, libelle, code, duree_max) VALUES
 (1, 'Congé annuel', 'CA', 30),
 (2, 'Congé maladie', 'CM', 90),
 (3, 'Congé maternité', 'MAT', 120),
 (4, 'Congé paternité', 'PAT', 14),
 (5, 'Congé sans solde', 'CSS', 180),
 (6, 'Congé exceptionnel', 'CE', 5),
 (7, 'RTT', 'RTT', 12);
<<<<<<< HEAD
=======
>>>>>>> 2b8eb512 (deploie)
-- creer la base de donnee
CREATE DATABASE rh;

-- se connecter a la base de donnee
\c rh

--Pour lister les tables dans la base de donnee
\dt

INSERT INTO api_etatcivil (nom) 
VALUES 
    ('Célibataire'), 
    ('Marié(e)'), 
    ('Divorcé(e)'), 
    ('Veuf/Veuve');

INSERT INTO api_typecontrats ("TypeContrat") 
VALUES 
    ('Salarié'), 
    ('Consultant'),
    ('Stage');

INSERT INTO api_sexes (nom) 
VALUES 
    ('Masculin'), 
    ('Féminin');

INSERT INTO api_modefinancement (nom) 
VALUES 
    ('Fond Mondial'), 
    ('Alliance Gavi'), 
    ('Banque Mondiale/PPSB'), 
    ('Banque Mondiale/PARN');

INSERT INTO api_relations (nom, grade) 
VALUES 
    ('Père', 1), 
    ('Mère', 1), 
    ('Cousin', 2), 
    ('Cousine', 2),
    ('Conjoint(e)', 1),
    ('Frère', 2),
    ('Sœur', 2),
    ('Autre', 3);   


SET client_encoding TO 'UTF8';
SET client_encoding TO 'WIN1252';
SET client_encoding TO 'LATIN1';

INSERT INTO api_services (nom) 
VALUES 
    ('Direction'),
    ('Ressources Humaines'),
    ('Comptabilité et Finances'),
    ('Logistique'),
    ('Informatique / IT'),
    ('Passation de Marchés'),
    ('Suivi et Évaluation'),
    ('Technique / Opérationnel');

INSERT INTO api_postes (nom, grade) 
VALUES 
    ('Coordonnateur de Projet', 1),
    ('Responsable Administratif et Financier', 1),
    ('Chef de Service', 2),
    ('Responsable des Ressources Humaines', 2),
    ('Expert Technique Senior', 2),
    ('Specialiste en Passation de Marches', 2);

INSERT INTO api_role  (name,created_at)  
VALUES
     ('admin',NOW()),
     ('User',NOW()),
     ('Superadmin',NOW()),
     ('Chef',NOW()),
     ('GP',NOW()),
     ('RF',NOW());


ajout pour admin direct // ça marche pas:
 SET session_replication_role = 'replica'; 
 SET session_replication_role = 'origin';     

Update role test:
 UPDATE api_login
 SET role_id = 1
 WHERE email_id = 'misaharitsoa@gmail.com';

pour creation admin login json {
    {
    "email": "admin@mail.com",
    "password": "admin",
    "role": 1
}
}

DROP TABLE IF EXISTS api_statut, api_typeconge, api_loginadmin, api_soldeconge, api_conge CASCADE;

INSERT INTO api_statut (id, statut) VALUES
 (1, 'En attente'),
 (2, 'Approuvé'),
 (3, 'Refusé');


INSERT INTO api_typeconge (id, libelle, code, duree_max) VALUES
 (1, 'Conge Planifié', 'CP', 30),
 (2, 'Permission', 'PE', 90),
 (3, 'Conge Annuel', 'CA', 30),
 (4, 'Recuperation', 'RE', 90);

 -- À exécuter après makemigrations + migrate
-- Table cible : api_evenementpermission (préfixe Django = app_label + nom model en lowercase)
-- Adapter le nom de table selon ton app_label réel

INSERT INTO api_evenementpermission (code, libelle, duree_defaut, est_fractionnable, delai_prise) VALUES
(1, 'Mariage du salarié et circoncision d''un enfant du salarié',        3.0,  FALSE, NULL),
(2, 'Mariage d''un enfant, du père, de la mère, ou d''un enfant du conjoint de l''employé', 3.0, FALSE, NULL),
(3, 'Naissance de l''enfant, adoption d''un enfant',                      3.0,  TRUE,  15),
(4, 'Décès du conjoint, de l''enfant, du père, de la mère de l''agent, du père ou de la mère du conjoint, d''un des petits-enfants', 3.0, FALSE, NULL),
(5, 'Décès d''un frère, d''une sœur de l''employé, d''un frère ou d''une sœur du conjoint, des grands-parents, d''un gendre de l''agent', 1.0, FALSE, NULL),
(6, 'Obligations reliées à la garde, à la santé ou à l''éducation d''un enfant mineur', NULL, FALSE, NULL),
(7, 'Obligations reliées à l''état de santé du conjoint, du père, de la mère de l''employé', NULL, FALSE, NULL);
