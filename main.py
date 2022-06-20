import asyncio
import websockets
import pymysql
from config import host, user, password, db_name



USERS = set()
useres = {}



async def addUser(websocket):
    useres[websocket] = "polzowatel"
    USERS.add(websocket)


async def removeUser(websocket):
    await asyncio.wait([user.send(str(useres[websocket]) + " left") for user in USERS])
    useres.pop(websocket)
    USERS.remove(websocket)


async def socket(websocket, path):
    await addUser(websocket)
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        while True:
            message = await websocket.recv()
            a = message[0:7]
            if useres[websocket] == "polzowatel" or useres[websocket] == "":
                useres[websocket] = message
                with connection.cursor() as cursor:
                    select_query = "SELECT * FROM `messages`;"
                    cursor.execute(select_query)
                    rows = cursor.fetchall()
                    preAns = ""
                    for row in rows:
                        preAns += row['text']
                        preAns += '\n'
                    await asyncio.wait([user.send(preAns) for user in USERS if user == websocket])

                await asyncio.wait([user.send(message + " joined the chat") for user in USERS])
                mes = message + " joined the chat"
                with connection.cursor() as cursor:
                    insert_query = f"INSERT INTO `messages` (text) VALUES ('{mes}');"
                    cursor.execute(insert_query)
                    connection.commit()
            else:
                await asyncio.wait([user.send(str(useres[websocket]) + ": " + message) for user in USERS])
                mes = str(useres[websocket]) + ": " + message
                with connection.cursor() as cursor:
                    insert_query = f"INSERT INTO `messages` (text) VALUES ('{mes}');"
                    cursor.execute(insert_query)
                    connection.commit()

    finally:
        await removeUser(websocket)
        mes = str(useres[websocket]) + " left"
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO `messages` (text) VALUES ('{mes}');"
            cursor.execute(insert_query)
            connection.commit()
        connection.close



start_server = websockets.serve(socket, 'localhost', 80)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()