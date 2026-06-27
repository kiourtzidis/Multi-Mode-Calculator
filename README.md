A multi-mode calculator application built in Python using CustomTkinter, featuring a custom expression evaluation engine. Currently under development. Additional features and documentation will be added as development progresses.

## Current Features
- Basic Mode

## Unfinished Features
- Scientific Mode
- Graph Mode

## Planned Features
- Temperature Conversion Mode
- Currency Conversion Mode
- Date Calculation Mode

## Technical Details
- The calculator does not rely on Python's built-in `eval()` or `exec()` functions, nor external parsing libraries.
- The expression evaluation system was implemented from scratch using:
  - Custom Lexer
  - Token system
  - Pratt Parser
  - Abstract Syntax Tree (AST)
  - AST-based evaluator
