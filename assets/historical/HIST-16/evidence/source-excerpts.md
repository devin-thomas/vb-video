# HIST-16 — source excerpts

## Project sources (unchanged)

### sources/SCRIPT.md:629–631
sha256 `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`

~~~~text
And then there was **Java**, which Sun Microsystems released in 1995 with the slogan "Write Once, Run Anywhere." Java was the future — everyone knew it. But in 1995, Java was brand new, brutally slow, had almost no libraries, and its GUI toolkit — AWT — was so ugly it could make you cry. Java would eventually eat the world, but not yet. Not in 1995.

**[VISUAL: A Java AWT application. The buttons look wrong on every platform.]**
~~~~

The same passage sits in the working script at `War/SCRIPT.md:686–688`, unchanged.

### sources/ASSET_PLAN.md:99
sha256 `8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7`

~~~~text
| 11 | Java AWT application (ugly) | Wikipedia "Abstract Window Toolkit" | High |
~~~~

## External evidence (short excerpts; full copies in evidence/source-pages/)

### The Java Tutorial, "AWT Components" page — Princeton spring 1996 mirror
`evidence/source-pages/princeton-spring96/components.html` (HTTP Last-Modified: Mon, 26 Feb 1996 18:15:19 GMT)

The image is the page's fallback picture for its applet:

~~~~html
<img src=images/GUIWindow.gif width=506 height=232>
~~~~

Surrounding page text: "Here's a picture of the window you'd see if you were using a Java-compatible browser". The page's separate FileDialog picture is described as the one "that the Solaris Applet Viewer brings up". That sentence refers to FileDialog.gif, not to GUIWindow.gif.

### GUIWindow.java — same mirror
`evidence/source-pages/princeton-spring96/GUIWindow.java` (HTTP Last-Modified: Mon, 26 Feb 1996 18:15:23 GMT)

~~~~java
public class GUIWindow extends Frame {
        window.setTitle("The AWT Components");
~~~~

(lines 19 and 107; the program builds Menu, TextField, Button, Checkbox, Choice, Label, TextArea, List and a Canvas from java.awt only.)

### Copyright page — same mirror
`evidence/source-pages/princeton-spring96/copyright.html`

The terms say all Tutorial material "may not be published in other works without express written permission from Sun Microsystems", under "© 1995 Sun Microsystems, Inc. All rights reserved."

### Byte-identical later copies
- UPenn CIS 629 mirror: Last-Modified 10 Sep 1997. That edition links the JDK 1.1 API and says the applet shown is "a 1.0 version".
- CMU 15-212 spring 1998 mirror: Last-Modified 10 Jan 1998.
