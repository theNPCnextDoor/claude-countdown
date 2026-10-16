# Solveur « Des chiffres et des lettres »

Prérequis : Python 3.14 et Node.js 20.19+ (ou 22.12+), requis par Vite 8.

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
