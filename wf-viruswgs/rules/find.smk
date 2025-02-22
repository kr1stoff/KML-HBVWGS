rule bwa_mem_datasets_se:
    input:
        reads=["qc/fastp/{sample}.1.fastq"],
        idx=multiext(
            config["database"]["datasets"], ".amb", ".ann", ".bwt", ".pac", ".sa"
        ),
    output:
        "find/{sample}.bam",
    log:
        "logs/find/{sample}_bwa_datasets.log",
    benchmark:
        "logs/find/{sample}_bwa_datasets.bm"
    params:
        extra=r"-R '@RG\tID:{sample}\tSM:{sample}'",
        sorting="samtools",  # Can be 'none', 'samtools' or 'picard'.
        sort_order="coordinate",  # Can be 'queryname' or 'coordinate'.
        sort_extra="",  # Extra args for samtools/picard.
    conda:
        config["conda"]["basic"]
    threads: config["threads"]["high"]
    wrapper:
        f"file:{workflow.basedir}/wrappers/bio/bwa/mem"


use rule bwa_mem_datasets_se as bwa_mem_datasets_pe with:
    input:
        ["qc/fastp/{sample}.1.fastq", "qc/fastp/{sample}.2.fastq"],


rule samtools_coverage_datasets:
    input:
        "find/{sample}.bam",
    output:
        "find/{sample}.coverage",
    log:
        "logs/find/{sample}_samtools_coverage.log",
    benchmark:
        "logs/find/{sample}_samtools_coverage.bm"
    conda:
        config["conda"]["basic"]
    shell:
        "samtools coverage {input} >{output}"


rule find_most_similar:
    input:
        rules.samtools_coverage_datasets.output,
    output:
        "find/{sample}_most_similar.id",
    log:
        "logs/find/{sample}_find_most_similar.log",
    benchmark:
        "logs/find/{sample}_find_most_similar.bm"
    conda:
        config["conda"]["python"]
    script:
        "../scripts/find_most_similar.py"


rule virus_type:
    input:
        most_similar=rules.find_most_similar.output[0],
        acc_type=config["database"]["acc_type"],
    output:
        "type/{sample}.type",
    log:
        "logs/type/{sample}.virus_type.log",
    benchmark:
        "logs/type/{sample}.virus_type.bm"
    script:
        "../scripts/virus_type.py"


rule find_ref:
    input:
        rules.virus_type.output,
    output:
        "find/{sample}_ref.fa",
    params:
        hbvtype=config["database"]["hbvtype"],
    log:
        "logs/find/{sample}_find_ref.log",
    benchmark:
        "logs/find/{sample}_find_ref.bm"
    conda:
        config["conda"]["python"]
    script:
        "../scripts/find_ref.py"


rule ref_index:
    input:
        rules.find_ref.output[0],
    output:
        multiext(rules.find_ref.output[0], ".amb", ".ann", ".bwt", ".pac", ".sa"),
    log:
        "logs/find/{sample}_ref.log",
    benchmark:
        "logs/find/{sample}_ref.bm"
    params:
        extra="",
    conda:
        config["conda"]["basic"]
    wrapper:
        f"file:{workflow.basedir}/wrappers/bio/bwa/index"
