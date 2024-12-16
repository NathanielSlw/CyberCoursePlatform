## Online Cybersecurity Course Platform

Ce projet est une **plateforme de cours en ligne** centrée sur la cybersécurité, permettant aux utilisateurs de s'inscrire, de naviguer dans un catalogue de cours, de suivre leurs progrès, et de générer des certificats après avoir complété les cours. Il offre également une fonctionnalité de panier pour acheter des cours.

Le projet utilise Flask pour le backend, SQLite pour la base de données, et Bootstrap pour un design épuré et responsive.

---

Sommaire :
* Liens 
* Lancer notre projet
* Fonctionnalités 
* Structure du projet 

---

### Liens 
* Lien des slides de présentation : [Slides de présentation](./Slides_Presentation_Projet.pptx)
* Lien de la vidéo de démonstration : [Vidéo de démonstration](./Video_demo_site.mp4)

### Lancer notre projet 

Installer les bibliothèques : 
```
pip install flask flask-sqlalchemy flask-migrate werkzeug
```

Lancer le serveur : 
```
flask run
```

### Fonctionnalités

#### 1. Gestion des utilisateurs
- **Inscription et connexion** :
  - Création de compte avec validation de base des champs.
  - Connexion sécurisée avec hashage des mots de passe.
- **Déconnexion** :
  - Session sécurisée permettant de se déconnecter facilement.

#### 2. Catalogue de cours
- **Affichage des cours** :
  - Liste des cours disponibles avec image, description, et prix.
- **Détails des cours** :
  - Informations détaillées sur chaque cours, y compris les chapitres associés.

#### 3. Gestion des achats
- **Panier d'achat** :
  - Ajout de cours au panier.
  - Consultation du panier avec calcul du prix total.
  - Retrait de cours du panier.
- **Achat de cours** :
  - Transfert des cours achetés vers la liste des cours de l'utilisateur.

#### 4. Suivi des progrès
- **Progrès des chapitres** :
  - Possibilité de marquer les chapitres comme terminés.
  - Mise à jour automatique de la progression globale d’un cours.
- **Accès aux chapitres** :
  - Lecture des chapitres de cours achetés.

#### 5. Génération de certificats
- **Téléchargement des certificats** :
  - Les utilisateurs peuvent télécharger un certificat après avoir complété 100 % d’un cours.

### Structure du projet

```
/ProjetCyberPlatform/
  ├── app.py               # Fichier principal de l'application Flask
  ├── models.py            # Définition des modèles de base de données
  ├── templates/           # Dossier des fichiers HTML
       ├── register.html
       ├── login.html
       ├── dashboard.html
       ├── course_detail.html
       ├── cart.html
       ├── my_courses.html
       ├── apropos.html
  ├── migrations/          # Dossier des fichiers de migration
  ├── instance/
      ├── app.db           # Fichier de base de données SQLite
```
