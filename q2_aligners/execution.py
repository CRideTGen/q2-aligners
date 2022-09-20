import time

import parsl
from pathlib import Path

from parsl import ThreadPoolExecutor
from parsl.app.app import python_app, bash_app, join_app
from parsl.config import Config
from parsl.launchers import SrunLauncher
from parsl.providers import SlurmProvider
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_hostname

config = Config(
    executors=[
        HighThroughputExecutor(
            max_workers=1,
            address=address_by_hostname(),
            provider=SlurmProvider(
                min_blocks=0,
                max_blocks=1,
                init_blocks=1,
                nodes_per_block=1,
                cores_per_node=1,
                walltime='00:10:00',
                scheduler_options="#SBATCH --ntasks-per-node=5",
                launcher=SrunLauncher(),
                parallelism=0,
                exclusive=False
            )
        )
    ]
)

config = Config(
    executors=[
        ThreadPoolExecutor(
            max_threads=4,
            label='local_threads'
        )
    ]
)
parsl.load(config)
