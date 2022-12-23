from fiche import Fiche, from_entry
import feedparser

class Flux:

    def __init__(self, url: str) -> None:
        self.__url = url
        self.__cache: set[str] = set()

    def update(self) -> list[Fiche]:
        feed = feedparser.parse(self.__url)
        fiches = []
        for entry in feed.entries:
            if entry.link not in self.__cache:
                fiches.append(from_entry(entry))
        return fiches
