# Diagramme d'Activité - Calcul des Moyennes

Ce diagramme détaille l'algorithme de calcul des moyennes selon les règles du cahier des charges (Section 4).

```mermaid
activityDiagram
    start
    :Identifier Etudiant et Matière;
    :Récupérer les notes (CC, EXAM, RATTRAPAGE);
    
    if (Rattrapage existe ?) then (Oui)
        :La note de rattrapage devient la moyenne;
    else (Non)
        if (CC et EXAM existent ?) then (Oui)
            :Calculer (CC * 0.4) + (EXAM * 0.6);
        else (Une seule note)
            :La note disponible est la moyenne;
        endif
    endif

    :Appliquer pénalités d'absence (-0.01/h);
    :Fixer la moyenne finale de la matière;
    :Pousser vers le calcul de l'UE;
    stop
```
