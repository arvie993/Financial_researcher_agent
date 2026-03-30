#!/usr/bin/env python
# src/financial_researcher/main.py
import os
from datetime import date

import litellm
litellm.drop_params = True

_original_completion = litellm.completion
def _patched_completion(*args, **kwargs):
    kwargs.pop("stop", None)
    return _original_completion(*args, **kwargs)
litellm.completion = _patched_completion

from financial_researcher.crew import FinancialResearcher

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the Financial Researcher crew.
    """
    today = date.today()
    inputs = {
        'company': 'Tesla',
        'current_date': today.strftime('%B %d, %Y'),
        'current_year': str(today.year),
    }

    # Create and run the crew
    result = FinancialResearcher().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    run()