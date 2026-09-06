import os, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
portrait=root/"assets/profile.jpg"
if portrait.exists(): subprocess.run([sys.executable,str(root/"scripts/generate_portrait.py"),"--input",str(portrait),"--output",str(root/"generated/portrait.svg")],check=True)
subprocess.run([sys.executable,str(root/"scripts/generate_stats.py")],check=True)
