from myblog import db
from myblog.models import User
import pytest
from myblog import bcrypt


def test_login(test_client,init_db):
    failed_response = test_client.post("/login", data=dict(email="tom@c.com"
                                                    , password="wrong_password"), follow_redirects=True)

    assert b"The email or password you entered is incorrect" in failed_response.data

    response = test_client.post("/login",data=dict(email="tom@c.com"
                                                  ,password="password"),follow_redirects=True)

    assert response.status_code == 200
    assert b"tom" in response.data
    assert b"Logged in Successfully" in response.data
    assert b"Logout" in response.data
    assert b"Login" not in response.data
    assert b"Register" not in response.data
    assert b"Profile" in response.data
    assert b"Blog History" in response.data


def test_logout(test_client):
    response = test_client.get("logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"Create your own blog" in response.data
    assert b"Let's get started" in response.data
    assert b"Login" in response.data


def test_register(test_client,init_db):
    response = test_client.post("/register", data=dict(username="register", email="register@regi.com",
                                                       password="password",confirm_password="password")
                                            ,follow_redirects=True)

    assert response.status_code == 200
    assert b"Log In" in response.data
    assert b"Forgot your" in response.data

    # testing if registered user exits in db
    user = User.query.filter_by(username="register").first()
    assert user is not None


@pytest.mark.parametrize(("username", "email","password","confirm_password", "message"), [
    ("tom", "eg@c.com", "121212","121212", b"That username already exist."),
    ("Bom", "tom@c.com", "121212","121212", b"That email already exist."),
    ("tom1", "eg@c.com", "1212","1212", b"Field must be at least 6 characters long."),
    ("","","","",b"This field is required.")])
def test_register_validate_input(test_client,init_db, username, email, password, confirm_password, message):
    response = test_client.post("/register", data=dict(username=username, email=email,
                                                       password=password,confirm_password=confirm_password)
                                        )
    assert message in response.data


def test_is_loggedin(test_client,init_db,auth):
    auth.login()
    response = test_client.post("/login",data=dict(email="tom@c.com"
                                                  ,password="password"),follow_redirects=True)

    assert response.status_code == 200
    assert b"Blog History" in response.data
    assert b"tom's Blog" in response.data


def test_reset_password(test_client,init_db):
    user = User.query.filter_by(username="tom").first()
    token = user.get_reset_token()
    user = User.verify_reset_token(token)
    password = "pass_changed"
    response = test_client.post(f"/reset_password/{token}",
                                data=dict(password=password,
                                          confirm_password=password,),
                                follow_redirects=True)
    hashed_password = user.password
    is_match = bcrypt.check_password_hash(hashed_password, password)

    assert response.status_code == 200
    assert is_match == True
    assert b"Email" in response.data
    assert b"Your password has been updated" in response.data

