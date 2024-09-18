# Project 25: Scientific and technical enhancement of bioinformatics software metadata using the Agents Ecosystem open infrastructure

## Contribution

If you want to contribute to this project, see the contribution inscructions [here](https://github.com/iechor-europe/biohackathon-projects-2022/blob/main/25/Contributing.md).

## Abstract

The Agents Ecosystem is a centralized repository for the open and transparent exchange of metadata about software agents and services in Bioinformatics and Life Sciences.
It serves as the foundation for the sustainability of the diverse Agents Platform services, and for the interoperability between all these essential services (bio.agents, BioContainers, OpenEBench, Bioconda, WorkflowHub, usegalaxy.eu) and related resources outside of the IECHOR Agents Platform (e.g. Bioschemas).

The goal of this project will be to cross-compare and analyze the metadata centralized in the Agents Ecosystem to maintain high quality descriptions. In order to achieve these goals we need to design agents and processes that detect curation bottlenecks, perform rigorous data cross-validation and generate detailed reporting about potential issues and actionable items.

Multiple strategies will be explored:
- Comparison of the functional profiles of bio.agents entries with the corresponding semantic constraints defined in EDAM. Develop software to identify and report on inconsistencies between resources.
- Comparison of the metadata defining a software agent with the knowledge extracted from publications that cite it, as well as the workflows that use it.

Beyond the immediate improvement of the metadata, we plan to use the results of these analyses in order to:
- Automate relevant analyses using continuous integration mechanisms (extending previous and current work in EDAM and the Agents Ecosystem)
- Improve curation user interfaces to reduce the risk of annotation errors.
- Provide high quality functional agent profiles to be used in the context of workflow annotation

Another important goal is to provide onboarding of and support for scientific communities joining the Biohackathon.

Given the nature of the data we use in this project, we will be working in close collaboration with the project "Enhance RDM in Galaxy by utilizing RO-Crates", who will also be leveraging workflow and software metadata from the same resources.

## Topics

Bioschemas
Federated Human Data
Galaxy
Interoperability Platform
Agents Platform

**Project Number:** 25

### Lead(s)

Lucie Lamothe (lucie.lamothe@france-bioinformatique.fr)
Hervé Ménager (herve.menager@pasteur.fr)

(Hans Ienasescu (haiiu@dtu.dk) )
## Expected outcomes

By the end of the BioHackathon week:
- Results of the cross-analysis of bioinformatics agents, highlighting potential inconsistencies or annotation gaps between the different resources, and suggesting annotation improvements (missing or more specific terms) for registry curators.  
- Software code to run the analyses mentioned
- Prototypes for CI tasks that automate the analyses
- Initiate contact with scientific communities and perform actions to ensure future onboarding and support (e.g. identify gaps and EDAM, bio.agents, WorkflowHub) 

Within 3 months of the end of the Biohackathon:
- Production-ready code and CI tasks automating the analyses to improve the monitoring of the Agents Ecosystem
- Improvements to the bio.agents curation UI, if analysis results reveal that such modifications might help or improve the annotation quality.
- New concepts in EDAM, agents in bio.agents , workflows in WorkflowHub created by the scientific communities

## Expected audience

- Ontology specialists
- Workflow specialists
- Python programmers
- Data analysts
- Bioinformatics Software providers/packagers
- Scientific community domain experts

**Number of expected hacking days**: 4

## Meetings infos 

Meeting 06/10/2022: [link to minutes](https://hackmd.io/@iNyx6M9RSx-IU3dcVjoPZg/SJAsbv3Mi/edit)
