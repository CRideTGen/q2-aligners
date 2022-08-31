import qiime2
from qiime2.plugins import readmappers
print("loading sequences")
sequences = qiime2.Artifact.load("/home/cridenour/tmp/test_data/paired-end-demux-test.qza")
print("loading reference")
ref_genome = qiime2.Artifact.load("/home/cridenour/tmp/test_data/reference/reference_index.qza")
print("running output")
output = readmappers.actions.mem_paired(sequences)
output.output_sams.save("cool_beans_mem_paired", ".qza")