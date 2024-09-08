import requests
from models.Auth import PreRequest, Login, Token, TokenResponse
from helpers.oauth_codes import OauthHelper
from urllib.parse import urljoin


class AuthClient:

    def __init__(self, auth_url: str, client_id: str):
        self.auth_url = auth_url
        self.client_id = client_id
        self.redirect_url = urljoin(self.auth_url, "/authorized")
        self.code = None

    def pre_request(self, request_data: PreRequest):
        response = requests.get(f"{self.auth_url}/oauth2/authorize", params=request_data.dict(), allow_redirects=False)
        jsessionid = response.cookies.get('JSESSIONID')
        redirect_url1 = response.headers['Location']

        response2 = requests.get(redirect_url1, cookies=response.cookies)
        xsrf = response2.cookies.get("XSRF-TOKEN")
        response2.raise_for_status()
        return xsrf, jsessionid

    def login(self, jsessionid, request_data):
        # Здесь отправляем без редиректов, так как из-за того, то куки к запросу жестко заданы, он протаскивает их дальше по редиректу, а должен менять
        response = requests.post(f"{self.auth_url}/login", data=request_data,
                                 cookies={"JSESSIONID": jsessionid, "XSRF-TOKEN": request_data['_csrf']},
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=False)
        redirect_url_1 = response.headers.get("Location")

        response_2 = requests.get(redirect_url_1, cookies={"JSESSIONID": response.cookies.get('JSESSIONID')},
                                  allow_redirects=False)
        code = response_2.headers.get("Location").split("code=", 1)[1]

        response_3 = requests.get(self.redirect_url, cookies={"JSESSIONID": response_2.cookies.get('JSESSIONID')},
                                  params="code=" + code)

        response_3.raise_for_status()
        return code

    def token(self, request_data: Token):
        response = requests.post(f"{self.auth_url}/oauth2/token", data=request_data.dict())
        response.raise_for_status()
        return TokenResponse(**response.json()).access_token

    def do_login(self, username: str, password: str):
        code_verifier = OauthHelper.generate_code_verifier()
        code_challenge = OauthHelper.generate_code_challenge(code_verifier)

        pre_request_data = PreRequest(
            response_type="code",
            client_id="client",
            scope="openid",
            redirect_uri=self.redirect_url,
            code_challenge=code_challenge,
            code_challenge_method="S256"
        )

        xsrf, jsessionid = self.pre_request(request_data=pre_request_data)

        login_data = {
            "_csrf": f"{xsrf}",
            "username": f"{username}",
            "password": f"{password}"
        }

        code = self.login(jsessionid, request_data=login_data)

        token_request_data = Token(
            code=code,
            redirect_uri=self.redirect_url,
            code_verifier=code_verifier,
            grant_type="authorization_code",
            client_id="client"
        )

        token_response = self.token(request_data=token_request_data)

        return token_response
