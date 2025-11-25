from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class JobBoard(Base):
  __tablename__ = 'job_boards'
  id = Column(Integer, primary_key=True)
  slug = Column(String, nullable=False, unique=True)
  logo_path = Column(String, nullable=True)

  job_post = relationship("JobPost")


class JobPost(Base):
  __tablename__ = 'job_posts'
  id = Column(Integer, primary_key=True)
  job_board_id = Column(Integer, ForeignKey('job_boards.id'))
  title = Column(String, nullable=False)
  description = Column(String, nullable=False)
  is_open = Column(Boolean, nullable=True, default=True)

  job_board = relationship("JobBoard")
  job_application = relationship("JobApplication")


class JobApplication(Base):
  __tablename__ = 'job_applications'
  id = Column(Integer, primary_key=True)
  job_post_id = Column(Integer, ForeignKey('job_posts.id'))
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  email = Column(String, nullable=False)
  resume_path = Column(String, nullable=True)

  job_post = relationship("JobPost")