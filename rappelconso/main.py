from flux import Flux


if __name__ == "__main__":
    flux = Flux("https://data.economie.gouv.fr/api/records/1.0/search/?dataset=rappelconso0&q=&rows=20&sort=date_de_publication&facet=categorie_de_produit&facet=sous_categorie_de_produit&facet=nom_de_la_marque_du_produit&facet=conditionnements&facet=zone_geographique_de_vente&facet=distributeurs&facet=motif_du_rappel&facet=risques_encourus_par_le_consommateur&facet=conduites_a_tenir_par_le_consommateur&facet=modalites_de_compensation&facet=date_de_publication")
    fiches = flux.update()
    for fiche in fiches:
        print(fiche)
