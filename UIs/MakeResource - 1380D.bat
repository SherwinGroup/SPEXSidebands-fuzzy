@ECHO OFF
set input="%~1"
set postpend="_ui.py"
set output=%input:~1,-4%
pyrcc5 -o %input:~0,-5%_rc.py" %input%