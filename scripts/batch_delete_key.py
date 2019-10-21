#-*- coding: utf-8 -*-
import sys;
reload(sys);
sys.setdefaultencoding("utf8")
import redis




redis_conn = redis.Redis(host='192.168.118.188', port=6379, db=0)
redis_conn.delete(*redis_conn.keys(pattern='*test*'))






