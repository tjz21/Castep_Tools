# Castep Tools 🔧

Collection of helpful scripts for post processing CASTEP output files. All scripts are available as executable CLI programs written in Python 3 with the [argparse](https://docs.python.org/3/library/argparse.html) library. 

## Contents

|     Script Name     |                    Description                     | Ready |
| :------------------ | :------------------------------------------------- | :---: |
|  check_converge.py  |   Analyzes convergence of geometry optimization    |   ✓   |
| scf_troubleshoot.py |       Troubleshoots failed SCF calculations        |   ✗   |
|   phonon_nudge.py   |  Displaces atoms in unit cell along a phonon mode  |   ✗   |
|     SI_ready.py     | Extracts necessary data for supporting information |   ✗   |

### Usage
Simply navigate to the folder with the castep output file and run the desired program.

<div style="text-align:center;">
  <img src="https://github.com/LinusP217/Castep_Tools/blob/main/castep_tool_demo.gif" width="700" height="369">
</div>

---

### Download
Make a copy of the entire repository with the following command in a terminal:
```bash
git clone https://github.com/LinusP217/Castep_Tools.git
```

or if you would just like one specific file, use `wget` and the raw url for that file:

<img align="center" src='https://github.com/tjz21/DAC_metals/blob/main/raw_link_image.png' width = "600" height = "63.4">

```bash
wget [raw URL of specific file]
```

