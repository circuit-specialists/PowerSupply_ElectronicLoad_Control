pyinstaller -F -i lib\CircuitSpecialists.ico .\gui.py -n CSPSELC --clean
del setup.py
:: py2applet --make-setup gui.py
:: python setup.py build