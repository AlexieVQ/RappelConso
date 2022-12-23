class Cache:
    """Cache des GUID des fiches déjà traitées."""

    def __init__(self, chemin: str) -> None:
        """Charge les données cachées dans le fichier texte de chemin donné."""
        self.__cache: set[str] = set()
        try:
            self.__fichier = open(chemin, "r+")
        except IOError:
            self.__fichier = open(chemin, "w+")
        for l in self.__fichier:
            self.__cache.add(l.strip())

    def __contains__(self, guid: str) -> bool:
        return guid in self.__cache

    def add(self, guid: str) -> None:
        """Ajoute le GUID donné au cache."""
        if guid not in self.__cache:
            self.__cache.add(guid)
            self.__fichier.write(guid + "\n")
            self.__fichier.flush()

    def __del__(self):
        self.__fichier.close()
