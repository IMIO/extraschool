.. AES documentation master file, created by
   sphinx-quickstart on Tue Sep  8 15:33:32 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Checklist avant lancement de projet !
=====================================

.. toctree::
   :maxdepth: 3
   
#############
Introduction.
#############

Avant de se lancer dans l'implémentation de la solution AES, il est important de se poser les bonnes questions qui feront de ce projet une success story.

Certaines réponses se trouvent dans le règlement communal.

#############
Signalétique.
#############

*******************
Import des données.
*******************
Il est possible d'importer les signalétiques enfant et parent venant de fichiers xls.
Les logiciels de gestion d'école peuvent exporter ce genre de fichiers, il faut cependant faire attention à quelques détails.

* Est-ce que les données sont à jour ?

	* En septembre, c'est rarrement le cas !
	* Il peut être intéressant d'utiliser un formulaire d'inscription.
	
	| ex. Formulaire
	| Cela permet d'être à jour rapidement
	
* Format d'export
	
	* Demander aux directeurs d'écoles de respecter le même format d'export
		
		* Ordre des colonnes
		* Libellé des colonnes
	
		| :download:`ex. format.xls <doc/import.xls>`

******
Ecole.
******
On parle ici de l'entité administrative (direction), dont dépendent une ou plusieurs implantations

Champs obligatoires :

* Nom
* Adresse

*************
Implantation.
*************
On parle ici du batiment qui dépend d'une école (direction)

Champs obligatoires :

* Nom
* Adresse
* Nom de l'école dont elle dépend

***************
Lieu d'accueil.
***************
Le lieu d'accueil est l'endroit ou se déroule une activité, il peut être partagé par plusieurs implantations scolaire.

Champs obligatoires :

* Nom
* Adresse
* Liste des implantations scolaire qui sont suceptiblent d'y organiser des activités

*******
Parent.
*******
Personne responable à qui les documents seront adressés

* Nom
* Prénom
* Adresse
* Diférenciation positive (Rapport ONE)
* Mode d'envoie des documents (facture, invitation à payer ...) 
	
	Valeurs possibles
	
	* courrier
	* email
	* courrier et email

*******
Enfant.
*******
Dans le cas d'enfant de parents séparés, l'enfant est encodé 2 fois dans l'application afin de simplifier la gestion administratives.

* Factures séparées papa et maman.
* attestations fiscale séparées.
* les parents n'on pas de visibilité sur la facturation de leur ex conjoint. 

Champs obligatoires :

* Nom
* Prénom
* Implantation scolaire
* Niveau

	Valeurs possibles
	
	* 1ère maternelle
	* 2ème maternelle
	* 3ème maternelle
	* 1ère primaire
	* 2ère primaire
	* 3ère primaire
	* ...
	* 6ème primaire
	
* Date de naissance
* Parent responsable

*********
Activité.
*********
On entend par activité, toute période de temps nécéssitant le suivi de la présence de l'enfant
ex. Accueil du matin, repas de midi, bricolage du mercredi ...

Champs obligatoires :

* Nom
* Niveau auquel s'adresse l'activité

	Valeurs possibles
	
	* maternelle
	* primaire
	* maternelle et primaire
	
* Est-ce une activité sur inscription uniquement ?
* Quand est-ce que l'activité a lieu ?

	* jour de la semaine
	* horaire (heure de début et heure de fin)

* Lieux d'accueil (plusieurs valeurs possibles)
* Est-ce subsidié par l'ONE ?
* Est-ce que cette activité doit apparaître sur l'attestation fiscale ?
* Catégorie d'activité
* Est-ce qu'il y a des regroupements de plusieurs implantations scolaire sur le même lieux d'accueil ?

*********************
Catégorie d'activité.
*********************

Les activités sont gérées par des pouvoirs organisateurs qui sont parfois indépendants et qui ont leurs propres règles, 
c'est ici que nous allons les définir.

* Logo à utiliser sur les documents
* Numéro de compte bancaire
* Communication structurée

	* Préfixe (les 3 premiers chiffres)
		
		il peut être différent pour :
		
		* l'invitation à pré-payer
		* la facture
		* le rappel
 
 	* Format du document, le mieux est de demander un exemple au responssable financier
 		
 		* invitation à pré-payer
 		* facture
 		* rappel

####################
Journée pédagogique.
####################

* Avez-vous déjà les dates ?
* Faut il être inscrit ?
* Y a t'il des garderies avant et/ou après la journée pédagogique ?
* Ou est organisé l'accueil ces jours là ?


##############
Liste de prix.
##############

* Quel prix est associé à quelle activité ?
* Réduction en fonction de la position de l'enfant
	
	* Lister ces réductions
	* Comment est calculée la position de l'enfant
	
		* Regroupement
	
			* Par parent 
			
				En cas de famille recomposée habitant sous le même toit, les 2 familles sont prises séparément 
	
			* Par adresse
	
				En cas de famille recomposée habitant sous le même toit, les 2 familles sont considérées comme une fammille unique 

		* Calcul de la position
		
			* Absolue
			
				la position de l'enfant est sa position par ordre décroissant sur la date de naissance 
			
			* Par présence à l'activité
			
				la position de l'enfant est sa position par ordre d'arrivée à l'activité
			
			* Par nombre
			
				la position de l'enfant est déterminée par le nombre d'enfants présents à l'activité
	
	* Unité de temps 
	
		* minute
		* 15 minutes
		* 30 minutes
		* 60 minutes
		* ...
		
	* Tolérance
	
		Il est possible de paramètrer une tolérence exprimée en minute pour le calcule de la durée.
		
		| ex. unité : 30 minutes, tolérancce 5 minute
		|	durée mesurée 34 minutes -> durée facturée 1*30 minutes
		|	durée mesurée 36 minutes -> durée facturée 2*30 minutes
		
	* Avez-vous un système de pénalité pour les retard, si oui lequel ?
	* Avez-vous des plages horaires gratuite
	* avez-vous des périodes d'étude qui doivent être décomptée 
	
		

###########
Smartphone.
###########
Le smartphone est utilisé par les accueillantes pour enregistrer les présences des enfants.
 
* Le smartphone est dédié à la gestion des présence	
* Un smartphone minimum par lieu d'accueil
* Le smartphone reste sur le lieu d'accueil
* Penser à sécuriser le smartphone pour le protéger du vol
* Penser à la connexion internet
 	
	Le smartphone s'utilise en mode déconnecté d'internet, 
 	cependant il faut absolument une connexion une fois par jour pour transmettre les données au serveur.

 	* wifi
 	
 		Attention !
 	
 		* Pas toujours disponible.
 		* Certains directeurs d'école sont contre pour des raisons de santé. 
 		
 			Dans ce cas, il possible d'utiliser une prise avec minuteur qui active le wifi la nuit pour la transmission 
 			et qui le désactive quand les enfants sont à l'école 
 	
 	* 3G
 	
 		* Pas toujours disponible
 		* un abonnement est obligatoires, le plus petit convient parfaitement 

#########
QR-Codes.
#########
Il en faut un par enfant

* il sont habituellement distibué dans les écoles, par classe afin de ne pas désorganiser l'accueil les premiers jours
* il n'est pas forcément nominatif, le nom de l'enfant apparait sur le smartphone au moment du scan, 

	il est donc très facile pour l'accueillante de vérifier que le QR-Code appartient bien à l'enfant. 

* Fabrication
	
	* Il est possible de les imprimer via l'application
		* plastifié
		* papier indéchirable (utilisé dans les aéroports)

			`PAPIER POLYESTER INDECHIRABLE EN 195µ FORMAT A4 <https://www.google.be/search?q=PAPIER+POLYESTER+INDECHIRABLE+EN+195%C2%B5+FORMAT+A4>`_

		* prévoir des anneaux (porte clef)
		* prévoir des rivets (utilisé au service population 
		 
			

#############
Communication
#############

Communiquer sur les changements est primordial pour la réussite du projet, la difficulté n'est pas sur la technique mais bien sur l'aspect humain.
Il faut prévoir un courrier qui explique aux parents les changements.

* Le QR-Code contient uniquement un identifiant interne qui ne représente rien en dehors du contexte de l'application.
	
	.. image:: img/qrcode.png
	
	ce QR-Code contient juste l'identifiant : "1"
	
* Inssister sur les avantages

	* Gain de temps pour les accueillantes qui peuvent ainsi mieux se consacrer à l'accueil des enfants.
	* Transparence pour la facturation.
	* Gain de temps pour les coordinateurs qui peuvent dès lors mieux se concentrer sur leur projet ATL.
	 


...