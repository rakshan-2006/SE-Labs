# Reflection — Static Code Analysis

## 1. What I Learned

This lab helped me understand how static code analysis tools identify code quality, formatting, and security issues without requiring manual inspection of every line.

Pylint helped identify documentation, naming, and maintainability problems. Bandit highlighted potentially unsafe operations, including unrestricted expression evaluation, insecure serialization, and shell command execution. Flake8 identified formatting and style violations.

## 2. Fixes Applied

I improved the code by adding docstrings, adopting snake_case naming, removing unused imports, avoiding mutable default arguments, and correcting formatting.

I also replaced unrestricted eval() with a restricted arithmetic evaluator, replaced pickle storage with JSON, removed shell command execution, replaced MD5 with SHA-256 for the demonstration identifier, and used the secrets module for prescription references.

The hardcoded password was removed in favour of an environment variable.

## 3. Results

The Pylint score improved from 4.83/10 to 10.00/10. Bandit findings decreased from 8 potential issues to zero, and Flake8 violations decreased from 21 to zero.

These results demonstrate how static analysis can guide systematic improvements in Python code.

## 4. Conclusion

Static analysis is useful for identifying issues early and improving readability, maintainability, and security. However, clean static-analysis reports do not guarantee that a program is free from every bug or security risk. Testing and careful review remain necessary.
