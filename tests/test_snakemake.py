from kml_viruswgs import create_snakemake_configfile
from kml_viruswgs import get_sample_names_by_samptab
from kml_viruswgs import run_snakemake


work_dir = '/data/mengxf/Project/KML241212_HBV_WGS/result/25010802'
sample_table = '/data/mengxf/Project/KML241212_HBV_WGS/input/input.tsv'


def test_create():
    sample_names = get_sample_names_by_samptab(sample_table)
    create_snakemake_configfile(sample_names, work_dir)


# def test_run():
#     run_snakemake(work_dir)
