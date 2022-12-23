from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup
import requests

from categorie import Categorie, categorie

@dataclass
class Fiche:
    """Fiche rappel concernant un produit."""

    rappelguid: str
    nom_de_la_marque_du_produit: str
    noms_des_modeles_ou_references: str
    categorie_de_produit: str
    sous_categorie_de_produit: str
    date_de_publication: str
    motif_du_rappel: str
    risques_encourus_par_le_consommateur: str
    conduites_a_tenir_par_le_consommateur: str
    modalites_de_compensation: str
    distributeurs: str
    zone_geographique_de_vente: Optional[str]
    date_debut_fin_de_commercialisation: str
    lien_vers_la_fiche_rappel: str
    liens_vers_les_images: str

    @property
    def titre(self) -> str:
        """Titre de la fiche"""
        if not hasattr(self, "__titre"):
            page = requests.get(self.lien_vers_la_fiche_rappel).text
            dom = BeautifulSoup(page, "html.parser")
            self.__titre = dom.find("p", class_="product-main-title").text
        return self.__titre

    @property
    def categorie(self) -> Categorie:
        """Catégorie du produit"""
        if not hasattr(self, "__categorie"):
            self.__categorie = categorie(self.categorie_de_produit)
        return self.__categorie

    @property
    def sous_categorie(self) -> Categorie:
        """Sous-catégorie du produit"""
        if not hasattr(self, "__sous_categorie"):
            self.__sous_categorie = categorie(self.sous_categorie_de_produit)
        return self.__sous_categorie

    @property
    def hashtags(self) -> list[str]:
        """Liste de hashtags (sans #)."""
        if not hasattr(self, "__hashtag"):
            self.__hashtags = list(filter(lambda c: c is not None, [
                self.categorie.hashtag,
                self.sous_categorie.hashtag,
            ]))
        return self.__hashtags

    @property
    def cw(self) -> str | None:
        """Content warning de l'article (None si l'article n'est pas
        sensible."""
        if not hasattr(self, "__cw"):
            if self.categorie.sensible or self.sous_categorie.sensible:
                self.__cw = self.categorie.nom + ", " + self.sous_categorie.nom
            else:
                self.__cw = None
        return self.__cw

    def printable_hashtags(self) -> str:
        """Liste des hashtags avec # séparés par des espaces."""
        return " ".join(map(lambda h: "#" + h, self.hashtags))

    def corps(self) -> str:
        """Corps du statut à poster."""
        return f"#RappelProduit\n" \
            f"{self.titre} - {self.nom_de_la_marque_du_produit}\n\n" \
            \
            f"Risques : {self.risques_encourus_par_le_consommateur}\n\n" \
            \
            f"Motif : {self.motif_du_rappel}\n" \
            f"{self.lien_vers_la_fiche_rappel}\n\n" \
            \
            f"{self.printable_hashtags()}"

    def __str__(self) -> str:
        return self.corps()
