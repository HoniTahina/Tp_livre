import oracledb

_un = "SYSTEM"
_cs = "localhost/XEPDB1"
_pw = 'tporacle12345'
_connection = None


def db():
    global _pw, _connection

    if _connection:
        return _connection

    _connection = oracledb.connect(user=_un, password=_pw, dsn=_cs)
    return _connection


