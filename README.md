Voici ce que ressort le code download_and_cleanning :
                                                                                             

On a a chaque fois la modif effectué et le nombre de colonnes affectées par cette modif.
Il y a donc 8 etapes de nettoyages mais 2 ne sont pas pertinentes ( Duplicate user_id with conflicting content  et Chronology checks )
Explication de chaque étapes :

- On a donc supprimer les doublons, 

- Il n y a donc pas pour un même user id plusieurs ligne avec des infos differentes , 

- On supprime les user id QA car ce sont des faux comptes créés par les développeurs ou les testeurs,

- On a mis les dates au bon format car il y avait 2 types de format dates, on a gardé le format AAAA-MM-JJ,

- On enleves les lignes avec des dates d inscriptions aberrantes (comme l'année 1900, ou 2099)

- On gère les differenctes écritures qui correspondent à un un même canal, pour ne pas avoir des classes différentes qui reprensente le même canal en réalité

- On creer une nouvelle classe Unknow pour le pays du user quand le pays n'est pas renseigné
 
