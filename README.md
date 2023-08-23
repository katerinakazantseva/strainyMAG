# MetagenomeStrainy_ONT_pipeline
## Introduction

The stRainy pipeline is designed to analyze real metagenome data obtained from ONT sequencing technology. Due to the complexity of real metagenomic data, this pipeline suggests a two-step approach. First, the assembly is split into Metagenome-Assembled Genomes (MAGs), and subsequently, the stRainy tool is applied to each MAG individually. This approach improves the accuracy and efficiency of strain-level analysis for complex metagenomic samples.

## Data
### Input data
As an innput data use ONT reads
### Output data

## Installation

### Requirements
* snakemake env
* strainy env

### Install
Follow the installation instructions provided by stRainy to install the stRainy tool.
Install the required assembly tool and MAG binning tool following their respective documentation.

## Pipeline Steps
* Build metagenome assembly using metaFlye
* Call MAGs metabat
* Quality assurance checkM2
* Filtration MAGs based on completeness, coverage and contamination
* Phasing each bam with stRainy

### Configuration

### How to run

