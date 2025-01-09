import sys
from Bio import SeqIO
from Bio import BiopythonParserWarning
import warnings
warnings.filterwarnings("ignore", category=BiopythonParserWarning)


sys.stderr = open(snakemake.log[0], "w")


consensus_file = snakemake.input.cons
type_file = snakemake.input.hbvtype
embl_dict = snakemake.params.extra
output_file = snakemake.output[0]


with open(type_file) as f:
    # * C1, B2, B4 ... 这样写的子分型，用 [0] 取第一个字母
    hbvtype = f.read().strip()[0]

embl_file = embl_dict[hbvtype]

samp_fa = list(SeqIO.parse(consensus_file, 'fasta'))[0]
rec = list(SeqIO.parse(embl_file, "embl"))[0]

with open(output_file, 'w') as f:
    f.write('Gene\tAA_Mut\n')
    for feat in rec.features:
        if feat.type == 'CDS':
            gene = feat.qualifiers['PRABI_name'][0]
            # * dna
            # print(feat.location.extract(rec).seq)
            # print(feat.location.extract(samp_fa).seq)
            # aa
            ref_aa = feat.qualifiers['translation'][0]
            # * 可以使用 feature location 位置提取输入的 fasta 文件的基因位置
            # join(2307..3212,1..1623) 这种会很方便
            samp_aa = feat.location.extract(samp_fa).seq.translate(stop_symbol='')
            # 逐个位置查看, 不同的输出突变
            for i in range(len(ref_aa)):
                if ref_aa[i] != samp_aa[i]:
                    f.write(f'{gene}\t{ref_aa[i]}{i+1}{samp_aa[i]}\n')
