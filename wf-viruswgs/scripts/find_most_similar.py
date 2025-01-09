import sys
import pandas as pd

sys.stderr = open(snakemake.log[0], "w")


# coverage = '/data/mengxf/Project/KML241212_HBV_WGS/result/25010801/find/BD205.coverage'
coverage = snakemake.input[0]
most_similar_file = snakemake.output[0]


df = pd.read_table(coverage, usecols=['#rname', 'coverage'])
# * 只看覆盖度排名即可
df['coverage'] = df['coverage'].astype(float)
df.sort_values('coverage', ascending=False, inplace=True)
most_similar = df.reset_index().loc[0, '#rname']

with open(most_similar_file, 'w', newline='') as f:
    f.write(most_similar)
