__author__ = 'Mr.Bool'
import configparser
import hashlib
import sys
config=configparser.ConfigParser()
config.read(u'accounts.cfg')
m_passs=[]
l_sections=[]
for section in config.sections():
    m=hashlib.md5()
    m2=hashlib.md5()
    l_sections.append(section)
    password=config.get(section,'Password')
    m.update(password.encode('utf-8'))
    print('第一次加密',m.hexdigest())
    m2.update(m.hexdigest().encode('utf-8'))
    m_passs.append(m2.hexdigest())
    print(m2.hexdigest())

for i in range(len(section)):
    config.set(l_sections[i],'Password',m_passs[i])
config.write(open(u'accounts.cfg','w'))