import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine, Table, Column, select, ForeignKey, Integer, String, Float,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker,scoped_session, query
from flask_login import UserMixin

metadata = MetaData()

engine = create_engine('sqlite:///FantasyLeagueOfIreland.db', echo=False)  # echo=False
Base = declarative_base()
session = sessionmaker(bind=engine, autoflush=False)()

class User(Base, UserMixin):
     __tablename__ = "User"
     id = Column(Integer, primary_key=True)
     email = Column(String)
     password = Column(String)

     def checkEmail(self):
         check = session.query(User).filter(User.email == self.email)
         users = []
         for row in check:
             users.append(row)
         return users

    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def get_id(self):
    #     return self.id
    #
    # def is_anonymous(self):
    #      """False, as anonymous users aren't supported."""
    #      return False
    #
    #  def addUser(self):
    #      session.add(self)
    #      session.commit()
    #      session.close()

    #
    #  def getUser(self):
    #      check = session.query(User).filter(and_(User.email==self.email,User.password==self.password))
    #      users = []
    #      for row in check:
    #          users.append(row)
    #      return users
    #
    #  def returnUser(self):
    #      user = User.query(User).filter(and_(User.email==self.email,User.password==self.password))
    #      return user
    #

User.metadata.create_all(engine)




#Query Users script
#users = session.query(User).filter(User.email=='ianol@amazon.com')
#for row in users:
#    print (row.email,row.password)




#ed_user = User(email="bruce@hotmail.com", password="BrueC")
#check = ed_user.getUser()
#km=[]
#for row in check:
#    km.append(row)
#print (len(km))


#for row in check:
#    print (row.id, row.email,row.password)




#session.add(ed_user)
#session.commit()
#session.close()
