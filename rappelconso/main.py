import logging
import os

from dotenv import load_dotenv
from flux import Flux
from mastodon import Mastodon
from draft import Draft
from cache import Cache
from fiche import Fiche


def get_env(nom: str) -> str | None:
    """Retourne la valeur de la variable de configuration de nom donnée.

    - Si une variable d'environnement NOM_FILE est définie, retourne le contenu
      du fichier référencé.
    - Sinon, retourne la valeur de la variable d'environnement NOM.
    """
    chemin = os.getenv(nom + "_FILE")
    if chemin is not None:
        fichier = open(chemin, "r")
        val = fichier.readline().strip()
        fichier.close()
        return val
    else:
        return os.getenv(nom)

def publier_fiches(fiches: list[Fiche], cache: Cache) -> None:
    if len(fiches) == 0:
        logging.info("Aucune nouvelle fiche à publier.")
        return
    logging.info("Publication de %d nouvelles fiches...", len(fiches))
    for fiche in fiches:
        logging.info("Publication de la fiche %s...",
            fiche.lien_vers_la_fiche_rappel)
        try:
            mastodon.post(Draft(fiche))
            cache.add(fiche.rappelguid)
        except Exception as e:
            logging.error("Erreur pendant la publication de la fiche : %s", e)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    cache = Cache(get_env("RAPPELCONSO_FICHIER_CACHE"))
    flux = Flux("https://data.economie.gouv.fr/api/records/1.0/search/?dataset=rappelconso0&q=&rows=10&sort=date_de_publication&facet=categorie_de_produit&facet=sous_categorie_de_produit&facet=nom_de_la_marque_du_produit&facet=conditionnements&facet=zone_geographique_de_vente&facet=distributeurs&facet=motif_du_rappel&facet=risques_encourus_par_le_consommateur&facet=conduites_a_tenir_par_le_consommateur&facet=modalites_de_compensation&facet=date_de_publication", cache)
    mastodon = Mastodon("rivals.space", get_env("RAPPELCONSO_BEARER_TOKEN"))
    publier_fiches(flux.update(), cache)
