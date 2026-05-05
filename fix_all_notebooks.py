#!/usr/bin/env python3
"""
Fix all notebooks to use explicit OpenAIModel instead of string model IDs.

This prevents Strands from inferring Bedrock when AWS credentials are present.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

def find_strands_notebooks(root_dir: Path) -> List[Path]:
    """Find all notebooks that use strands."""
    notebooks = []
    for notebook_path in root_dir.rglob("*.ipynb"):
        # Skip checkpoints
        if ".ipynb_checkpoints" in str(notebook_path):
            continue

        # Skip already fixed
        if "00-blog-framework-comparison" in str(notebook_path):
            print(f"  ⏭️  Skipping (already fixed): {notebook_path.name}")
            continue

        with open(notebook_path, 'r') as f:
            content = f.read()
            if 'strands' in content.lower():
                notebooks.append(notebook_path)

    return notebooks

def read_notebook(path: Path) -> Dict:
    """Read notebook as JSON."""
    with open(path, 'r') as f:
        return json.load(f)

def write_notebook(path: Path, notebook: Dict):
    """Write notebook as JSON."""
    with open(path, 'w') as f:
        json.dump(notebook, f, indent=1)

def get_cell_source(cell: Dict) -> str:
    """Get cell source as string."""
    source = cell.get('source', '')
    if isinstance(source, list):
        return ''.join(source)
    return source

def set_cell_source(cell: Dict, new_source: str):
    """Set cell source (preserve list format if it was list)."""
    if isinstance(cell.get('source', ''), list):
        # Convert string to list of lines
        cell['source'] = [line + '\n' if i < len(new_source.split('\n')) - 1 else line
                         for i, line in enumerate(new_source.split('\n'))]
    else:
        cell['source'] = new_source

def has_openai_model_import(source: str) -> bool:
    """Check if cell already imports OpenAIModel."""
    return 'from strands.models.openai import OpenAIModel' in source

def has_model_string_issue(source: str) -> bool:
    """Check if cell uses model as string instead of object."""
    patterns = [
        r'model\s*=\s*["\']gpt-',           # model="gpt-4o-mini"
        r'MODEL\s*=\s*["\']gpt-',           # MODEL = "gpt-4o-mini"
        r'OpenAIModel\(model_id=["\']',     # Already has OpenAIModel
    ]

    # Has model string issue if matches first two patterns
    has_string = bool(re.search(patterns[0], source) or re.search(patterns[1], source))
    # But not if already using OpenAIModel
    already_fixed = bool(re.search(patterns[2], source))

    return has_string and not already_fixed

def fix_cell_source(source: str) -> Tuple[str, bool]:
    """
    Fix cell source to use OpenAIModel.
    Returns (fixed_source, was_modified).
    """
    if not has_model_string_issue(source):
        return source, False

    modified = False
    new_source = source

    # Add import if not present
    if not has_openai_model_import(source):
        # Find where to insert import (after other strands imports)
        lines = source.split('\n')
        insert_idx = 0

        for i, line in enumerate(lines):
            if 'from strands' in line or 'import strands' in line:
                insert_idx = i + 1
            elif line.strip() and not line.strip().startswith('#') and insert_idx > 0:
                # Found first non-import line after imports
                break

        if insert_idx > 0:
            lines.insert(insert_idx, 'from strands.models.openai import OpenAIModel')
            new_source = '\n'.join(lines)
            modified = True

    # Fix MODEL = "gpt-4o-mini" pattern
    pattern1 = r'MODEL\s*=\s*["\']([^"\']+)["\']'
    if re.search(pattern1, new_source):
        new_source = re.sub(
            pattern1,
            r'MODEL = OpenAIModel(model_id="\1")',
            new_source
        )
        modified = True

    # Fix model="gpt-4o-mini" in function calls
    pattern2 = r'model\s*=\s*["\']([^"\']+)["\']'
    matches = list(re.finditer(pattern2, new_source))

    # Process from end to start to preserve indices
    for match in reversed(matches):
        model_value = match.group(1)
        if model_value.startswith('gpt-') or model_value.startswith('claude-'):
            # Check if this is inside a function call (not a variable assignment)
            before = new_source[:match.start()]
            if '=' in before.split('\n')[-1] and 'MODEL' not in before.split('\n')[-1]:
                # This is model= in a function call, replace it
                new_source = (
                    new_source[:match.start()] +
                    f'model=OpenAIModel(model_id="{model_value}")' +
                    new_source[match.end():]
                )
                modified = True

    return new_source, modified

def fix_notebook(notebook_path: Path, dry_run: bool = False) -> Dict[str, int]:
    """
    Fix a single notebook.
    Returns stats: {cells_modified, cells_total}.
    """
    notebook = read_notebook(notebook_path)
    cells_modified = 0
    cells_total = len(notebook.get('cells', []))

    for cell in notebook.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue

        source = get_cell_source(cell)
        fixed_source, was_modified = fix_cell_source(source)

        if was_modified:
            cells_modified += 1
            if not dry_run:
                set_cell_source(cell, fixed_source)

    if cells_modified > 0 and not dry_run:
        write_notebook(notebook_path, notebook)

    return {
        'cells_modified': cells_modified,
        'cells_total': cells_total,
        'notebook_path': notebook_path,
    }

def main():
    """Main script."""
    print("=" * 70)
    print("🔧 Automated Notebook Fix: model string → OpenAIModel")
    print("=" * 70)

    root_dir = Path('/Users/eliaws/Documents/repositories/how-to-evaluate-ai-agents-sample-for-aws')

    print("\n📂 Finding Strands notebooks...")
    notebooks = find_strands_notebooks(root_dir)
    print(f"   Found {len(notebooks)} notebooks to check\n")

    # Dry run first
    print("🔍 Analyzing notebooks (dry run)...")
    results = []
    for notebook_path in notebooks:
        result = fix_notebook(notebook_path, dry_run=True)
        if result['cells_modified'] > 0:
            results.append(result)
            rel_path = notebook_path.relative_to(root_dir)
            print(f"   ⚠️  {rel_path}")
            print(f"      {result['cells_modified']}/{result['cells_total']} cells need fixing")

    if not results:
        print("\n✅ All notebooks are already fixed!")
        return

    print(f"\n📊 Summary:")
    print(f"   {len(results)} notebooks need fixes")
    print(f"   {sum(r['cells_modified'] for r in results)} total cells to modify")

    # Auto-apply fixes (no confirmation needed)
    print("\n🔨 Applying fixes automatically...")

    # Apply fixes
    print("\n🔨 Applying fixes...")
    for result in results:
        notebook_path = result['notebook_path']
        fix_notebook(notebook_path, dry_run=False)
        rel_path = notebook_path.relative_to(root_dir)
        print(f"   ✅ Fixed: {rel_path}")

    print("\n" + "=" * 70)
    print(f"✅ Complete! Fixed {len(results)} notebooks")
    print("=" * 70)
    print("\nChanges applied:")
    print("  • Added: from strands.models.openai import OpenAIModel")
    print("  • Replaced: MODEL = \"gpt-4o-mini\"")
    print("  • With: MODEL = OpenAIModel(model_id=\"gpt-4o-mini\")")
    print("  • Replaced: model=\"gpt-4o-mini\"")
    print("  • With: model=OpenAIModel(model_id=\"gpt-4o-mini\")")

if __name__ == "__main__":
    main()
