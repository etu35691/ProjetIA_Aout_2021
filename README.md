# Projet Intelligence Artificielle
Instructions afin de faire les migrations:
-Supprimer les dossiers de migrations
-Supprimer (éventuellement) la dbsq_lite
-Utiliser:
1."python manage.py makemigrations game"
2."python manage.py makemigrations AI"
3."python manage.py makemigrations connection"
4."python manage.py migrate --run-syncdb"

Les pages ne sont pas encore liées entre elles mais le seront pour la démo vidéo.
Notre module d'entrainement n'est pas encore développé. (18/12)
Lorsque deux IA jouent entre elles, le résultat s'affiche dans le terminal.


Pour se connecter et se créer un compte:
1.Aller sur la page http://127.0.0.1:8000/connection/

Pour lancer une partie:
1.Avoir créé des utilisateurs sur http://127.0.0.1:8000/connection/signup et/ou des IA sur http://127.0.0.1:8000/connection/signup_ai
2.Aller sur la page : http://127.0.0.1:8000/game/
3.Entrer deux utilisateurs précédemment créés.
4.Pour voir les statistiques aller sur la page http://127.0.0.1:8000/game/stats
5.Pour entrainer deux IA aller sur la page http://127.0.0.1:8000/AI/train
