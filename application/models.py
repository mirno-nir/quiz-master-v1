from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy import Integer, String, ForeignKey, DateTime
from .database import db

class User(db.Model):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    qualification: Mapped[Optional[str]] = mapped_column(String)
    dob: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String, default='general')
    user_score: Mapped[List['Scores']] = relationship(back_populates='user', cascade='all, delete-orphan')

class Subject(db.Model):
    __tablename__ = 'subject'
    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_name: Mapped[str] = mapped_column(String, unique=True)
    subject_description: Mapped[Optional[str]] = mapped_column(String)
    chapters: Mapped[List['Chapter']] = relationship(back_populates='subject', cascade='all, delete-orphan')

class Chapter(db.Model):
    __tablename__ = 'chapter'
    chapter_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey(Subject.subject_id))
    chapter_name: Mapped[str] = mapped_column(String, unique=True)
    chapter_description: Mapped[Optional[str]] = mapped_column(String)
    subject: Mapped['Subject'] = relationship(back_populates='chapters')
    quiz: Mapped[List['Quiz']] = relationship(back_populates='chapter', cascade='all, delete-orphan')
    questions_chapter: Mapped[List['Question']] = relationship(back_populates='chapter_question', cascade='all, delete-orphan')

class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chapter_id: Mapped[int] = mapped_column(Integer, ForeignKey(Chapter.chapter_id))
    quiz_date: Mapped[str] = mapped_column(String)
    quiz_time_duration: Mapped[int] = mapped_column(Integer)
    quiz_remarks: Mapped[Optional[str]] = mapped_column(String)
    chapter: Mapped['Chapter'] = relationship(back_populates='quiz')
    questions: Mapped[List['Question']] = relationship(back_populates='quizes', cascade='all, delete-orphan')
    scores: Mapped[List['Scores']] = relationship(back_populates='quiz_score', cascade='all, delete-orphan')

class Question(db.Model):
    __tablename__ = 'question'
    question_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey(Quiz.quiz_id))
    chapter_id: Mapped[int] = mapped_column(Integer, ForeignKey(Chapter.chapter_id))
    question_title: Mapped[str] = mapped_column(String)
    question_statement: Mapped[str] = mapped_column(String)
    correct_option: Mapped[str] = mapped_column(String)
    option_1: Mapped[str] = mapped_column(String)
    option_2: Mapped[str] = mapped_column(String)
    option_3: Mapped[str] = mapped_column(String)
    option_4: Mapped[str] = mapped_column(String)
    quizes: Mapped['Quiz'] = relationship(back_populates='questions')
    chapter_question: Mapped['Chapter'] = relationship(back_populates='questions_chapter')

class Scores(db.Model):
    __tablename__ = 'scores'
    score_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey(Quiz.quiz_id))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.user_id))
    time_stamp_of_attempt: Mapped[str] = mapped_column(DateTime)
    quiz_time_duration: Mapped[int] = mapped_column(Integer)
    total_score: Mapped[int] = mapped_column(Integer)
    quiz_score: Mapped['Quiz'] = relationship(back_populates='scores')
    user: Mapped['User'] = relationship(back_populates='user_score')

