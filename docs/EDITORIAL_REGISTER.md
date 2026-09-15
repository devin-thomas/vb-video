# Editorial and evidence register

These are review gates, not a rewritten script. Code observations are derived by reading the supplied source, not by claiming it has been compiled here. External history/current-policy/legal claims remain unverified. The three original files are immutable. Production may proceed to internal proof while publication remains gated.

## R01 — Stale “today” dates

**Source anchors:** `SCRIPT.md:148–150`; `SCRIPT.md:691–705`

**Issue:** The script uses 2024 as today. This pack does not silently update the episode or its claims to a new year.

**Required decision / handling:** Producer selects publication framing; verify any current-status statement at actual execution/publication time.

**Status:** Open. No correction or clearance authorized by this pack.

## R02 — Categorical VB4 installation/license assertion

**Source anchors:** `SCRIPT.md:148–148`

**Issue:** The source asserts that legal installation is impossible and licenses do not transfer, but supplies no license evidence.

**Required decision / handling:** Keep this unverified legal assertion out of new graphics. Obtain appropriate source/rights review or an explicitly approved wording change. This pack is not a legal determination.

**Status:** Open. No correction or clearance authorized by this pack.

## R03 — Classic-inspired VB.NET versus actual VB4

**Source anchors:** `Program.vb:1–8`; `SCRIPT.md:150–166`; `SCRIPT.md:659–669`

**Issue:** The attached program labels itself classic-inspired, enables modern VB options, and is presented via a modern .NET console workflow. A literal VB4 execution or platform-feature claim is not established by these files.

**Required decision / handling:** Label the executable demo VB.NET; do not fabricate a VB4 compile/run. Verify version-specific syntax, platform capabilities, and UI panel names before historical claims.

**Status:** Open. No correction or clearance authorized by this pack.

## R04 — “Recursion” heading versus repeated inner loop

**Source anchors:** `SCRIPT.md:434–460`; `Program.vb:204–205`; `Program.vb:220–270`

**Issue:** The supplied PlayRound repeats a Do/Loop and does not call itself. The chapter title says “recursion.” This is a source/code discrepancy, not an externally researched correction.

**Required decision / handling:** Preserve the original title proof; producer decides wording. Code-faithful diagrams may show the loop but must not add a recursive call.

**Status:** Open. No correction or clearance authorized by this pack.

## R04a — ByRef / ByVal simplification

**Source anchors:** `SCRIPT.md:273–275`; `Program.vb:23–26`; `Program.vb:149–152`; `Program.vb:204–205`

**Issue:** The script’s general reference/copy explanation is too underspecified to justify a deep-copied array graphic. The source contains arrays and structures containing arrays.

**Required decision / handling:** Use the scoped Integer illustration, verify its semantics in a separate harness, and obtain primary VB documentation before any general array/reference/default-passing claim. Proposed teaching examples are labeled as such.

**Status:** Open. No correction or clearance authorized by this pack.

## R05 — Insufficient cards and symmetric burn behavior

**Source anchors:** `SCRIPT.md:188–192`; `SCRIPT.md:483–489`; `Program.vb:220–232`; `Program.vb:258–268`

**Issue:** The code sets one BurnCount=min(3, Player1.Count, Player2.Count), burns that amount from both hands, then checks Player1-empty before Player2-empty on the next pass. If both are empty then, that ordering awards the pot to Player2. The narration’s generalized lose-on-insufficient-cards rule does not fully specify this.

**Required decision / handling:** Do not alter the program. Use fully supplied normal examples by default; any short-hand storyboard needs a separate exact-state test and producer decision.

**Status:** Open. No correction or clearance authorized by this pack.

## R06 — Round cap, counter reporting, and cycle wording

**Source anchors:** `Program.vb:59–71`; `Program.vb:91–93`; `SCRIPT.md:420–420`

**Issue:** RoundNumber increments before testing >20000. Reaching the cap branch leaves it at 20001 although only 20000 PlayRound calls may have completed. The output says “deck cycle detected,” but the source contains a cap, not a saved-state cycle detector.

**Required decision / handling:** Retain true output in captures and flag its wording. Diagrams call it a round cap; do not claim an exact cycle algorithm or silently patch the counter.

**Status:** Open. No correction or clearance authorized by this pack.

## R07 — Pot allocation versus cards actually in play

**Source anchors:** `Program.vb:28–29`; `Program.vb:207–208`; `SCRIPT.md:458–458`

**Issue:** Pot(HAND_CAPACITY * 2 - 1) with HAND_CAPACITY=52 declares indices 0…103. The game has only 52 physical cards; 2/10/18 are live-count examples under full burns.

**Required decision / handling:** Show allocated slots and live card count as distinct concepts. Verify the exact VB bound interpretation in the runtime harness; no 104-card deck graphic.

**Status:** Open. No correction or clearance authorized by this pack.

## R08 — Sample script output versus actual captures

**Source anchors:** `SCRIPT.md:532–566`; `SCRIPT.md:571–573`; `SCRIPT.md:732–736`; `Program.vb:114–126`

**Issue:** Narration supplies example results and specific double-war text. No attached execution transcript proves those are results from this Program.vb. ShuffleDeck has New Random() and no supplied seed.

**Required decision / handling:** Capture real logs and record real totals; label teaching fixtures or replay as such. Do not modify the source solely to force the sample outcomes.

**Status:** Open. No correction or clearance authorized by this pack.

## R09 — Mac-product and historical-tooling claims

**Source anchors:** `SCRIPT.md:645–671`

**Issue:** The narrator explicitly expresses uncertainty about “Visual Basic for Mac.” Other Mac-tool/GUI/era claims have no supporting historical sources attached.

**Required decision / handling:** Research exact product identities and period APIs with primary sources. Missing results are not proof. A 404 joke or neutral replacement requires producer approval and cannot substitute for evidence.

**Status:** Open. No correction or clearance authorized by this pack.

## R10 — Classic declaration rules and historical return/Dim claims

**Source anchors:** `SCRIPT.md:227–229`; `SCRIPT.md:305–305`; `SCRIPT.md:370–372`

**Issue:** Several language-history claims are asserted without primary documentation. The source’s choice to declare variables at the top does not establish a universal historical requirement.

**Required decision / handling:** Render the code as written. Verify historical necessity/defaults/origins before adding categorical explanatory text.

**Status:** Open. No correction or clearance authorized by this pack.

## R11 — Popularity, installed base, prices, and real VB applications

**Source anchors:** `SCRIPT.md:12–12`; `SCRIPT.md:45–55`; `SCRIPT.md:623–633`; `SCRIPT.md:685–691`

**Issue:** The source makes superlative market/popularity/production-code claims and describes broad real-world use, but provides no supporting data. A screenshot’s appearance does not prove its implementation language.

**Required decision / handling:** Keep statistics and rankings out of new artwork unless evidenced. Document actual VB provenance for application collages; route broad narration assertions to the producer.

**Status:** Open. No correction or clearance authorized by this pack.

## R12 — Current VB.NET status and migration/lifecycle claims

**Source anchors:** `SCRIPT.md:691–707`

**Issue:** Current maintenance/support assertions and historical migration framing are narration, not verified lifecycle evidence in this pack.

**Required decision / handling:** Use current official evidence when executing the research task; date all status statements and obtain approval for changes. Avoid turning “maintenance mode” into an invented support or security promise.

**Status:** Open. No correction or clearance authorized by this pack.

## R13 — Influence diagram versus proven lineage

**Source anchors:** `SCRIPT.md:709–711`

**Issue:** A sequence of arrows in the script is not evidence of direct technical or causal descent.

**Required decision / handling:** Evidence and label every edge. A neutral shared-ideas diagram is only a proposed alternative until approved.

**Status:** Open. No correction or clearance authorized by this pack.

## R14 — Per-image licensing, archive capture, and public availability

**Source anchors:** `ASSET_PLAN.md:81–107`; `ASSET_PLAN.md:109–122`; `SCRIPT.md:749–763`

**Issue:** The plan’s likely-public-domain, fair-use, and public-browsing statements are assumptions, not item-specific rights records.

**Required decision / handling:** Record the original rights holder/creator, file-specific terms, access method, and credit. Unknown rights stay blocked. No unapproved account creation, payment, watermark removal, or CAPTCHA bypass.

**Status:** Open. No correction or clearance authorized by this pack.

## R15 — Dates, versions, and representative historical code

**Source anchors:** `SCRIPT.md:67–116`; `SCRIPT.md:299–305`; `SCRIPT.md:609–631`

**Issue:** The files provide historical dates and feature claims but no cited primary verification, and no exact C/MFC/FORTRAN source for the requested reference graphics.

**Required decision / handling:** Verify era/version claims during assigned research; label newly written samples representative. Do not pad C to 80 lines, force a shorter BASIC example, or invent execution evidence.

**Status:** Open. No correction or clearance authorized by this pack.

## R16 — Download/runtime/version and price assumptions

**Source anchors:** `SCRIPT.md:595–599`; `SCRIPT.md:661–667`; `SCRIPT.md:685–685`

**Issue:** The narration names a runtime “something like VBRUN300.DLL” within a VB4-era story and uses illustrative file sizes, modem time, and purchase price. These are not independently established measurements or product terms.

**Required decision / handling:** Keep the requested 9:42 as an illustrative mockup. Verify runtime version, distribution details, and quantitative claims before making factual captions.

**Status:** Open. No correction or clearance authorized by this pack.

## R17 — Missing project file

**Source anchors:** `SCRIPT.md:160–166`; `Program.vb:7–8`

**Issue:** War.vbproj is referenced in the script but was not uploaded. Only ASSET_PLAN.md, SCRIPT.md, and Program.vb are original inputs.

**Required decision / handling:** Generate a derived isolated project using the actual installed SDK and record every property change. Never present the derived .vbproj as an original attachment or guaranteed scaffold default.

**Status:** Open. No correction or clearance authorized by this pack.
