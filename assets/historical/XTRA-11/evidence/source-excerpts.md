# XTRA-11 source excerpts

Two kinds of input are kept apart here: the project's script (the reason for the visual) and external historical evidence (why this application counts as a documented classic Visual Basic business tool). Nothing below is paraphrased into a quotation. Personal contact details in the vendor documents (an individual's e-mail address, telephone numbers) are deliberately not copied.

## 1. Project script: `sources/SCRIPT.md:685–687` (unchanged)

SHA-256 of `sources/SCRIPT.md`: `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`

~~~~text
That's not hyperbole. Before VB, writing a Windows application was a professional skill that required significant training. After VB, a motivated person with a $100 software purchase and a library book could build something real in a weekend. Accountants wrote tools to automate their spreadsheets. Teachers built quiz applications. Small business owners made inventory trackers. None of these people would have called themselves programmers. They were people with problems who discovered that Visual Basic was good enough to solve them.

**[VISUAL: Collage of real-world VB applications — maybe screenshots from old forums or software archives. Internal business tools, data entry forms, simple utilities.]**
~~~~

The same paragraph and visual cue appear unchanged in the working script `War/SCRIPT.md` at lines 742 and 744 (checked 2026-09-15).

## 2. External evidence: Internet Archive item `MEDLEY_SEC90034`

- Item page: https://archive.org/details/MEDLEY_SEC90034
- Metadata API: https://archive.org/metadata/MEDLEY_SEC90034
- Item title (archive catalogue text, not the product name): "Nicely Done Invoicing Program For Windows"
- Item metadata: creator "Eastern Digital Resources"; date "1993-06-13"; collections softwarelibrary_win3_productivity / softwarelibrary_win3 / softwarelibrary / emulation; uploader account softwarelibrary@textfiles.com; publicdate 2016-02-27 18:18:57; emulator dosbox; emulator_start `d:\runapp INVOICE.EXE`. No license or licenseurl field is present.
- Accessed: 2026-09-15.

### 2a. Distribution file list (`SEC90034.ZIP`, read through the archive's zip directory view; no executable was downloaded or run)

| File | Timestamp in zip | Bytes |
|---|---|---|
| CATALOG.TXT | 1993-06-12 16:31 | 34223 |
| CUSTOMER.DBF | 1993-02-17 19:27 | 512 |
| CUSTOMER.TXT | 1992-12-18 15:27 | 70 |
| DBCONVRT.EXE | 1993-02-17 19:20 | 45057 |
| HELP.TXT | 1993-06-12 16:25 | 9290 |
| INVOICE.EXE | 1993-06-12 16:13 | 223534 |
| INVOICES.DBF | 1993-02-17 19:27 | 2560 |
| MANUAL.WRI | 1993-06-12 16:22 | 26880 |
| PRODUCTS.DBF | 1993-02-17 19:27 | 512 |
| PRODUCTS.TXT | 1992-09-06 20:34 | 682 |
| RELEASE.TXT | 1993-06-12 16:24 | 1147 |
| SETUP.CFG | 1993-06-12 16:16 | 204 |

### 2b. Development-language evidence: the publisher's own documentation

Text documents were read individually from `https://archive.org/download/MEDLEY_SEC90034/SEC90034.ZIP/<FILE>`.

`RELEASE.TXT` (SHA-256 `c0d276aa0a4a4d428b8bf95b2f6be2e7142426be9a69764c5e8fa6cf98939f44`), version history, lines 7–10 and the final entry:

~~~~text
2.00    02/17/93  Changed standard file format to Dbase compatible
                  Added open invoice status and updating
                  Cleaned up and sped up logo printing
                  Recompiled program using Visual BASIC 2.0
...
2.06    06/12/93  Added several options to allow you to change the look of
~~~~

`HELP.TXT` (SHA-256 `8ea5b2b4184f823ad78515f917ba46fe23a34fb89de1ec888b93f77bbd3c4aa0`), lines 36–37:

~~~~text
3. The program is now running under Visual BASIC version 2.0.  You'll
find this version somewhat faster than the earlier version.  It also
~~~~

`MANUAL.WRI` (Windows Write document, SHA-256 `8208dd4c365668f15ab15673f2a3b1ff75b168d7935933f6908e2cf98bba42ca`), installation section, printable-text extraction:

~~~~text
In order to use INVOICE-IT you will need to have the Visual BASIC runtime library, VBRUN200.DLL in your Windows System directory.
~~~~

### 2c. Identity and product scope (same documents)

- Product name as printed in the documents and in the program's title bar: "INVOICE - IT FOR WINDOWS" / "INVOICE-IT FOR WINDOWS".
- Publisher as printed: "published by Eastern Digital Resources", with a post-office-box address in South Carolina (address not needed for the asset).
- Stated purpose (HELP.TXT): creating and printing invoices for users who need only the invoicing function, and integration with the publisher's "Total Business Solution" accounting software.
- Version of this distribution: the latest entry in RELEASE.TXT is 2.06 dated 06/12/93, matching the 1993-06-12 zip timestamps. Treat "v2.06" as the best-supported version label; the program's own About box was not inspected.

### 2d. Terms stated by the publisher (relevant to R14)

- HELP.TXT line 8: "This edition of INVOICE - IT is distributed as shareware."
- MANUAL.WRI License section (paraphrased): the program is not public domain or free software. Trial users may copy the unmodified shareware edition so that others can evaluate it. No fee may be charged, and it may not be bundled with other products without a license from the publisher. These are terms for redistributing the software. They say nothing about screenshots or video use.

### 2e. The screenshot itself

- The archive lists `screenshot_01.jpg` as an original (not derivative) file: 66785 bytes, SHA-1 `8a51465aa1c817a809c6abab92ee3aa701a80d92`, mtime 1456597998 (2016-02-27 18:33:18 UTC). It is byte-identical to the item's `00_coverscreenshot.jpg`.
- It shows the INVOICE-IT main window running in the archive's in-browser Windows 3.1 (DOSBox) emulation: an empty invoice form with sample data (next invoice number 3379, which follows the value 3378 in the distributed SETUP.CFG, and a default note reading "Thank you for your business.").
- Its Date field reads **02-27-2016**. That is the emulator clock on the capture day (the archive publicdate is 2016-02-27), not a 1993 date. It is left uncropped on purpose.
- The capture ends partway down the window, just below the NOTES box. That crop comes from the archive's capture, not from this project.
