from requests.adapters import HTTPAdapter
from requests.models import PreparedRequest, Response


class Interceptor(HTTPAdapter):
    def init(self, auth_client):
        super().__init__()
        self.auth_client = auth_client

    def build_response(self, req: PreparedRequest, resp: Response) -> Response:
        response = super().build_response(req, resp)
        if response.is_redirect and "Location" in response.headers:
            location = response.headers["Location"]
            if "code=" in location:
                code = location.split("code=")[-1].split("&")[0]
                self.auth_client.code = code
        return response
