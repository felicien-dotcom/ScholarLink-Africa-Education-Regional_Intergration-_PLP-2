# ScholarLink Africa – Data Sources and Verification Report

Data Lead: Joseph · Checked: 20/11/2026 · File: `scholarships.csv` (30 rows, full funding only)

## Method
- The team decided to keep only **fully funded** opportunities. Partial awards (fixed tuition discounts or capped grants) were removed.
- Every row was checked on the provider's official website. Deadlines are DD/MM/YYYY and none were invented. A closed row keeps its real closing date, and the app hides closed rows from search automatically.
- `level` is `Undergraduate`, `Masters` or `Any` (both). `country` means who can apply. Where only some African countries qualify, the eligibility text lists them.
- Each eligibility text starts with one of two labels:
  - **FULL**: a named scholarship that covers tuition and living costs.
  - **FULL NEED MET**: a university that states on its official site that it meets 100% of demonstrated financial need for every admitted student, including international students. For a low-income student this usually covers the full cost, but the student must first be admitted and must apply for aid on time.

## Summary
- 16 named full scholarships, 14 full-need universities.
- 23 open, 7 closed (as of 20/11/2026).
- Master's options: Commonwealth Shared (open until 08/12/2026), Chevening (closed 06/10/2026), Makerere (UG + Masters, closed 05/06/2026). UCT's postgraduate round closed 31/10/2026 and Pretoria's closed 30/09/2026 (see the eligibility text).

## A. Named full scholarships (16)
| # | Scholarship | Provider | Level | Deadline | Status |
|---|---|---|---|---|---|
| 1 | UNHCR DAFI Scholarship - Protestant University of Rwanda | UNHCR / DAFI and Protestant University of Rwanda | UG | 15/11/2026 | Closed |
| 2 | Zawadi Africa Education Fund Scholarship (Kenya) | Zawadi Africa Education Fund | UG | 16/03/2026 | Closed |
| 3 | UCT Mastercard Foundation Scholars Program (2027 intake) | Mastercard Foundation / University of Cape Town | UG | 30/09/2026 | Closed |
| 4 | Pretoria Mastercard Foundation Scholars Program (2027 intake) | Mastercard Foundation / University of Pretoria | UG | 31/08/2026 | Closed |
| 5 | Makerere Mastercard Foundation Scholars Program (2026/2027) | Mastercard Foundation / Makerere University | UG + Masters | 05/06/2026 | Closed |
| 6 | ALU Scholarship - Mastercard Foundation Scholars Program | African Leadership University | UG | 30/11/2026 | Open |
| 7 | Lester B. Pearson International Scholarship (Fall 2027) | University of Toronto | UG | 09/10/2026 | Closed |
| 8 | Berea College International Admission (fully funded) | Berea College | UG | 30/11/2026 | Open |
| 9 | EARTH University Mastercard Foundation Scholars Program | EARTH University and Mastercard Foundation | UG | 31/01/2027 | Open |
| 10 | ALCHE Mastercard Foundation Scholars Program (Mauritian applicants) | African Leadership College of Higher Education and Mastercard Foundation | UG | 23/01/2027 | Open |
| 11 | Reach Oxford Scholarship (2027 entry) | University of Oxford | UG | 26/01/2027 | Open |
| 12 | Wesleyan African Scholars Program | Wesleyan University | UG | 15/01/2027 | Open |
| 13 | Turkiye Burslari (Turkiye Scholarships) Bachelor's | Government of Turkiye (YTB) | UG | 20/02/2027 | Open |
| 14 | UGHE MBBS-MGHD Scholarship (University of Global Health Equity) | University of Global Health Equity | UG | 17/01/2027 | Open |
| 15 | Commonwealth Shared Scholarships (2027/28) | Commonwealth Scholarship Commission in the UK | Masters | 08/12/2026 | Open |
| 16 | Chevening Scholarships (2027-2028) | UK Government (FCDO) - Chevening | Masters | 06/10/2026 | Closed |

## B. Universities that meet 100% of need (14)
| # | Scholarship | Provider | Level | Deadline | Status |
|---|---|---|---|---|---|
| 17 | Harvard College Need-Based Financial Aid (international) | Harvard University | UG | 01/02/2027 | Open |
| 18 | Yale College Need-Based Financial Aid (international) | Yale University | UG | 15/02/2027 | Open |
| 19 | Princeton Undergraduate Financial Aid (international) | Princeton University | UG | 01/02/2027 | Open |
| 20 | MIT Undergraduate Financial Aid (international) | Massachusetts Institute of Technology | UG | 15/02/2027 | Open |
| 21 | Brown University Financial Aid (international first-year) | Brown University | UG | 01/02/2027 | Open |
| 22 | Bowdoin College Financial Aid (international) | Bowdoin College | UG | 05/01/2027 | Open |
| 23 | University of Notre Dame Financial Aid (international) | University of Notre Dame | UG | 15/01/2027 | Open |
| 24 | Tufts University Financial Aid (international) | Tufts University | UG | 04/01/2027 | Open |
| 25 | Dartmouth College Financial Aid (international) | Dartmouth College | UG | 01/02/2027 | Open |
| 26 | Amherst College Financial Aid (international) | Amherst College | UG | 15/01/2027 | Open |
| 27 | Williams College Financial Aid (international) | Williams College | UG | 04/01/2027 | Open |
| 28 | Wellesley College Financial Aid (international) | Wellesley College | UG | 08/01/2027 | Open |
| 29 | Swarthmore College Financial Aid (international) | Swarthmore College | UG | 04/01/2027 | Open |
| 30 | Stanford University Financial Aid (international) | Stanford University | UG | 15/02/2027 | Open |

## Removed in this revision
| Scholarship | Reason |
|---|---|
| Dundee Vice-Chancellor's Africa; Dundee Global Excellence | Partial: fixed tuition reduction |
| Lu Memorial; Wells Mountain Initiative; PEO International Peace | Partial: capped grant (USD 5,000 / 3,000 / 12,500) |
| York International Scholarship of Distinction; Amref International University | Partial |
| Ashesi University Scholarship | May be full or partial (30–100%); applicants cannot choose which award they get |
| Mauritius-Africa Scholarship Scheme | Tuition capped (MUR 100,000–160,000) and living costs only partly covered |
| UBC Karen McKellin ILOT | Need-based "up to full cost"; full cover is not guaranteed |
| Johns Hopkins; Minerva | Aid limited or explicitly partial for international students |
| NYU Abu Dhabi | Current official pages do not state that 100% of need is met |

The 13 scholarships from the team list that had no verifiable official deadline are still excluded: CAMFED, Jim Ovia/AAI, Kenyatta University, Strathmore, Equity, Standard Bank, KNUST, Gondar, Covenant, University of Nairobi, USAP, Aga Khan Foundation, Stamps.

## Sources
The official page for every scholarship is in the `link` column of `scholarships.csv`. The 100%-need claims were confirmed on: college.harvard.edu/financial-aid/how-aid-works, finaid.yale.edu/policies, admission.stanford.edu/apply/international, admissions.tufts.edu (International Student Aid). Other rows were checked on the linked pages.

## Testing
Imported into a clean local SQLite copy (no `--replace`): 30 imported, 0 skipped. All 8 unit tests pass.
