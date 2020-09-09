#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'show'
    start_time = db.Column('start_time', db.DateTime, primary_key=True)
    venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    artist = db.relationship('Artist', backref=db.backref('venues', lazy=True))            
    venue = db.relationship('Venue', backref=db.backref('artist', lazy=True))
                 

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_talent_statement = db.Column(db.String(1000))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_talent_statement = db.Column(db.String(1000))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  venue_query = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  city_state =''
  for venue in venue_query:
      upcoming_shows = Show.query.filter(Show.start_time > current_time, Show.venue_id==venue.id).all()
      if city_state == venue.city + venue.state:
          data[len(data)-1]["venues"].append({
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows": len(upcoming_shows)
              })
      else: 
          city_state = venue.city + venue.state
          data.append({
              "city": venue.city,
              "state": venue.state,
              "venues": [{
                  "id": venue.id,
                  "name": venue.name,
                  "num_upcoming_shows": len(upcoming_shows)
                  }]
              })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    tag = request.form.get('search_term')
    search = "%" + tag +"%"
    venue_query = Venue.query.filter(Venue.name.ilike(search)).all()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = []
    for venue in venue_query:
        upcoming_shows = Show.query.filter(Show.start_time > current_time, Show.venue_id==venue.id).all()
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(upcoming_shows)})
        
    response ={"count": len(venue_query),
               "data": data}
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    
    venue = Venue.query.filter(Venue.id == venue_id).first()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    upcoming_shows_query = Show.query.filter(Show.start_time > current_time, Show.venue_id==venue.id).all()
    past_shows_query = Show.query.filter(Show.start_time < current_time, Show.venue_id==venue.id).all()
    upcoming_shows = []
    past_shows = []
    for show in upcoming_shows_query:
        upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": Artist.query.filter(Artist.id == show.artist_id).first().name,
            "artist_image_link": Artist.query.filter(Artist.id == show.artist_id).first().image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')})
        
    for show in past_shows_query:
        past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": Artist.query.filter(Artist.id == show.artist_id).first().name,
            "artist_image_link": Artist.query.filter(Artist.id == show.artist_id).first().image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')})
    
    data = {
        "id": venue.id,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "website": venue.website,
        "image_link": venue.image_link,
        "seeking_description": venue.seeking_talent_statement,
        "past_shows_count": len(past_shows_query),
        "upcoming_shows_count": len(upcoming_shows_query),
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        }
  
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    error = False
    form = VenueForm()
    if form.validate_on_submit():
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebk_link']
        website_link = request.form['website_link']
        seeking_talent ='N'
        seeking_talent = request.form.get('seeking_talent')
        if seeking_talent == 'y':
            seeking_talent =True
        seeking_talent_statement = request.form['seeking_talent_statement']
        image_link = request.form['image_link']
        phone = request.form['phone']
    else:
        flash('Venue ' + request.form['name'] + ' failed due to validation error!')
        return  render_template('forms/new_venue.html', form=form)
    try:
        
        venue = Venue(name=name, city=city, state=state, address=address, genres=genres,
                      facebook_link=facebook_link, phone=phone, image_link=image_link,
                      seeking_talent=seeking_talent, seeking_talent_statement=seeking_talent_statement,
                      website=website_link)
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally: 
        db.session.close()
    if error:
        flash('Venue ' + request.form['name'] + ' Failed!')
        abort (400)
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
        
        
    
    

  # on successful db insert, flash success
    
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    error = False;
    try:
        venue = Venue.query.filter(Venue.id == venue_id).first()
        shows = Show.query.filter(Show.venue_id == venue_id).all()
        for show in shows:
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally: 
        db.session.close()
    if error:
        flash('Delete Venue' + ' Failed!')
        abort (400)
    else:
        flash('Venue was successfully deleted!')
        return render_template('pages/home.html')
        
        
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
    
  data=[]
  
  artist_query = Artist.query.all()
  
  for artist in artist_query:
      data.append({
              "id": artist.id,
              "name": artist.name
              })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    tag = request.form.get('search_term')
    search = "%" + tag +"%"
    artist_query = Artist.query.filter(Artist.name.ilike(search)).all()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = []
    for artist in artist_query:
        upcoming_shows = Show.query.filter(Show.start_time > current_time, Show.venue_id==artist.id).all()
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(upcoming_shows)})
        
    response ={"count": len(artist_query),
               "data": data}
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    artist = Artist.query.filter(Artist.id == artist_id).first()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    upcoming_shows_query = Show.query.filter(Show.start_time > current_time, Show.artist_id==artist.id).all()
    past_shows_query = Show.query.filter(Show.start_time < current_time, Show.artist_id==artist.id).all()
    upcoming_shows = []
    past_shows = []
    for show in upcoming_shows_query:
        upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": Venue.query.filter(Venue.id == show.venue_id).first().name,
            "venue_image_link": Venue.query.filter(Venue.id == show.venue_id).first().image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')})
        
    for show in past_shows_query:
        past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": Venue.query.filter(Venue.id == show.venue_id).first().name,
            "venue_image_link": Venue.query.filter(Venue.id == show.venue_id).first().image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')})
    
    data = {
        "id": artist.id,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "facebook_link": artist.facebook_link,
        "website": artist.website,
        "seeking_talent": artist.seeking_talent,
        "seeking_description":artist.seeking_talent_statement,
        "past_shows_count": len(past_shows_query),
        "upcoming_shows_count": len(upcoming_shows_query),
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        }
  
    return render_template('pages/show_artist.html', artist=data)


@app.route('/artist/<artist_id>/delete', methods=['POST'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    error = False;
    try:
        artist = Artist.query.filter(Artist.id == artist_id).first()
        shows = Show.query.filter(Show.artist_id == artist_id).all()
        for show in shows:
            db.session.delete(show)
        db.session.delete(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally: 
        db.session.close()
    if error:
        flash('Delete Artist' + ' Failed!')
        abort (400)
    else:
        flash('Artist was successfully deleted!')
        return render_template('pages/home.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.filter(Artist.id == artist_id).first()
  form = ArtistForm(obj=artist)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    
  error = False
  form = ArtistForm()
  artist = Artist.query.filter(Artist.id==artist_id).first()
  if form.validate_on_submit():
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.genres = request.form.getlist('genres')
      artist.facebook_link = request.form['facebk_link']
      artist.website_link = request.form['website_link']
      seeking_talent = request.form.get('seeking_talent')
      if seeking_talent == 'y':
          artist.seeking_talent =True
      else:
          artist.seeking_talent = False
      artist.seeking_talent_statement = request.form['seeking_talent_statement']
      artist.image_link = request.form['image_link']
      artist.phone = request.form['phone']     
  else:
        flash('Artist ' + request.form['name'] + ' failed due to validation error!')
        return  render_template('forms/edit_artist.html', form=form, artist= artist)
  try:
      db.session.commit()
  except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
  finally: 
        db.session.close()
  if error:
        flash('Edit Artist' + ' Failed!')
        abort (400)
  else:
        flash('Artist was successfully edited!')
        return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  venue= Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  form = VenueForm()
  venue = Venue.query.filter(Venue.id==venue_id).first()
  if form.validate_on_submit():
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.address = request.form['address']
      venue.genres = request.form.getlist('genres')
      venue.facebook_link = request.form['facebk_link']
      venue.website_link = request.form['website_link']
      seeking_talent = request.form.get('seeking_talent')
      if seeking_talent == 'y':
          venue.seeking_talent =True
      else:
          venue.seeking_talent = False
      venue.seeking_talent_statement = request.form['seeking_talent_statement']
      venue.image_link = request.form['image_link']
      venue.phone = request.form['phone']     
  else:
        flash('Venue ' + request.form['name'] + ' failed due to validation error!')
        return  render_template('forms/edit_venue.html', form=form, venue= venue)
  try:
      db.session.commit()
  except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
  finally: 
        db.session.close()
  if error:
        flash('Edit Venue' + ' Failed!')
        abort (400)
  else:
        flash('Venue was successfully edited!')
        return redirect(url_for('show_venue', venue_id=venue_id))
      
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

    error = False
    form = ArtistForm()
    if form.validate_on_submit():
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebk_link']
        phone = request.form['phone']
        website_link = request.form['website_link']
        image_link = request.form['image_link']
        seeking_talent ='N'
        seeking_talent = request.form.get('seeking_talent')
        if seeking_talent == 'y':
            seeking_talent = True
        seeking_talent_statement = request.form['seeking_talent_statement']
    else:
        flash('Artist ' + request.form['name'] + ' failed due to validation error!')
        return  render_template('forms/new_artist.html', form=form)
    try:
        artist = Artist(name=name, city=city, state=state, genres=genres,
                      facebook_link=facebook_link, phone=phone, image_link=image_link,
                      seeking_talent=seeking_talent, seeking_talent_statement=seeking_talent_statement,
                      website=website_link)
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally: 
        db.session.close()
    if error:
        flash('Artist ' + request.form['name'] + ' Failed!')
        abort (400)
    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
  # on successful db insert, flash success
 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
    
    
    show_query = Show.query.all()
    data = []
    for show in show_query:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": Venue.query.filter(Venue.id == show.venue_id).first().name, 
            "artist_id": show.artist_id,
            "artist_name": Artist.query.filter(Artist.id == show.artist_id).first().name,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
            })
  
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    error = False
    try:
        start_time = request.form['start_time']
        venue_id = request.form['venue_id']
        artist_id = request.form['artist_id']
        new_shows = Show(start_time=start_time, venue_id=venue_id, artist_id=artist_id)
        db.session.add(new_shows)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally: 
        db.session.close()
    if error:
        flash('Show was unsuccessfully listed!')
        abort (400)
    else:
        flash('Show was successfully listed!')
        return render_template('pages/home.html')
        
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
