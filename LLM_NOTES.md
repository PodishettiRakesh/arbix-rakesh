# LLM Notes

This file documents example prompts used during the Arbix AI practical exercise and one correction made after reviewing tool output.

## Example Prompts (paraphrased)

1. **Project planning**
   - "How should I structure a small FastAPI project for a scoring API with tests and a React frontend?"

2. **Scoring logic**
   - "Suggest a simple explainable credit scoring algorithm using land area, repayment history, and income band with exactly 3 reason codes."

3. **Testing**
   - "Generate FastAPI unit test ideas for a POST /score endpoint — one happy path and one validation error case."

4. **Logging**
   - "How should structured logging look for audit trails on a scoring API without logging sensitive fields?"

5. **Frontend integration**
   - "How can a minimal React form call a FastAPI /score endpoint and display validation errors inline?"

## Correction Example

After reviewing generated scoring logic, I adjusted the implementation to ensure:

- The final score is always capped at `100` using `min(100, round(score, 2))`
- Exactly **3** reason codes are always returned: `[repayment_reason, land_reason, income_reason]`
- Land area boundary at `2` and `5` acres was verified against the spec (`>= 2` = medium, `> 5` = large)
- Frontend validation errors were moved inline under each field instead of only showing a single bottom alert

## Personal Review Checklist

- [x] Ran `pytest -v` after each backend phase
- [x] Verified `POST /score` via Swagger and curl
- [x] Tested frontend form against live backend on port `8002`
- [x] Confirmed audit logs exclude `crop_type` and other sensitive fields
