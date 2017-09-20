from Database import Database
import os, shutil

database = Database('revertfile.db')

revert_list = database.read_from_table('revert_table')


for reversion in revert_list:
    source = reversion[1]
    destination = reversion[0]

    try:
        shutil.move(source,destination)
    except Exception as e:
        print("Error moving files: " + str(e))
