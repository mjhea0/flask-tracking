from flask import Blueprint, Response, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import current_user, login_required
from app import app, db, login_manager
from app.tracking.models import Site, Visit
from app.tracking.forms import RegisterSiteForm
from datetime import datetime
from app.tracking.geodata import get_geodata
from app.tracking.decorators import crossdomain


mod = Blueprint('tracking', __name__)


@mod.route('/sites/', methods=('GET', 'POST'))
@login_required
def sites_view():
    form = RegisterSiteForm(request.form)
    sites = current_user.sites.all()
    if form.validate_on_submit():
        site = Site()
        form.populate_obj(site)
        site.user_id = current_user.id
        db.session.add(site)
        db.session.commit()
        return redirect('/sites/')
    return render_template('tracking/index.html', form=form, sites=sites)

#http://proj1-6170.herokuapp.com/sites/<%= @current_user.id %>/visited?event='+tracker.settings.event+'&data='+tracker.settings.data+'&visitor='+tracker.settings.visitor
@mod.route('/visit/<int:site_id>/visited', methods=('GET','POST'))
@crossdomain(origin="*", methods=["POST", "GET, OPTIONS"], headers="Content-Type, Origin, Referer, User-Agent", max_age="3600") 
def register_visit(site_id):
    site = Site.get_by_id(site_id)
    if site:
        browser = request.headers.get('User-Agent')
        date = datetime.now()
        event = request.args.get('event')
        url = request.url
        ip_address = request.remote_addr
        geo = get_geodata(ip_address)
        location_full = ", ".join([geo['city'],geo['zipcode'],geo['latitude'],geo['longitude']])
        location = ", ".join([geo['city'],geo['zipcode']])
        visit = Visit(browser, date, event, url, ip_address, location_full, location)
        visit.site_id = site_id
        db.session.add(visit)
        db.session.commit()
    return Response("visit recorded", content_type="text/plain")

# self, browser=None, date=None, event=None, url=None, ip_address=None, location_full=None