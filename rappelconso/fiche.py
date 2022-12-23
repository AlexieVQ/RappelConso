from dataclasses import dataclass
from typing import Optional

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

    def __str__(self) -> str:
        return f"#RappelProduit\n" \
            f"{self.nom_de_la_marque_du_produit}\n\n" \
            \
            f"Risques : {self.risques_encourus_par_le_consommateur}\n\n" \
            \
            f"Motif : {self.motif_du_rappel}\n" \
            f"{self.lien_vers_la_fiche_rappel}"
