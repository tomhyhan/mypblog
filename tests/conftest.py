import os
import tempfile

import pytest

from myblog import testing_myblog, db, bcrypt
from myblog.models import User, Project, Reply, Tore, Article


@pytest.fixture
def test_client():
    app = testing_myblog()

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    # tests happen HERE!
    yield testing_client

    ctx.pop()


@pytest.fixture
def init_db(scope="session"):
    db.drop_all()
    db.create_all()

    # adding test user data
    hashed_pass1 = bcrypt.generate_password_hash("password").decode("utf-8")
    hashed_pass2 = bcrypt.generate_password_hash("testing").decode("utf-8")
    user = User(username="tom", email="tom@c.com", password=hashed_pass1)
    user1 = User(username="testuser1", email="testuser1@test.com", password=hashed_pass2)
    db.session.add(user)
    db.session.add(user1)
    db.session.commit()

    # adding testing project data
    project = Project(title="test", content="test", user_id=user.id,id=1)
    project1 = Project(title="test", content="test", user_id=user1.id,id=2)
    db.session.add(project)
    db.session.add(project1)
    db.session.commit()

    #adding test article data
    article = Article(title="test", content="test", user_id=user.id,id=1)
    article1 = Article(title="test", content="test", user_id=user1.id,id=2)
    db.session.add(article)
    db.session.add(article1)
    db.session.commit()

    #adding test comment data
    reply = Reply(content="test_comment",username=user.username, project_id=project.id)
    db.session.add(reply)
    db.session.commit()

    #adding test reply data
    tore = Tore(content="test_reply",username=user.username, reply_id=reply.id)
    db.session.add(tore)
    db.session.commit()

    # tests happen HERE!
    yield db

    db.drop_all()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email="tom@c.com", password="password"):
        return self._client.post(
            "/login",
            data=dict(email=email, password=password)
            , follow_redirects=True
        )

    def logout(self):
        return self._client.get("/logout")


# authenticate the test user for testing
@pytest.fixture
def auth(test_client,init_db):
    login = AuthActions(test_client)
    return login


@pytest.fixture
def new_user():
    hashed_password = bcrypt.generate_password_hash("testing").decode("utf-8")
    user = User(username="tom", email="tom@c.com", password=hashed_password, id=1)
    return user


@pytest.fixture
def new_project():
    project = Project(title="test",content="test",user_id=1,id=1)
    return project


@pytest.fixture
def new_article():
    article = Article(title="test",content="test",user_id=1,id=1)
    return article


@pytest.fixture
def new_reply(new_user,new_project):
    reply = Reply(content="test",project_id=new_project.id,username=new_user.username,id=1)
    return reply


@pytest.fixture
def new_tore(new_reply,new_user):
    tore = Tore(content="test",reply_id=new_reply.id,username=new_user.username)
    return tore
