

import threading

from sqlalchemy import (
    Column, 
    String, 
    BigInteger
)

from . import SESSION, BASE




# save user ids in whitelists
class PMTABLE(BASE):
    __tablename__ = "approve"

    user_id = Column(BigInteger, primary_key=True)
    username = Column(String)

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = str(username) 




# save warn msg ids
class MSGID(BASE):
    __tablename__ = "pm msg id"

    user_id = Column(BigInteger, primary_key=True)
    msg_id = Column(BigInteger)

    def __init__(self, user_id, msg_id):
        self.user_id = user_id
        self.msg_id = msg_id




# save warn counts
class DISAPPROVE(BASE):
    __tablename__ = "disapprove"

    user_id = Column(BigInteger, primary_key=True)
    warn_count = Column(String)

    def __init__(self, user_id, warn_count):
        self.user_id = user_id
        self.warn_count = str(warn_count) 




PMTABLE.__table__.create(checkfirst=True)
MSGID.__table__.create(checkfirst=True)
DISAPPROVE.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




class PMPERMITSQL(object):
    # add message id of a user
    def set_msgid(self, user_id, msg_id):
        with INSERTION_LOCK:
            try:
                user = SESSION.query(MSGID).get(user_id)
                if not user:
                    user = MSGID(user_id, msg_id)
                else:
                    user.msg_id = msg_id
                SESSION.merge(user)
                SESSION.commit()
            finally:
                SESSION.close()

    # get warn message id
    def get_msgid(self, user_id):
        try:
            user = SESSION.query(MSGID).get(user_id)
            msg_id = None
            if user:
                msg_id = user.msg_id
                return msg_id
        finally:
            SESSION.close()


    # add user id to whitelist 
    def set_whitelist(self, user_id, username):
        with INSERTION_LOCK:
            user = SESSION.query(PMTABLE).get(user_id)
            try:
                if not user:
                    user = PMTABLE(user_id, username)
                else:
                    user.username = str(username)
                SESSION.add(user)
                SESSION.commit()
            finally:
                SESSION.close()
        return user_id


    # remove user id from whitelist
    def del_whitelist(self, user_id):
        with INSERTION_LOCK:
            user = SESSION.query(PMTABLE).get(user_id)
            try:
                if user:
                    SESSION.delete(user)
                    SESSION.commit()
            finally:
                SESSION.close()
            return False


    # get whitelist (approved)
    def get_whitelist(self, user_id):
        user = SESSION.query(PMTABLE).get(user_id)
        rep = ""
        if user:
            rep = user.username
        SESSION.close()
        return rep


    # warn table func
    def set_warn(self, user_id, warn_count):
        with INSERTION_LOCK:
            try:
                user = SESSION.query(DISAPPROVE).get(user_id)
                if not user:
                    user = DISAPPROVE(user_id, warn_count)
                else:
                    user.warn_count = warn_count
                SESSION.merge(user)
                SESSION.commit()
            finally:
                SESSION.close()


    # get warn func
    def get_warn(self, user_id):
        user = SESSION.query(DISAPPROVE).get(user_id)
        rep = ""
        if user:
            rep = user.warn_count
        SESSION.close()
        return rep


    # del warn func
    def del_warn(self, user_id):
        with INSERTION_LOCK:
            user = SESSION.query(DISAPPROVE).get(user_id)
            try:
                if user:
                    SESSION.delete(user)
                    SESSION.commit()
            finally:
                SESSION.close()
            return False
