# Solveur « Des chiffres et des lettres »

Prérequis : Python 3.14 et Node.js 20.19+ (ou 22.12+), requis par Vite 8.

## Préambule

J'ai décidé de créer une petite application avec Claude afin de tester cet outil. L'application a été complétée telle quelle en 3 prompts (sauf pour le fichier .gitignore que j'ai rajouté manuellement en allant sur gitignore.io) Ai-je eu du fun à faire ce projet qui a pris une demi-heure au total à faire? Pas du tout! Ça ne remplace pas le plaisir de programmer qui réside dans le fait de me casser la tête et d'écrire moi-même le code. Mais je reconnais l'avantage que ça peut apporter en entreprise.

## Backend (Django)
```
cd backend
python -m venv venv && source venv/bin/activate   # Windows : venv\Scripts\activate
pip install -r requirements.txt
python manage.py test        # facultatif
python manage.py runserver   # http://localhost:8000
```

## Frontend (React + Vite)
```
cd frontend
npm install
npm run dev                  # http://localhost:5173 (proxy /api -> :8000)
```

## Mettre à jour les dépendances
Les versions dans `package.json` (Vite 8, @vitejs/plugin-react 6, React 19) étaient
les plus récentes à la création du projet. Pour récupérer des versions plus récentes
et corriger les avertissements de `npm audit` :
```
cd frontend
npx npm-check-updates -u && npm install
npm audit
```
Côté Python : `pip install -U -r requirements.txt` (Django 5.2.8 ou plus pour Python 3.14).
