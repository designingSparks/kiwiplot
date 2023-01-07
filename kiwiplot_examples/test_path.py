'''
Checks that the local kiwiplot package is in the system path.
When using VS Code, run code in the kiwiplot_examples folder using the run menu.
The local kiwiplot package is added to the path in the .env file, which is placed at the root level of the project.
'''
import sys
for item in sys.path:
    print(item)