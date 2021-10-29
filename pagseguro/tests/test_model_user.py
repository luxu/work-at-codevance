import pytest
from django.contrib.auth.models import User
from model_mommy import mommy


@pytest.fixture
def user(db):
    return mommy.make(
        User,
        username="olivia",
        password="2"
    )


@pytest.fixture
def users(db):
    return mommy.make(User, 3)


@pytest.fixture
def resp(client, db):
    return client.get('/')


def test_should_username(user) -> None:
    assert user.password is 'marinaul'
    assert user.username is 'marinaul'
