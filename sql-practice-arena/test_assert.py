import pandas as pd

df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"X": [1, 2], "Y": [3, 4]})

try:
    pd.testing.assert_frame_equal(df1, df2, check_names=False)
    print("Success with check_names=False")
except AssertionError as e:
    print("Failed with check_names=False:", e)

df1.columns = df2.columns
try:
    pd.testing.assert_frame_equal(df1, df2, check_names=False)
    print("Success after setting columns equal")
except AssertionError as e:
    print("Failed after setting columns equal:", e)
