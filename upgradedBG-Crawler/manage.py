import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from base import Base
from settings import DB_CONNECTION_STRING
from subprocess import call

COMMANDS = ['cretedb', 'crawl', 'collect', 'seed']

command = sys.argv[1]

if command not in COMMANDS:
    sys.exit('{} not found'.format(command))


engine = create_engine(DB_CONNECTION_STRING)


def createdb():
    Base.metadata.create_all(engine)


def crawl():
    call(['python3', 'crawler.py'])


def collect():
    call(['python3', 'collector.py'])


def seed():
    Session = sessionmaker(bind=engine)
    session = Session()

    domain = models.Domain(url='https://register.start.bg')
    link = models.Link(url=domain.ulr, domain=domain)
    session.add(domain)
    session.add(link)
    session.commit()

f = globals()[command]
f()
