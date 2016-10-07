#!/usr/bin/env
import pandas as pd
df = pd.read_stata('New_Master.dta')
dummy_list = []
# for i df['firepac']:
#     dummy_list.append(0)
# df['financial_services_comm'] = dummy_list
# run this code or similar code in python manage.py shell

# Create desired party dataframe column:
# for i in xrange(434):
#     ...:     df['party_1'] = 'Dem'
# for n, i in enumerate(df['party']):
#      ...:     if i == 0.0:
#      ...:         df['party_1'][n] = 'Rep'
#      ...:     elif i == 1.0:
#      ...:         df['party_1'][n] = 'Dem'
# ABOVE FUNCTION: if df['party'] (this is the column that came with dataset)
# is 0 - party_1 is 'Rep' and if df['party'] value is 1 then the member is a 'Dem'
# Must do this or similar to vote_1, vote_2, and switch