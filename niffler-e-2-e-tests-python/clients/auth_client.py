import requests
from models.auth import PreRequest, Login, Token, TokenResponse
from helpers.oauth_codes import OauthHelper
from urllib.parse import urljoin
from clients.interceptor import Interceptor


class AuthClient:

    def __init__(self, auth_url: str, client_id: str):
        self.auth_url = auth_url
        self.client_id = client_id
        self.redirect_url = urljoin(self.auth_url, "/authorized")
        self.code = None

        self.session = requests.Session()
        self.session.mount("https://", Interceptor(self))

    def pre_request(self, request_data: PreRequest):
        response = requests.get(f"{self.auth_url}/oauth2/authorize", params=request_data.dict())
        xsrf = response.cookies.get("XSRF-TOKEN")
        response.raise_for_status()
        return xsrf

    def login(self, request_data: Login):
        response = requests.post(f"{self.auth_url}/login", data=request_data.dict())
        response.raise_for_status()

    def token(self, request_data: Token):
        response = requests.post(f"{self.auth_url}/oauth2/token", data=request_data.dict())
        response.raise_for_status()
        return response.json()

    def do_login(self, username: str, password: str):
        code_verifier = OauthHelper.generate_code_verifier()
        code_challenge = OauthHelper.generate_code_challenge(code_verifier)

        pre_request_data = PreRequest(
            response_type="code",
            client_id=self.client_id,
            scope="openid",
            redirect_uri=self.redirect_url,
            code_challenge=code_challenge,
            code_challenge_method="S256"
        )

        xsrf = self.pre_request(request_data=pre_request_data)

        login_data = Login(
            xsrf=f"{xsrf}",
            username=username,
            password=password
        )

        self.login(request_data=login_data)

        token_request_data = Token(
            code=self.code,
            redirect_uri=self.redirect_url,
            code_verifier=code_verifier,
            grant_type="authorization_code",
            client_id=self.client_id
        )

        token_response = self.token(request_data=token_request_data)

        return token_response



