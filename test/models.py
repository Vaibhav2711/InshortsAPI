from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
#from sqlalchemy.orm import relationship


from .database import Base




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique = True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    tries = Column(Integer)
    access_token = Column(String, default=" ")
    access_token_type = Column(String,default = " ")
    business_account = Column(String,default = "No")
    company_name = Column(String,default = "")

    #items = relationship("Item", back_populates="owner")



#class Item(Base):

 #   __tablename__ = "items"


  #  id = Column(Integer, primary_key=True, index=True)
  #  title = Column(String, index=True)
  #  description = Column(String, index=True)
  #  owner_id = Column(Integer, ForeignKey("users.id"))

  #  owner = relationship("User", back_populates="items")

