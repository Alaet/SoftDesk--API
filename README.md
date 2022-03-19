[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

# SoftDeskAPI

Solution B2B servant à remonter et suivre des problèmes techniques (Ticketing System)


## Démarrage

Une fois l'appliction télécharger, pour mettre en place :

1. A partir de votre terminal, se mettre au niveau du répertoire "APISoftDesk".


2. Créer un environnement virtuel avec la commande:

   `python3 -m venv venv` ou `py -m venv venv`


3. Activer l'environnement virtuel:

   `venv\Scripts\activate`


4. Installer les bibliothèques nécessaires depuis le répertoire "APISoftDesk":

   `pip install -r requirements.txt`


5. Lancer le serveur Django:
   - Pour initialiser une base de donnée :
   
   
      `python3 manage.py makemigrations`

      `python3 manage.py migrate` 
      
      `py manage.py runserver` ou `python3 manage.py runserver` 

Lien vers la documentation de l'API :

[SoftDeskAPI Documentation](https://documenter.getpostman.com/view/19944119/UVsFyThV)