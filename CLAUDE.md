# CLAUDE.md

## Projet
Solveur du jeu « Des chiffres et des lettres » (Countdown). L'utilisateur saisit les 6 nombres tirés et l'objectif ; l'application renvoie la suite d'opérations qui produit l'objectif, ou à défaut celle qui s'en approche le plus. Ce n'est **pas** un jeu : aucun tirage aléatoire, aucun chronomètre.

- Backend : Django (Python 3.14), sans base de données, sans Django REST Framework.
- Frontend : React 19 + Vite 8 (JavaScript, pas de TypeScript).
- Langue de l'interface, des commentaires et des messages d'erreur : français.

## Structure
```
backend/
  manage.py
  config/            settings.py, urls.py, wsgi.py
  solver/
    solver.py        algorithme de recherche (logique pure, sans Django)
    views.py         endpoint POST /api/solve/
    urls.py
    tests.py
frontend/
  vite.config.js     proxy /api -> http://localhost:8000
  src/App.jsx        formulaire, validation, affichage du résultat
  src/styles.css
```

## Commandes
```
# Backend (depuis backend/)
pip install -r requirements.txt
python manage.py runserver        # :8000
python manage.py test

# Frontend (depuis frontend/)
npm install
npm run dev                       # :5173
npm run build
```
Node.js 20.19+ est requis (Vite 8).

## Règles du jeu (à respecter dans toute modification)
- 6 nombres : chacun est un petit nombre (1 à 10) ou un grand nombre (25, 50, 75 ou 100).
- Un petit nombre (1 à 10) ne peut apparaître que deux fois au maximum.
- Un grand nombre (25, 50, 75, 100) ne peut apparaître qu'une seule fois.
- Objectif : entier de 100 à 999 inclus.
- Opérations : `+`, `-`, `×`, `÷`. Chaque nombre est utilisé **une fois au maximum** (pas obligatoirement tous).
- Les résultats intermédiaires doivent être des **entiers strictement positifs** : pas de négatifs, pas de fractions, pas de zéro.
- Un résultat intermédiaire peut être réutilisé dans une autre opération, dans n'importe quel ordre.
- Si l'objectif est inatteignable, renvoyer la meilleure approche (plus petit écart).

## API
`POST /api/solve/`
```json
{ "numbers": [25, 50, 75, 100, 3, 6], "target": 952 }
```
Réponse 200 :
```json
{ "exact": true, "value": 952, "difference": 0,
  "steps": [{ "left": 75, "op": "×", "right": 3, "result": 225 }] }
```
Réponse 400 : `{ "error": "..." }` (nombres ou objectif invalides). La validation est faite côté serveur (`views.py`) **et** côté client (`App.jsx`) ; toute modification des règles doit être faite aux deux endroits.

## Conventions
- Python : type hints obligatoires sur tous les paramètres et types de retour de chaque fonction, y compris dans les tests (`-> None`). Les structures de données du solveur sont des `TypedDict` (`solver.py`). Utiliser les génériques natifs (`list[int]`, `X | None`), pas `typing.List`/`Optional`.
- `solver.py` ne doit pas importer Django : il reste testable seul.
- Pas de dépendance côté Django au-delà de Django lui-même (le CORS est évité grâce au proxy Vite).
- React : composants fonctionnels et hooks ; pas de bibliothèque d'état ni de CSS externe.
- Le bouton « Lancer la recherche » reste désactivé tant que les 6 nombres et l'objectif ne sont pas tous valides.
- Dépendances npm : garder Vite et @vitejs/plugin-react à jour (voir README, section « Mettre à jour les dépendances »).

## Algorithme (`solver.py`)
Recherche exhaustive récursive : à chaque étape, on choisit deux nombres, on les remplace par le résultat d'une opération valide, puis on recommence avec la liste réduite. Optimisations en place :
- mémoïsation des états déjà explorés (`seen`), la clé étant l'ensemble des couples (valeur, nombre de nombres utilisés) ;
- opérations inutiles ignorées (`a - a`, `× 1`, `÷ 1`) ;
- toujours le plus grand opérande à gauche (évite les négatifs et les doublons de commutativité) ;
- arrêt immédiat dès qu'une solution exacte est trouvée.

Chaque valeur garde l'arbre d'opérations qui l'a produite ; `_steps` l'aplatit en liste ordonnée pour l'affichage.

## Tests
- `test_exact` : 25, 50, 75, 100, 3, 6 → 952 est atteignable.
- `test_closest` : six 1 → 999 est inatteignable ; le meilleur résultat est 9 (`(1+1+1)×(1+1+1)`), écart de 990.
- `test_api_validation` : l'API refuse une requête invalide avec un code 400.
- `test_api_small_number_max_twice` / `test_api_small_number_twice_ok` : un petit nombre présent trois fois est refusé (400) ; présent deux fois, il est accepté (200).
- `test_api_large_number_max_once` / `test_api_large_numbers_all_distinct_ok` : un grand nombre présent deux fois est refusé (400) ; quatre grands nombres distincts sont acceptés (200).

Ajouter un test pour toute nouvelle règle ou tout nouveau cas limite du solveur.

## Pièges connus
- `settings.py` est configuré pour le développement (`DEBUG = True`, `SECRET_KEY` en dur, `ALLOWED_HOSTS = ["*"]`, `csrf_exempt` sur l'endpoint) : à durcir avant tout déploiement.
- Python 3.14 requiert Django 5.2.8 ou plus.
