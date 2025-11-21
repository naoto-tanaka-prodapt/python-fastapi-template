from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class JobBoard(Base):
  __tablename__ = 'job_boards'
  id = Column(Integer, primary_key=True)
  slug = Column(String, nullable=False, unique=True)

  job_post = relationship("JobPost")


class JobPost(Base):
  __tablename__ = 'job_posts'
  id = Column(Integer, primary_key=True)
  job_board_id = Column(Integer, ForeignKey('job_boards.id'))
  title = Column(String, nullable=False)
  description = Column(String, nullable=False)

  job_board = relationship("JobBoard")