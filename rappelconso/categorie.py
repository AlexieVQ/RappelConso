from dataclasses import dataclass


@dataclass
class Categorie:
    """Catégorie d'un article."""

    nom: str
    """Nom sous lequel la catégorie apparaît dans le data set"""
    hashtag: str
    """Nom simplifié en CamelCase pour un hashtag (sans #)."""
    sensible: bool = False
    """Vrai si les articles de cette catégorie doivent être marqués comme
    sensibles."""

__CATEGORIES: dict[str, Categorie] = {}

def __add(nom:str, hashtag: str, sensible: bool=False):
    """Ajoute la catégorie donnée à la liste des catégories."""
    __CATEGORIES[nom] = Categorie(nom, hashtag, sensible)

def categorie(nom: str) -> Categorie:
    """Retourne la catégorie de nom donné."""
    return __CATEGORIES[nom]

__add("Alimentation", "Alimentation", True)
__add("Automobiles et moyens de déplacement", "Mobilité")
__add("Bébés-Enfants (hors alimentaire)", "BébésEnfants")
__add("Hygiène-Beauté", "HygièneBeauté")
__add("Vêtements, Mode, EPI", "Vêtements")
__add("Sports-loisirs", "Sports")
__add("Maison-Habitat", "Maison")
__add("Appareils électriques, Outils", "Outils")
__add("Equipements de communication", "Communication")
__add("Autres", "Autres")
