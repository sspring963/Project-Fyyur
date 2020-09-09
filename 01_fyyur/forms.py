from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length, Regexp, Optional

class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[DataRequired(message="Please include artist id.") ]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired(message="Please include venue id.")] 
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(message="Please include start time.") ],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', 
        validators=[DataRequired(), Length(max=120, message="Input is too long.")]
    )
    city = StringField(
        'city', 
        validators=[DataRequired(), Length(max=120, message="Input is too long.")]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', 
        validators=[DataRequired()]
    )
    phone = StringField(
        'phone', 
        [DataRequired(), 
        Regexp(r'^\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}$', 
               message="Invalid phone number. Please use xxx-xxx-xxx format.")]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL( message="URL Required")]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
             ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    seeking_talent = BooleanField(
        'seeking_talent', validators=[Optional()])
    seeking_talent_statement = StringField(
        'seeking_talent_statement', validators=[Optional()])
    website_link = StringField(
        'website_link', validators=[Optional(), URL(message="URL Required")])
    facebk_link = StringField(
        'facebook_link', validators=[Optional(), URL(message="URL Required")])
    

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired(), Length(max=120, message="Input is too long.")]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(max=120, message="Input is too long.")]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone', validators=[
            DataRequired(), Regexp(r'^\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}$', 
            message="Invalid phone number. Please use xxx-xxx-xxx format.")]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL(message="URL Required")]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebk_link = StringField(
        'facebook_link', validators=[Optional(), URL(message="URL Required")]
    )
    seeking_talent = BooleanField(
        'seeking_talent', validators=[Optional()])
    seeking_talent_statement = StringField(
        'seeking_talent_statement', validators=[Optional()] )
    website_link = StringField(
        'website_link', validators=[Optional(), URL(message="URL Required")])

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
