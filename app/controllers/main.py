from flask import (
    Blueprint, render_template
)
from app.controllers import default
from app.models.tables import User, Post, CatsTags, ZipperPostsCatsTags

bp = Blueprint('main', __name__)


@bp.route('/webapp')
def webapp():
#category scheme
    cats = CatsTags.query.all()
    catag_id = []
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_id_ = CatsTags.query.filter_by(id=cat.id).first().id
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_id.append(catag_id_)
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme
    return render_template('main_pwa/index.html',
                           title='Flask-PWA',
                           catag_name=catag_name,
                           catag_colour=catag_colour,
                           len_cats = len(catag_name))