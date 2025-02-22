rule gene_aa_mutation:
    input:
        cons=rules.bcftools_consensus.output.cons2,
        hbvtype=rules.virus_type.output[0],
    output:
        "aamut/{sample}.tsv",
    log:
        "logs/aamut/{sample}_gene_aa_mutation.log",
    benchmark:
        "logs/aamut/{sample}_gene_aa_mutation.bm"
    params:
        embl=config["database"]["hbvtype"]["embl"],
        mafft=config["software"]["mafft"]
    conda:
        config["conda"]["python"]
    script:
        "../scripts/gene_aa_mut.py"
