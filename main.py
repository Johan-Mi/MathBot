#!/usr/bin/env python3
"""This module contains the math bot, which evaluates mathematical
expressions."""

import math
import discord
from lark import Lark, Transformer

client = discord.Client()

PREFIX = "="


class CalcTransformer(Transformer):  # pylint: disable=too-few-public-methods
    """Transformer for the parser."""
    @staticmethod
    def _num(args):
        return float(args[0])

    @staticmethod
    def _add(args):
        return args[0] + args[1]

    @staticmethod
    def _sub(args):
        return args[0] - args[1]

    @staticmethod
    def _mul(args):
        return args[0] * args[1]

    @staticmethod
    def _div(args):
        return args[0] / args[1]

    @staticmethod
    def _negate(args):
        return -args[0]

    @staticmethod
    def _exp(args):
        return args[0]**args[1]

    @staticmethod
    def _func_call(args):
        def unknown_func(_):
            raise NameError(f"Function {args[0]}() does not exist")

        return {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "log": math.log10,
            "ln": math.log,
            "abs": abs,
        }.get(args[0], unknown_func)(args[1])


parser = Lark.open("grammar.lark", parser="lalr", transformer=CalcTransformer)


@client.event
async def on_ready():
    """Lets you know when the bot starts."""
    print(f"Discord version: {discord.__version__}")
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    """Responds when someone else sends a message."""
    if message.author == client.user:
        return
    if message.content.startswith(PREFIX):
        expr = message.content[len(PREFIX):]

        try:
            result = f"{expr} = {parser.parse(expr)}"
        except ZeroDivisionError:
            result = "Tried to divide by zero!"
        except Exception as err:
            result = str(err)
        await message.channel.send(result)


def main():
    """Runs the bot with the token from the file called 'token'."""
    with open("token") as token_file:
        token = token_file.read()
    client.run(token)


if __name__ == "__main__":
    main()
