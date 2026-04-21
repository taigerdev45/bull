# Diagramme de Déploiement (Deployment Diagram)

Ce diagramme représente l'architecture physique et l'exécution de l'application.

```mermaid
deploymentDiagram
    node "Poste Utilisateur" as Client {
        node "Navigateur Web" as Browser {
            component "Nuxt 3 App (SPA)"
        }
    }

    node "Vercel (Cloud)" as Vercel {
        component "Frontend Static Assets"
    }

    node "Render (Cloud)" as Render {
        node "Docker Container" as Backend {
            component "Django REST API"
            component "Gunicorn Server"
        }
    }

    node "Supabase (Cloud)" as Supabase {
        database "PostgreSQL Instance"
        component "Supabase GoTrue (Auth)"
    }

    Browser -- HTTPS : "Protocol (Port 443)"
    Browser -- Render : "REST API Calls"
    Render -- Supabase : "JDBC/TCP (Port 5432/6543)"
    Render -- HTTPS : "JWT Validation"
```
