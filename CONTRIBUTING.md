Contributing to Agent Engineering
Thank you for your interest in making AI agents safer! This document explains how to contribute.

Ways to Contribute
1. Document Attack Techniques
Found a new way agents can be manipulated? Document it:

Create a file in attacks/techniques/ using the template below
Include: description, examples, why it works, indicators, mitigations
Submit a PR
Template: attacks/techniques/TECHNIQUE-NAME.md

# Technique Name

## Classification
- **Category:** (Identity/Manipulation/Technical/Multi-Agent)
- **Sophistication:** (Low/Medium/High)
- **Target:** (Credentials/Actions/Information/Trust)

## Description
What is this technique and how does it work?

## Examples
Concrete examples of this attack in action.

## Why It Works
What makes agents vulnerable to this?

## Indicators
How can an agent recognize this attack?

## Mitigations
How can agents defend against this?

## References
Links to related research, incidents, or discussions.
2. Report Real-World Incidents
Seen an attack in the wild? Document it (anonymized):

Create a file in attacks/real-world/ with format YYYY-MM-DD-short-name.md
Remove any identifying information
Focus on the technique, not the attacker
Template: attacks/real-world/YYYY-MM-DD-incident-name.md

# Incident: Short Name

- **Date:** YYYY-MM-DD
- **Platform:** Where it occurred
- **Attack Type:** Classification
- **Sophistication:** Low/Medium/High

## What Happened
Describe the attack.

## Attack Analysis
Break down the technique used.

## Outcome
How did the target agent respond?

## Lessons Learned
What can we learn from this?
3. Improve Defenses
Have ideas for better defense patterns?

Add to defenses/patterns.md or create new files
Include practical implementation guidance
Test against known attacks if possible
4. Create Training Scenarios
Help agents learn to recognize attacks:

Add scenarios to training/scenarios/
Include the attack prompt, expected defense, and explanation
Vary difficulty levels
5. Fix Documentation
Typos, unclear explanations, broken links — all welcome fixes.

Contribution Process
Fork the repository
Create a branch for your contribution
Make your changes following the templates above
Submit a PR with a clear description
Code of Conduct
Focus on security, not attacking real agents
Anonymize all incident reports
Don't include working exploits against specific platforms
Be respectful and constructive
Questions?
Open an issue or reach out to the maintainers.

Every contribution makes agents safer. 🔮
