# Element451 Calculated Fields V2

Element451 Calculated Fields V2 is an AI skill that helps Element451 users create, understand, test, and troubleshoot calculated-field formulas—even if they have little or no experience writing formulas.

## What the skill can help with

The skill can create formulas for:

- Imports
- Exports
- Workflow and Rule Formula Fields
- Calculated payments

It can help with tasks such as:

- Building conditional logic
- Cleaning and formatting text
- Mapping values, GUIDs, terms, majors, and taxonomy data
- Parsing, validating, and formatting dates
- Handling time zones and daylight saving time
- Working with application and milestone root fields
- Counting matching records
- Finding the latest or earliest matching value
- Returning a value associated with the winning record
- Preventing blank values from becoming incorrect dates or numbers
- Troubleshooting formula errors, Preview Export problems, and values that evaluate correctly but do not save

For complex formulas, the skill can produce a complete paste-ready formula, explain how it works, identify important assumptions, and suggest test cases.

## What to provide

Users can describe what they need in plain language. For the best result, include:

- Where the formula will be used: Import, Export, Workflow/Rule Formula Field, or calculated payment
- The source columns or Element field slugs
- The desired result
- Any required conditions, priorities, exclusions, or fallback behavior
- Institution-specific GUIDs or mappings
- A redacted sample when working with application, milestone, or other repeatable root-field data

Do not share API keys, passwords, or unnecessary student information.

## Example request

> Create an export formula that finds the most recent Deposit milestone for a specific application and set of terms. Exclude one major, allow milestones with no major, return the date as MM/DD/YYYY, and return a blank value if no qualifying milestone exists.

## Tenant-neutral design

The skill does not assume that every institution uses the same fields, GUIDs, terms, majors, labels, or business rules. Users should supply the identifiers and mappings from their own Element451 instance.

Examples included in the skill use fictional or generalized values to demonstrate formula techniques.

## Repository contents

- `SKILL.md` contains the main instructions and workflow.
- `references/` contains function guidance, formula patterns, root-field techniques, testing notes, and documented runtime observations.
- `scripts/` contains formatting, linting, formula-building, and diagnostic utilities.
- `agents/` contains the skill interface configuration.
- `assets/` contains the skill icon.

## Important note

This is an independent community resource and is not an official Element451 product. Formula behavior can vary by context, so complex formulas should be tested in Element451. Export formulas should be checked in both Test Formula/Evaluate and Preview Export.
