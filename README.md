# AI Knowledge Sharing Platform

Web aplikacija za dijeljenje znanja — FastAPI backend + Next.js frontend + PostgreSQL.

## Struktura

```
sept_dws/
├── backend/          # FastAPI API
│   ├── database/     # konekcija na bazu
│   ├── models/       # SQLAlchemy modeli
│   ├── schemas/      # Pydantic validacija
│   ├── routers/      # API rute
│   └── services/     # trending, preporuke
└── frontend/         # Next.js aplikacija
    └── src/
        ├── app/      # stranice
        └── components/
```

## Pokretanje

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy database\.env.example database\.env
# u .env upisi DATABASE_URL
uvicorn main:app --reload
```

API: http://127.0.0.1:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Aplikacija: http://localhost:3000

## Funkcionalnosti

- Registracija i prijava (administrator / autor / citalac)
- CRUD objava
- Lajk, komentar, sacuvaj
- Kolekcije
- AI preporuke i trending
- Admin panel
- Autor panel sa statistikom

## Autor

Adin Music
