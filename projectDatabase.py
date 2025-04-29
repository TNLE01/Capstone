"""This file connects to the mysql database and has functions to used on the table."""

import mysql.connector

print("Connecting to the database...")
connected = False
try:
    database = mysql.connector.connect(host = "localhost", user = "root", passwd = "pass", database = "plantproject")
    connected = True
    print("Connected to the database.")
    cursor = database.cursor()
except:
    print("Error: Could not connect to the database.")
    connected = False


def addToTable(ID, name):
    """
    This function add a row to the mysql table.
    
    Parameters:
    ID (int): The ID of the list item.
    name (str): The name of the saved list item.
    """

    sql = 'INSERT INTO plantlist (tag, plant_save_name) VALUES (%s, %s)'
    val = (ID, name)
    cursor.execute(sql, val)
    database.commit()
    print(cursor.rowcount, "record inserted.")

def removeFromTable(ID):
    """
    This function removes a row to the mysql table.
    
    Parameters:
    ID (int): The ID of the row to remove.
    """
    
    cursor.execute('DELETE FROM plantlist WHERE tag = (%s)', (ID,))
    database.commit()
    print(cursor.rowcount, "record deleted.")

def addImageData(ID, img):
    """
    This function add a row to the mysql table.
    
    Parameters:
    ID (int): The ID of the list item.
    img (str): The file to add to the corresponding ID.
    """

    sql = 'UPDATE plantlist SET plant_image = (%s) WHERE tag = (%s)'
    val = (img, ID)
    cursor.execute(sql, val)
    database.commit()
    print(cursor.rowcount, "record updated.")

def isEmpty():
    """
    This function see if the mysql table is empty.

    Returns:
    bool: True if the table is empty, False otherwise.
    """

    cursor.execute('SELECT COUNT(*) FROM plantlist')
    result = cursor.fetchone() 
    if result[0] == 0:
        return True
    else:
        return False

def rowCount():
    """
    This function counts the number of rows on the table.

    Returns:
    int: The number of rows in the table.
    """

    cursor.execute('SELECT COUNT(*) FROM plantlist')
    result = cursor.fetchone() 
    return result[0]
