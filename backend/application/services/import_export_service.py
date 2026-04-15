from typing import List, Dict
from infrastructure.parsers.openpyxl_parser import OpenpyxlParser
from infrastructure.generators.excel_generator import ExcelGenerator
from application.commands.importer_evaluations_command import ImporterEvaluationsCommand, ImporterEvaluationsHandler

class ImportExportService:
    """Service haut niveau pour la gestion des fichiers Excel."""

    def __init__(self, parser: OpenpyxlParser, 
                 generator: ExcelGenerator,
                 import_handler: ImporterEvaluationsHandler):
        self._parser = parser
        self._generator = generator
        self._import_handler = import_handler

    def importer_evaluations(self, contenu_fichier: bytes, saisie_par: str) -> Dict:
        # 1. Parsing
        parse_result = self._parser.parser(contenu_fichier)
        
        # 2. Exécution Commande
        command = ImporterEvaluationsCommand(parse_result, saisie_par)
        rapport_import = self._import_handler.executer(command)
        
        return {
            "parsing": {
                "lignes_total": parse_result.total_lignes,
                "lignes_valides": parse_result.nb_succes,
                "erreurs_format": [e.model_dump() for e in parse_result.erreurs]
            },
            "importation": rapport_import
        }

    def exporter_resultats_promotion(self, promotion_id: str) -> bytes:
        # Todo: Récupérer données réelles via Query Handler
        donnees_simulees = {"promo": promotion_id, "etudiants": []}
        return self._generator.generer_rapport_promotion(donnees_simulees)
