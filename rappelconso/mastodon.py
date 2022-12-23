import jsons
import requests
from requests import HTTPError
from draft import Draft


class Mastodon:
    """Accès à l'API Mastodon."""

    def __init__(self, domain: str, bearer_token: str) -> None:
        """Crée un nouvel accès à l'API Mastodon.

        domain: nom de domaine de l'instance.
        bearer_token: Bearer token de l'utilisateur.
        """
        self.__domain = domain
        self.__bearer_token = bearer_token

    def post(self, draft: Draft):
        """Publie le brouillon donné."""
        reponse = requests.post(
            f"https://{self.__domain}/api/v1/statuses",
            data=jsons.dump(draft.body),
            headers={
                "Authorization": "Bearer " + self.__bearer_token,
                "Idempotency-Key": draft.idempotency_key,
            }
        )
        if not reponse.ok:
            raise HTTPError(f"{reponse.json()['error']} ({draft.fiche})")
