import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from base import Base
from models import Server


engine = create_engine("sqlite:///servers.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('servers_histogram.json', 'r') as f:
    data = json.load(f)

end_histogram = {}
for pl in data.values():
    end_histogram[pl] = list(data.values()).count(pl)

servers = [Server(platform=key, quantity=end_histogram[key])
           for key in end_histogram]

session.add_all(servers)
session.commit()


with open('end_servers_histogram.json', 'w') as ff:
    json.dump(end_histogram, f, ensure_ascii=False)
