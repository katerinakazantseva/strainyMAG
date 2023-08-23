# MetagenomeStrainy_ONT_pipeline
## Introduction

The pipeline is designed to analyze real metagenome data obtained from ONT sequencing technology. Due to the complexity of real metagenomic data, this pipeline suggests a two-step approach. First, the assembly is split into Metagenome-Assembled Genomes (MAGs), and subsequently, the stRainy tool(https://github.com/katerinakazantseva/stRainy) is applied to each MAG individually.

## Data
### Input data
As an innput data use ONT reads
### Output data
* __flye_output/__
* __strainy_split/__
* __bins/__ - 
* __qa_bins/__ - 
* __strainy_final/__
* __ransformed_bins/__ 
* __qa_transformed_bins__ - 


## Installation
```
git clone https://github.com/katerinakazantseva/MetagenomeStrainy_ONT_pipeline.git
cd MetagenomeStrainy_ONT_pipeline
```

### Requirements
* Snakemake conda env https://snakemake.github.io/
* Strainy env https://github.com/katerinakazantseva/stRainy
* Clair3 https://github.com/HKU-BAL/Clair3
* Checkm2 conda env https://github.com/chklovski/CheckM2
* metabat2 installed in snakemake env https://anaconda.org/bioconda/metabat2

## Pipeline Steps
* Build metagenome assembly using metaFlye
* Call MAGs metabat
* Quality assurance checkM2
* Filtration MAGs based on completeness, coverage and contamination
* Phasing each bam with stRainy

### Configuration
Before run please update parameters in snakemake file:

* __input_reads__ - reads path (.fq)
* __flye_path__ - Flye path
* __conda_path__ Conda envs path (i.e "~/miniconda3/envs/")
* __strainy_path__ - Strainy path
* __clair_model_path__ - Clair model path (r1041_e82_400bps_sup_v420 is recomended see https://github.com/nanoporetech/rerio)

### How to run
```
conda activate snakemake
snakemake --snakefil snakemake --cores 30 --use-conda 
```

