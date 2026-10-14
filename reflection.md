# Lab 5 — Reflection

> The supplied handout mentions reflection questions but does not include their exact wording. These responses cover the lab's stated learning outcomes; use the instructor's exact questions if they were provided separately.

### 1. What is static code analysis, and why is it useful?

Static code analysis checks source code without running the program. It helps find likely bugs, risky coding patterns, and style problems early, making code easier to maintain and review.

### 2. What issues did the tools and code review help identify?

The review identified a mutable default argument, broad exception handling, unsafe shell command construction, a hard-coded unused password, use of MD5 for an identifier, weak input validation, implicit file encoding, inconsistent naming, and execution at import time.

### 3. How do Pylint, Bandit, and Flake8 differ?

Pylint checks broader code quality, likely programming mistakes, naming, and documentation. Bandit looks for common Python security risks. Flake8 checks PEP 8 style and pycodestyle/pyflakes findings. They overlap in places, but their combined feedback gives a more useful review than any single tool.

### 4. What did you learn, and what are the limitations of static analysis?

I learned to fix the underlying causes rather than hide warnings: use `None` for mutable defaults, handle missing records explicitly, validate inputs, avoid shell execution, and use safe file handling. Static analysis cannot prove that a program is correct or fully secure, so I also ran the program and unit tests and reviewed the changes manually.
