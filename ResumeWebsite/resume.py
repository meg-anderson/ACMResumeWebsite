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

    honors = db.execute(
        'SELECT h.id, title, givenby, description, created'
        ' FROM honors h'
        ' ORDER BY created DESC'
    )

    return render_template('resume/index.html', experiences=experiences, skills = skills, honors=honors)


@bp.route('/workexp/create', methods=('GET', 'POST'))
@login_required
def create_workexp():
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

    return render_template('resume/workexp/create.html')


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
def update_workexp(id):
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

    return render_template('resume/workexp/update.html', experience=experience)


@bp.route('workexp/<int:id>/delete', methods=('POST',))
@login_required
def delete_workexp(id):
    get_experience(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('resume.index'))

@bp.route('/skill/create', methods=('GET', 'POST'))
@login_required
def create_skill():
    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO skills (title, description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, description, g.user['id'])
            )
            db.commit()
            return redirect(url_for('resume.index'))

    return render_template('resume/skills/create.html')


def get_skill(id, check_author=True):

    db = get_db()

    skill = db.execute(
        'SELECT s.id, title, description, author_id, username'
        ' FROM skills s JOIN user u ON s.author_id = u.id'
        ' WHERE s.id = ?',
        (id,)
    ).fetchone()

    if skill is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and skill['author_id'] != g.user['id']:
        abort(403)

    return skill


@bp.route('skill/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_skill(id):
    skill = get_skill(id)

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        error = None


        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE skills SET title = ?, description = ?'
                ' WHERE id = ?',
                (title, description, id)
            )
            db.commit()
            return redirect(url_for('resume.index'))

    return render_template('resume/skills/update.html', skill=skill)


@bp.route('skill/<int:id>/delete', methods=('POST',))
@login_required
def delete_skill(id):
    get_skill(id)
    db = get_db()
    db.execute('DELETE FROM skills WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('resume.index'))

@bp.route('/honor/create', methods=('GET', 'POST'))
@login_required
def create_honor():
    if request.method == 'POST':

        title = request.form['title']
        givenby = request.form['givenby']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO honors (title, givenby, description, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, givenby, description, g.user['id'])
            )
            db.commit()
            return redirect(url_for('resume.index'))

    return render_template('resume/honors/create.html')


def get_honor(id, check_author=True):

    db = get_db()

    honor = db.execute(
        'SELECT h.id, title, givenby, description, author_id, username'
        ' FROM honors h JOIN user u ON h.author_id = u.id'
        ' WHERE h.id = ?',
        (id,)
    ).fetchone()

    if honor is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and honor['author_id'] != g.user['id']:
        abort(403)

    return honor


@bp.route('honor/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_honor(id):
    honor = get_honor(id)

    if request.method == 'POST':

        title = request.form['title']
        givenby = request.form['givenby']
        description = request.form['description']
        error = None


        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE honors SET title = ?, givenby = ?, description = ?'
                ' WHERE id = ?',
                (title, givenby, description, id)
            )
            db.commit()
            return redirect(url_for('resume.index'))

    return render_template('resume/honors/update.html', honor=honor)


@bp.route('honor/<int:id>/delete', methods=('POST',))
@login_required
def delete_honor(id):
    get_honor(id)
    db = get_db()
    db.execute('DELETE FROM honors WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('resume.index'))