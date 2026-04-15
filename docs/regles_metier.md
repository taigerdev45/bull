# 📐 Référentiel et Règles Métier

## Structure Pédagogique LP ASUR

### Semestre 5 (30 crédits)
| UE | Libellé | Crédits | Matières (Coefficient/Crédits) |
|----|---------|---------|-------------------------------|
| **UE5-1** | Enseignement Général | 11 | Anglais technique (1/2), Management d'équipe (1/1), Communication (2/1), Droit de l'informatique (2/2), Gestion de projets (1/1), Veille technologique (1/1), Consolidation bases de la programmation (2/2), Conception BDD et SQL (2/2) |
| **UE5-2** | Réseaux d'Entreprise | 19 | Remise à niveau IOS (2/2), Connaissance des réseaux LAN (2/2), Les langages du script (2/2), Virtualisation (3/3), Application client-serveur (2/2), Téléphonie IP avancée (2/2), Services à valeur ajoutée (2/2), CCNA2 (1/2) |

### Semestre 6 (30 crédits)
| UE | Libellé | Crédits | Matières (Coefficient/Crédits) |
|----|---------|---------|-------------------------------|
| **UE6-1** | Sciences de Base | 20 | Environnement Windows (3/3), Environnement Linux (3/3), Interopérabilité (3/3), Cryptage et Authentification (2/2), Prévention et Sécurité (3/3), Optimisation de l'accès Internet (3/3), Contrôle d'accès distant (2/2), CCNA3 (1/1) |
| **UE6-2** | Télécommunications et Réseaux | 10 | Méthodologie de rédaction du rapport de stage (2/2), Soutenance (8/8) |

## Algorithmes de Calcul

### 1. Moyenne d'une matière
```python
if rattrapage_existe:
    moyenne = note_rattrapage          # Rattrapage remplace l'intégralité
else:
    moyenne = (CC × 0.4) + (Examen × 0.6)  # Pondération officielle 40/60

moyenne_finale = max(0, moyenne - (heures_absence × 0.01))
```

### 2. Validation d'UE (Compensation)
Le système applique la règle de compensation globale du semestre :
- **Acquise Directe** : Si moyenne UE >= 10.0
- **Compensée** : Si moyenne UE < 10.0 MAIS Moyenne Générale Semestre >= 10.0
- **Non Acquise** : Si Moyenne Générale Semestre < 10.0

### 3. Mentions
- **Passable** : [10.0 - 12.0[
- **Assez Bien** : [12.0 - 14.0[
- **Bien** : [14.0 - 16.0[
- **Très Bien** : [16.0 - 20.0]
