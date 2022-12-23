from html.parser import HTMLParser
from feedparser import FeedParserDict

class Fiche:

    def __init__(self,
                 titre: str,
                 description: str,
                 lien: str,
                 lien_image: str) -> None:
        self.titre = titre
        self.description = description
        self.lien = lien
        self.lien_image = lien_image

    def __str__(self) -> str:
        return f"{self.description}Informations, distributeurs et lots "\
            f"concernés 👉️ {self.lien}"

class __Parser(HTMLParser):

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)

    def handle_data(self, data: str) -> None:
        self.__string += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "p":
            self.__string += "\n\n"

    def parse(self, plain_html: str) -> str:
        self.__string = ""
        self.feed(plain_html)
        return self.__string

__PARSER = __Parser()

def from_entry(entry: FeedParserDict) -> Fiche:
    return Fiche(
        titre=entry.title,
        description=__PARSER.parse(entry.summary),
        lien=entry.link,
        lien_image=entry.enclosures[0].href
    )
