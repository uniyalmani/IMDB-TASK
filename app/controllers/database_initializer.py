from sqlmodel import Session, create_engine, SQLModel
# from app.models import database_model
import os

# print("yes")

env = os.environ

URL = env.get("URL")

# URL = "mysql://fynd_acad:fynd123@mysql_db:3306/fynd_acad" 
# URL = "postgresql://yzdjobfynqbkrz:988db33fbc8223f7cb05c2ddbf9b98cb015c3fbf1db67a1c0c4842666a91cb9a@ec2-54-160-109-68.compute-1.amazonaws.com:5432/d4p8p034hhe96o"

engine = create_engine(URL)

SQLModel.metadata.create_all(engine)