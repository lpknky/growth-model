Voici ce que ressort le code download_and_cleanning :
                                                                                                 rule  rows_affected                         action  rows_remaining
                                                                                        Raw users.csv          70851                 loaded as text           70851
                                                                                 Exact duplicate rows            562            dropped, first kept           70289
                                                           Duplicate user_id with conflicting content              0                     none found           70289
                                           Internal/test accounts (user_id 'QA_', channel 'internal')             45                        removed           70244
                                                          Mixed date format dd/mm/yyyy in signup_date           1358         parsed day-first, kept           70244
                                                            Impossible signup_date (1900, 1970, 2099)              7   removed (no cohort possible)           70237
                        Inconsistent channel labels ('tiktok','meta_ads','Facebook Ads','google_ads')           7336       harmonised to 6 channels           70237
                                                                                      Missing country           1494 kept as 'Unknown', not imputed           70237
Chronology checks (trial<signup, sub<trial, end<=start, plan/end without sub, dates after extraction)              0           violations remaining           70237


Il y a donc 8 etapes de nettoyages mais 2 ne sont pas pertinentes ( Duplicate user_id with conflicting content  et Chronology checks )
Explication de chaque étapes :

- On a donc supprimer les doublons, 

- Il n y a donc pas pour un même user id plusieurs ligne avec des infos differentes , 

- On supprime les user id QA car ce sont des faux comptes créés par les développeurs ou les testeurs,

- On a mis les dates au bon format car il y avait 2 types de format dates, on a gardé le format AAAA-MM-JJ,

- On enleves les lignes avec des dates d inscriptions aberrantes (comme l'année 1900, ou 2099)

- On gère les differenctes écritures qui correspondent à un un même canal, pour ne pas avoir des classes différentes qui reprensente le même canal en réalité

- On creer une nouvelle classe Unknow pour le pays du user quand le pays n'est pas renseigné
 
