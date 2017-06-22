.. AES documentation master file, created by
   sphinx-quickstart on Tue Sep  8 15:33:32 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Facturier
=========

.. toctree::
   :maxdepth: 3
   
#############
Introduction.
#############

Un facturier est l’ensemble des factures des parents durant la période d’un mois. Celles-ci sont générés pour tous les établissements scolaires.

#############
Signalétique.
#############


Pour effectuer la génération d’un facturier, il faut se rendre dans le menu “facturation”.
Une fiche apparaît avec des informations obligatoires telles que :
  * Catégorie d’activité
  * Implantation scolaire
  * Début par défaut
  * Fin par défaut
  * Date de la facture
  * Echéance
Lorsque vous confirmez les informations, cela va générer toutes les factures des différents parents.


##################
Génération des PDF
##################


Lorsque vous avez généré le facturier, les différents pdf sont en cours de création. (Il vous met d’ailleurs un message pour vous le signaler en haut à droite de la fiche du facturier)
Cela peut prendre quelques minutes, mais il est utile de rafraîchir votre page afin de les voir s’afficher.
Si après le rafraîchissement il n’y a toujours pas de PDF, il suffit d’attendre encore quelques minutes et de rafraîchir à nouveau.


##########################
Mode d'envoi de la facture
##########################

Les factures peuvent être envoyées :
  * Uniquement par courrier
  * Uniquement par email
  * Par courrier et par email
Ce choix s’effectue au niveau de la fiche des parents. Cette section est valable aussi pour le mode d’envoi des rappels.
Après ce choix effectué sur les différentes fiches, les factures pourront être envoyées comme l’ont décidé les parents.

Lorsque nous sommes sur la fiche d’un facturier (Facturier - Sélectionner une ligne),
nous pouvons apercevoir deux boutons :
  * Factures courrier
  * Email factures


*****************
Factures courrier
*****************

Cette action nous renvoie la liste des factures où les parents désirent recevoir la facture par courrier.
Il faut donc sélectionner toute la liste. Pour cela, cocher la case située à gauche de la colonne nommée “Parent”. (Cette case sélectionnera automatiquement toutes les lignes des factures).
On doit cliquer sur le bouton “Imprimer” situé au-dessus et prendre le rapport nommé “Facture”.

*************
Email facture
*************

Cette action nous renvoie la liste des factures où les parents désirent recevoir la facture par email. Celui-ci doit, bien évidemment, être renseigné sur la fiche du parent.
l faut donc sélectionner toute la liste. Pour cela, cocher la case située à gauche de la colonne nommée “Parent”. (Cette case sélectionnera automatiquement toutes les lignes des factures).
On doit cliquer sur le bouton “Autres options” situé au-dessus et prendre l’action “Invoice mail” afin d’envoyer les différentes factures par email.
Remarque importante : Les factures affichées sont ouvertes. Celles à un montant de 0.00 euro ou payé ne seront pas affichées dans aucune liste.
En effet, il est inutile de renvoyer à un parent une facture qu’il a déjà payé ou une facture contenant un montant nul.
