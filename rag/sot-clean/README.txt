# SoT Collection — RAG Corpus

**Corpus:** 23 research documents from Nava Healthcare's "School of Thought" (SoT) research series.
**Topic:** Healthcare staffing, clinician recruitment, agency models, travel nursing, visa pathways, and workforce strategy.
**Location:** `/root/.openclaw/workspace/rag/sot-clean/`

---

## Documents (23 files)

1. sot_Agency_Nurse_Dependency_Impacts_and_Solutions.txt
2. sot_Bilingual_Clinicians_Literature_Review__Analysis.txt
3. sot_Clinician_Soft_Skills_Impact_and_Recruitment.txt
4. sot_Clinician_Turnover_Root_Cause_Analysis.txt
5. sot_Contingent_Staffing_and_Patient_Outcomes.txt
6. sot_Healthcare_Agency_Conversion_Fees_Explained.txt
7. sot_Healthcare_Benefits_Waiting_Period_Research.txt
8. sot_Healthcare_Reputation_Drivers_Patient__Clinician.txt
9. sot_Healthcare_Staffing_Agency_Evaluation.txt
10. sot_Healthcare_Staffing_Compliance_Research_Outline.txt
11. sot_Healthcare_Staffing_Conversion_Analysis.txt
12. sot_Healthcare_Staffing_Fee_Structures_Analyzed.txt
13. sot_Healthcare_Staffing_Value_Extraction_Analysis.txt
14. sot_Healthcare_Visa_Pathways_EB-3_vs._TN.txt
15. sot_Hybrid_Staffing_Model_Analysis.txt
16. sot_International_Nurse_Recruitment_Program_Analysis(1).txt
17. sot_International_Nurse_Recruitment_Program_Analysis.txt
18. sot_Nava_Healthcare_Market_Analysis.txt
19. sot_Permanent_Healthcare_Staffing_Analysis.txt
20. sot_Travel_Nurse_Assignment_Behavior_Research.txt
21. sot_Travel_Nurse_Contract_Research_Request.txt
22. sot_Travel_Nurse_Program_Research_Findings.txt
23. sot_US_Healthcare_Surges_Causes_Impacts_Management.txt

**Total corpus word count:** ~107,700 words (23 documents)

---

## How to Use in Ask Dusk Sessions

In your query, reference the path so Dusk retrieves the right documents:

```
I'm asking about [topic] — check /root/.openclaw/workspace/rag/sot-clean/ for relevant SoT research.
```

Example queries:

- "What does the SoT corpus say about agency conversion fees vs. permanent hire costs?"
- "Find any documents in /root/.openclaw/workspace/rag/sot-clean/ discussing EB-3 visa pathways vs. TN status."
- "What are the key findings on travel nurse assignment behavior in the SoT research?"
- "Summarize the SoT documents related to contingent staffing and patient outcomes."

The path `/root/.openclaw/workspace/rag/sot-clean/` is the canonical location for these files.

---

## Notes

- All documents were converted from `.docx` source files in `/root/.openclaw/workspace/SoT-Collection/` using `python-docx`.
- Plain text only — no formatting, headers, or footers preserved.
- Each file contains only body text, separated by blank lines between paragraphs.
- The two `International_Nurse_Recruitment_Program_Analysis` files (with and without the `(1)` suffix) correspond to the two `.docx` source files of the same name — both are included as separate documents.