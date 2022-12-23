from flux import Flux


if __name__ == "__main__":
    flux = Flux("https://rappel.conso.gouv.fr/rss")
    fiches = flux.update()
    for fiche in fiches:
        print(fiche)
