import subprocess

from sys import platform


def os_notify(title, text):
  if platform == "darwin":
    CMD = """
    on run argv
      display notification (item 2 of argv) with title (item 1 of argv)
    end run
    """
    subprocess.call(["osascript", "-e", CMD, title, text])
