class Historique:
    """Historique des GUID des fiches déjà traitées."""

    def __init__(self, chemin: str) -> None:
        """Charge les GUID sauvegardées dans le fichier texte de chemin
        donné.
        """
        self.__historique: set[str] = set()
        try:
            self.__fichier = open(chemin, "r+")
        except IOError:
            self.__fichier = open(chemin, "w+")
        for l in self.__fichier:
            self.__historique.add(l.strip())

    def __contains__(self, guid: str) -> bool:
        return guid in self.__historique

    def add(self, guid: str) -> None:
        """Ajoute le GUID donné à l'historique."""
        if guid not in self.__historique:
            self.__historique.add(guid)
            self.__fichier.write(guid + "\n")
            self.__fichier.flush()

    def __del__(self):
        self.__fichier.close()
