import asyncio

import cowsay

clients: dict[str, asyncio.Queue] = {}

commands = [
    "who",
    "cows",
    "login",
    "say",
    "yield",
    "quit",
]

addr_to_client = {}


async def chat(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    message = asyncio.create_task(reader.readline())
    receive = None
    writer.write(
        f"msg: Hello, it is cow chat. Command list: {' '.join(commands)}\n".encode()
    )
    await writer.drain()
    while not reader.at_eof():
        wait_for = [message]
        if receive is not None:
            wait_for.append(receive)
        done, _ = await asyncio.wait(wait_for, return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is receive:
                receive = asyncio.create_task(clients[addr_to_client[me]].get())
                writer.write(
                    (
                        "msg: "
                        + cowsay.cowsay(f"{q.result()}\n", cow=addr_to_client[me])
                        + "\n"
                    ).encode()
                )
                await writer.drain()
                continue

            message = asyncio.create_task(reader.readline())
            command, *args = q.result().decode().strip().split(maxsplit=2)
            if command not in commands:
                writer.write("msg: Unknown command, please try again\n".encode())
                await writer.drain()
                continue

            match command:
                case "who":
                    writer.write((f"{command} " + " ".join(clients) + "\n").encode())
                    await writer.drain()

                case "cows":
                    available_cows = set(cowsay.list_cows()) - set(clients)
                    writer.write(
                        (f"{command} " + " ".join(available_cows) + "\n").encode()
                    )
                    await writer.drain()

                case "login":
                    if me in addr_to_client:
                        writer.write("msg: You have already logged in\n".encode())
                        await writer.drain()
                        continue
                    if len(args) == 0:
                        writer.write("msg: You have to specify cow name\n".encode())
                        await writer.drain()
                        continue
                    cow_name = args[0]
                    if cow_name in clients:
                        writer.write(
                            "msg: User with this cow name already exists. Use other cow name\n".encode()
                        )
                        await writer.drain()
                        continue
                    if cow_name not in cowsay.list_cows():
                        writer.write(
                            "msg: Unknown cow name, try one of available\n".encode()
                        )
                        await writer.drain()
                        continue
                    clients[cow_name] = asyncio.Queue()
                    addr_to_client[me] = cow_name
                    receive = asyncio.create_task(clients[addr_to_client[me]].get())
                    writer.write(
                        f"{command} Successful log in, welcome to chat\n".encode()
                    )
                    await writer.drain()

                case "say":
                    if me not in addr_to_client:
                        writer.write(
                            "msg: Login is required for this command\n".encode()
                        )
                        await writer.drain()
                        continue
                    if len(args) != 2:
                        writer.write(
                            "msg: Invalid value of command arguments, must be 2 arguments\n".encode()
                        )
                        await writer.drain()
                        continue
                    send_to, text = args
                    if send_to not in clients:
                        writer.write(
                            f"msg: User with username {send_to} does not exist\n".encode()
                        )
                        await writer.drain()
                        continue
                    await clients[send_to].put(text)
                    writer.write(f"{command} success\n".encode())
                    await writer.drain()

                case "yield":
                    if me not in addr_to_client:
                        writer.write(
                            "msg: Login is required for this command\n".encode()
                        )
                        await writer.drain()
                        continue
                    if len(args) < 1:
                        writer.write(
                            "msg: Invalid value of command arguments, must be 1 argument\n".encode()
                        )
                        await writer.drain()
                        continue
                    text = args[0]
                    if len(args) == 2:
                        text += f" {args[1]}"
                    tasks = []
                    for client in clients:
                        if addr_to_client[me] != client:
                            tasks.append(asyncio.create_task(clients[client].put(text)))
                    await asyncio.gather(*tasks)
                    writer.write(f"{command} success\n".encode())
                    await writer.drain()

                case "quit":
                    if me in addr_to_client:
                        del clients[addr_to_client[me]]
                        del addr_to_client[me]
                    message.cancel()
                    if receive is not None:
                        receive.cancel()
                    writer.close()
                    await writer.wait_closed()
                    return
    message.cancel()
    if receive is not None:
        receive.cancel()
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
