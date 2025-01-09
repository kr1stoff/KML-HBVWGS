import sys
import os
import shutil
from Bio import AlignIO
from Bio import SeqIO
from Bio import BiopythonParserWarning
import warnings
warnings.filterwarnings("ignore", category=BiopythonParserWarning)


sys.stderr = open(snakemake.log[0], "w")


consensus_file = snakemake.input.cons
type_file = snakemake.input.hbvtype
embl_dict = snakemake.params.embl
mafft = snakemake.params.mafft
outfile = snakemake.output[0]


with open(type_file) as f:
    # * C1, B2, B4 ... 这样写的子分型，用 [0] 取第一个字母
    hbvtype = f.read().strip()[0]

embl_file = embl_dict[hbvtype]

samp_fa = list(SeqIO.parse(consensus_file, 'fasta'))[0]
rec = list(SeqIO.parse(embl_file, "embl"))[0]

with open(outfile, 'w') as g:
    g.write('Gene\tAA_Mut\n')
    for feat in rec.features:
        if feat.type == 'CDS':
            gene = feat.qualifiers['PRABI_name'][0]
            if gene in ["P", "S"]:
                # * dna
                # print(feat.location.extract(rec).seq)
                # print(feat.location.extract(samp_fa).seq)
                # * aa
                ref_aa = feat.qualifiers['translation'][0]
                samp_aa = feat.location.extract(samp_fa).seq.translate(stop_symbol='')

                # mafft
                _temp_ref_aa_file = f'{outfile}_{gene}_ref.faa'
                _temp_samp_aa_file = f'{outfile}_{gene}_samp.faa'
                _temp_align_file = f'{outfile}_{gene}_align.faa'

                with open(_temp_ref_aa_file, 'w') as f:
                    f.write(f'>REF_{gene}\n{ref_aa}')
                with open(_temp_samp_aa_file, 'w') as f:
                    f.write(f'>SAMP_{gene}\n{samp_aa}')
                os.system(
                    f'{mafft} --quiet --6merpair --keeplength --addfragments {_temp_samp_aa_file} {_temp_ref_aa_file} > {_temp_align_file}')
                align = AlignIO.read(_temp_align_file, 'fasta')
                for i in range(len(align[0])):
                    pair_base = align[:, i]
                    # mafft: X 表示序列中存在不确定性或缺失信息; - 表示为了对齐序列而引入的空位
                    if (len(set(pair_base)) > 1) and ('X' not in pair_base) and ('-' not in pair_base):
                        g.write(f'{gene}\t{pair_base[0]}{i+1}{pair_base[1]}\n')

                # * 删掉中间文件
                # os.remove(_temp_ref_aa_file)
                # os.remove(_temp_samp_aa_file)
                # os.remove(_temp_align_file)
