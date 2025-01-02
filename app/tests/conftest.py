import pytest
from project import app


@pytest.fixture()
def app():
    main = app()