# Static Code Analysis — Issues and Fixes

## 1. Objective

Static code analysis was performed on `pharmacy_manager.py` using Pylint, Bandit, and Flake8 to identify code quality, security, and formatting issues.

## 2. Tools Used

- **Pylint:** Checks Python code quality, naming conventions, documentation, and common programming errors.
- **Bandit:** Identifies potential security vulnerabilities in Python code.
- **Flake8:** Checks Python style and common formatting violations.

## 3. Issues Identified and Fixes Applied

| Tool | Issue identified | Fix applied |
|---|---|---|
| Pylint | Missing module and function docstrings | Added documentation |
| Pylint | Non-standard camelCase function names | Renamed functions using snake_case |
| Pylint | Mutable default argument in `add_medicine()` | Replaced the mutable default with `None` |
| Pylint | Unused imports and formatting problems | Removed unused imports and corrected formatting |
| Bandit | Use of `eval()` | Replaced unrestricted evaluation with a restricted arithmetic expression evaluator |
| Bandit | Use of MD5 | Replaced MD5 with SHA-256 for the demonstration identifier |
| Bandit | Predictable random prescription references | Used the `secrets` module |
| Bandit | Unsafe `pickle` serialization | Replaced pickle storage with JSON |
| Bandit | Shell command execution using `os.system()` | Replaced it with direct output |
| Bandit | Hardcoded password | Read the configured password from an environment variable |
| Flake8 | Unused imports, bare exception handling, and line-length violations | Removed unused imports, corrected exception handling, and formatted the code |

## 4. Before-and-After Results

| Tool | Before | After |
|---|---|---|
| Pylint | 4.83/10 | 10.00/10 |
| Bandit | 8 potential issues, including 2 High-severity findings | 0 findings |
| Flake8 | 21 reported violations | 0 reported violations |

## 5. Conclusion

The analysis and subsequent fixes improved code readability, maintainability, formatting, and security. All three tools were run again after the changes. Pylint achieved a score of 10.00/10, Bandit reported no issues, and Flake8 produced no violations.