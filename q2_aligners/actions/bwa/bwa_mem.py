import pathlib
import subprocess
from pathlib import Path

import pandas as pd
import parsl
from parsl.app.app import bash_app
from parsl.channels import LocalChannel
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.providers import LocalProvider
from q2_nasp2_types.alignment import SAMFileDirFmt
from q2_nasp2_types.index import BWAIndex, BWAIndexDirFmt
from q2_types.per_sample_sequences import SingleLanePerSamplePairedEndFastqDirFmt, \
    SingleLanePerSampleSingleEndFastqDirFmt

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

#get
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


def mem_paired(sequences: SingleLanePerSamplePairedEndFastqDirFmt) -> SAMFileDirFmt:
    # ref = str(ref_genome.view(BWAIndexDirFmt).path.joinpath("dna-sequences.fasta"))
    ref = "/home/cridenour/tmp/test_data/reference/f6779c89-cba0-462e-86ff-46185bcd006f/data/dna-sequences.fasta"
    output_sams = SAMFileDirFmt()
    seq_df = sequences.manifest.view(pd.DataFrame)
    paired_reads = [i for i in seq_df.itertuples()]
    for sample_name, f, r in paired_reads:
        output_sams_path = Path(output_sams.path).joinpath(f"{sample_name}.sam")
        build_cmd = ['bwa', 'mem', ref, f, r]

        with open(output_sams_path, 'w') as s_file:
            process = subprocess.run(build_cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True, stdin=None,
                                     cwd=None)
            output = process.stdout
            s_file.write(output)

        # bwa_mem_align_paired(f, r, ref, output_sams_path)

    return output_sams
