# How to Run This Notebook

## ✅ Works Anywhere

The notebook now works in **any environment** (terminal, Jupyter, scripts) thanks to using explicit `OpenAIModel`.

## Quick Start

### Option 1: Jupyter Notebook (Recommended for Interactive Use)

```bash
# 1. Navigate to directory
cd 00-blog-framework-comparison

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Ensure dependencies are installed
uv pip install -r requirements.txt

# 4. Start Jupyter
jupyter notebook

# 5. In Jupyter web interface:
#    - Open: 01-framework-comparison.ipynb
#    - Click: Cell → Run All
```

### Option 2: Python Script (For Automation)

```bash
cd 00-blog-framework-comparison
source .venv/bin/activate
jupyter nbconvert --to script 01-framework-comparison.ipynb
python 01-framework-comparison.py
```

Both work identically now!

## The Fix

The notebook uses **explicit `OpenAIModel`** instead of string model IDs:

```python
from strands.models.openai import OpenAIModel

JUDGE_MODEL = OpenAIModel(model_id="gpt-4o-mini")
```

This forces Strands to use OpenAI regardless of AWS environment variables.

## Expected Output

### Cell 1 (Setup)
```
✓ Using explicit OpenAI model: <strands.models.openai.OpenAIModel object at 0x...>
Loaded 3 test cases: ['flight_search_good', 'flight_search_hallucinated', 'weather_query']
nest_asyncio applied (fixes Jupyter event loop conflict)
```

### Cell 2 (Strands Round 1)
```
Strands: Output Quality (2.9s)
╭──────────────────────────── 📊 Evaluation Report ────────────────────────────╮
│ Overall Score: 1.00           ...                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```
**Scores should be > 0.0** (not 0.00). ✅

### Cell 3 (PydanticAI Round 1)
```
Evaluating pydantic_task ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

--- PydanticAI: Output Quality (3.7s) ---
                       Evaluation Summary: pydantic_task
```

### Cell 4 (DeepEval Round 1)
```
✨ You're running DeepEval's latest Helpfulness [GEval] Metric!...

Overall Metric Pass Rates
Helpfulness [GEval]: 66.67% pass rate
```

## Troubleshooting

### "Unable to locate credentials" (Strands)

This should NOT happen with the explicit `OpenAIModel`. If you see this:

**Check:**
1. Is `OPENAI_API_KEY` environment variable set?
   ```bash
   echo $OPENAI_API_KEY  # Should print sk-...
   ```
2. Did you use explicit `OpenAIModel` in the code?
   ```python
   from strands.models.openai import OpenAIModel
   JUDGE_MODEL = OpenAIModel(model_id="gpt-4o-mini")
   ```

### "The provided model identifier is invalid" (Strands)

This means Strands is still trying to use Bedrock. This should NOT happen with explicit `OpenAIModel`.

**Fix:**
1. Verify the notebook setup cell shows:
   ```
   ✓ Using explicit OpenAI model: <strands.models.openai.OpenAIModel object...>
   ```
2. If using a script, make sure you converted the updated notebook:
   ```bash
   jupyter nbconvert --to script 01-framework-comparison.ipynb --output notebook_updated.py
   python notebook_updated.py
   ```

### PydanticAI or DeepEval errors

These frameworks use OpenAI directly and should work regardless of configuration.

If you see errors:
1. Verify `OPENAI_API_KEY` environment variable is set
2. Check your OpenAI API quota/credits at https://platform.openai.com/usage
3. Try running just the PydanticAI or DeepEval cells independently

## Verification Checklist

When the notebook runs correctly:

- [x] Setup cell prints: "✓ Using explicit OpenAI model"
- [x] Strands evaluations return scores > 0.0 (not 0.00)
- [x] PydanticAI shows evaluation progress bar
- [x] DeepEval shows metric summaries
- [x] No "ValidationException" errors
- [x] No "Unable to locate credentials" errors
- [x] Timing comparison table displays at end
- [x] Visualization charts render correctly

## Performance Expectations

Typical execution times for 3 test cases:

| Framework | Time | Why |
|-----------|------|-----|
| Strands | 2-4s | Direct API calls to OpenAI |
| PydanticAI | 3-5s | Type validation + API calls |
| DeepEval | 4-6s | Additional metric processing |

Total notebook execution: **~20-30 minutes** (includes all 3 rounds × 3 frameworks)

## Environment Variables Required

```bash
export OPENAI_API_KEY=sk-...  # Required for all frameworks
```

Optional (but handled automatically):
```bash
# These are from Claude Code - notebook handles them automatically
# You don't need to set or unset these manually
export CLAUDE_CODE_USE_BEDROCK=1  
export AWS_BEARER_TOKEN=...
```

The explicit `OpenAIModel` solution works regardless of these AWS variables.
