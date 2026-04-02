# NutriTrack Pro - Documentation Technique

NutriTrack Pro est une solution Cloud Native de suivi nutritionnel. Elle permet la gestion des objectifs caloriques, le suivi pondéral via des graphiques dynamiques et la documentation visuelle des repas.

---

## 1. Architecture du Système

L'application repose sur une architecture découplée pour garantir la persistance des données dans un environnement Cloud éphémère.

* **Backend :** Django 5.x (Python) - Gestion de la logique métier et de l'ORM.
* **Frontend :** HTML5 / CSS3 (Variables CSS) / Chart.js (Visualisation de données).
* **Base de Données :** PostgreSQL (via Supabase) - Choisi pour la persistance et la gestion des relations complexes.
* **Stockage Médias :** Cloudinary (SaaS) - Déportation des images pour contrer le stockage éphémère du PaaS.

---

## 2. Installation et Configuration Locale

### Pré-requis
* Python 3.10+
* Environnement virtuel (venv)
* Bibliothèque Pillow (pour le traitement d'images)

### Procédure de lancement
1. **Activer l'environnement virtuel** :
   ```bash
   source env/bin/activate  # Linux/Mac
   .\env\Scripts\activate   # Windows

## 3. Stratégie de Déploiement (Cloud)

Le projet utilise un modèle hybride pour maximiser la fiabilité tout en restant sur des offres gratuites (Free Tier).

| Composant        | Modèle | Fournisseur | Justification Technique |
|------------------|--------|------------|------------------------|
| Application      | PaaS   | Render     | Déploiement automatisé via GitHub (CI/CD) |
| Base de données  | DBaaS  | Supabase   | Persistance des données en production |
| Stockage Médias  | SaaS   | Cloudinary | Stockage permanent des images |

---

## 4. Modélisation des Données (Modèles Django)

### FoodItem
Référentiel des aliments :
- nom
- calories (kcal/100g)
- protéines
- glucides
- lipides
- image

### MealEntry
Journal alimentaire :
- utilisateur
- aliment (FoodItem)
- quantité
- date
- calcul automatique des calories et macros

### WeightEntry
Suivi du poids :
- utilisateur
- poids
- date

### Profile
Extension du modèle User :
- objectif calorique journalier
- autres métriques personnalisées

---

## 5. Dépendances de Production (requirements.txt)
* **django>=5.0**
* **Pillow**
* **dj-database-url**
* **django-cloudinary-storage**
* **gunicorn**
* **whitenoise**

---

## 6. Sécurité et Maintenance

### Variables d’environnement
Utilisation d’un fichier `.env` pour stocker :
- SECRET_KEY
- DATABASE_URL
- CLOUDINARY_URL

### Configuration Django en production
- DEBUG = False
- ALLOWED_HOSTS configuré
- SECURE_SSL_REDIRECT = True

### Fichiers statiques
Configuration de WhiteNoise pour servir les fichiers statiques sans serveur externe.

---

## 7. Persistance des Données

Le système de fichiers des plateformes PaaS est éphémère.

Solution mise en place :
- Base de données externalisée (Supabase)
- Stockage des médias externalisé (Cloudinary)

Résultat :
- Données persistantes
- Images conservées après redéploiement
- Meilleure scalabilité

---

## 8. Améliorations Futures

- Ajout d’une API REST (Django REST Framework)
- Authentification OAuth (Google, Apple)
- Application mobile (React Native / Flutter)
- Recommandations nutritionnelles intelligentes
- Suivi des micronutriments

---

## 9. Monitoring et Logs

- Configuration du logging Django
- Intégration possible avec Sentry
- Surveillance uptime (UptimeRobot ou équivalent)

---

## 10. Performance

Optimisations possibles :
- Mise en cache (Redis)
- Optimisation des requêtes ORM (select_related, prefetch_related)
- Compression des fichiers statiques

---

## 11. Conclusion

NutriTrack Pro est conçu comme une application Cloud Native :

- Architecture découplée
- Services externalisés
- Haute résilience aux redéploiements
- Facilité de montée en charge

Le projet constitue une base solide pour une application nutritionnelle moderne et évolutive.