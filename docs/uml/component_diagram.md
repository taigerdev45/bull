# Diagramme de Composants - Bull ASUR v2.5

Architecture modulaire et hybride du système.

```mermaid
graph TD
    subgraph Client [Client Side / PWA]
        UI[Premium Monochrome UI]
        PWA[PWA / Service Worker]
        Notif[Notification Center]
        Export[jsPDF Engine]
    end

    subgraph Frontend [Nuxt.3 Framework]
        Store[Auth Store / Cookies]
        Composables[API Composables]
        Aura[Kinetic Aura Engine]
    end

    subgraph Backend [Django DDD Core]
        subgraph API_Layer
            REST[Rest API Views]
            JWT[JWT Validator]
        end
        
        subgraph Domain_Layer
            Calc[Moteur de Calcul DDD]
            Rules[Règles de Validation]
        end
        
        subgraph Infras_Layer
            Repo[Django ORM]
            Adapter[Auth Adapters]
        </div>
    end

    subgraph Cloud [Data & Auth]
        Supa[(Supabase / Postgres)]
    end

    UI --> Notif
    UI --> Export
    UI --> Aura
    PWA --> UI
    UI --> Store
    Store --> Composables
    Composables --> REST
    REST --> JWT
    JWT --> Calc
    Calc --> Rules
    Calc --> Repo
    Repo --> Supa
```
