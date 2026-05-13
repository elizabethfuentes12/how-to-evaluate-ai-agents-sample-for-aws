import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as path_effects

# Create figure with dark background
fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor('#0a0a0a')  # Very dark background
ax.set_facecolor('#0a0a0a')
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# Title and subtitle with white text
title = ax.text(8, 9.2, '3 Ways to Evaluate AI Agents', 
                ha='center', va='top', fontsize=42, fontweight='bold', 
                color='white', family='sans-serif')

subtitle = ax.text(8, 8.5, 'Framework Comparison: Strands Agents, PydanticAI, DeepEval',
                   ha='center', va='top', fontsize=24, 
                   color='#cccccc', family='sans-serif')

# Common styling
box_width = 2.5
box_height = 1.2
oval_width = 2.2
oval_height = 1.0

# Starting X position for Agent Output box
start_x = 1.5
start_y = 5.0

# Agent Output box (white/light gray)
agent_box = FancyBboxPatch((start_x, start_y - box_height/2), box_width, box_height,
                           boxstyle="round,pad=0.1", 
                           edgecolor='white', facecolor='#2a2a2a',
                           linewidth=3)
ax.add_patch(agent_box)
ax.text(start_x + box_width/2, start_y, 'Agent\nOutput',
        ha='center', va='center', fontsize=22, fontweight='bold',
        color='white', family='sans-serif')

# === ROW 1: Strands Agents (Blue) ===
row1_y = 6.5

# Arrow from Agent Output to Strands
arrow1 = FancyArrowPatch((start_x + box_width, start_y), (5.0, row1_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#4A9EFF')
ax.add_patch(arrow1)

# Strands Agents box
strands_x = 5.0
strands_box = FancyBboxPatch((strands_x, row1_y - box_height/2), box_width, box_height,
                            boxstyle="round,pad=0.1",
                            edgecolor='#4A9EFF', facecolor='#1a3a5a',
                            linewidth=3)
ax.add_patch(strands_box)
ax.text(strands_x + box_width/2, row1_y, 'Strands\nAgents',
        ha='center', va='center', fontsize=22, fontweight='bold',
        color='#4A9EFF', family='sans-serif')

# Arrow to OutputEvaluator
arrow2 = FancyArrowPatch((strands_x + box_width, row1_y), (8.5, row1_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#4A9EFF')
ax.add_patch(arrow2)

# OutputEvaluator box
eval_x = 8.5
eval_box = FancyBboxPatch((eval_x, row1_y - box_height/2), box_width, box_height,
                         boxstyle="round,pad=0.1",
                         edgecolor='#4A9EFF', facecolor='#2a4a6a',
                         linewidth=3)
ax.add_patch(eval_box)
ax.text(eval_x + box_width/2, row1_y, 'OutputEvaluator\n+ Experiment',
        ha='center', va='center', fontsize=20, fontweight='bold',
        color='#66B2FF', family='sans-serif')

# Arrow to Score oval
arrow3 = FancyArrowPatch((eval_x + box_width, row1_y), (12.5, row1_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#4A9EFF')
ax.add_patch(arrow3)

# Score oval
score_x = 12.5
score_oval = mpatches.Ellipse((score_x + oval_width/2, row1_y), oval_width, oval_height,
                             edgecolor='#4A9EFF', facecolor='#3a5a8a',
                             linewidth=3)
ax.add_patch(score_oval)
ax.text(score_x + oval_width/2, row1_y, 'Score\n+ Reason',
        ha='center', va='center', fontsize=20, fontweight='bold',
        color='#66B2FF', family='sans-serif')

# === ROW 2: PydanticAI (Green) ===
row2_y = 4.5

# Arrow from Agent Output to PydanticAI
arrow4 = FancyArrowPatch((start_x + box_width, start_y), (5.0, row2_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#5CB85C')
ax.add_patch(arrow4)

# PydanticAI box
pydantic_x = 5.0
pydantic_box = FancyBboxPatch((pydantic_x, row2_y - box_height/2), box_width, box_height,
                             boxstyle="round,pad=0.1",
                             edgecolor='#5CB85C', facecolor='#1a3a1a',
                             linewidth=3)
ax.add_patch(pydantic_box)
ax.text(pydantic_x + box_width/2, row2_y, 'PydanticAI',
        ha='center', va='center', fontsize=22, fontweight='bold',
        color='#5CB85C', family='sans-serif')

# Arrow to LLMJudge
arrow5 = FancyArrowPatch((pydantic_x + box_width, row2_y), (8.5, row2_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#5CB85C')
ax.add_patch(arrow5)

# LLMJudge box
judge_x = 8.5
judge_box = FancyBboxPatch((judge_x, row2_y - box_height/2), box_width, box_height,
                          boxstyle="round,pad=0.1",
                          edgecolor='#5CB85C', facecolor='#2a4a2a',
                          linewidth=3)
ax.add_patch(judge_box)
ax.text(judge_x + box_width/2, row2_y, 'LLMJudge\n+ Dataset',
        ha='center', va='center', fontsize=20, fontweight='bold',
        color='#7FD77F', family='sans-serif')

# Arrow to Score oval
arrow6 = FancyArrowPatch((judge_x + box_width, row2_y), (12.5, row2_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#5CB85C')
ax.add_patch(arrow6)

# Score oval
score2_oval = mpatches.Ellipse((score_x + oval_width/2, row2_y), oval_width, oval_height,
                              edgecolor='#5CB85C', facecolor='#3a5a3a',
                              linewidth=3)
ax.add_patch(score2_oval)
ax.text(score_x + oval_width/2, row2_y, 'Score\n+ Pass/Fail',
        ha='center', va='center', fontsize=20, fontweight='bold',
        color='#7FD77F', family='sans-serif')

# === ROW 3: DeepEval (Orange) ===
row3_y = 3.0

# Arrow from Agent Output to DeepEval
arrow7 = FancyArrowPatch((start_x + box_width, start_y), (5.0, row3_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#FF9933')
ax.add_patch(arrow7)

# DeepEval box
deepeval_x = 5.0
deepeval_box = FancyBboxPatch((deepeval_x, row3_y - box_height/2), box_width, box_height,
                             boxstyle="round,pad=0.1",
                             edgecolor='#FF9933', facecolor='#3a2a1a',
                             linewidth=3)
ax.add_patch(deepeval_box)
ax.text(deepeval_x + box_width/2, row3_y, 'DeepEval',
        ha='center', va='center', fontsize=22, fontweight='bold',
        color='#FF9933', family='sans-serif')

# Arrow to GEval
arrow8 = FancyArrowPatch((deepeval_x + box_width, row3_y), (8.5, row3_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#FF9933')
ax.add_patch(arrow8)

# GEval box
geval_x = 8.5
geval_box = FancyBboxPatch((geval_x, row3_y - box_height/2), box_width, box_height,
                          boxstyle="round,pad=0.1",
                          edgecolor='#FF9933', facecolor='#4a3a2a',
                          linewidth=3)
ax.add_patch(geval_box)
ax.text(geval_x + box_width/2, row3_y, 'GEval\n+ evaluate()',
        ha='center', va='center', fontsize=20, fontweight='bold',
        color='#FFB366', family='sans-serif')

# Arrow to Score oval
arrow9 = FancyArrowPatch((geval_x + box_width, row3_y), (12.5, row3_y),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color='#FF9933')
ax.add_patch(arrow9)

# Score oval
score3_oval = mpatches.Ellipse((score_x + oval_width/2, row3_y), oval_width, oval_height,
                              edgecolor='#FF9933', facecolor='#5a4a3a',
                              linewidth=3)
ax.add_patch(score3_oval)
ax.text(score_x + oval_width/2, row3_y, 'Score\n+ Reason',
        ha='center', va='center', fontsize=20, fontweight='bold',
        color='#FFB366', family='sans-serif')

# Add margins for dev.to cropping
plt.tight_layout(pad=1.5)

# Save with dark background
plt.savefig('3-ways-evaluate-ai-agents-framework-comparison-cover.png', 
            dpi=150, bbox_inches='tight', facecolor='#0a0a0a', edgecolor='none')
print("✓ Dark background cover image generated successfully")
