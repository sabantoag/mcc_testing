// This script is used to execute the tests in the mcc_testing-0.1 directory.
//It activates the conda environment, runs the tests with pytest, and then deactivates the environment.
@echo off

cd mcc_testing-0.1
call conda activate 82-16496
call pytest --log-cli-level=DEBUG
call conda deactivate
