from pathlib import Path

import pandas as pd
from parsl.channels import LocalChannel
from q2_nasp2_types.types import BWAIndex, BWAIndexDirFmt, SAMFileDirFmt
from q2_types.per_sample_sequences import SingleLanePerSampleSingleEndFastqDirFmt, \
    SingleLanePerSamplePairedEndFastqDirFmt

import time

import parsl
from pathlib import Path

from parsl import ThreadPoolExecutor
from parsl.app.app import python_app, bash_app, join_app
from parsl.config import Config
from parsl.launchers import SrunLauncher
from parsl.providers import SlurmProvider, LocalProvider
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_hostname

config = Config(
    executors=[
        HighThroughputExecutor(
            label="htex_Local",
            worker_debug=True,
            cores_per_worker=1,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                max_blocks=1,
            ),
        )
    ],
)

parsl.clear()
parsl.load(config)


@bash_app
def bwa_mem_align_single():
    pass


@bash_app
def bwa_mem_align_paired(forward, reverse, reference, output_sam):
    return f"bwa mem {reference} {forward} {reverse} > {output_sam}"


def mem_single(sequences: SingleLanePerSampleSingleEndFastqDirFmt, ref_genome: BWAIndex) -> SAMFileDirFmt:
    output_sams = SAMFileDirFmt()
    seq_path = Path(str(sequences))
    output_sams_path = Path(output_sams.path).joinpath("test.sam")

    with open(output_sams_path, 'w') as ff:
        ff.write("test1")
    return output_sams


def mem_paired(sequences: SingleLanePerSamplePairedEndFastqDirFmt, ref_genome: BWAIndex) -> SAMFileDirFmt:
    output_sams = SAMFileDirFmt()
    seq_df = sequences.manifest.view(pd.DataFrame)
    ref = str(ref_genome.view(BWAIndexDirFmt).path.joinpath("dna-sequences.fasta"))
    paired_reads = [i for i in seq_df.itertuples()]

    for id, f, r in paired_reads:
        output_sams_path = str(Path(output_sams.path).joinpath(f"{id}.sam"))

        # bwa_mem_align_paired(f, r, ref, output_sams_path)

    return output_sams
