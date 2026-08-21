"""Vérification reCAPTCHA v3 (urllib, sans dépendance externe).

Désactivée en développement (DEBUG) ou quand la clé secrète est absente :
le formulaire reste utilisable, le score n'est simplement pas vérifié.
"""

import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


def verify_recaptcha(response_token: str, remote_ip: str | None = None) -> bool:
    """Retourne True si le token reCAPTCHA est valide (ou si la vérification est désactivée)."""
    secret = settings.RECAPTCHA_SECRET_KEY
    if not secret or settings.DEBUG:
        return True
    if not response_token:
        logger.warning("reCAPTCHA : token manquant.")
        return False
    data = urllib.parse.urlencode(
        {"secret": secret, "response": response_token, **({"remoteip": remote_ip} if remote_ip else {})}
    ).encode("utf-8")
    try:
        req = urllib.request.Request(
            settings.RECAPTCHA_VERIFY_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # réseau/API indisponible : on refuse par sécurité
        logger.error("reCAPTCHA : échec de la vérification (%s).", exc)
        return False
    if not payload.get("success"):
        logger.warning("reCAPTCHA : rejeté par Google (%s).", payload.get("error-codes"))
        return False
    score = float(payload.get("score", 0))
    if score < settings.RECAPTCHA_MIN_SCORE:
        logger.warning("reCAPTCHA : score trop bas (%.2f).", score)
        return False
    return True
