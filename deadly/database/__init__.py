from .postgres.afk_sql import AFKSQL
from .postgres.notes_sql import NOTESSQL
from .postgres.pmpermit_sql import PMPERMITSQL
from .postgres.dv_sql import DVSQL
from .postgres.welcome_sql import WELCOMESQL



class Database(
    AFKSQL,
    NOTESSQL,
    PMPERMITSQL,
    DVSQL,
    WELCOMESQL
    ):
    pass
