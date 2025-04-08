from sqlalchemy import Column, Integer, String, Date

from infra.base import Base


class TODOEntity(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    expire_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    user = Column(String, nullable=False)
