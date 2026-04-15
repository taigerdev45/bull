#  Architecture Technique

## Stack Technologique

### Frontend
- **Framework** : Next.js 14 (App Router)
- **Styling** : Tailwind CSS + shadcn/ui
- **State Management** : TanStack Query
- **Génération PDF** : Puppeteer

### Backend
- **Framework** : Django 5 + Django REST Framework (DRF)
- **Base de données** : Firebase Firestore (NoSQL)
- **Auth** : Firebase Authentication (JWT)
- **Validation** : Pydantic

## Principes de Développement (POO/DDD)
L'application suit strictement les principes de la **Clean Architecture** et du **Domain-Driven Design (DDD)** :

- **Domain Layer** (Pur Python) : Contient la logique métier, les entités (`Etudiant`, `Evaluation`), les Value Objects (`Note`, `Moyenne`) et les interfaces des repositories.
- **Application Layer** : Orchestre les cas d'utilisation (Service Layer, Commands, Queries).
- **Infrastructure Layer** : Implémente les détails techniques (Firebase, Auth, Génération Excel).
- **Interfaces Layer** : Points d'entrée de l'application (API REST, CLI).

## Structure du Backend
```
backend/
├── domain/                    # Cœur métier (pur, testable)
│   ├── entities/              # Etudiant, UE, Matière, Evaluation...
│   ├── value_objects/         # Note, Moyenne, Coefficient (immutables)
│   ├── services/              # Calculateurs, Validateurs, Décideurs
│   └── repositories/          # Interfaces (DIP)
├── application/               # Orchestration (Commands, Queries)
├── infrastructure/            # Firebase, Persistence, Config
└── interfaces/                # API REST Django
```
