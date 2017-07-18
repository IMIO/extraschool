.. AES documentation master file, created by
   sphinx-quickstart on Tue Sep  8 15:33:32 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Configuration des smartphones
=============================

.. toctree::
   :maxdepth: 3
   
############
Introduction
############

Utilisation des smartphones à l'application AES


#########################
Encodage QR Code attribué
#########################

Pour ce type d'encodage, l'enfant est en possession d'un QR Code propre.

  * Matin
     * À l'arrivée de l'enfant, appuyer sur ENTRÉE (Le nom est situé dans un grand carré vert)
  * Soir
     * À la sortie de l'enfant, appuyer sur SORTIE (Le nom est situé dans un grand carré rouge)

.. image:: img/screenshot/home_application_aes.png


########################
Encodage QR Code anonyme
########################

Pour ce type d'encodage, l'enfant n'est pas en possession d'un QR Code propre mais on lui attribue un QR Code.

.. image:: img/screenshot/anonyme_1.png

Pour l'encodage il suffit :

  * de taper la première lettre du nom ou du prénom afin de faire apparaître la liste des enfants contenant cette lettre.
  * de sélectionner dans la liste qui apparaît les coordonnées qui correspondent à l'enfant.
  * Lorsque vous avez sélectionné l'enfant, et que celui-ci apparaît dans le cadre entouré en orange, appuyer sur OK.

.. image:: img/screenshot/anonyme_2.png

NOTE IMPORTANTE : Il n'est pas necesaire de recommencer ENTRÉE ou SORTIE


########################
Attribution d'un QR Code
########################

Lorsqu'un nouvel enfant est arrvié dans l'établissement scolaire OU lorsque l'enfant n'est jamais venu à l'accueil.
Autrement dit :

  * Il n'apparaît pas encore dans la liste du logiciel
  * Un QR Code ne lui a pas encore été attribué

Dans ce cas :

  * Scanner un nouveau QR Code

.. image:: img/screenshot/qr_code_1.png

  * Taper le nom et le prénom de l'enfant dans le cadre entouré en Orange

.. image:: img/screenshot/qr_code_2.png

  * Lorsque les coordonnées sont exactes, appuyer sur OK.

.. image:: img/screenshot/qr_code_3.png

Maintenant que l'enfant possède un QR Code et que ses coordonées ont été encodés, il faut procéder comme pour l'encodage ordinaire.

###########
Bouton MENU
###########


#######
Astuces
#######

  * L'encodage manuel apparaît lorsque vous avez laissé votre doigt trop longtemps appuyé sur ENTRÉE ou sur SORTIE. Pour revenir en arrière, appuyer sur la flèche "Retour en arrière".
  * Pour supprimer un mauvais encodage : Laisser votre doigt appuyer sur le nom de l'enfant. Un message apparaîtra : "Voulez-vous supprimer ? Oui / Non"
  * Il est normal que :
     * Le matin : la liste qui apparaît sur le smartphone est vide (Les données ont été transmises pendant la nuit)
     * Le soir : La liste qui apparaît sur le smartphone est pleine (Les données seront transmises durant la nuit)



