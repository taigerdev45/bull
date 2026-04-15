from dataclasses import dataclass
from typing import List, Dict
from application.commands.command import Command
from infrastructure.parsers.parse_result import ParseResult, EvaluationImportDTO
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from domain.repositories.i_matiere_repository import IMatiereRepository
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.entities.evaluation import Evaluation, TypeEvaluation, Note

@dataclass(frozen=True)
class ImporterEvaluationsCommand(Command):
    parse_result: ParseResult
    saisie_par: str

class ImporterEvaluationsHandler:
    """Gère l'importation massive des notes avec validation métier."""

    def __init__(self, etudiant_repo: IEtudiantRepository, 
                 matiere_repo: IMatiereRepository,
                 evaluation_repo: IEvaluationRepository):
        self._etudiant_repo = etudiant_repo
        self._matiere_repo = matiere_repo
        self._evaluation_repo = evaluation_repo

    def executer(self, command: ImporterEvaluationsCommand) -> Dict:
        rapport = {"succes": 0, "erreurs": []}
        evaluations_a_creer = []

        # Cache pour éviter les requêtes DB répétitives
        etudiants_cache = {}
        matieres_cache = {}

        for dto in command.parse_result.succes:
            # 1. Résoudre Étudiant
            etudiant = etudiants_cache.get(dto.matricule)
            if not etudiant:
                etudiant = self._etudiant_repo.get_by_matricule(dto.matricule)
                if etudiant: etudiants_cache[dto.matricule] = etudiant

            if not etudiant:
                rapport["erreurs"].append(f"Étudiant '{dto.matricule}' introuvable.")
                continue

            # 2. Résoudre Matière
            matiere = matieres_cache.get(dto.matiere_libelle)
            if not matiere:
                matiere = self._matiere_repo.get_by_libelle(dto.matiere_libelle)
                if matiere: matieres_cache[dto.matiere_libelle] = matiere

            if not matiere:
                rapport["erreurs"].append(f"Matière '{dto.matiere_libelle}' introuvable.")
                continue

            # 3. Créer Évaluations (CC, Examen, Rattrapage)
            if dto.note_cc is not None:
                evaluations_a_creer.append(Evaluation(
                    etudiant_id=etudiant.id,
                    matiere_id=matiere.id,
                    type=TypeEvaluation.CC,
                    note=Note(dto.note_cc),
                    saisie_par=command.saisie_par
                ))
            
            if dto.note_examen is not None:
                evaluations_a_creer.append(Evaluation(
                    etudiant_id=etudiant.id,
                    matiere_id=matiere.id,
                    type=TypeEvaluation.EXAMEN,
                    note=Note(dto.note_examen),
                    saisie_par=command.saisie_par
                ))

            if dto.note_rattrapage is not None:
                evaluations_a_creer.append(Evaluation(
                    etudiant_id=etudiant.id,
                    matiere_id=matiere.id,
                    type=TypeEvaluation.RATTRAPAGE,
                    note=Note(dto.note_rattrapage),
                    saisie_par=command.saisie_par
                ))

        # 4. Persistence Batch
        if evaluations_a_creer:
            self._evaluation_repo.bulk_creer(evaluations_a_creer)
            # Todo: Déclencher recalcul cascade ici pour les étudiants concernés
            rapport["succes"] = len(evaluations_a_creer)

        return rapport
