from hr import DBUtility, DataLayerError
try:
    db_config = DBUtility.getDBConfiguration()
    print(db_config)
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
