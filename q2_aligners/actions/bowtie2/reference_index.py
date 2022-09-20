import subprocess

from q2_types.bowtie2 import Bowtie2IndexDirFmt
from q2_types.feature_data import DNAFASTAFormat


def _run_command(cmd, verbose=True, stdout=None, stdin=None, cwd=None):
    if verbose:
        print('Running external command line application. This may print '
              'messages to stdout and/or stderr.')
        print('The commands to be run are below. These commands cannot '
              'be manually re-run as they will depend on temporary files that '
              'no longer exist.')
        print('\nCommand:', end=' ')
        print(' '.join(cmd), end='\n\n')
    subprocess.run(cmd, check=True, stdout=stdout, stdin=stdin, cwd=cwd)


def bowtie2_build(sequences: DNAFASTAFormat,
                  n_threads: str = 1) -> Bowtie2IndexDirFmt:
    database = Bowtie2IndexDirFmt()
    build_cmd = ['bowtie2-build', '--threads', str(n_threads),
                 str(sequences), str(database.path / 'db')]
    _run_command(build_cmd)
    return database
