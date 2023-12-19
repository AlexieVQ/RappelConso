from fiche import Fiche


class Draft:
    """Brouillon d'un status Mastodon (corps et source)."""

    def __init__(self, fiche: Fiche) -> None:
        self.fiche = fiche
        self.body = {
            "status": fiche.corps(),
            # "spoiler_text": fiche.cw,
            "sensitive": fiche.cw is not None,
            "language": "fr",
            "visibility": "public",
        }
        if fiche.cw is not None:
            self.body["sensitive"] = "true"

    @property
    def idempotency_key(self) -> str:
        """Clé d'unicité du brouillon (header Idempotency-Key)."""
        return self.fiche.rappelguid
