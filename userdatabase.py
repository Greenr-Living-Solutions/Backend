import websockets
import asyncio
from io import StringIO
import pandas as pd

print("Starting Signup Server...")


async def userdatabase(websocket, path):
    users = pd.DataFrame()
    df = pd.read_csv('users.csv')
    while 1:
        try:
            data = await websocket.recv()
            data = data.split(" ")
            if data[0] == "Login":
                print("Login attempt from " + data[1] + ", " + data[2])
                data.remove("Login")
                df = df.values
                if data in df.tolist():
                    await websocket.send("True")
                    print("Authenticating user...")
                else:
                    await websocket.send("False")
                    print("User not found. Notifying front-end...")
            else:
                data = [data]
                users = users.append(data)
                print("A new user has been added to the database")
                users.to_csv("users.csv", mode='a', header=False, index=False)
        except:
            websockets.serve("0.0.0.0", 8000,
                             ping_interval=None, ping_timeout=None)


start_server = websockets.serve(
    userdatabase, "0.0.0.0", 8000, ping_interval=None, ping_timeout=None)

asyncio.get_event_loop().run_until_complete(start_server)
if asyncio.get_event_loop().is_closed():
    asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
