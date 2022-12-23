from typing import Any
import jsons
import requests
from requests import HTTPError, Response
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

    def post(self, draft: Draft) -> None:
        """Publie le brouillon donné. Gère l'upload de l'image."""
        id_image = self.upload_image(draft.fiche.liens_vers_les_images)
        draft.body['media_ids[]'] = id_image
        reponse = requests.post(
            f"https://{self.__domain}/api/v1/statuses",
            data=draft.body,
            headers={
                "Authorization": "Bearer " + self.__bearer_token,
                "Idempotency-Key": draft.idempotency_key,
            }
        )
        Mastodon.__raise_error(reponse, draft.fiche)

    def upload_image(self, lien: str) -> str:
        """Upload l'image du lien donné sur le compte Mastodon. Retourne son
        id.
        """
        image_rep = requests.get(lien, stream=True)
        image_rep.raise_for_status()
        reponse = requests.post(
            f"https://{self.__domain}/api/v2/media",
            files={ "file": image_rep.raw },
            headers={ "Authorization": "Bearer " + self.__bearer_token },
        )
        Mastodon.__raise_error(reponse)
        return reponse.json()['id']

    def __raise_error(reponse: Response, data: Any | None = None) -> None:
        """Lève une exception si la réponse est négative."""
        if not reponse.ok:
            message = reponse.json()['error']
            if data is not None:
                message += f" ({data})"
            raise HTTPError(message)
