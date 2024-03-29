from sqlalchemy.orm import sessionmaker
from namnak.models import NamnakDB, db_connect, create_table


class NamnakPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        namnakdb = NamnakDB()
        namnakdb.category = item['category']
        namnakdb.group = item['group']
        namnakdb.title = item['title']
        namnakdb.summary = item['summary']
        namnakdb.thumbnail = item['thumbnail']
        namnakdb.link = item['link']
        namnakdb.source = item['source']
        namnakdb.text = item['text']
        namnakdb.images = item['images']
        namnakdb.movies = item['movies']
        namnakdb.html = item['html']

        try:
            session.add(namnakdb)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item
