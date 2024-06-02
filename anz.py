import pandas as pd

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("csvfile",
                    help="anz csv report to ingest", metavar="FILE")

args = parser.parse_args()

data = pd.read_csv(args.csvfile, names=["date","amount","description","recipient","recipient_account","payid","extra_note","extra_desc"], keep_default_na=False)
print(data.head())
print(data.count())
print(data.dtypes)

#print(data[lambda df: df["recipient"].notnull()]["recipient"])
# ensure all columns are treated as strings
#for c in ["description","recipient","recipient_account","payid","extra_note","extra_desc"]:
#    data[c] = data[c].astype(str)

# combine recipients and recipient_account
#data["payee"] = data["recipient"] + '|' + data["recipient_account"] + "|" + data["payid"]
data['payee'] = data[["recipient","recipient_account","payid"]].apply(lambda row: '|'.join(row.values.astype(str)), axis=1)
#data['recipient'].combine(data['recipient_account'], lambda a, b: ((a or "") + "|" + (b or "")) or None, None)
#data['recipient'].combine(data['payid'], lambda a, b: ((a or "") + "|" + (b or "")) or None, None)

# combine description with extra_desc
data['notes'] = data[["description","extra_desc","extra_note"]].apply(lambda row: '|'.join(row.values.astype(str)), axis=1)
#data["description"].combine(data["extra_desc"], lambda a,b: a + "|" + (b or ""))
#data["description"].combine(data["extra_note"], lambda a,b: a + "|" + (b or ""))
# data["notes"] = data["description"] + '|' + data["extra_desc"] + "|" + data["extra_note"]


final = data[["date","payee","notes","amount"]]

final.to_csv("processed_" + args.csvfile)

print(final.head())
