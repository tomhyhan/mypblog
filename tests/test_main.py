from myblog.models import User, Project, Tore, Reply, Article
from myblog import db

def test_new_project(test_client,auth):
    auth.login()
    response = test_client.post('/project/new', data=dict(title='test',
                                                               content='content',
                                                               user_id=1)
                                 ,follow_redirects=True)

    assert response.status_code == 200
    assert b'content' in response.data
    assert b'test' in response.data


def test_new_project_update(test_client,init_db,auth):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    post = Project.query.filter_by(id=1).first()
    response = test_client.post(f'/project/{user.username}/{post.id}/update',
                                data=dict(title="test",content="change_content"),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'change_content' in response.data
    assert b'title' in response.data
    assert b'Project has been successfully updated' in response.data


def test_new_article(test_client,auth):
    auth.login()
    response = test_client.post('/article/new', data=dict(title='test',
                                                               content='content',
                                                               user_id=1)
                                 ,follow_redirects=True)

    assert response.status_code == 200
    assert b'content' in response.data
    assert b'test' in response.data


def test_new_article_update(test_client,init_db,auth):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    article = Article.query.filter_by(id=1).first()
    response = test_client.post(f'/article/{user.username}/{article.id}/update',
                                data=dict(title="test",content="change_content"),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'change_content' in response.data
    assert b'title' in response.data
    assert b'Article has been successfully updated' in response.data


def test_new_comment(test_client,auth,init_db):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    post = Project.query.filter_by(id=1).first()
    response = test_client.post('project/tom', data=dict(content='comment123',
                                                         username=user.username,
                                                         project_id=post.id,
                                                         ),
                                follow_redirects=True
                                )

    assert response.status_code == 200
    assert b'comment123' in response.data


def test_new_reply(test_client,auth):
    auth.login()


    response = test_client.post('project/tom', data=dict(content='reply123',
                                                         username='Bar',
                                                         project_id=1),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'reply123' in response.data


def test_delete_project(test_client,auth,init_db):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    post = Project.query.filter_by(id=1).first()
    response = test_client.post(f'/project/{user.username}/{post.id}/delete'
                                ,follow_redirects=True)


    assert response.status_code == 200
    assert b'Your project has been successfully deleted' in response.data

    # check if the project has been deleted
    post = Project.query.filter_by(id=1).first()
    assert post is None


def test_delete_comment(test_client,auth,init_db):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    reply = Reply.query.filter_by(id=1).first()
    response = test_client.post(f'/project/{user.username}/{reply.id}/delete_reply'
                                ,follow_redirects=True)


    assert response.status_code == 200
    assert b'Your comment has been successfully deleted' in response.data

    # check if the comment has been deleted
    reply = Reply.query.filter_by(id=1).first()
    assert reply is None


def test_delete_reply(test_client,auth,init_db):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    tore = Tore.query.filter_by(id=1).first()
    response = test_client.post(f'/project/{user.username}/{tore.id}/d'
                                ,follow_redirects=True)


    assert response.status_code == 200
    assert b'Your reply has been successfully deleted' in response.data

    # check if the Reply has been deleted
    tore = Tore.query.filter_by(id=1).first()
    assert tore is None


def test_delete_article(test_client,auth,init_db):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    post = Article.query.filter_by(id=1).first()
    response = test_client.post(f'/article/{user.username}/{post.id}/delete'
                                ,follow_redirects=True)

    assert response.status_code == 200
    assert b'Your article has been successfully deleted' in response.data

    # check if the article has been deleted
    post = Article.query.filter_by(id=1).first()
    assert post is None

