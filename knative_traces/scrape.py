import pandas as pd


df_invocations = pd.read_csv("invocations_per_function_md.anon.d01.csv")
df_invocations.reset_index(inplace=True)
df_invocations = df_invocations[["HashFunction"]+[str(i) for i in range(1, 1441)]]


#df_memory = pd.read_csv("app_memory_percentiles.anon.d01.csv")[["HashFunction","AverageAllocatedMb"]]
#df_memory.set_index("HashFunction",inplace=True)

df_duration = pd.read_csv("function_durations_percentiles.anon.d01.csv")[["HashFunction","Average"]]
df_duration.set_index("HashFunction",inplace=True)

#df_output = pd.DataFrame(columns=["HashFunction", "Memory", "Duration"] + [str(i) for i in range(1, 1441)])
df_output = pd.DataFrame(columns=["HashFunction", "Duration"] + [str(i) for i in range(1, 1441)])
df_total_req = pd.DataFrame(columns=["HashFunction","TotalInvocations"])
for index, row in df_invocations.iterrows():
  try:
    df_total_req = df_total_req.append({
      "HashFunction": row["HashFunction"],
      "TotalInvocations": (row[[str(i) for i in range(1,1441)]].sum())
    }, ignore_index=True)
    if (row[[str(i) for i in range(1,1441)]].sum()) > 100000:
      df_output = df_output.append({
       "HashFunction": row["HashFunction"],
       #"Memory": df_memory.loc[row["HashFunction"], "AverageAllocatedMb"],
       "Duration": df_duration.loc[row["HashFunction"], "Average"],
       **row[[str(i) for i in range(1,1441)]].to_dict()
      }, ignore_index=True)
  except:
    print("Missing: " + row["HashFunction"])
  #if df_output.shape[0] == 100:
  #  break

#tmp = df_output["Duration"].values
#x_std = [(x-tmp.min())/(tmp.max()-tmp.min()) for x in tmp]
#x_scaled = [int(round(x*(100-1)+1)) for x in x_std]
#df_output["Duration"] = x_scaled

df_output.to_csv("traces_invocations_gt_100K.csv", index=False)
df_total_req.to_csv("traces_total_req.csv",index=False)
