import os

def exe_cmd(cmd):
    print(f"executing : \n{cmd}")
    os.system(cmd)
    print("\n\n")

if __name__=="__main__":
    print('\n\n\nStep 1\n')
    conf = {
        "qs":25,
        'threads':40,
        'db':'/scratch/st-spakpour-1/metaphlanDB202103/', ## this is for metaphlan 4
        'dbname':  'mpa_vJan21_CHOCOPhlAnSGB_202103', ## this is for metaphlan 4
        'minlen':70,
        'headcrop':15,
    }

    trimmed_folder = f'trimmed_{conf["qs"]}_{conf["minlen"]}_{conf["headcrop"]}'
    metaphlan_folder = f'mpa4_{trimmed_folder}'

    if metaphlan_folder not in os.listdir():
        os.mkdir(metaphlan_folder)

    if "sams" not in os.listdir(metaphlan_folder):
        os.mkdir(f"{metaphlan_folder}/sams")

    files = {}
    for fo in os.listdir(trimmed_folder):
        # the next 4 lines may need modifications, the idea is to skip the files which are not our fastq files (or any other file formats) and only analyze the fastq files.
        for f in os.listdir(f"{trimmed_folder}/{fo}"):
            filepath = f"{trimmed_folder}/{fo}/{f}"
            if ".fastq" not in f: continue
            if "_kneaddata_paired_" not in f: continue
            print(f"{filepath}\n")
            id = "-".join(f.split('-')[:-1])  ## This line may need modification depending on the type of the files naming. The ideas is to extract the id of the sample out of the file name.

            if id not in files:
                files[id] = []
                files[id].append(f)
            else:
                files[id].append(f)

    for id in files.keys():
        for f in files[id]:
            if "_paired_1" in f : f1 = f
            elif "_paired_2" in f: f2 = f

        cmd = f"metaphlan -t rel_ab_w_read_stats --bowtie2db {conf['db']} {trimmed_folder}/{id}/{f1},{trimmed_folder}/{id}/{f2} -x {conf['dbname']}" \
              f" -s {metaphlan_folder}/sams/{f1.replace('.fastq','').replace('_R1','').replace('_paired_1','')}.sam.bz2" \
              f" --bowtie2out {metaphlan_folder}/{f1.replace('.fastq','').replace('_R1','').replace('_paired_1','')}.bowtie2.bz2" \
              f" --nproc {conf['threads']}  --input_type fastq --add_viruses --sample_id_key {id}" \
              f" --unclassified_estimation" \
              f" -o {metaphlan_folder}/{f1.replace('.fastq','').replace('_R1','').replace('_paired_1','')}.txt" \
              f" >> {metaphlan_folder}/{'_'.join(f1.split('_')[:2])}_cmd.log 2>&1"

        exe_cmd(cmd)

    cmd2 = f"merge_metaphlan_tables.py {metaphlan_folder}/*_kneaddata.txt > outputs/merged_abundance_table_{metaphlan_folder}.txt"
    exe_cmd(cmd2)



