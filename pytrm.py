#!/usr/bin/env python3
"""
pytrm.py - High-Performance Custom Python POSIX Shell
Version: 1.0.1
Upgrades: Deep-vetted multi-chain chaining execution, fixed hash type matching, escaped logo blocks.
"""

import os
import sys
import tty
import termios
import subprocess
import getpass
import shlex
import re

# --- Color Profiles & Terminal Anchors ---
ORANGE = "\033[38;5;208m"
RED = "\033[31m"
BLUE = "\033[34m"
GRAY = "\033[90m"
RESET = "\033[0m"
CLEAR_LINE = "\r\033[2K"

# Explicit list of custom commands built directly into our script code
BUILTIN_COMMANDS = ['cd', 'exit', 'sysinfo', 'history', 'help']

def display_banner():
    """
    Renders the stylized PYTRM ASCII Boot Banner.
    All backslashes are properly escaped using raw string blocks to prevent parsing crashes.
    """
    banner = r"""
  _____ __     _______ ____  __  __ 

 |  __ \\ \   / /_   _|  _ \|  \/  |
 | |__) |\ \_/ /  | | | |_) | \  / |
 |  ___/  \   /   | | |  _ <| |\/| |
 | |       | |   _| |_| |_) | |  | |
 |_|       |_|  |_____|____/|_|  |_|
                     v1.0.1 Patch Release
    """
    print(banner)
    print("Welcome to the Python Terminal Shell Environment.")
    print("Type 'exit' to log out. Use Tab or Right-Arrow to complete commands.\n")

def get_all_commands():
    """Indexed available system binaries into memory on initialization."""
    commands = set(BUILTIN_COMMANDS)
    paths = ['/bin', '/usr/bin', '/sbin', '/usr/sbin']
    for path in paths:
        if os.path.exists(path):
            try:
                for item in os.listdir(path):
                    commands.add(item)
            except PermissionError:
                continue
    return sorted(list(commands)), commands

# --- Memory Cache Layer ---
SYSTEM_COMMANDS_LIST, SYSTEM_COMMANDS_SET = get_all_commands()
HISTORY = []

def is_valid_command(cmd_string):
    """Performs instant hash lookups against the cached system command set."""
    if not cmd_string.strip():
        return True
    try:
        parts = shlex.split(cmd_string)
    except ValueError:
        parts = cmd_string.strip().split(' ')
    if not parts or not parts[0]:
        return True
    return parts[0] in SYSTEM_COMMANDS_SET

def get_autocomplete_hint(buffer):
    """Retrieves inline command matches from the cached memory structure."""
    if not buffer or ' ' in buffer or is_valid_command(buffer):
        return ""
    for cmd in SYSTEM_COMMANDS_LIST:
        if cmd.startswith(buffer):
            return cmd[len(buffer):]
    return ""

def get_closest_command(typo):
    """Calculates Levenshtein distance thresholds for input spell-checking."""
    def distance(s1, s2):
        if len(s1) < len(s2):
            return distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        prev = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr = [i + 1]
            for j, c2 in enumerate(s2):
                curr.append(min(prev[j+1]+1, curr[j]+1, prev[j]+(c1!=c2)))
            prev = curr
        return prev[-1]

    best_match, min_dist = None, 3
    for cmd in SYSTEM_COMMANDS_LIST:
        dist = distance(typo, cmd)
        if dist < min_dist:
            min_dist, best_match = dist, cmd
    return best_match

def print_sysinfo():
    """Displays core kernel memory statistics and configuration baselines."""
    print(f"\n{ORANGE}--- System Information Matrix ---{RESET}")
    try:
        with open('/proc/meminfo', 'r') as f:
            total, free = 0, 0
            for line in f:
                if "MemTotal" in line:
                    total = int(line.split()[1]) // 1024
                if "MemFree" in line:
                    free = int(line.split()[1]) // 1024
            print(f"Memory Allocation: {total - free} MB / {total} MB")
    except Exception:
        print("Memory Allocation: Unable to read system metrics")
    print(f"Active Account: {getpass.getuser()}")
    print(f"Execution Subshell: Python {sys.version.split()[0]}\n")

def print_history():
    """Displays the chronological shell execution history."""
    if not HISTORY:
        print("History log is empty.")
        return
    print()
    for idx, cmd in enumerate(HISTORY, start=1):
        print(f" {GRAY}{idx:>3}{RESET} {cmd}")
    print()

def print_help():
    """Displays only our unique, custom built-in shell commands with descriptions."""
    print(f"\n{ORANGE}--- Pytrm Built-in Custom Shell Commands ---{RESET}")
    descriptions = {
        "cd": "Changes the current working directory (e.g., cd ~/src)",
        "exit": "Safely terminates your current pytrm session layouts",
        "sysinfo": "Prints real-time host RAM allocation metrics and active user info",
        "history": "Displays a chronological ledger of commands typed this session",
        "help": "Shows this custom command overview layout dashboard"
    }
    for cmd in BUILTIN_COMMANDS:
        print(f" {BLUE}{cmd:<10}{RESET} {descriptions.get(cmd, '')}")
    print(f"\n{GRAY}* Any other command typed will pass directly to the Linux system environment.{RESET}\n")

def get_live_input(prompt_prefix, old_settings):
    """Captures character buffers natively and renders real-time syntax coloring."""
    fd = sys.stdin.fileno()
    buffer = ""
    history_index = len(HISTORY)
    try:
        tty.setraw(fd)
        sys.stdout.write(prompt_prefix)
        sys.stdout.flush()
        while True:
            char = sys.stdin.read(1)
            if char in ['\r', '\n']:
                sys.stdout.write('\r\n')
                sys.stdout.flush()
                break
            elif char == '\x7f':  # Backspace
                if len(buffer) > 0:
                    buffer = buffer[:-1]
            elif char == '\x1b':  # Escape sequence (Arrows)
                next1, next2 = sys.stdin.read(1), sys.stdin.read(1)
                if next1 == '[':
                    if next2 == 'A':  # Up Arrow
                        if history_index > 0:
                            history_index -= 1
                            buffer = HISTORY[history_index]
                    elif next2 == 'B':  # Down Arrow
                        if history_index < len(HISTORY) - 1:
                            history_index += 1
                            buffer = HISTORY[history_index]
                        else:
                            history_index = len(HISTORY)
                            buffer = ""
                    elif next2 == 'C':  # Right Arrow (Autocomplete)
                        hint = get_autocomplete_hint(buffer)
                        if hint:
                            buffer += hint
            elif char == '\t':  # Tab (Autocomplete)
                hint = get_autocomplete_hint(buffer)
                if hint:
                    buffer += hint
            elif char == '\x03':  # Ctrl+C
                raise KeyboardInterrupt
            elif 32 <= ord(char) <= 126:
                buffer += char

            # --- RENDER REFRESH ENGINE ---
            tokens = re.split(r'%%|;', buffer)
            base_buffer = tokens[0].strip() if tokens else ""
            text_color = BLUE if is_valid_command(base_buffer) else RED
            hint = get_autocomplete_hint(buffer)
            
            sys.stdout.write(CLEAR_LINE)
            sys.stdout.write(f"{prompt_prefix}{text_color}{buffer}{GRAY}{hint}{RESET}")
            if hint:
                sys.stdout.write("\b" * len(hint))
            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return buffer

# --- Main Command Execution Loop ---
def main():
    display_banner()
    fd = sys.stdin.fileno()
    original_terminal_settings = termios.tcgetattr(fd)
    
    while True:
        try:
            current_dir = os.getcwd()
            home_path = os.path.expanduser("~")
            display_path = current_dir.replace(home_path, "~", 1) if current_dir.startswith(home_path) else current_dir
            prompt_prefix = f"{ORANGE}{display_path} >{RESET} "
            
            raw_command = get_live_input(prompt_prefix, original_terminal_settings)
            full_input = raw_command.strip()
            if not full_input:
                continue
            if not HISTORY or HISTORY[-1] != full_input:
                HISTORY.append(full_input)

            # --- MULTI-OPERATOR CHAINING PARSER ENGINE ---
            tokens = re.split(r'(%%|;)', full_input)
            sub_commands = [tokens[i].strip() for i in range(0, len(tokens), 2)]
            operators = [tokens[i] for i in range(1, len(tokens), 2)]
            last_command_failed = False
            
            for idx, command in enumerate(sub_commands):
                if not command:
                    continue
                if idx > 0 and operators[idx-1] == '%%' and last_command_failed:
                    break
                    
                try:
                    parts = shlex.split(command)
                except ValueError as e:
                    print(f"shell: syntax error: {e}")
                    last_command_failed = True
                    continue
                    
                if not parts:
                    continue
                first_word = parts[0]
                
                if first_word == "exit":
                    print("Terminating session layout...")
                    sys.exit(0)
                if first_word == "sysinfo":
                    print_sysinfo()
                    last_command_failed = False
                    continue
                if first_word == "history":
                    print_history()
                    last_command_failed = False
                    continue
                if first_word == "help":
                    print_help()
                    last_command_failed = False
                    continue
                    
                # Built-in structured directory router
                if first_word == "cd":
                    target_dir = parts[1] if len(parts) > 1 else "~"
                    expanded_dir = os.path.expanduser(target_dir)
                    try:
                        os.chdir(expanded_dir)
                        last_command_failed = False
                    except Exception as e:
                        print(f"shell: cd: {target_dir}: {e}")
                        last_command_failed = True
                    continue
                    
                # Check if command executable exists
                if not is_valid_command(first_word):
                    suggestion = get_closest_command(first_word)
                    if suggestion:
                        print(f"Did you mean: {ORANGE}{suggestion}{RESET}?")
                    else:
                        print(f"shell: {first_word}: command not found")
                    last_command_failed = True
                    continue
                    
                # Run external applications while cleanly out of raw mode
                try:
                    result = subprocess.run(command, shell=True, check=False)
                    sys.stdout.flush()
                    last_command_failed = (result.returncode != 0)
                except Exception as e:
                    print(f"shell: execution error: {e}")
                    last_command_failed = True
        except (KeyboardInterrupt, EOFError):
            print(f"\nUse 'exit' to close the terminal session.")

if __name__ == "__main__":
    main()
