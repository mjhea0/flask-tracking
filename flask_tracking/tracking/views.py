from flask import abort, Blueprint, flash, jsonify, Markup, redirect, render_template, url_for
from flask.ext.login import current_user, login_required

from .forms import SiteForm, VisitForm
from .models import Site, Visit
from flask_tracking.data import query_to_list


tracking = Blueprint("tracking", __name__)


@tracking.route("/")
def index():
    if not current_user.is_anonymous():
        return redirect(url_for(".view_sites"))
    return render_template("index.html")


@tracking.route("/sites", methods=("POST", ))
@login_required
def add_site():
    form = SiteForm()
    if form.validate_on_submit():
        Site.create(owner=current_user, **form.data)
        flash("Added site")
        return redirect(url_for(".view_sites"))

    return render_template("validation_error.html", form=form)


@tracking.route("/sites/<int:site_id>")
@login_required
def view_site_visits(site_id=None):
    site = Site.query.get_or_404(site_id)
    if not site.user_id == current_user.id:
        abort(401)
    query = Visit.query.filter(Visit.site_id == site_id)
    data = query_to_list(query)
    title = "visits for {}".format(site.base_url)
    return render_template("data_list.html", data=data, title=title)


@tracking.route("/sites/<int:site_id>/visit", methods=("POST",))
def add_visit(site_id=None):
    site = Site.query.get_or_404(site_id)
    # WTForms does not coerce obj or keyword arguments
    # (otherwise, we could just pass in `site=site_id`)
    # CSRF is disabled in this case because we will *want*
    # users to be able to hit the /site/:id endpoint from other sites.
    form = VisitForm(csrf_enabled=False, site=site)

    if form.validate_on_submit():
        Visit.create(**form.data)
        # No need to send anything back to the client
        # Just indicate sucess with the response code
        # (204 is "I succeded, but I don't have anything
        # to send to you right now.")
        return '', 204

    return jsonify(error="Missing required data")


@tracking.route("/sites")
@login_required
def view_sites():
    query = Site.query.filter(Site.user_id == current_user.id)
    data = query_to_list(query)
    form = SiteForm()

    results = []

    try:
        # The header row should not be linked
        results = [next(data)]
        for row in data:
            row = [_make_link(cell) if i == 0 else cell
                   for i, cell in enumerate(row)]
            results.append(row)
    except StopIteration:
        # This happens when a user has no sites registered yet
        # Since it is expected, we ignore it and carry on.
        pass

    return render_template("tracking/sites.html", sites=results, form=form)


_LINK = Markup('<a href="{url}">{name}</a>')


def _make_link(site_id):
    url = url_for(".view_site_visits", site_id=site_id)
    return _LINK.format(url=url, name=site_id)
