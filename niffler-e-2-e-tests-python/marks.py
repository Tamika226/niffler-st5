import pytest


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    login_page = pytest.mark.usefixtures("login_page")
    profile_page = pytest.mark.usefixtures("profile_page")
    register_page = pytest.mark.usefixtures("register_page")
    identification_page = pytest.mark.usefixtures("identification_page")


class Actions:
    login = pytest.mark.usefixtures("login")
