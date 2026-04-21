# Diagramme d'Activité - Validation UE / Compensation

Ce diagramme explique le processus de validation d'une UE et les règles de compensation.

```mermaid
activityDiagram
    start
    :Calculer moyenne pondérée de l'UE;
    if (Moyenne >= 10/20) then (Oui)
        :Statut : VALIDÉE (Acquise);
        :Attribuer tous les crédits ECTS;
    else (Non)
        :Vérifier Moyenne Générale Semestre;
        if (Moyenne Générale >= 10/20 et pas de note < 07/20) then (Oui)
            :Statut : COMPENSÉE;
            :Attribuer tous les crédits ECTS;
        else (Non)
            :Statut : NON VALIDÉE (Échec);
            :Crédits non attribués;
        endif
    endif
    stop
```
