from myblog.models import User, Project, Reply


def test_comment1(test_client,init_db,auth):
    auth.login()
    user = User.query.filter_by(username='tom').first()
    project = Project.query.filter_by(id=1).first()
    posts = Project.query.filter_by(user_id=user.id).order_by(Project.data_posted.desc()).paginate(per_page=3)


    response = test_client.post(f'/project/tom',
                                data=dict(project_id=1,
                                          content="!@#$%^&",
                                          username='tom'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'!@#$%^&' in response.data




