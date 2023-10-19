import os

def exe_cmd(cmd):
    print(f"executing : \n{cmd}")
    os.system(cmd)
    print("\n\n")

if __name__=="__main__":


    conf = {
        "qs":25,
        'threads':40, ## number of cores which are going to be used
        'ref_db':'/scratch/st-spakpour-1/kneaddataDB',
        'data_folder': "Data", ## sequencing files should be here with each sample in a separate folder
    	'max_memory':"2000m",
        'minlen':70,
        'headcrop':15,
        'crop':150
    }

    folderpath = conf['data_folder']
    trimmed_folder = f'trimmed_{conf["qs"]}_{conf["minlen"]}_{conf["headcrop"] if "headcrop" in conf else"_"}'

    if trimmed_folder not in os.listdir():
        os.mkdir(trimmed_folder)

    for f in os.listdir(folderpath):

        if ".fastq" not in f: continue
        if "R1" in f:
            read1 = f
            read2 = read1.replace('R1','R2')
        elif 'R2' in f: continue

        print(read1,"\n",read2,"\n")

        id = "-".join(read1.split('-')[:-1])  ## This line may need modification depending on the type of the files naming. The ideas is to extract the id of the sample out of the file name.

        os.mkdir(f"{trimmed_folder}/{id}")

        minlen = conf['minlen']
        qs = conf['qs']
        headcrop = conf['headcrop']
        CROP =  conf['crop']

        if 'headcrop' in conf:
            trimmomatic_options = f'SLIDINGWINDOW:4:{qs}  HEADCROP:{headcrop} MINLEN:{minlen} CROP:{CROP}'
        else:
            trimmomatic_options =  f'SLIDINGWINDOW:4:{qs} MINLEN:{minlen} CROP:{CROP}'


        cmd = f" kneaddata --input {folderpath}/{read1} --input {folderpath}/{read2} --threads {conf['threads']}" \
              f" --processes {conf['threads']}  --reference-db {conf['ref_db']}  --output {trimmed_folder}/{id}" \
              f" --max-memory {conf['max_memory']} --remove-intermediate-output" \
              f" --trimmomatic /home/raminka/.local/bin/Trimmomatic-0.39  --trimmomatic-options '{trimmomatic_options}'" \
              f"  >> {trimmed_folder}/{id}/cmd_logfile.txt 2>&1"

        os.system(cmd)


