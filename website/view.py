from flask.helpers import flash
from flask.json import jsonify
from website.models import Note
from flask import Blueprint,render_template
from flask.globals import request
from flask_login import login_required, current_user
from flask_login.config import LOGIN_MESSAGE_CATEGORY
from sqlalchemy.sql.functions import user
from .models import Note
from . import db
from flask import flash
import json


views = Blueprint('views',__name__)
 
@views.route('/', methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!',category='error')
        else:
            new_note = Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Not Added',category='success')
    return render_template("home.html",user=current_user) 

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note=json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})

