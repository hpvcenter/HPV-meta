# HPV-meta
Bioinformatics pipeline for HPV detection in RNA sequencing specimens. 
“HPV-meta" performs several steps including quality trimming ([trimmomatic](https://github.com/usadellab/Trimmomatic) and [cutadapt](https://github.com/marcelm/cutadapt/)), human genome filtering ([nextgenmap](https://github.com/Cibiv/NextGenMap)), [samtools](https://github.com/samtools/samtools), HPV detection ([diamond](https://github.com/bbuchfink/diamond)), cut-off settlement, coverage calculation, variant calling and fasta generation.

**Flowchart**

![41598_2022_17318_Fig1_HTML](https://github.com/hpvcenter/HPV-meta/assets/67340348/3256e6cb-9ba1-4cb4-80d2-d32c7b7ca5f1)


**Contents:**
The content of the repository is as follows:

- src - contains the source Jupyter notebooks files for each bioinformatic program
- settings - consists configuration file for arguments to the program in YAML format
- jobs_config - Hopsworks Jobs configuration JSONs
- airflow_pipeline - Python script for the running the pipeline as Airflow DAG
- postprocessing: phyton scripts for cutt-off settlement, coverage analysis, variant calling and fasta generation

To setup the pipeline we first need a running Hospworks cluster. To know more about open-source version of Hopsworks and installation check the [github repo](https://github.com/dhananjay-mk/hopsworks) or visit the official [documentation](https://docs.hopsworks.ai/latest/)

Once the Hopsworks cluster is installed, the pipeline can be setup in below steps:

 1. Create datasets for output and input. Upload the data into the input dataset
 2. Clone this repo into the Hopsworks project or upload the source code 
 3. Modify the settings.yml
 4. Create jobs. You may use the jobs_config JSON files to import the job configs
 5. Upload the airflow pipeline python script. This contains the Airflow DAG. You have the modify project name, user name and provide a unique DAG name


**When using the tool in published research, please cite:**
Ure A, Mukhedkar D, Arroyo Mühr LS. Using HPV-meta for human papillomavirus RNA quality detection. Sci Rep. 2022 Jul 29;12(1):13058. doi: 10.1038/s41598-022-17318-5. PMID: 35906372; PMCID: PMC9338075.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9338075/
