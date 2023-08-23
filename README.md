# MetagenomeStrainy_ONT_pipeline
## Introduction

The pipeline is designed to analyze real metagenome data obtained from ONT sequencing technology. Due to the complexity of real metagenomic data, this pipeline suggests a two-step approach. First, the assembly is split into Metagenome-Assembled Genomes (MAGs), and subsequently, the [**stRainy**](https://github.com/katerinakazantseva/stRainy) is applied to each MAG individually. Please note that only MAGs with coverage>30, contamination <20 and completeness >80 will be phased.

## Data
### Input data
As an innput data use ONT reads

### Output data
* __flye_output__ initial metagenome assembly
* __bins__ - initial MAG binning
* __qa_bins__ - initial MAG quality
* __strainy_final__ phased MAGs
* __transformed_bins__ phased MAGs fasta files
* __qa_transformed_bins__ - phased MAG quality


## Installation
```
git clone https://github.com/katerinakazantseva/MetagenomeStrainy_ONT_pipeline.git
cd MetagenomeStrainy_ONT_pipeline
```

### Requirements
* [**Snakemake**](https://snakemake.github.io/) conda environment 
* [**stRainy**](https://github.com/katerinakazantseva/stRainy) conda environment 
* [**Clair3**](https://github.com/HKU-BAL/Clair3) conda environment 
* [**Checkm2**](https://github.com/chklovski/CheckM2) conda environment 
* [**metabat2**](https://anaconda.org/bioconda/metabat2) installed in snakemake conda environment 

## Pipeline Steps
* Build a metagenome assembly with metaFlye
* Call MAGs with metabat
* Check the quality of MAGs with checkM2
* Filtering MAGs by completeness, coverage and contamination
* Phasing each MAG with stRainy

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

