from myblog import testing_myblog


def test_config():
    app = testing_myblog()
    assert app.testing
    app.config['TESTING'] = False
    assert not app.testing
