import pytest
import app
app.path.insert(1, 'app/main/main.py')
@pytest.fixture
def client():
    client = app.test_client()
    
    yield client