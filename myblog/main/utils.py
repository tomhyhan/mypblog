from datetime import datetime
from myblog.models import Project


def is_new(user):
    first_post = Project.query.filter_by(user_id=user.id).first()
    new = False
    diff = datetime.utcnow() - first_post.data_posted
    diff_indays = diff.total_seconds()/86400
    if diff_indays <= 7:
        new = True
        return new
    return new

