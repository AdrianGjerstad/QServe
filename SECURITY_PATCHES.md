# Security Patch Log

#### Entries noted most recently at bottom (e.g. w01 above w02)

<h2><span title="QSERVE SECPAT INDICATOR">QSSP</span><span title="PATCH A IN WEEK">a</span><span title="WEEK 38 OF YEAR 2019">19w38</span><span title="MAJOR/URGENT PATCH">M</span></h2>

- Set response for request path starting with '//' to **404 Not Found**
  - Originally started path at root of local machine
- Set response for request path starting with '/~' to **404 Not Found**
  - Originally started path at base directory of executing user
- Set response for request path starting with '/..' to **404 Not Found**
  - Originally continued the rest of the path starting at the parent directory

----

<div style="text-align: right;">
How to read example entry (Based on QSSPa19w38M):<br/>
QSSP - QServe Security Patch Indicator aka This is a security patch title for QServe<br/>
a - The first patch pushed out in the week (which starts on Monday and ends on Sunday)<br/>
19w38 - Patch pushed out in the 38th week of the year 2019.<br/>
M - Patch is urgent and may result in security infringements if not updated quickly.<br/>
  m - Patch is minor and may effect your server, but no major issues will arise.<br/>
</div>
