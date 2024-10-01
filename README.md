# P300SpellerNFB

This repository contains the code for two key components used in a clinical trial: a P300 speller for neurofeedback training and a Random Dot Motion (RDM) task designed to assess cognitive abilities, particularly attention. The details of the trial can be found in the following journal articles:

 - Noble SC, Woods E, Ward T, Ringwood JV. “Adaptive P300-Based Brain-Computer Interface for Attention Training: Protocol for a Randomized Controlled Trial.” JMIR Res Protoc 2023, 12:e46135, doi: 10.2196/46135

 - Noble SC, Woods E, Ward T, Ringwood JV. “Accelerating P300-Based Neurofeedback Training for Attention Enhancement Using Iterative Learning Control: A Randomised Controlled Trial.” J Neural Eng 2024, 21(2), doi: 10.1088/1741-2552/ad2c9e

Please make sure to cite these article when using this code.

Repository Overview:
 - OVScenarios, metaboxes, and ConfigurationFiles: These folders contain code for a modified version of OpenViBE’s xDAWN P300 speller, used for neurofeedback training.
 - RDMTask: Contains the code for the RDM task, developed using PsychoPy, which tests cognitive abilities related to attention.
 - ExperimentBatch.cmd: A script that automates the experimental session for the clinical trial.
 - control1.m, control2.m, experimental.m: MATLAB scripts that adjust the task difficulty of the P300 speller to personalize the training based on performance.
