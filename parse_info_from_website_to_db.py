import requests
from bs4 import BeautifulSoup as bs
import re
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

answer = requests.get('https://www.codewars.com/users/leaderboard')
q = bs(answer.text, 'html.parser')
usr_pattern = re.compile('data-username="[a-zA-Z0-9 _.-]+"')
honor_pattern = re.compile('\d+,\d+')

q1 = q.find_all('tr')


users_lst = []
for i in q1:
    tmp = []
    user_name = re.findall(usr_pattern, str(i))
    user_honor = re.findall(honor_pattern, str(i))
    tmp.append(''.join(user_name).strip('data-username="'))
    tmp.append(re.sub(',','.',''.join(user_honor)))
    users_lst.append(tmp)



#users_lst = [['g964', '352.235'],['test', '333.455']]
engine = sa.create_engine('postgresql://postgres:pswd_123@192.168.1.5:5432/postgres')

print(f' user: {users_lst}')

base = declarative_base()

class Codewars_users(base):
    __tablename__ = 'codewars_users'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String)
    honor = sa.Column(sa.Float)

    def __repr__(self):
        return f'codewars_users name={self.username},honor={self.honor} '


base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()
add_rows = []
for i in users_lst:
        if i[0] and i[1]:
            user_value = i[0]
            honor_value = float(i[1])
            add_rows.append(Codewars_users(username=user_value, honor=honor_value))
        if not i[0] or not i[1]:
            continue
# print(add_rows)
session.add_all(add_rows)
session.commit()