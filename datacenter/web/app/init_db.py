# import sqlite3
#
# connection = sqlite3.connect('database.db')
#
#
# with open('../../db/objects.sql') as f:
#     connection.executescript(f.read())
#
# cur = connection.cursor()
#
# cur.execute("INSERT INTO posts (id_obj, stat, warehouse_id, deliver_id, gps, time_stamp) VALUES (?, ?)")
#
#
# connection.commit()
# connection.close()
