"""
Utility & UI Helper Functions
"""

import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_menu(options):
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")
    print("-" * 50)


def get_input(prompt, default=None, as_float=False):
    try:
        suffix = f" [{default}]: " if default else ": "
        value = input(f"  {prompt}{suffix}").strip()
        if not value and default is not None:
            value = default
        if as_float:
            return float(value) if value else None
        return value
    except (ValueError, KeyboardInterrupt):
        return None
