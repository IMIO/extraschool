.. AES documentation master file, created by
   sphinx-quickstart on Tue Sep  8 15:33:32 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Gestion des parents divorcés
============================

.. toctree::
   :maxdepth: 3

Dans le cas d'enfant de parents séparés, l'enfant est encodé 2 fois dans l'application afin de simplifier la gestion administrative.

* Factures séparées papa et maman.
* Attestations fiscales séparées.
* Les parents n'ont pas de visibilité sur la facturation de leur ex-conjoint.

On va donc créer les deux parents et deux fois le même enfant dans l'application.
On pourra donc relier une fiche enfant au papa et l'autre fiche enfant à maman.
Sur l'une des deux fiches enfants, dans le nom ou le prénom, nous mettons "papa" ou "maman" afin d'avoir une meilleure et une plus rapide visualisation.

Il faudra donc imprimer deux QR Codes pour cet enfant et scanner en fonction de la personne qui vient le déposer ou le chercher.

