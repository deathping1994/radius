import MySQLdb
import os
from hashlib import md5
import json
import redis
import datetime
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get('DB_USER', 'radius')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'radius')
DB_NAME = os.environ.get('DB_NAME', 'radius')


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)

class DBHelper(object):
      """docstring for DBHelper"""
      db = MySQLdb.connect(host= DB_HOST,
                  user=DB_USER,
                  passwd=DB_PASSWORD,
                  db=DB_NAME)
      redis = redis.StrictRedis(host='localhost', port=6379, db=0)

      @classmethod
      def get_db(cls):
            if not cls.db:
                  cls.db = MySQLdb.connect(host=DB_HOST,
                        user=DB_USER,
                        passwd=DB_PASSWORD,
                        db=DB_NAME)
                  return cls.db
            return cls.db
      @classmethod
      def execute_query(cls,db_cursor, sql):
	    print sql
            cached_result = cls._get_result_from_cache(sql)
            if cached_result:
                  return json.loads(cached_result)
            db_cursor.execute(sql)
            results = cls.get_results(db_cursor)
            cls._set_result_in_cache(sql,results)
	    return results
      @classmethod
      def _get_result_from_cache(cls, sql):
            sql_hash = md5(sql).hexdigest()
            cached_result = cls.redis.get(sql_hash)
            return cached_result
      @classmethod
      def _set_result_in_cache(cls, sql, matches):
            sql_hash = md5(sql).hexdigest()
            cls.redis.set(sql_hash,json.dumps(matches, default=lambda o: o.isoformat() if hasattr(o, 'isoformat') else o),300)
      @classmethod
      def get_results(cls, db_cursor):
            desc = [d[0] for d in db_cursor.description]
            results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
            return results

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__