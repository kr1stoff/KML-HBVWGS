import sys
import shutil


sys.stderr = open(snakemake.log[0], "w")

type_file = snakemake.input[0]
type_dict = snakemake.params.hbvtype
output_file = snakemake.output[0]

with open(type_file) as f:
    # * C1, B2, B4 ... 这样写的子分型，用 [0] 取第一个字母
    hbvtype = f.read().strip()[0]

genome = type_dict['genome'][hbvtype]
shutil.copyfile(genome, output_file)
