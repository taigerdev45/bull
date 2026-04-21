# Diagramme d'Activité - Décision du Jury

Ce diagramme illustre la logique finale de délibération annuelle (Section 4.7).

```mermaid
activityDiagram
    start
    :Calculer total crédits acquis (S5 + S6);
    if (Total >= 60 crédits) then (Oui)
        :Statut : ADMIS (DIPLÔMÉ);
        :Attribuer Mention Annuelle;
    else (Non)
        if (Total >= 50 crédits et UE de stage/soutenance échouée) then (Oui)
            :Statut : REPRISE SOUTENANCE;
        else (Non)
            :Statut : REDOUBLEMENT;
        endif
    endif
    stop
```
