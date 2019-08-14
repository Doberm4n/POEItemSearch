rmdir /Q /S build
rmdir /Q /S dist
c:\Python27\Scripts\pyinstaller POEItemSearch.py -w --noupx --version-file=version.txt --icon=res\search.ico
pause