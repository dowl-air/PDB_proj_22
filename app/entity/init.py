
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session

MYSQL_DEFAULT_PORT = 3306

def sql_init(base, host: str = 'localhost', port: int = MYSQL_DEFAULT_PORT, username: str = 'pdb', password: str = 'pdb', echo: bool = False) -> Session:
	engine = sa.create_engine('mysql+mysqlconnector://%s:%s@%s:%d/pdb' % (username, password, host, port), echo=echo)
	Session = sessionmaker(engine)
	session = Session()

	base.metadata.create_all(engine) # create tables

	return session
