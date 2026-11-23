
import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWKClient, PyJWKClientError
from jwt.exceptions import InvalidTokenError


KEYCLOAK_ISSUER = os.environ["KEYCLOAK_ISSUER"]
KEYCLOAK_JWKS_URL = os.environ["KEYCLOAK_JWKS_URL"]

jwks_client = PyJWKClient(KEYCLOAK_JWKS_URL, timeout=5)

# Mengaktifkan autentikasi Bearer pada Swagger UI
security = HTTPBearer(
    scheme_name="BearerAuth",
    description="Masukkan Access Token dari Keycloak",
)


def require_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    if credentials.scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=401,
            detail="Bearer token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=KEYCLOAK_ISSUER,
            audience="sbdt-api",
            options={
                "require": ["exp", "iat", "iss", "sub", "aud"],
                "verify_aud": True,
            },
        )

        if payload.get("typ") != "Bearer":
            raise InvalidTokenError("Token must be an access token")

        if payload.get("azp") != "sbdt-api":
            raise InvalidTokenError("Unauthorized client")

        return payload

    except PyJWKClientError:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve Keycloak signing key",
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired JWT token",
            headers={"WWW-Authenticate": "Bearer"},
        )
