from myblog.models import User, Project, Reply, Tore, Article
from flask import url_for

def test_project_page(test_client,init_db):
    user = User.query.filter_by(username='tom').first()
    reply = Reply.query.filter_by(project_id=1).first()
    tore = Tore.query.filter_by(reply_id=reply.id).first()
    response = test_client.get(f'/project/{user.username}')

    assert response.status_code == 200
    assert b'Category' in response.data
    assert b'Blog History' in response.data
    assert b'Project' in response.data
    assert b'Article' in response.data
    assert b'Profile' in response.data
    assert reply.content.encode('UTF-8') in response.data
    assert tore.content.encode('UTF-8') in response.data


def test_new_project_page(test_client,auth):

    auth.login()
    response1 = test_client.get('/project/new')

    assert response1.status_code == 200
    assert b'Upload a new project' in response1.data
    assert b'Title' in response1.data
    assert b'Content' in response1.data


def test_aproject_page(test_client,init_db):
    user = User.query.filter_by(username='tom').first()
    post = Project.query.filter_by(id=1).first()
    response = test_client.get(f'/project/{user.username}/{post.id}')

    assert response.status_code == 200
    assert b'test' in response.data
    assert b'tom' in response.data


def test_new_project_update_page(test_client,init_db,auth):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    post = Project.query.filter_by(id=1).first()
    response = test_client.get(f'/project/{user.username}/{post.id}/update')

    assert response.status_code == 200
    assert b'Update your project' in response.data
    assert post.title.encode('UTF-8') in response.data
    assert post.content.encode('UTF-8') in response.data


def test_article_page(test_client,init_db):
    user = User.query.filter_by(username='tom').first()
    response = test_client.get(f'/article/{user.username}')

    assert response.status_code == 200
    assert b'Category' in response.data
    assert b'Blog History' in response.data
    assert b'Article' in response.data
    assert b'Profile' in response.data


def test_new_article_page(test_client,auth):
    auth.login()
    response1 = test_client.get('/article/new')

    assert response1.status_code == 200
    assert b'Upload a new article' in response1.data
    assert b'Title' in response1.data
    assert b'Content' in response1.data


def test_anarticle_page(test_client,init_db):
    user = User.query.filter_by(username='tom').first()
    post = Article.query.filter_by(id=1).first()
    response = test_client.get(f'/article/{user.username}/{post.id}')

    assert response.status_code == 200
    assert b'test' in response.data
    assert b'tom' in response.data


def test_new_article_update_page(test_client,init_db,auth):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    post = Article.query.filter_by(id=1).first()
    response = test_client.get(f'/project/{user.username}/{post.id}/update')

    assert response.status_code == 200
    assert b'Update your project' in response.data
    assert post.title.encode('UTF-8') in response.data
    assert post.content.encode('UTF-8') in response.data
