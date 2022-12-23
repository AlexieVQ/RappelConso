from dataclasses import dataclass
from typing import Optional


@dataclass
class Categorie:
    """Catégorie d'un article."""

    nom: str
    """Nom sous lequel la catégorie apparaît dans le data set"""
    hashtag: Optional[str] = None
    """Nom simplifié en CamelCase pour un hashtag (sans #)."""
    sensible: bool = False
    """Vrai si les articles de cette catégorie doivent être marqués comme
    sensibles."""

__CATEGORIES: dict[str, Categorie] = {}

def __add(nom:str, hashtag: Optional[str]=None, sensible: bool=False):
    """Ajoute la catégorie donnée à la liste des catégories."""
    __CATEGORIES[nom] = Categorie(nom, hashtag, sensible)

def categorie(nom: str) -> Categorie:
    """Retourne la catégorie de nom donné."""
    return __CATEGORIES.get(nom, Categorie(nom))

# Catégories de premier niveau
__add("Alimentation", "Alimentation", True)
__add("Automobiles et moyens de déplacement", "Mobilité")
__add("Bébés-Enfants (hors alimentaire)")
__add("Hygiène-Beauté")
__add("Vêtements, Mode, EPI")
__add("Sports-loisirs", "Sports")
__add("Maison-Habitat", "Maison")
__add("Appareils électriques, Outils", "Outils")
__add("Equipements de communication", "Communication")
__add("Autres", "Autres")

# Sous-catégories
# Alimentaire
__add("Alcool et vin", "Alcool")
__add("Aliments pour animaux domestiques", "Animaux")
__add("Aliments pour animaux d'élevage", "Animaux")
__add("Aliments pour bébés", "Bébés")
__add("Beurres d'origine végétale, graisses margarines et huiles", "Végétal")
__add("Eaux", "Eau")
__add("Fruits et légumes", "Végétal")
__add("Lait et produits laitiers", "ProduitsLaitiers")
__add("Oeufs et produits à base d'oeufs", "Oeufs")
__add("Plats préparés et snacks", "PlatsPréparés")
__add("Produits de la pêche et d'aquaculture", "Poisson")
__add("Produits sucrés", "Sucré")
__add("Soupes, sauces et condiments", "Condiments")
__add("Viandes", "Viande")

# Mobilité
__add("Vélos, bicyclettes, vélos à assistance électrique", "Vélo")
__add("Tous types d'accessoires", "Accessoires")

# Enfants
__add("Jouets", "Jouets")
__add("Articles pour enfants et puériculture", "Puériculture")
__add("Matériels scolaires", "MatérielScolaire")

# Hygiène, beauté
__add("Cosmétiques", "Cosmétiques")
__add("Dispositifs médicaux grand public", "Médical")
__add("Produits de tatouage", "Tatouage")

# Vêtements
__add("Vêtements, textiles, accessoires de mode", "Vêtements")
__add("Bijouterie", "Bijoux")

# Maison
__add("Articles de décoration", "Intérieur")
__add("Articles imitant les denrées alimentaires", "FausseNourriture", True)
__add("Appareils à gaz", "Gaz")
__add("Appareils à pression", "Pression")
__add("Mobilier", "Intérieur")
__add("Produits chimiques", "ProduitsChimiques")
__add("Produits de construction", "Travaux")
__add("Matériel de cuisine (sauf électroménager)", "Cuisine")

# Appareils électriques
__add("Appareils électriques, électroménager", "Électroménager")
