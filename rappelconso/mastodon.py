import logging
from typing import Any
import requests
from requests import HTTPError, Response
from draft import Draft
from fiche import Fiche


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
        medias_ids = []
        for lien in draft.fiche.liens_vers_les_images.split(" "):
            try:
                medias_ids.append(self.upload_image(lien), draft.fiche)
            except HTTPError as e:
                logging.warning("[Fiche %s] Erreur HTTP lors de la requête de " \
                    "l'image %s : %s (image ignorée)", draft.fiche.rappelguid,
                    lien, e)
        if len(medias_ids) > 0:
            draft.body['media_ids[]'] = medias_ids
        reponse = requests.post(
            f"https://{self.__domain}/api/v1/statuses",
            data=draft.body,
            headers={
                "Authorization": "Bearer " + self.__bearer_token,
                "Idempotency-Key": draft.idempotency_key,
            }
        )
        Mastodon.__raise_error(reponse, draft.fiche)

    def upload_image(self, lien: str, fiche: Fiche) -> str:
        """Upload l'image du lien donné sur le compte Mastodon. Retourne son
        id.
        """
        image_rep = requests.get(lien, stream=True)
        image_rep.raise_for_status()
        reponse = requests.post(
            f"https://{self.__domain}/api/v2/media",
            files={
                "file": image_rep.raw,
                "description": f"{fiche.titre} - " \
                    f"{fiche.nom_de_la_marque_du_produit} - "\
                    f"{fiche.noms_des_modeles_ou_references}",
            },
            headers={ "Authorization": "Bearer " + self.__bearer_token },
        )
        Mastodon.__raise_error(reponse)
        return reponse.json()['id']

    def __raise_error(reponse: Response, data: Any | None = None) -> None:
        """Lève une exception si la réponse est négative."""
        if not reponse.ok:
            message = f"{reponse.status_code} : {reponse.json()['error']}"
            if data is not None:
                message += f" ({data})"
            raise HTTPError(message)
