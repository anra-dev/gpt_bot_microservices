from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings


# создаем базу данных
engine = create_engine(settings.DATABASE, echo=True)

# создаем сессию
Session = sessionmaker(bind=engine)
session = Session()
