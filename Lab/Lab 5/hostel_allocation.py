import os
import random
from typing import Any

import yaml
from flask import Flask, abort, render_template_string, request

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""

rooms: dict[str, dict[str, Any]] = {}
allocations: dict[str, dict[str, Any]] = {}
waitlist: list[str] = []
app = Flask(__name__)


def load_config(text: str = CONFIG) -> dict[str, Any]:
    """Load block configuration safely and initialize the room inventory."""
    config = yaml.safe_load(text)
    if not isinstance(config, dict) or not isinstance(config.get("blocks"), dict):
        raise ValueError("Configuration must contain a 'blocks' mapping.")

    rooms.clear()
    allocations.clear()
    waitlist.clear()
    for block, info in config["blocks"].items():
        for key in ("gender", "rooms", "capacity", "fee"):
            if key not in info:
                raise ValueError(f"Block {block!r} is missing {key!r}.")
        if info["rooms"] < 1 or info["capacity"] < 1 or info["fee"] < 0:
            raise ValueError(f"Block {block!r} has invalid room settings.")
        for number in range(1, info["rooms"] + 1):
            rooms[f"{block}{number}"] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }
    return config


def allocate_room(
    student_id: str,
    name: str,
    gender: str,
    year: int,
    preferred: list[str] | None = None,
) -> str | None:
    """Allocate a compatible bed, or add the student to the waitlist."""
    if not isinstance(year, int) or isinstance(year, bool) or year < 1:
        return None
    if student_id in allocations:
        return allocations[student_id]["room"]

    preferred_rooms = preferred or []
    ordered_rooms = list(dict.fromkeys(preferred_rooms + list(rooms.keys())))
    for room_no in ordered_rooms:
        room = rooms.get(room_no)
        if room is None:
            continue
        if room["gender"] != gender:
            continue
        if len(room["occupants"]) >= room["capacity"]:
            continue
        room["occupants"].append(student_id)
        allocations[student_id] = {"name": name, "room": room_no, "year": year}
        if student_id in waitlist:
            waitlist.remove(student_id)
        return room_no

    if student_id not in waitlist:
        waitlist.append(student_id)
    return None


def vacate_room(student_id: str) -> bool:
    """Remove a student from their room; return whether they were allocated."""
    allocation = allocations.pop(student_id, None)
    if allocation is None:
        return False
    occupants = rooms[allocation["room"]]["occupants"]
    if student_id in occupants:
        occupants.remove(student_id)
    return True


def monthly_fee(student_id: str, days_stayed: int) -> int:
    """Calculate full 30-day periods charged to an allocated student."""
    if days_stayed < 0:
        raise ValueError("days_stayed cannot be negative.")
    if student_id not in allocations:
        raise KeyError(f"Student {student_id!r} has no room allocation.")
    room = rooms[allocations[student_id]["room"]]
    months = days_stayed // 30
    return months * room["fee"]


def priority_order(students: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort students by year, with more senior students first."""
    return sorted(students, key=lambda student: student["year"], reverse=True)


def room_lottery(student_ids: list[str]) -> list[str]:
    """Return a randomized ordering of student IDs."""
    return random.sample(student_ids, len(student_ids))


def vacant_beds() -> int:
    """Count every unoccupied bed, including beds in partially filled rooms."""
    return sum(
        room["capacity"] - len(room["occupants"])
        for room in rooms.values()
    )


def connect_warden_db() -> dict[str, str | bool]:
    """Return demo connection metadata without embedding a real password."""
    password = os.environ.get("WARDEN_DB_PASSWORD", "")
    return sqlite_connect(host="localhost", user="warden", password=password)


def sqlite_connect(host: str, user: str, password: str) -> dict[str, str | bool]:
    """Simulate a database connection for this lab exercise."""
    return {"host": host, "user": user, "connected": bool(password)}


@app.route("/room")
def room_lookup() -> str:
    """Display a student's room, safely escaping user-controlled content."""
    student_id = request.args.get("id", "").strip()
    if not student_id:
        abort(400, description="Please provide a student id using ?id=...")
    allocation = allocations.get(student_id)
    return render_template_string(
        "<h1>Room for {{ student_id }}: {{ allocation }}</h1>",
        student_id=student_id,
        allocation=allocation if allocation is not None else "Not allocated",
    )


def run_portal() -> None:
    """Run the portal without enabling Flask's interactive debugger."""
    app.run(debug=False)


def main() -> None:
    """Run a small demonstration of the allocation functions."""
    load_config()
    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])
    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthly_fee("S1", 45))
    sample_students = [{"year": 1}, {"year": 4}, {"year": 2}]
    print("Priority (seniors first?):", [s["year"] for s in priority_order(sample_students)])
    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    load_config()
    main()
