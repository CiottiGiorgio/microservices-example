import asyncio
import multiprocessing
import os
import time
import timeit
from time import sleep

import grpc.aio

from microservices_example.users import service, users_pb2_grpc
from microservices_example.types_pb2 import UserId, User


async def run():
    unix_socket_path = os.getcwd() + "/microservices.sock"
    async with grpc.aio.insecure_channel(f"unix://{unix_socket_path}") as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        await asyncio.gather(
            stub.AddUser(User(name="Marco")),
            stub.AddUser(User(name="Antonio"))
        )
        user1, user2 = await asyncio.gather(
            stub.GetUser(UserId(id=0)),
            stub.GetUser(UserId(id=1)),
        )
        # await stub.AddUser(User(name="Marco"))
        # await stub.AddUser(User(name="Antonio"))
        # user1 = await stub.GetUser(UserId(id=0))
        # user2 = await stub.GetUser(UserId(id=1))
        print(user1)
        print(user2)


if __name__ == '__main__':
    users_subprocess = multiprocessing.Process(target=service.run)
    users_subprocess.start()

    sleep(0.25)
    start = time.time()
    asyncio.run(run())
    end = time.time()
    print(end - start)

    users_subprocess.kill()
