import jwt
from datetime import datetime, timedelta
from django.conf import settings
from pytz import utc


def creer_token_jwt(claims: dict, duree: int = None):
    if duree is None:
        duree = settings.JWT_TOKEN_DURATION  # Utiliser la durée définie dans les paramètres

    now = datetime.now(utc)
    payload = {
        'exp': now + timedelta(seconds=duree),
        'iat': now,
        'nbf': now,
        **claims
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token if isinstance(token, str) else token.decode('utf-8')


def verifier_token_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return True, "Token valide", payload
    except jwt.ExpiredSignatureError:
        return False, "Token expiré", None
    except jwt.InvalidTokenError:
        return False, "Token invalide", None



