from flask import Blueprint, render_template, url_for, abort, redirect, flash, request
from flask_login import current_user, login_required
from myblog import db
from myblog.models import User, Project, Article, Reply, Tore
from myblog.main.forms import ProjectForm, ArticleForm, ReplyForm, ReplyReplyForm
from myblog.main.utils import is_new
from myblog.config import S3Config

main = Blueprint("main",__name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home', location=S3Config.S3_LOCATION)


@main.route('/project/<user>',methods=["GET","POST"])
def project(user):
    username = User.query.filter_by(username=user).first_or_404()
    page = request.args.get('page',1,type=int)
    posts = Project.query.filter_by(user_id=username.id).order_by(Project.data_posted.desc()).paginate(per_page=3)
    next_url = url_for('main.project', user=username.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.project', user=username.username, page=posts.prev_num) if posts.has_prev else None

    if posts.total == 0:
        new = False
    else:
        new = is_new(username)
    reply_form = ReplyForm()

    to_reply = ReplyReplyForm()
    replies = Reply.query
    toreplies = Tore.query

    if reply_form.submit1.data and reply_form.validate_on_submit():
        reply = Reply(content=reply_form.content.data, username=current_user.username, project_id=reply_form.id.data)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('main.project', user=username.username,page=page))
    if to_reply.submit2.data and to_reply.validate_on_submit():
        reply_to = Tore(content=to_reply.content.data, username=current_user.username, reply_id=to_reply.id.data)
        db.session.add(reply_to)
        db.session.commit()
        return redirect(url_for('main.project', user=username.username, page=page))
    return render_template('project.html', title='Project',
                           user=username, project=True,
                           posts=posts, page=page,
                           next_url=next_url, prev_url=prev_url,
                           is_new=new, form=reply_form, replies=replies,
                           reply_form=to_reply,toreplies=toreplies,
                           locations=S3Config.S3_LOCATION)


@main.route('/project/new', methods=["GET","POST"])
@login_required
def new_project():
    project_form = ProjectForm()
    username = User.query.filter_by(username=current_user.username).first_or_404()
    if project_form.validate_on_submit():
        post = Project(title=project_form.title.data, content=project_form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your project has been created", 'success')
        return redirect(url_for('main.project', user=current_user.username))
    return render_template('create_project.html', title="New Project", form=project_form,
                                   user=username, legend= 'Upload a new project')


@main.route('/project/<user>/<int:post_id>', methods=["GET","POST"])
def aproject(user,post_id):
    post = Project.query.get_or_404(post_id)
    username = User.query.filter_by(username=user).first_or_404()
    return render_template('aproject.html', title=post.title, post=post, user=username)


@main.route('/project/<user>/<int:post_id>/update', methods=["GET","POST"])
@login_required
def aproject_update(user,post_id):
    post = Project.query.get_or_404(post_id)
    username = User.query.filter_by(username=user).first_or_404()
    project_form = ProjectForm()
    if post.author != current_user:
        abort(403)
    if project_form.validate_on_submit():
        post.title = project_form.title.data
        post.content = project_form.content.data
        db.session.commit()
        flash('Project has been successfully updated',"success")
        return redirect(url_for('main.aproject', user=username.username, post_id = post.id))
    elif request.method == 'GET':
        project_form.title.data = post.title
        project_form.content.data = post.content
    return render_template('create_project.html', title=post.title, post=post,
                                   user=username, form=project_form,
                                   legend= 'Update your project')


@main.route('/project/<user>/<int:post_id>/delete', methods=["POST"])
@login_required
def delete_aproject(user,post_id):
    post = Project.query.get_or_404(post_id)
    reply = Reply.query.filter_by(project_id=post.id).first()
    try:
        Tore.query.filter_by(reply_id = reply.id).delete()
    except:
        pass
    Reply.query.filter_by(project_id=post.id).delete()

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your project has been successfully deleted', 'success')
    return redirect(url_for('main.project', user=current_user.username))


@main.route('/project/<user>/<int:reply_id>/delete_reply', methods=["POST"])
@login_required
def reply_delete(user,reply_id):
    username = User.query.filter_by(username=user).first_or_404()
    reply = Reply.query.filter_by(id=reply_id).first_or_404()
    try:
        Tore.query.filter_by(reply_id = reply.id).delete()
    except:
        pass
    if reply.username != current_user.username:
        abort(403)
    Reply.query.filter_by(id=reply.id).delete()
    db.session.commit()
    flash('Your comment has been successfully deleted','success')
    return redirect(url_for('main.project',user=username.username))


@main.route('/project/<user>/<int:tore_id>/d', methods=["POST"])
@login_required
def tore_delete(user,tore_id):
    username = User.query.filter_by(username=user).first_or_404()
    tore = Tore.query.filter_by(id=tore_id).first_or_404()
    if tore.username != current_user.username:
        abort(403)
    Tore.query.filter_by(id=tore.id).delete()
    db.session.commit()
    flash('Your reply has been successfully deleted','success')
    return redirect(url_for('main.project',user=username.username))

# --------------------------Article---------------------------------------

@main.route('/article/<user>',methods=["GET","POST"])
def article(user):
    username = User.query.filter_by(username=user).first_or_404()
    page = request.args.get('page',1,type=int)
    projects = Project.query.filter_by(user_id=username.id).all()
    posts = Article.query.filter_by(user_id=username.id).order_by(Article.data_posted.desc()).paginate(per_page=3)
    next_url = url_for('main.article', user=username.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.article', user=username.username, page=posts.prev_num) if posts.has_prev else None
    if not projects:
        new = False
    else:
        new = is_new(username)
    return render_template('article.html', title='Article',
                           user=username, article=True,
                           posts=posts, page=page,
                           next_url=next_url, prev_url=prev_url,
                           is_new= new)


@main.route('/article/new', methods=["GET","POST"])
@login_required
def new_article():
    article_form = ArticleForm()
    username = User.query.filter_by(username=current_user.username).first_or_404()
    if article_form.validate_on_submit():
        post = Article(title=article_form.title.data, content=article_form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your article has been created", 'success')
        return redirect(url_for('main.article', user=current_user.username))
    return render_template('create_article.html', title="New Article", form=article_form,
                                   user=username, legend= 'Upload a new article')


@main.route('/article/<user>/<int:post_id>', methods=["GET","POST"])
def anarticle(user,post_id):
    post = Article.query.get_or_404(post_id)
    username = User.query.filter_by(username=user).first_or_404()
    return render_template('anarticle.html', title=post.title, post=post, user=username)


@main.route('/article/<user>/<int:post_id>/update', methods=["GET","POST"])
@login_required
def anarticle_update(user,post_id):
    post = Article.query.get_or_404(post_id)
    username = User.query.filter_by(username=user).first_or_404()
    article_form = ArticleForm()
    if post.author != current_user:
        abort(403)
    if article_form.validate_on_submit():
        post.title = article_form.title.data
        post.content = article_form.content.data
        db.session.commit()
        flash('Article has been successfully updated',"success")
        return redirect(url_for('main.anarticle', user=username.username, post_id = post.id))
    elif request.method == 'GET':
        article_form.title.data = post.title
        article_form.content.data = post.content
    return render_template('create_article.html', title=post.title, post=post,
                                   user=username, form=article_form,
                                   legend= 'Update your Article')


@main.route('/article/<user>/<int:post_id>/delete', methods=["POST"])
@login_required
def delete_anarticle(user,post_id):
    post = Article.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your article has been successfully deleted', 'success')
    return redirect(url_for('main.article', user=current_user.username))

