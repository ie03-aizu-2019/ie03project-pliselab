import time
import subprocess


start = time.time()
p = subprocess.Popen(["cat", "../source/data/input.txt"], stdout=subprocess.PIPE)
p.wait()
print("come")
res = subprocess.check_output(
    ["python3", "../source/main.py", "-m", "all"], stdin=p.stdout)
p.stdout.close()
elapsed_time = time.time() - start
print(res.decode("utf8"))
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
