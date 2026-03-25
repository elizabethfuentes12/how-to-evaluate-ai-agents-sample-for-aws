# Guardrail Hooks: Blocking Unsafe Tool Calls in Real-Time

**Post-hoc evaluation catches problems after the user sees them. This demo blocks dangerous tool calls (booking, cancellation) before execution using Strands hooks with `event.cancel_tool`.**

Based on: [StepShield](https://arxiv.org/abs/2601.22136) (Jan 2026)

## Files

| File | Purpose |
|------|---------|
| `03-guardrail-hooks.ipynb` | **Main demo** — SafetyGuardrail hook blocking book_hotel and cancel_booking |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `03-guardrail-hooks.ipynb`. Runs 3 queries: 1 safe (allowed), 2 dangerous (blocked).

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
