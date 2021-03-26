import sys
from pulzarutils.constants import Constants
from pulzarcore.core_rdb import RDB

def update_schema(schema_type):
    """Compare version and run the update
    """
    db_path = Constants.DB_JOBS if schema_type == 'master' else Constants.DB_NODE_JOBS
    rdb = RDB(db_path)  
    current_version = Constants.VERSION
    result = rdb.execute_sql_with_results('SELECT version, sqlcmd FROM metadata ORDER BY id DESC LIMIT 1')
    if len(result) != 1:
        raise ('Metadata should have len=1')
    sql = result[0][1]
    db_version = result[0][0]
    db_version_split = db_version.split('.')
    version_split = current_version.split('.')
    current_build_number = int(version_split[0]) + int(version_split[1]) + int(version_split[2])
    db_build_number = int(db_version_split[0]) + int(db_version_split[1]) + int(db_version_split[2])

    if current_build_number > db_build_number and sql is not None:
        # Run updates in the database if is needed.
        rdb.execute_sql(sql)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2 and isinstance(args[1], str):
        update_schema(args[1])
    raise ('Argument error')





