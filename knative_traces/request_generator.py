#!/usr/bin/env  python3


import pandas as pd
import time
import subprocess

IP ="128.110.153.106"
PORT ="31826"

traces = pd.read_csv("traces.csv")
for i in range(1,1441):
  df_tmp = traces[traces[str(i)] > 0]
  for index, row in df_tmp.iterrows():
    with open("%d_%s.txt" % (i, row["HashApp"]),"wb") as out:
      mem = max(1, row["Memory"]//row[str(i)])
      subprocess.Popen("loadtest -n %d -c %d -H \"Host: wgk-hpa.default.example.com\" \"http://%s:%s/?memory=%d&duration=%d\"" % (row[str(i)], row[str(i)], IP, PORT, mem, row["Duration"]), stdout=out, shell=True)
  time.sleep(1)

