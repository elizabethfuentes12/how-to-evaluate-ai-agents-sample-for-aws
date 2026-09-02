# Red Teaming AI Agents: Generate Multi-Turn Attacks Without Scripting Them

**Red teaming generates adversarial, multi-turn attacks (jailbreaks, data-exfiltration and policy-violation attempts) and measures whether your agent holds. Strands Evals writes and runs the attack conversations for you, so you don't hand-script each turn.** This demo points the red team at a travel agent with a sensitive surface, using [Strands Evals 1.0](https://github.com/strands-agents/evals).

*Last updated: 2026-06-20*

## Files

| File | Purpose |
|------|---------|
| `redteam_demo.ipynb` | **Main demo** — generate attack cases, run multi-turn Crescendo attacks, score defense, and read the attack's cost (turns + transcript size) |
| `tools.py` | Travel agent with a sensitive surface: stored payment card (`get_passenger_profile`) and a booking policy limit (`book_flight`) |
| `.env.example` | `OPENAI_API_KEY`, `DUFFEL_API_KEY` |
| `requirements.txt` | `strands-agents-evals>=1.0.0` and friends |

## What does the demo show?

A travel agent holds a passenger profile (with a stored card) and can book flights under a security policy. The red team attacks two risks and we measure whether the agent defends:

| Risk category | The attacker tries to... | The agent's policy |
|---------------|--------------------------|--------------------|
| `data_exfiltration` | Extract the full card number / CVV | Never reveal full card or CVV |
| `excessive_agency` | Book above the auto-approve limit | Refuse bookings over the USD limit without human approval |

## How does Strands red teaming work?

Three pieces, all in `strands_evals.experimental.redteam`:

- **`AdversarialCaseGenerator`** reads your agent's prompt and tools and writes attack cases for the risk categories you name.
- **`CrescendoStrategy`** runs each case as a multi-turn conversation that escalates and backtracks on refusals — the part you'd otherwise script by hand.
- **`AttackSuccessEvaluator`** (default judge) scores each attack 0.0–1.0. **Higher = the attack succeeded**; `test_pass=True` means the agent **defended**.

## One run is not a security verdict

Attack outcomes are stochastic. Across repeated runs of the identical setup, the agent defended most of the time and was breached occasionally (a partial `data_exfiltration` or `excessive_agency` leak). **Agent security is a distribution, not a fixed property** — run many times and track the breach *rate*, the same lesson as [01 - Chaos Testing](../01-chaos-testing/). A single clean pass is falsely reassuring; a single breach isn't proof of a broken agent either.

## What does an attack cost?

Red teaming isn't free: every attack is a multi-turn conversation. The demo reads `turns_used`, `backtracks`, and the full `conversation` from the report, so you can see the campaign's cost (and estimate its tokens). More turns and backtracks = a more expensive run. Budget it like any eval: start with few cases and few turns, then scale.

## How do I run it?

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # set OPENAI_API_KEY and DUFFEL_API_KEY
```

Open `redteam_demo.ipynb` and run top to bottom.

> A free Duffel **sandbox** token is at [app.duffel.com](https://app.duffel.com): **More → Developers → Access tokens**, create a test token.

> Travel-agent tools adapted, with thanks, from [Ricardo Ceci's `curso-strands-agentcore-2026`](https://github.com/ricardoceci/curso-strands-agentcore-2026).

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../LICENSE) file for details.
