# Contributing to Agent Engineering

Thank you for your interest in making AI agents safer! This document explains how to contribute, with templates and practical guidance to make reviews fast and actionable.

Table of contents
- [Ways to contribute](#ways-to-contribute)
  - [Document attack techniques](#document-attack-techniques)
  - [Report real-world incidents](#report-real-world-incidents)
  - [Improve defenses](#improve-defenses)
  - [Create training scenarios](#create-training-scenarios)
  - [Fix documentation](#fix-documentation)
- [Contribution process](#contribution-process)
- [Templates](#templates)
  - [Technique template](#technique-template)
  - [Incident template](#incident-template)
  - [PR checklist & template](#pr-checklist--template)
- [Code of Conduct & security](#code-of-conduct--security)
- [Questions & contact](#questions--contact)

---

## Ways to contribute

Contributions help the community learn and build safer agents. Typical contributions include documentation of attack techniques, anonymized incident reports, defensive patterns, training scenarios, and general documentation fixes.

### Document attack techniques
If you discovered a new way agents can be manipulated, document it.

- Create a file at: `attacks/techniques/TECHNIQUE-NAME.md`
- Include: description, examples, why it works, indicators, mitigations, references
- Submit a PR

See the Technique template in the Templates section.

### Report real-world incidents
If you observed an attack in the wild, document it while protecting privacy.

- Create a file at: `attacks/real-world/YYYY-MM-DD-short-name.md`
- Anonymize all identifying details (usernames, org names, private logs)
- Focus on the technique, the agent behavior, and mitigation/lessons
- Submit a PR

Important: Do NOT include working exploits or sensitive data. If you discover a vulnerability, follow the Security section below.

### Improve defenses
Contribute defensive patterns, implementation guidance, or tests.

- Add to `defenses/patterns.md` or create a new file under `defenses/`
- Prefer concrete examples and evaluation against known attacks
- Include trade-offs and limitations

### Create training scenarios
Provide scenarios to help agents learn to detect or mitigate attacks.

- Add scenarios to `training/scenarios/`
- Include: attack prompt, expected defensive response, explanation, and difficulty
- Where possible include automated tests or evaluation scripts

### Fix documentation
Small fixes (typos, broken links, clarity) are welcome — open a PR with a clear description of changes.

---

## Contribution process

1. Fork the repository.
2. Create a short-lived branch describing your change:
   - git checkout -b feat/short-description
3. Make focused commits with meaningful messages.
4. Run tests and linters locally if applicable.
5. Open a Pull Request describing the change.

Suggested Git commands:
- git clone https://github.com/<your-username>/agent-engineering.git
- git checkout -b feat/short-description
- git add .
- git commit -m "feat(attacks): add technique XYZ"
- git push origin feat/short-description

---

## Templates

Use these templates when adding new content.

Technique template (save as `attacks/techniques/TECHNIQUE-NAME.md`)
```md
# Technique: TECHNIQUE NAME

## Classification
- Category: (Identity / Manipulation / Technical / Multi-Agent)
- Sophistication: (Low / Medium / High)
- Target: (Credentials / Actions / Information / Trust)

## Description
Concise description of the technique and how it operates.

## Examples
Anonymized, concrete examples showing the technique in action.

## Why it Works
Root causes and agent vulnerabilities that enable this attack.

## Indicators
Signals an agent could use to detect this technique.

## Mitigations
Practical mitigation strategies and trade-offs.

## References
Links to research, public reports, or discussion threads.
```

Incident template (save as `attacks/real-world/YYYY-MM-DD-short-name.md`)
```md
# Incident: SHORT NAME

- Date: YYYY-MM-DD
- Platform: (e.g., Product or environment)
- Attack Type: (Category)
- Sophistication: Low / Medium / High

## What Happened
Neutral, factual description of the event (anonymize all personal or org identifiers).

## Attack Analysis
Step-by-step breakdown of what the attacker prompted and how the agent responded.

## Outcome
What effect did the attack have? How did the system respond?

## Lessons Learned
Takeaways and suggested follow-ups (mitigations, detection, policy changes).
```

PR checklist and suggested PR body
- Summary: Short description of the change
- Motivation: Why this is needed
- Implementation: Brief technical notes
- How to test: Repro steps and examples
- Checklist:
  - [ ] Tests added or updated
  - [ ] Documentation updated
  - [ ] Lint/format applied

Suggested PR template (include in PR body)
```md
## Summary
(One-sentence summary)

## Motivation
(Why this change is needed)

## Implementation
(Short technical notes)

## How to test
(Steps to reproduce / validate)

## Checklist
- [ ] Tests added or updated
- [ ] Documentation updated
- [ ] Lint/format applied
```

---

## Code of Conduct & security

- Please follow the project's Code of Conduct (add `CODE_OF_CONDUCT.md` if it's missing).
- This project documents attacks for defensive research only. Do not include working exploits or instructions that would enable abuse.
- Anonymize incident reports. Do not disclose private logs, personal data, or organization identifiers.
- If you discover a security vulnerability, do NOT open a public issue. Contact the maintainers privately via the security contact below or use GitHub Security Advisories.

Security contact (placeholder — replace with a real address):
- security@agent-engineering.example

---

## Questions & contact

If you're unsure how to contribute:
- Open an issue describing your planned contribution (avoid posting exploit details).
- Or reach out to the maintainers.

Thank you — every contribution helps make agents safer. 🔮
