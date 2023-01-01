import asyncio
import logging
import os

from grpc import aio

from microservices_example.types_pb2 import UserId, User
from microservices_example.users.users_pb2_grpc import UsersServicer, add_UsersServicer_to_server


class Users(UsersServicer):
    def __init__(self):
        self.database = list()

    async def AddUser(self, request: User, context: aio.ServicerContext) -> UserId:
        next_id = len(self.database)
        self.database.append(request)
        return UserId(id=next_id)

    async def GetUser(self, request: UserId, context: aio.ServicerContext) -> User:
        return self.database[request.id]


async def serve() -> None:
    server = aio.server()
    add_UsersServicer_to_server(Users(), server)
    unix_socket_path = os.getcwd() + "/microservices.sock"
    listen_addr = f"unix://{unix_socket_path}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


def run():
    asyncio.run(serve())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
