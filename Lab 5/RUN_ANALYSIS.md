# Running and saving the required analysis reports

The analysis tools could not be installed in the environment used to prepare this submission because package downloads were unavailable. Therefore, no Pylint/Bandit/Flake8 output has been fabricated. Run the following commands on your computer to create genuine reports.

```bash
python -m venv venv
source venv/bin/activate        # Windows PowerShell: .\venv\Scripts\Activate.ps1
python -m pip install flask pyyaml pylint bandit flake8

# Reports for the supplied original code
python -m pylint hostel_allocation_original.py > reports/before/pylint_report.txt 2>&1
python -m bandit -r hostel_allocation_original.py > reports/before/bandit_report.txt 2>&1
python -m flake8 hostel_allocation_original.py > reports/before/flake8_report.txt 2>&1

# Reports for the cleaned code
python -m pylint hostel_allocation.py > reports/after/pylint_report.txt 2>&1
python -m bandit -r hostel_allocation.py > reports/after/bandit_report.txt 2>&1
python -m flake8 hostel_allocation.py > reports/after/flake8_report.txt 2>&1
```

Use the actual results to update `issues.md` with any exact warning IDs and line numbers. The assignment targets a Pylint score above 9.5 and asks for three commits documenting fixes. Suggested commit sequence:

```bash
git init
git add hostel_allocation_original.py hostel_allocation.py RUN_ANALYSIS.md
 git commit -m "Fix code quality issues identified by Pylint"
git add issues.md
git commit -m "Address security findings identified by Bandit"
git add reflection.md
 git commit -m "Apply style cleanup and document Flake8 review"
```

These are suggested commit messages, not commits already created. If you want genuine before/after reports and the final score, run the commands in an environment where the three tools can be installed.
