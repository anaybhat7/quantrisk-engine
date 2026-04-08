import matplotlib.pyplot as plt
from pathlib import Path

def save_backtest_outputs(fig, report_text, prefix="advanced"):
    """
    Saves the backtest chart and statistical summary to the utils directory.
    """
    out_dir = Path("utils")
    
    # Save the plot
    fig_path = out_dir / f"{prefix}_backtest_chart.png"
    fig.savefig(fig_path, bbox_inches='tight', dpi=300)
    
    # Save the text report
    txt_path = out_dir / f"{prefix}_summary.txt"
    with open(txt_path, "w") as f:
        f.write(report_text)
        
    print(f"\n[SUCCESS] Outputs saved to:")
    print(f" -> {fig_path}")
    print(f" -> {txt_path}")