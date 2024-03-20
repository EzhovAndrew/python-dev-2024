import cmd
import readline
import shlex
import socket
import threading
from time import sleep


class CowClient(cmd.Cmd):
    intro = "Welcome to the cow chat. Type help or ? to list commands.\n"
    prompt = "(cowchat) > "

    def __init__(
        self,
        completekey: str = "tab",
        stdin=None,
        stdout=None,
    ) -> None:
        super().__init__(completekey, stdin, stdout)
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sck.bind(("localhost", 11111))
        self.sck.connect(("localhost", 1337))
        self.cmpl_result = None
        self.active_cmd = []

    def do_login(self, arg: str) -> None:
        self.active_cmd.append(("login", "cmd"))
        if arg == "":
            print("You must specify cow name")
            return
        cow_name = shlex.split(arg)[0]
        self.sck.send(f"login {cow_name}\n".encode())

    def do_who(self, arg: str) -> None:
        self.active_cmd.append(("who", "cmd"))
        self.sck.send("who\n".encode())

    def do_cows(self, arg: str) -> None:
        self.active_cmd.append(("cows", "cmd"))
        self.sck.send("cows\n".encode())

    def do_say(self, arg: str) -> None:
        self.active_cmd.append(("say", "cmd"))
        if arg == "":
            print("You must specify cow name and message string")
            return
        words = shlex.split(arg)
        if len(words) < 2:
            print("You must specify cow name and message string")
            return
        cow_name, *message_words = words
        message = " ".join(message_words)
        self.sck.send(f"say {cow_name} {message}\n".encode())

    def do_yield(self, arg: str) -> None:
        self.active_cmd.append(("yield", "cmd"))
        if arg == "":
            print("You must specify message string")
            return
        words = shlex.split(arg)
        if len(words) < 1:
            print("You must specify message string")
            return
        self.sck.send(f"yield {' '.join(words)}\n".encode())

    def do_quit(self, arg: str) -> None:
        self.sck.send("quit\n".encode())
        exit(0)

    def complete_login(self, text: str, line: str, begidx: int, endidx: int):
        args = shlex.split(line)
        match len(args), line[endidx - 1]:
            case 1, _:
                self.active_cmd.append(("cows", "cmpl"))
                self.sck.send("cows\n".encode())
                while self.cmpl_result is None:
                    sleep(0.01)
                res = self.cmpl_result.split()
                self.cmpl_result = None
                return res

            case 2, " ":
                pass

            case 2, _:
                self.active_cmd.append(("cows", "cmpl"))
                self.sck.send("cows\n".encode())
                while self.cmpl_result is None:
                    sleep(0.01)
                res = self.cmpl_result.split()
                self.cmpl_result = None
                return [x for x in res if x.startswith(args[1])]

    def complete_say(self, text: str, line: str, begidx: int, endidx: int):
        args = shlex.split(line)
        match len(args), line[endidx - 1]:
            case 1, _:
                self.active_cmd.append(("who", "cmpl"))
                self.sck.send("who\n".encode())
                while self.cmpl_result is None:
                    sleep(0.01)
                res = self.cmpl_result.split()
                self.cmpl_result = None
                return res

            case 2, " ":
                pass

            case 2, _:
                self.active_cmd.append(("who", "cmpl"))
                self.sck.send("who\n".encode())
                while self.cmpl_result is None:
                    sleep(0.01)
                res = self.cmpl_result.split()
                self.cmpl_result = None
                return [x for x in res if x.startswith(args[1])]

    def listen_server(self) -> None:
        data = ""
        while True:
            while "\n" not in data:
                new_msg = self.sck.recv(1024).decode()
                if not new_msg:
                    if data:
                        print(
                            f"\n{data}\n{self.prompt}{readline.get_line_buffer()}",
                            end="",
                            flush=True,
                        )
                    return
                data += new_msg
            answer, data = data.rsplit("\n", maxsplit=1)
            for message in answer.split("\n"):
                if message.startswith("msg"):
                    print(
                        f"\n{answer[5:]}\n{self.prompt}{readline.get_line_buffer()}",
                        end="",
                        flush=True,
                    )
                    continue
                command, *answer = message.split(maxsplit=1)
                if answer:
                    answer = " ".join(answer)
                else:
                    answer = ""
                for i, act_cmd in enumerate(self.active_cmd[::-1]):
                    if command not in act_cmd:
                        continue
                    if act_cmd[1] != "cmd":
                        self.cmpl_result = answer
                        self.active_cmd = (
                            self.active_cmd[: len(self.active_cmd) - i - 1]
                            + self.active_cmd[len(self.active_cmd) - i :]
                        )
                        continue
                    print(
                        f"\n{answer}\n{self.prompt}{readline.get_line_buffer()}",
                        end="",
                        flush=True,
                    )
                    self.active_cmd = (
                        self.active_cmd[: len(self.active_cmd) - i - 1]
                        + self.active_cmd[len(self.active_cmd) - i :]
                    )


def main() -> None:
    cmdline = CowClient()
    timer = threading.Thread(target=cmdline.listen_server)
    timer.start()
    cmdline.cmdloop()


if __name__ == "__main__":
    main()
