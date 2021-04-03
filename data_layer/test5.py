from hr import DataLayerError, DBConnection
try:
    connection = DBConnection.getConnection()
    print("Connected to Database")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
finally:
    try:
        if connection.is_connected():
            connection.close()
    except:
        pass
