from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, false, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from database import engine
from enums import ModelGPTEnumForBD
from settings import DEFAULT_MODEL

# создаем Base класс
Base = declarative_base()


# создаем модель данных
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    contexts = relationship("Context", back_populates="user")
    is_admin = Column(Boolean, nullable=False, server_default=false())
    model = Column(SQLAlchemyEnum(ModelGPTEnumForBD), default=DEFAULT_MODEL)


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    question = Column(String)
    answer = Column(String)
    is_active = Column(Boolean)
    context_id = Column(Integer, ForeignKey('context.id'))
    context = relationship("Context", back_populates="messages")


class Context(Base):
    __tablename__ = 'context'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    system_role = Column(String)
    is_active = Column(Boolean)
    # name = Column(String)
    # is_deleted = Column(Boolean, nullable=False, server_default=false())
    user = relationship("User", back_populates="contexts")
    messages = relationship("Message", back_populates="context")


if __name__ == '__main__':
    # создаем таблицы в базе данных
    Base.metadata.create_all(engine)
