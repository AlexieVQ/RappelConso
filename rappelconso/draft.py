from fiche import Fiche


class Draft:
    """Brouillon d'un status Mastodon (corps et source)."""

    def __init__(self, fiche: Fiche) -> None:
        self.fiche = fiche
        self.body = {
            "status": fiche.corps(),
            "sensitive": fiche.cw is not None,
            "spoiler_text": fiche.cw,
            "language": "fr",
            "visibility": "private",
        }

    @property
    def idempotency_key(self) -> str:
        """Clé d'unicité du brouillon (header Idempotency-Key)."""
        return self.fiche.rappelguid
