# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password_hash = Column(String(64))
    picture = Column(String)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'picture': self.picture
        }

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, app, expiration=600):
        serializer = Serializer(app.secret_key, expires_in=expiration)
        return serializer.dumps({'id': self.id})


class Proposal(Base):
    __tablename__ = 'proposal'
    id = Column(Integer, primary_key=True)
    filled = Column(String)

    request_id = Column(Integer, ForeignKey('request.id'))
    request = relationship("Request")
    user_proposed_from_id = Column(Integer, ForeignKey('user.id'))
    user_proposed_from = relationship("User", primaryjoin = "Proposal.user_proposed_from_id == User.id")
    user_proposed_to_id = Column(Integer, ForeignKey('user.id'))
    user_proposed_to = relationship("User", primaryjoin = "Proposal.user_proposed_to_id == User.id")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'filled': self.filled,
            'request_id': self.request_id,
            'user_proposed_from_id': self.user_proposed_from_id,
            'user_proposed_to_id': self.user_proposed_to_id
        }


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")
    meal_type = Column(String)
    location_string = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    meal_time = Column(String)
    filled = Column(String)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meal_type': self.meal_type,
            'location_string': self.location_string,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'meal_time': self.meal_time,
            'filled': self.filled
        }


class MealDate(Base):
    __tablename__ = 'meal_date'
    id = Column(Integer, primary_key=True)
    restaurant_name = Column(String)
    restaurant_address = Column(String)
    restaurant_picture = Column(String)
    meal_time = Column(String)

    user_1_id = Column(Integer, ForeignKey('user.id'))
    user_1 = relationship("User", primaryjoin = "MealDate.user_1_id == User.id")

    user_2_id = Column(Integer, ForeignKey('user.id'))
    user_2 = relationship("User", primaryjoin = "MealDate.user_2_id == User.id")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'restaurant_name': self.restaurant_name,
            'restaurant_address': self.restaurant_address,
            'restaurant_picture': self.restaurant_picture,
            'meal_time': self.meal_time,
            'user_1_id': self.user_1_id,
            'user_2_id': self.user_2_id
        }


engine = create_engine('sqlite:///meet-n-eat.db')

Base.metadata.create_all(engine)
