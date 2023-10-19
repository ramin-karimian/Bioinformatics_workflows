import os

def exe_cmd(cmd):
    print(f"executing : \n{cmd}")
    os.system(cmd)
    print("\n\n")

if __name__=="__main__":


    conf = {
        "qs":25,
        'threads':12,
        'ref_db':'/scratch/st-spakpour-1/kneaddataDB',
        'data_folder': "/project/st-spakpour-1/Data_Leah/",
    	'max_memory':"2000m",
        'minlen':70,
        'headcrop':15,
    }


    data_folder = f'/scratch/st-spakpour-1/bioinformatic-pipelines-workflow/trimmed_{conf["qs"]}_{conf["minlen"]}_{conf["headcrop"]}'

    fastqc_folder = f'/scratch/st-spakpour-1/bioinformatic-pipelines-workflow/qc_results/fastqc_{data_folder.split("/")[-1]}'
    multiqc_folder = f'/scratch/st-spakpour-1/bioinformatic-pipelines-workflow/qc_results/multiqc_{data_folder.split("/")[-1]}'

    print('\n\n\nFastQC step\n')
    cmd1 = f"fastqc -f fastq -o {fastqc_folder} {data_folder}/*-*/*_kneaddata_paired_*.fastq -t {conf['threads']} > PBS_files/logfiles/{fastqc_folder.split('/')[-1]}.log 2>&1 "


    if f'fastqc_{data_folder.split("/")[-1]}' not in os.listdir("qc_results"):
        os.mkdir(fastqc_folder)
        os.mkdir(multiqc_folder)

    exe_cmd(cmd1)
    print('\n\n\nMultiQC step\n')
    cmd2 = f"multiqc {fastqc_folder} -o {multiqc_folder}"
    exe_cmd(cmd2)
