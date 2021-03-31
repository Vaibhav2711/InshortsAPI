import bcrypt
from passlib.context import CryptContext
passwd = 's$cret12'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#hashed_password = pwd_context.hash(passwd)
#salt = bcrypt.gensalt()
#hashed = bcrypt.hashpw(passwd, salt)

#print(salt)
#print(hashed_password)


if pwd_context.verify(passwd, '$2b$12$ReSuxdD7UzdPqExBEQrcl.LzNR2rftboqlKFwFPoL.eSEo1NED2AW'):
    print("match")
else:
    print("does not match")

