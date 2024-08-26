import pytest


class LoginTestPages:
    main_page = pytest.mark.usefixtures("main_page")
