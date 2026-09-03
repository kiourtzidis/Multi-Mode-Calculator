A multi-mode calculator application built in Python using CustomTkinter, featuring a custom expression evaluation engine. Currently under development. Additional features will be added as development progresses.

## Current Features
- Basic Mode
- Scientific Mode
- Unit Conversion Mode
- Currency Conversion Mode

## Unfinished Features
- Graph Mode

## Planned Features
- Date Calculation Mode

## Technical Details
- The calculator does not rely on Python's built-in `eval()` or `exec()` functions, nor external parsing libraries.
- The expression evaluation system was implemented from scratch using:
  - Custom Lexer
  - Token system
  - Pratt Parser
  - Abstract Syntax Tree (AST)
  - AST-based evaluator
