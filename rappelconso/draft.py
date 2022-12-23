from typing import Optional
from attr import dataclass

from fiche import Fiche


@dataclass
class DraftBody:
    """Brouillon d'un statut Mastodon. Voir
    https://docs.joinmastodon.org/methods/statuses/#create.
    """

    status: str
    sensitive: bool
    spoiler_text: Optional[str]
    #media_ids: list[str] = []
    visibility: str = "private"
    language: str = "fr"

class Draft:
    """Brouillon d'un status Mastodon (corps et source)."""

    def __init__(self, fiche: Fiche) -> None:
        self.fiche = fiche
        self.body = DraftBody(
            status=fiche.corps(),
            sensitive=fiche.cw is not None,
            spoiler_text=fiche.cw,
        )

    @property
    def idempotency_key(self) -> str:
        """Clé d'unicité du brouillon (header Idempotency-Key)."""
        return self.fiche.rappelguid
