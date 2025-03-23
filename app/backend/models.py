from datetime import datetime, timezone
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.inspection import inspect
from sqlalchemy import DECIMAL

from api.clients.maps.routes_request import Coords


def get_uuid():
    return uuid4().hex


db = SQLAlchemy()


class Pub(db.Model):
    __tablename__ = "pubs"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)

    def get_as_dict(self):
        return {"id": self.id, "type": "pub", "attributes": {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != "id"}}


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    suggested_pub_id = db.Column(db.String(32), db.ForeignKey("pubs.id"))

    suggested_pub = db.relationship("Pub", backref="groups")

    def get_as_dict(self):
        return {
            "id": self.id,
            "type": "group",
            "attributes": {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != "id"},
        }


class UserGroupQuery(db.Model):
    __tablename__ = "userGroupQuery"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.String(32), db.ForeignKey("groups.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("usergroupquery", lazy=True))
    group = db.relationship("Group", backref=db.backref("usergroupquery", lazy=True))

    def get_as_dict(self):
        return {
            "id": self.id,
            "type": "userGroupQuery",
            "attributes": {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != "id"},
        }


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    address = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    second_name = db.Column(db.String(150), nullable=False)

    def get_as_dict(self):
        return {
            "id": self.id,
            "type": "user",
            "attributes": {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != "id"},
        }

class Location(db.Model):
    __tablename__ = 'locations'
    __table_args__ = (
        UniqueConstraint('name', 'lat', 'lng', name='uq_location_name_coords'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    lat = db.Column(db.DECIMAL(11, 8), nullable=False)
    lng = db.Column(db.DECIMAL(11, 8), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # Relationship to distances where this location is either origin or destination
    distances_as_origin = db.relationship('Distance', 
                                        foreign_keys='Distance.origin_id',
                                        backref='origin',
                                        cascade='all, delete-orphan')
    
    distances_as_destination = db.relationship('Distance',
                                             foreign_keys='Distance.destination_id',
                                             backref='destination',
                                             cascade='all, delete-orphan')

    @property
    def coords(self):
        return Coords(float(self.lat), float(self.lng))

    def __repr__(self):
        return f'<Location {self.name} ({self.lat}, {self.lng})>'
    
    @classmethod
    def get_or_create(cls, name, lat, lng, commit=False):
        """
        Get or create a location with thread-safe creation
        Args:
            commit: Whether to immediately commit the transaction
        """
        # Use no_autoflush to prevent premature INSERT
        with db.session.no_autoflush:
            existing = cls.query.filter(
                db.func.lower(cls.name) == name.lower(),
                cls.lat == round(lat, 8),
                cls.lng == round(lng, 8)
            ).first()

            if existing:
                return existing, False  # Return old record, False for not created
            
            # Create new location
            new_location = cls(
                name=name,
                lat=round(lat, 8),
                lng=round(lng, 8),
            )
            db.session.add(new_location)

            if commit:
                try:
                    db.session.commit()
                except db.IntegrityError:
                    db.session.rollback()
                    raise
            
            return new_location, True # Return new record, True for created
    



class Distance(db.Model):
    __tablename__ = 'distances'
    
    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    meters = db.Column(db.Integer)  # Distance in meters
    seconds = db.Column(db.Integer)  # Duration in seconds
    calculated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # Composite unique constraint to prevent duplicate entries
    __table_args__ = (
        UniqueConstraint('origin_id', 'destination_id', name='uq_origin_destination'),
        db.Index('idx_origin', 'origin_id'),
        db.Index('idx_destination', 'destination_id'),
    )

    def __repr__(self):
        return f'<Distance {self.origin_id}->{self.destination_id}: {self.seconds}s>'

    @classmethod
    def get_or_create(cls, origin:Location, destination:Location):
        """Get existing distance or create a new entry if none exists"""
        
        existing = cls.query.filter_by(
            origin_id=origin.id,
            destination_id=destination.id
        ).first()

        if existing:
            return existing, False
        
        new_distance = cls(origin_id=origin.id, destination_id=destination.id)
        db.session.add(new_distance)

        return new_distance, True
        
    def update_distance(self, meters, seconds):
        """Update distance metrics and timestamp"""
        self.meters = meters
        self.seconds = seconds
        self.calculated_at = datetime.now(timezone.utc)

class BayesianEmulation(db.Model):
    __tablename__ = "bayesian_emulation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    m_length = db.Column(db.Integer, nullable=False)
    d_length = db.Column(db.Integer, nullable=False)
    beta = db.Column(DECIMAL(precision=30, scale=15), nullable=False)
    sigma = db.Column(DECIMAL(precision=30, scale=15), nullable=False)
    theta = db.Column(DECIMAL(precision=30, scale=15), nullable=False)
    
class MVectorElement(db.Model):
    __tablename__ = "m_vector_elements"
    id = db.Column(db.Integer, primary_key=True)
    bayesian_emulation_id = db.Column(db.Integer, db.ForeignKey("bayesian_emulation.id"), nullable=False)
    index = db.Column(db.Integer, nullable=False)  # Row index (0-based)
    value = db.Column(DECIMAL(precision=30, scale=15), nullable=False)  # Value of the cell

    m_vector = db.relationship("BayesianEmulation", backref=db.backref("m_vector_elements", lazy=True))

    # Ensure that each element in a mVector is unique
    __table_args__ = (
        UniqueConstraint('bayesian_emulation_id', 'index', name='uq_m_vector_element'),
    ) 

class XTrainElements(db.Model):
    __tablename__ = "x_train_elements"
    id = db.Column(db.Integer, primary_key=True)
    bayesian_emulation_id = db.Column(db.Integer, db.ForeignKey("bayesian_emulation.id"), nullable=False)
    index = db.Column(db.Integer, nullable=False)  # Row index (0-based)
    value = db.Column(DECIMAL(precision=30, scale=15), nullable=False)  # Value of the cell

    m_vector = db.relationship("BayesianEmulation", backref=db.backref("x_train_elements", lazy=True))

    # Ensure that each element in a xTrain is unique
    __table_args__ = (
        UniqueConstraint('bayesian_emulation_id', 'index', name='uq_x_train_element'),
    )

class DElements(db.Model):
    __tablename__ = "d_elements"
    id = db.Column(db.Integer, primary_key=True)
    bayesian_emulation_id = db.Column(db.Integer, db.ForeignKey("bayesian_emulation.id"), nullable=False)
    index = db.Column(db.Integer, nullable=False)  # Row index (0-based)
    value = db.Column(DECIMAL(precision=30, scale=15), nullable=False)  # Value of the cell

    m_vector = db.relationship("BayesianEmulation", backref=db.backref("d_elements", lazy=True))

    # Ensure that each element in a D is unique
    __table_args__ = (
        UniqueConstraint('bayesian_emulation_id', 'index', name='uq_x_train_element'),
    )