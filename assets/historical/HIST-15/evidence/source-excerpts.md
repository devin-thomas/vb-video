# HIST-15 source excerpts

These excerpts are copied verbatim. Where a line is abridged, that is marked. Hashes and URLs are recorded in `source.json` and `provenance.json`.

## Input anchors (read-only `sources/`)

### sources/SCRIPT.md:625–627 (sha256 3821db54…9acb)

~~~~text
**PowerBuilder** was huge in the corporate database world. If you were building a line-of-business application that talked to an Oracle or Sybase database, PowerBuilder was the tool. It had a thing called DataWindows that made building data-entry forms almost trivially easy. But it was expensive, corporate, and basically invisible outside of IT departments.

**[VISUAL: A PowerBuilder DataWindow. Very corporate. Very 1995.]**
~~~~

### sources/ASSET_PLAN.md:98 (sha256 8f1769aa…eef7)

~~~~text
| 10 | PowerBuilder DataWindow | Old SAP/Sybase docs, retro software screenshots | Medium — more obscure |
~~~~

## External evidence: Internet Archive item `cbt-systems-microsoft-office-and-powersoft`

### Item metadata (archive.org/metadata API, retrieved 2026-09-15T20:40:42Z)

~~~~text
title:       CBT Systems Microsoft Office And Powersoft
creator:     CBT Systems Ltd.
date:        1997
collection:  cdrom_contributions
mediatype:   software
publicdate:  2025-08-19 05:20:06
licenseurl:  (absent)
rights:      (absent)
~~~~

### Disc label (uploader photo PXL_20250819_051756600.jpg on the item page; transcribed, not stored)

~~~~text
cbt systems · Visit us at www.cbtsys.com · P/N - CD003940
Microsoft® Office · Powersoft
Training Curriculum August 1997 · CD 11 of 16
~~~~

### ISO listing rows (view_archive endpoint)

~~~~text
pbdatc/PD4_504.DIB    1995-04-24 15:45:32    308278
pbdatc/HIGHLIGH.DIB   1995-03-30 09:50:18    45046
pbdatc/NEWDATWI.DIB   1995-04-13 11:04:44    64182
pbdatc/PD_1ST.DIB     1995-04-06 16:50:40    283300
pbdatc/PBDATC.DOC     1995-07-12 15:25:34    64625
pbdatc/VERSION.CBT    1996-04-04 11:50:58    27
manualsm/pbdatc.doc   1995-07-12 15:25:34    64625
manualsm/pb5dwc.doc   1996-06-24 11:00:00    72478
~~~~

### Course manual copyright notice

From `manualsm/pbdatc.doc`, text strings extracted without opening the document in an application:

~~~~text
PowerBuilderTM: 
DataWindow Concepts
  Copyright 1995 Powersoft Corporation. All rights reserved.
  Copyright 1995 CBT Systems Ltd. All rights reserved
All rights reserved.  No part of this publication may be reproduced or transmitted in any form or by any means, electronic or mechanical, including photocopy, recording, or any information storage or retrieval system without permission from CBT Systems Ltd or Powersoft Corporation.
Permission is, however, hereby granted to bona fide clients to photocopy this document or parts thereof to be used strictly in conjunction with the appropriate course.
~~~~

For comparison, `manualsm/pb5dwc.doc`:

~~~~text
PowerBuilder 5.0: 
DataWindow Concepts
  Copyright 1996 Powersoft Corporation. All rights reserved.
  Copyright 1996 CBT Systems Ltd. All rights reserved
~~~~

### Course identity: `pbdatc/CBTSETUP.INI` (abridged)

~~~~text
[Miscellaneous]
File Stub=pd
Character Setting=^
Course Name=PowerBuilder: DataWindow Concepts
~~~~

### Course build stamp: `pbdatc/VERSION.CBT` (complete)

~~~~text
K v4.0 - 13.06.95
C v1.2
~~~~

### Unit list: `pbdatc/UNITLIST.INI` (section header at line 1112)

~~~~text
[PowerBuilder: DataWindow Concepts]
  How DataWindows work
  Creating DataWindows
  Formatting DataWindows
  Displaying and validating data
  Making DataWindows work
  Edit control
  CloseQuery
~~~~

The same file also has the section header `[Moving from Powerbuilder 3.0a to 4.0]` at line 841. `pbdatc/SETUP.INI` includes `CourseName=Moving from PowerBuilder 3.0a to 4.0` and `CourseName=PowerBuilder: DataWindow Concepts`. The disc-root `UNITLIST.INI` has separate headers `[PB 5: DataWindow Concepts]` (line 2146) and `[PB5: DataWindow Construction Techniques]` (line 2745).

### Callout text match: `pbdatc/PD04.TXT` lines 321–323

~~~~text
Previewing the DataWindow enables you to see how using  edit styles has enhanced the presentation of the data.
|
But edit styles do more than that.
~~~~

The yellow callout in `source/original.dib` reads the same words.

### Presentation styles: `pbdatc/PD02.TXT` (abridged)

~~~~text
Each of the nine different presentation styles provided has a default format for presenting the data.
|
The nine predefined styles are Tabular, Grid, Freeform, Label, N-Up, Graph, Composite, Group, and Crosstab.
~~~~

## Background reference (not primary evidence)

- Wikipedia, "PowerBuilder" (read 2026-09-15): Sybase announced the Powersoft acquisition on 1994-11-15 and completed it on 1995-02-14.
- WinWorld, "PowerBuilder 4.x" (read 2026-09-15): lists a 1994 release date and notes that version 4 introduced 32-bit support.
