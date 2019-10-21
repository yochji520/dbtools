#-*-coding:utf-8-*-
import  MySQLdb
import sys
import os
import json
"""
con = MySQLdb.connect( host='192.168.118.118',user='ycj',passwd='123123',db='t1',port=3306,charset='utf8')
cur = con.cursor()
cur.execute("select count(*) from t1.t1")
a = cur.fetchone()
"""

reload(sys);
sys.setdefaultencoding("utf8")


yaml_path = os.path.join("../conf","usermanager.yaml")
f = open(yaml_path,'r')
s = f.read()
print s
x = json.loads(s,encoding='utf-8')
print x
