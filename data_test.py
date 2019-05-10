import pandas as pd

import data

d = data.create_df()
assert False == d.equals(data.dict_list_to_df(data.df_to_dict(d)))

dd, keys = data.df_to_json(d)
print(data.dict_list_mean(dd, keys))
