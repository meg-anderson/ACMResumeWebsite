from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ResumeWebsite.auth import login_required
from ResumeWebsite.db import get_db

bp = Blueprint('resume', __name__, url_prefix='/resume')


@bp.route('/')
def index():

    db = get_db()

    experiences = db.execute(
        'SELECT id, created, title, who, what, whenexp, author_id'
        ' FROM workexperience'
        ' ORDER BY created DESC'
    ).fetchall()

    skills = db.execute(
        # 'SELECT id, title, description, author_id'
        'SELECT *'
        ' FROM skills'
        ' ORDER BY created DESC'
    ).fetchall()

    # honors = db.execute(
    #     'SELECT p.id, honorstitle, honorswho, honorsbody'
    #     ' FROM skills p'
    #     ' ORDER BY created DESC'
    # )

    return render_template('resume/index.html', experiences=experiences, skills = skills)


@bp.route('/workexp/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':

        title = request.form['title']
        who = request.form['who']
        what = request.form['what']
        whenexp = request.form['whenexp']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO workexperience (title, who, what, whenexp, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, who, what, whenexp, g.user['id'])
            )
            db.commit()
            return redirect(url_for('resume.index'))

    return render_template('resume/create.html')


def get_experience(id, check_author=True):

    db = get_db()

    experience = db.execute(
        'SELECT w.id, title, who, what, whenexp, author_id, username'
        ' FROM workexperience w JOIN user u ON w.author_id = u.id'
        ' WHERE w.id = ?',
        (id,)
    ).fetchone()

    if experience is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and experience['author_id'] != g.user['id']:
        abort(403)

    return experience


@bp.route('workexp/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    experience = get_experience(id)

    if request.method == 'POST':

        title = request.form['title']
        who = request.form['who']
        what = request.form['what']
        whenexp = request.form['whenexp']
        error = None


        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE workexperience SET title = ?, who = ?, what = ?, whenexp = ?'
                ' WHERE id = ?',
                (title, who, what, whenexp, id)
            )
            db.commit()
            return redirect(url_for('resume.index'))

    return render_template('resume/update.html', experience=experience)


@bp.route('workexp/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_experience(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('resume.index'))