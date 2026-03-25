# Constraint Validation: Catching Invalid Tool Parameters

**Agents call the right tool with wrong parameters: dates in the past, check-out before check-in, negative amounts. This demo validates tool parameters with deterministic business rules (free, instant) and compares to LLM-based semantic checks.**

Based on research: [CCTU: Benchmark for Tool Use under Complex Constraints](https://arxiv.org/abs/2603.15309) (Mar 2026)

## Files

| File | Purpose |
|------|---------|
| `02-constraint-validation.ipynb` | **Main demo** — Constraint checker tests + live agent with validation hook |
| `constraint_checker.py` | **Standalone checker** — `validate_tool_call()` with rules per tool |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `02-constraint-validation.ipynb`. Tests constraint checker on known-bad inputs, then attaches a validation hook to a live agent.

```bash
# Or run standalone
python constraint_checker.py
```

## Research Background

- [CCTU](https://arxiv.org/abs/2603.15309) (Mar 2026) — 12 constraint categories, executable validation

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
