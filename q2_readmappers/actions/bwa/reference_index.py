import subprocess
from pathlib import Path

from q2_nasp2_types.types import BWAIndexDirFmt
from q2_types.feature_data import DNAFASTAFormat


def index(sequences: DNAFASTAFormat) -> BWAIndexDirFmt:
    database = BWAIndexDirFmt()
    seq_path = Path(str(sequences))
    db_path = Path(database.path)
    seq_sym_link = db_path.joinpath(seq_path.name)
    seq_sym_link.symlink_to(seq_path)

    build_cmd = ['bwa', 'index', str(seq_sym_link)]

    subprocess.run(build_cmd, check=True, stdout=None, stdin=None, cwd=None)
    seq_sym_link.unlink()

    return database
