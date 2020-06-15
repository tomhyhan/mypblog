from myblog import bcrypt


def test_new_user(new_user):
    assert new_user.username == 'tom'
    assert new_user.email == 'tom@c.com'
    assert new_user.password != 'testing'
    assert bcrypt.check_password_hash(new_user.password, "testing") == True


def test_new_project(new_project):
    assert new_project.content == "test"
    assert new_project.user_id == 1
    assert new_project.title == "test"


def test_new_article(new_article):
    assert new_article.content == "test"
    assert new_article.user_id == 1
    assert new_article.title == "test"


def test_new_reply(new_reply):
    assert new_reply.content == "test"
    assert new_reply.username == 'tom'
    assert new_reply.project_id == 1


def test_new_tore(new_tore):
    assert new_tore.content == "test"
    assert new_tore.username == 'tom'
    assert new_tore.reply_id == 1
