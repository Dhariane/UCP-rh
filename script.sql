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
     ('User',NOW());

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