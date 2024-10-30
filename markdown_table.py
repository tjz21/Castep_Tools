# nice way of formatting the table for the README 

from prettytable import PrettyTable
from prettytable import MARKDOWN

def create_markdown_table():
    # Create a PrettyTable object
    table = PrettyTable()

    # Define the column headers
    table.field_names = ["Script Name", "Description", "Ready"]

    # Add rows of data
    table.add_row(["check_converge.py", "Analyzes convergence of geometry optimization", "✓"])
    table.add_row(["geom_grabber.py", "Extracts last geometry from optimization into a new cell file", "✗" ])
    table.add_row(["scf_troubleshoot.py", "Troubleshoots failed SCF calculations", "✗" ])
    table.add_row(["phonon_nudge.py", "Displaces atoms in unit cell along a phonon mode", "✗" ])
    table.add_row(["SI_ready.py", "Extracts necessary data for supporting information", "✗" ])

    # Get the table in Markdown format
    table.set_style(MARKDOWN)
    markdown_table = table#.get_string(border=False, hrules=1)
    return markdown_table

# Print the markdown table to the console
markdown_table = create_markdown_table()
print(markdown_table)

