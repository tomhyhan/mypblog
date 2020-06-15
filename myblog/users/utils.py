import os
import secrets
from PIL import Image
from flask import current_app, url_for
from myblog import mail
from flask_mail import Message
import boto3, botocore

from myblog.config import S3Config

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3Config.S3_KEY,
   aws_secret_access_key=S3Config.S3_SECRET
)


def save_picture(form_picture, bucket_name, acl="public-read"):
    file_name = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    picture_file_name = file_name + ext
    # picture_path = os.path.join(current_app.root_path, 'static/profile_picture', picture_file_name)

    try:
        s3.upload_fileobj(
            form_picture,
            bucket_name,
            picture_file_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": form_picture.content_type
            }
        )
    except Exception as e:
        # This is a catch all exception.
        print("Something Happened: ", e)
        return e

    return f"{S3Config.S3_LOCATION}{picture_file_name}"

    # resize = (125,125)
    # img = Image.open(form_picture)
    # img.thumbnail(resize)
    # if ext == '.jpg':
    #     img = img.convert('RGB')
    # img.save(picture_path)
    #
    # return picture_file_name


def send_email(user):
    token = user.get_reset_token()
    msg = Message('Your Account Recovery',
                  recipients=[user.email])
    msg.body = f'''To reset your password, please visit the following link:
{url_for('users.reset_password', token=token, _external=True)}
    
If you are not trying to change your password, please ignore this email. It is possible that another user entered their information incorrectly.
'''
    mail.send(msg)
