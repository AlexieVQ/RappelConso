import logging
import os
from time import sleep, time

from dotenv import load_dotenv
from flux import Flux
from mastodon import Mastodon
from draft import Draft
from historique import Historique
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

def publier_fiches(
    fiches: list[Fiche],
    mastodon: Mastodon,
    historique: Historique,
) -> None:
    """Publie les fiches données, avec un intervalle de 15 min entre chaque
    publication.
    """
    if len(fiches) == 0:
        logging.info("Aucune nouvelle fiche à publier.")
        return
    logging.info("Publication de %d nouvelles fiches...", len(fiches))
    for fiche in fiches:
        logging.info("Publication de la fiche %s...",
            fiche.lien_vers_la_fiche_rappel)
        try:
            start = time()
            mastodon.post(Draft(fiche))
            historique.add(fiche.rappelguid)
            sleep_duration = 900 - time() + start
            if sleep_duration > 0:
                sleep(sleep_duration)
        except Exception as e:
            logging.error("Erreur pendant la publication de la fiche : %s", e)

def run(flux: Flux, mastodon: Mastodon, historique: Historique) -> None:
    """Exécute le bot, en récupérant les nouvelles fiches toutes les heures."""
    while True:
        logging.info("Récupération des nouveaux rappels produits...")
        start = time()
        publier_fiches(flux.update(), mastodon, historique)
        sleep_duration = 3600 - time() + start
        if sleep_duration > 0:
            sleep(sleep_duration)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    historique = Historique(get_env("RAPPELCONSO_FICHIER_HISTORIQUE"))
    flux = Flux("https://data.economie.gouv.fr/api/records/1.0/search/?dataset=rappelconso0&q=&rows=10&sort=date_de_publication&facet=categorie_de_produit&facet=sous_categorie_de_produit&facet=nom_de_la_marque_du_produit&facet=conditionnements&facet=zone_geographique_de_vente&facet=distributeurs&facet=motif_du_rappel&facet=risques_encourus_par_le_consommateur&facet=conduites_a_tenir_par_le_consommateur&facet=modalites_de_compensation&facet=date_de_publication", historique)
    mastodon = Mastodon("rivals.space", get_env("RAPPELCONSO_BEARER_TOKEN"))
    run(flux, mastodon, historique)
