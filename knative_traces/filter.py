import pandas as pd


df_invocations = pd.read_csv("traces_invocations_gt_100K.csv")
#df_invocations = df_invocations[df_invocations["Trigger"] == "http"]
df_invocations.reset_index(inplace=True)
#df_invocations = df_invocations[["HashFunction"]+[str(i) for i in range(1, 1441)]]

df_filtered_hash = pd.read_csv("hash_top_50.csv")
df_filtered_hash.reset_index(inplace=True)


#df_output = pd.DataFrame(columns=["HashFunction", "Memory", "Duration"] + [str(i) for i in range(1, 1441)])
df_output = pd.DataFrame(columns=["HashFunction", "Duration"] + [str(i) for i in range(1, 1441)])
for index, row in df_invocations.iterrows():
  try:
    if (row["HashFunction"] in df_filtered_hash["HashFunction"].to_numpy()):
      # Scale down the incoming request count by dividing by 60
      for i in range(1, 1441):
        row[str(i)] = round(row[str(i)]/60)
      df_output = df_output.append(row, ignore_index=True)
  except:
    print("Missing: " + row["HashFunction"])
  #if df_output.shape[0] == 100:
  #  break

#tmp = df_output["Duration"].values
#x_std = [(x-tmp.min())/(tmp.max()-tmp.min()) for x in tmp]
#x_scaled = [int(round(x*(100-1)+1)) for x in x_std]
#df_output["Duration"] = x_scaled

df_output.to_csv("traces_top_50.csv", index=False)
