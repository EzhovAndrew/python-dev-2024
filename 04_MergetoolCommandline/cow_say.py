import cmd
import os
import shlex

import cowsay

params = {
    "cowsay": ["message", "cow", "eyes", "tongue"],
    "cowthink": ["message", "cow", "eyes", "tongue"],
    "make_bubble": ["text"],
}

eyes = ["oO", "Oo", "XX", "OO", "DD", "$$"]
tongues = ["LL", "pp", "##", "@@"]


class cowsayCmd(cmd.Cmd):
    intro = "Welcome to the cowsay shell.   Type help or ? to list commands.\n"
    prompt = "(cowsay) > "

    def do_list_cows(self, arg):
        """
        List all cow filenames.

        Parameters
        ----------
        path: str, positional, optional.
            path to directory with cow files, same as COWPATH.
        """
        path = (
            os.environ.get("COWPATH", cowsay.COW_PEN)
            if arg == ""
            else shlex.split(arg)[0]
        )
        print(*cowsay.list_cows(path))

    def do_make_bubble(self, arg):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows.

        Parameters
        ----------
        text: str, positional, required.
            text that appears above the cows.
        """
        if arg == "":
            print("ERROR: missing 1 required positional argument.")
            return

        text = shlex.split(arg)[0]
        print(cowsay.make_bubble(text))

    def do_cowsay(self, arg):
        """
        Similar to the cowsay command.

        Parameters
        ----------
        message: str, positional, required.
            Message to be displayed by cowsay.
        cow: str, positional, optional.
            The cow that will output the message
        eyes: str, positional, optional.
            String displayed as cow eyes.
        tongue: str, positional, optional.
            String displayed as cow tongue
        """
        if arg == "":
            print("ERROR: missing 1 required positional argument.")
            return

        args = shlex.split(arg)
        message = args[0]
        cow = args[1] if len(args) > 1 else "default"
        eye = args[2] if len(args) > 2 else cowsay.Option.eyes
        tongue = args[3] if len(args) > 3 else cowsay.Option.tongue
        print(cowsay.cowsay(message=message, cow=cow, eyes=eye, tongue=tongue))

    def do_cowthink(self, arg):
        """
        Similar to the cowsay command.

        Parameters
        ----------
        message: str, positional, required.
            Message to be displayed by cowsay.
        cow: str, positional, optional.
            The cow that will output the message
        eyes: str, positional, optional.
            String displayed as cow eyes.
        tongue: str, positional, optional.
            String displayed as cow tongue
        """
        if arg is None:
            print("ERROR: missing 1 required positional argument.")
            return

        args = shlex.split(arg)
        message = args[0]
        cow = args[1] if len(args) > 1 else "default"
        eye = args[2] if len(args) > 2 else cowsay.Option.eyes
        tongue = args[3] if len(args) > 3 else cowsay.Option.tongue
        print(cowsay.cowthink(message=message, cow=cow, eyes=eye, tongue=tongue))

    def complete_cowsay(self, text, line, begidx, endidx):
        args = shlex.split(line)
        match len(args), line[endidx - 1]:
            case 2, " ":
                return [cow for cow in cowsay.list_cows()]

            case 3, " ":
                return [eye for eye in eyes]

            case 3, _:
                return [
                    cow
                    for cow in filter(
                        lambda pmt: pmt.startswith(args[2]), cowsay.list_cows()
                    )
                ]

            case 4, " ":
                return [tongue for tongue in tongues]

            case 4, _:
                return [
                    eye for eye in filter(lambda pmt: pmt.startswith(args[3]), eyes)
                ]

            case 5, x:
                if x == " ":
                    return
                return [
                    tongue
                    for tongue in filter(lambda pmt: pmt.startswith(args[4]), tongues)
                ]

    def complete_cowthink(self, text, line, begidx, endidx):
        args = shlex.split(line)
        match len(args), line[endidx - 1]:
            case 2, " ":
                return [cow for cow in cowsay.list_cows()]

            case 3, " ":
                return [eye for eye in eyes]

            case 3, _:
                return [
                    cow
                    for cow in filter(
                        lambda pmt: pmt.startswith(args[2]), cowsay.list_cows()
                    )
                ]

            case 4, " ":
                return [tongue for tongue in tongues]

            case 4, _:
                return [
                    eye for eye in filter(lambda pmt: pmt.startswith(args[3]), eyes)
                ]

            case 5, x:
                if x == " ":
                    return
                return [
                    tongue
                    for tongue in filter(lambda pmt: pmt.startswith(args[3]), tongues)
                ]


if __name__ == "__main__":
    cowsayCmd().cmdloop()
