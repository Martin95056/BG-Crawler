import tldextract
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from models import Link, Domain
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from settings import DB_CONNECTION_STRING
from datetime import datetime
import time


engine = create_engine(DB_CONNECTION_STRING)
Session = sessionmaker(bind=engine)
session = Session()


def is_url(url):
    return tldextract.extract(url).registered_domain != ''


def save(obj):
    session.add(obj)
    session.commit()


def main():
    unvisited_links = session.query(Link).\
                        filter(Link.visited_at == None).all()

    if len(unvisited_links) == 0:
        print("Nothing to visit right now.")

    for link in unvisited_links:
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'html.parser')

            for site_url in set([o.get('href') for o in soup.find_all('a')]):
                if site_url is None:
                    continue

                url = site_url

                if not is_url(site_url):
                    url = urljoin(link.get_domain(), site_url)

                print('Found: {}'.format(url))

                l = session.query(Link).\
                        filter(Link.url == url).first()

                if l is not None:
                    continue

                l = Link(url=url)
                domain = l.get_domain()

                domain_in_db = session.query(Domain).\
                                        filter(Domain.url == domain).\
                                        first()

                if domain_in_db in None:
                    print("Found new domain: {}".format(domain))
                    domain_in_db = Domain(url=domain)
                    save(domain_in_db)

                l.domain = domain_in_db
                save(l)

        except:
            print('Something went wrong.')
        finally:
            link.visited_at = datetime.now()
            save(link)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(1)
