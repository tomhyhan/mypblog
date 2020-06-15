from datetime import datetime
from myblog.models import Project


def test_is_new(test_client, init_db):
    first_post = Project.query.filter_by(user_id=1).first()
    new = False
    utcnow = datetime(2020,6,12)
    diff = utcnow - first_post.data_posted
    diff_indays = diff.total_seconds()/86400
    if diff_indays <= 7:
        new = True
    assert new == True
