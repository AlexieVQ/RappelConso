import jsons
import requests
from fiche import Fiche
from historique import Historique

class Flux:
    """Flux des fiches de rappel produit depuis l'API du Ministère de
    l'Économie.

    Le flux cache les fiches déjà retournées et ne retourne que les nouvelles à
    chaque mise à jour.
    """

    def __init__(self, url: str, historique: Historique) -> None:
        self.__url = url
        self.__historique = historique

    def update(self) -> list[Fiche]:
        """Récupère les nouvelles fiches publiées depuis la dernière mise à
        jour.
        """
        dataset = requests.get(self.__url).json()
        fiches = []
        for record in dataset['records']:
            guid: str = record['fields']['rappelguid']
            if guid not in self.__historique:
                fiches.append(jsons.load(record['fields'], Fiche))
        return fiches
