# Lab 5 — Reflection

**Note:** The supplied handout refers to four reflection questions, but the provided three-page PDF does not actually show the questions. The answers below cover four relevant reflection points based on the stated lab objectives and learning outcomes. If your instructor has a separate question sheet, use its exact wording.

## 1. What is static code analysis, and why is it useful?

Static code analysis checks source code without needing to run the program. It can find likely bugs, security risks, and style problems early. It is useful because it gives developers feedback before the code is deployed and makes the code easier to maintain.

## 2. What is the difference between Pylint, Flake8, and Bandit?

Pylint checks general code quality, naming, design, and possible programming mistakes. Flake8 mainly checks Python formatting and PEP 8 style rules. Bandit looks for common security risks, such as unsafe functions or insecure coding patterns. They overlap a little, but each focuses on a different area, so using all three gives broader coverage.

## 3. What important issues did you find and fix in this program?

The original program used an unsafe YAML loader, enabled Flask debug mode, inserted user input directly into HTML, and stored a database password in the source. It also had logic bugs: it could overfill rooms, ignored student gender, allowed duplicate allocations, did not remove students from room occupant lists when vacating, and counted only completely empty rooms when calculating vacant beds. I fixed these by using safe YAML loading, escaped template variables, disabling debug mode, reading the demo password from an environment variable, validating allocation rules, and updating the room state consistently.

## 4. What did you learn, and what are the limitations of static analysis?

I learned that code can look like it runs while still having security and logic problems. Static analysis tools are useful for catching common issues, but they cannot understand every requirement or guarantee that the program behaves correctly. For example, the tools may not identify that the vacant-bed calculation is logically wrong for partially occupied rooms. Running the program and testing important cases is still necessary. I would use static analysis together with manual review and tests rather than relying on only one method.
