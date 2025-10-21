import base64
import hashlib
import os


class OauthHelper:

    @staticmethod
    def generate_code_verifier() -> str:
        code_verifier = os.urandom(32)
        return base64.urlsafe_b64encode(code_verifier).rstrip(b'=').decode('utf-8')

    @staticmethod
    def generate_code_challenge(code_verifier: str) -> str:
        digest = hashlib.sha256(code_verifier.encode('ascii')).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('utf-8')
