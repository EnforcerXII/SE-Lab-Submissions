# Lab 5 — Static Code Analysis Issues

Line numbers below refer to the **original** `hostel_allocation_original.py` provided for the lab. Findings are based on code inspection; exact tool codes/severity should be copied from your own Pylint/Bandit/Flake8 reports after running the commands in `RUN_ANALYSIS.md`.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe YAML loader | Security | 21 | `yaml.load(..., Loader=yaml.Loader)` can construct arbitrary Python objects when the configuration is untrusted. | Replaced it with `yaml.safe_load()` and added basic configuration validation. |
| Flask debug mode enabled | Security | 80 | `debug=True` can expose an interactive debugger and should not be enabled in a deployed application. | Set `debug=False`. |
| User input concatenated into HTML | Security | 76–77 | The `id` query parameter is inserted directly into an HTML response, allowing HTML/script injection. | Use a Jinja template with escaped variables and validate missing IDs. |
| Hard-coded database password | Security | 66 | A password literal is embedded in source code and may be exposed in version control. | Read the demo password from `WARDEN_DB_PASSWORD`; no password is committed. |
| Incorrect room capacity check | Bug | 34 | `>` allows an extra occupant when a room is exactly full. | Check `len(occupants) >= capacity` before adding a student. |
| Gender is ignored | Bug | 29–38 | `gender` is accepted but never compared to the room's gender, so students can be assigned to an incompatible block. | Skip rooms whose configured gender does not match the student's gender. |
| Duplicate allocation possible | Bug | 29–38 | Allocating the same student again can append duplicate IDs and overwrite their allocation record. | Return the existing room if the student is already allocated. |
| Mutable default argument | Maintainability / bug risk | 29 | `preferred=[]` is a shared mutable default between calls. | Use `preferred=None` and create a fresh list for each call. |
| Vacating leaves stale occupant ID | Bug | 41–45 | The allocation dictionary entry is deleted, but the student remains in the room's occupants list. | Remove the student from both the allocation record and room occupant list. |
| Vacant-bed count is inaccurate | Bug | 58–63 | Only completely empty rooms are counted; free beds in partially occupied rooms are ignored. | Sum `capacity - occupant_count` for every room. |
| Seniority order is reversed from label | Logic | 52–53, 95 | Sorting ascending puts year 1 before year 4, despite the “seniors first” label. | Sort by year in descending order. |
| Missing student / invalid days not handled | Robustness | 47–50 | Unknown IDs raise an incidental `KeyError`; negative days are accepted. | Validate days and raise a clear error for missing allocations. |
| Unused imports and non-PEP 8 names/formatting | Style | 1–6, throughout | Unused imports, camelCase names, long lines, and missing spacing reduce readability and trigger style warnings. | Remove unused imports, use snake_case, add docstrings, and format consistently. |
| Remote logging configuration listener | Security / operational risk | 71–72 | The function starts a remote logging configuration listener on a network port without authentication controls. | Removed the listener from the cleaned version because the demo does not need remote logging. |
