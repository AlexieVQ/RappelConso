from argparse import ArgumentParser, Namespace
import sys
from flux import Flux
from mastodon import Mastodon
from draft import Draft
from cache import Cache


def parse_args() -> Namespace:
    parser = ArgumentParser(
        prog="RappelConso",
        description="Bot postant les nouvelles fiches de RappelConso sur " \
            "Mastodon",
    )
    parser.add_argument("-b", "--bearer-token", dest="token",
        help="Bearer token pour l'API Mastodon (doit avoir les accès " \
        "write:statuses et write:media)", required=True)
    parser.add_argument("-c", "--cache", dest="cache", help="Fichier texte " \
        "où cacher l'historique des fiches traitées", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    cache = Cache(args.cache)
    flux = Flux("https://data.economie.gouv.fr/api/records/1.0/search/?dataset=rappelconso0&q=&rows=10&sort=date_de_publication&facet=categorie_de_produit&facet=sous_categorie_de_produit&facet=nom_de_la_marque_du_produit&facet=conditionnements&facet=zone_geographique_de_vente&facet=distributeurs&facet=motif_du_rappel&facet=risques_encourus_par_le_consommateur&facet=conduites_a_tenir_par_le_consommateur&facet=modalites_de_compensation&facet=date_de_publication", cache)
    mastodon = Mastodon("rivals.space", args.token)
    fiches = flux.update()
    for fiche in fiches:
        mastodon.post(Draft(fiche))
        cache.add(fiche.rappelguid)
