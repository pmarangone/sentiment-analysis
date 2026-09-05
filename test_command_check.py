import subprocess
try:
    subprocess.run(["pytest"], check=True)
except Exception as e:
    print(e)
