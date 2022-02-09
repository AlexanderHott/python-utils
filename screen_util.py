#!/usr/bin/env python
# -*- coding:utf-8 -*-

from subprocess import getoutput
from multiprocessing import Process
from os import system
from time import sleep
import typing as t


class ScreenNotFoundError(Exception):
    """raised when the screen does not exists"""


class Screen(object):
    """Represents a gnu-screen object::
    >>> s=Screen("screenName", create=True)
    >>> s.name
    'screenName'
    >>> s.exists
    True
    >>> s.state
    >>> s.send_commands("man -k keyboard")
    >>> s.kill()
    >>> s.exists
    False
    """

    def __init__(self, name: str, create: bool = False, id=None, status=None) -> None:
        self.name: str = name
        self._id: str = id
        self._status: str = status
        if create:
            self.create()

    @property
    def id(self) -> str:
        """return the identifier of the screen"""
        if not self._id:
            self._set_screen_infos()
        return self._id

    @property
    def status(self) -> str:
        """return the status of the screen"""
        self._set_screen_infos()
        return self._status

    @property
    def exists(self) -> bool:
        """Tell if the screen session exists or not."""
        # output line sample:
        # "     28062.G.Terminal        (Detached)"
        lines = getoutput(f"screen -ls | grep -P {self.name}").split("\n")

        for l in lines:
            info, date, time, pm, status = l.split()
            id_, name, server = info.split(".")
            if name == self.name:
                return True
        return False

        # lines = getoutput("screen -ls | grep " + self.name).split("\n")
        # return self.name in [".".join(l.split(".")[1:]).split("\t")[0] for l in lines]

    def create(self) -> None:
        """create a screen, if does not exists yet"""
        if not self.exists:
            Process(target=self._delayed_detach).start()
            system("screen -UR " + self.name)

    def interrupt(self) -> None:
        """Insert CTRL+C in the screen session"""
        self._check_exists()
        system("screen -x " + self.name + ' -X eval "stuff \\003"')

    def kill(self) -> None:
        """Kill the screen applications then quit the screen"""
        self._check_exists()
        system("screen -x " + self.name + " -X quit")

    def detach(self) -> None:
        """detach the screen"""
        self._check_exists()
        system("screen -d " + self.name)

    def _delayed_detach(self) -> None:
        sleep(5)
        self.detach()

    def send_commands(self, *commands) -> None:
        """send commands to the active gnu-screen"""
        self._check_exists()
        for command in commands:
            sleep(0.02)
            system("screen -x " + self.name + ' -X stuff "' + command + '" ')
            sleep(0.02)
            system("screen -x " + self.name + ' -X eval "stuff \\015" ')

    def _check_exists(self, message="Error code: 404") -> None:
        """check whereas the screen exist. if not, raise an exception"""
        if not self.exists:
            raise ScreenNotFoundError(message)

    def _set_screen_infos(self) -> None:
        """set the screen information related parameters"""
        if self.exists:
            infos = getoutput("screen -ls | grep %s" % self.name).split("\t")[1:]
            self._id = infos[0].split(".")[0]
            self._date = infos[1][1:-1]
            self._status = infos[2][1:-1]

    def __repr__(self) -> str:
        # return "<%s '%s'>" % (self.__class__.__name__, self.name)
        return f"{self.__class__.__name__}(name={self.name}, id={self.id}, status={self.status})"

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self: "Screen", other: "Screen") -> bool:
        return (
            self.name == other.name
            and self.status == other.status
            and self.id == other.id
        )

    def __ne__(self: "Screen", other: "Screen") -> bool:
        return (
            self.id != other.id
            or self.status != other.status
            or self.name != other.name
        )

    def __gt__(self: "Screen", other: "Screen") -> bool:
        return self.id > other.id

    def __lt__(self: "Screen", other: "Screen") -> bool:
        return self.id < other.id

    def __ge__(self: "Screen", other: "Screen") -> bool:
        return self.id >= other.id

    def __le__(self: "Screen", other: "Screen") -> bool:
        return self.id <= other.id


def list_screens() -> list[Screen]:
    """List all the existing screens and build a Screen instance for each"""
    # 1560.pts-0.playmc       (11/24/2021 03:28:10 PM)        (Detached)
    # 1422.pts-0.playmc       (11/24/2021 03:26:45 PM)        (Detached)

    scrns = getoutput("screen -ls | grep -P '\t'").split("\n")
    screens = []
    for s in scrns:
        info, date, time, pm, status = s.split()
        id_, name, server = info.split(".")
        screens.append(Screen(id=id_, name=name, status=status))

    return screens
    # return [
    #     Screen(".".join(l.split(".")[1:]).split("\t")[0])
    #     for l in getoutput("screen -ls | grep -P '\t'").split("\n")
    # ]


# screens = list_screens()

# for screen in screens:
#     print(repr(screen))