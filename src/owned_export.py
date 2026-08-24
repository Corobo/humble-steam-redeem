"""Export mode -- dump the user's owned Steam games to a CSV."""

from __future__ import annotations

import csv
import time

from src.ownership import get_owned_apps
from src.steam_auth import steam_login
from src.utils import cls, print_info, print_rule, print_success, print_warning


def owned_export_mode() -> None:
    """Sign into Steam, fetch owned apps and write them to owned_steam_<ts>.csv."""
    cls()
    print_rule("Export Owned Steam Games")

    session = steam_login()
    print_success("Successfully signed in on Steam.")

    owned = get_owned_apps(session)
    if not owned:
        print_warning(
            "No ownership data available (a Steam Web API key is required). "
            "Nothing exported."
        )
        return

    ts = time.strftime("%Y%m%d-%H%M%S")
    filename = f"owned_steam_{ts}.csv"
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["appid", "name"])
        for appid, name in sorted(owned.items(), key=lambda kv: kv[1].lower()):
            writer.writerow([appid, name])

    print_success(f"Exported {len(owned)} owned games to {filename}")
    print_info(
        "This is the exact list Auto-Redeem compares Humble keys against "
        "(by app id and fuzzy name match)."
    )
