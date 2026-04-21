# 🚀 Manuel de Déploiement - Bull ASUR

Ce document guide le déploiement de l'application sur **Render** (Backend) et l'intégration avec **Supabase**.

## 1. Prérequis Supabase

Avant de déployer le code, configurez votre instance Supabase :
1. **Database** : Récupérez l'URL du Pooler (port 6543) pour une compatibilité IPv4 avec Render.
2. **Auth** : Notez votre `Anon Key` et votre `Service Role Key`.
3. **Sécurité (RLS)** : 
   - Copiez le contenu de `backend/scripts/supabase_rls.sql`.
   - Exécutez-le dans le **SQL Editor** de Supabase pour activer les politiques de sécurité.

## 2. Déploiement du Backend (Render)

L'application utilise le fichier `render.yaml` pour une configuration automatique.

### Étapes :
1. Créez un nouveau **Blueprint Instance** sur Render.
2. Liez votre dépôt GitHub.
3. Configurez le **Secret Group** `bulletin-shared-secrets` avec les variables suivantes :
   - `DATABASE_URL` : Format `postgres://...:6543/postgres?sslmode=require`
   - `SUPABASE_URL` : Votre URL de projet.
   - `SUPABASE_SERVICE_ROLE_KEY` : Votre clé secrète admin.
   - `SUPABASE_JWT_SECRET` : Le secret JWT de votre dashboard.
   - `DJANGO_SECRET_KEY` : Une chaîne aléatoire forte.
   - `ALLOWED_HOSTS` : `.onrender.com,localhost`

Le build lancera automatiquement `./render_build.sh` qui installe les dépendances et applique les migrations Django.

## 3. Déploiement du Frontend (Nuxt 3)

Le frontend peut être déployé sur **Vercel** ou **Netlify**.

### Variables d'environnement nécessaires :
- `NUXT_PUBLIC_API_URL` : URL de votre backend Render.
- `NUXT_PUBLIC_SUPABASE_URL` : Votre URL Supabase.
- `NUXT_PUBLIC_SUPABASE_ANON_KEY` : Votre clé publique anonyme.

## 4. Vérification Post-Déploiement

1. Accédez à l'URL du backend : `https://xxx.onrender.com/api/ping/`.
2. Vérifiez que les migrations ont bien créé les tables dans Supabase.
3. Testez l'authentification depuis le frontend.

---
> [!IMPORTANT]
> Toujours utiliser le port **6543** (Pooler) dans `DATABASE_URL` pour éviter les erreurs "Network is unreachable" fréquentes sur Render avec l'IPv6.
