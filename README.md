Welcome to the repository, here you will encounter all the codes used for the development of my thesis

- **/scripts/**: Contains all scripts used
    - **`clean_expose_binned.xml`**: This file is the sequencer, where we can change the clock delays and decide where to send the charge.
    - **`run_variables.sh`**: In this file, we can change the number of skips, CDS integration times, exposure time, bias voltage, and the dimensions of the CCD that will be read.
    - **`voltage_setup.xml`**: This script allows changing the values for the voltages of the clocks and gates.
    - **`panaSKImg_config_LTA_proc.json`**: This file contains the various WADERS processes to clean the data.
    - **`hot_columns_2.py`**: This script includes calculations for both dark current and gain, as well as the implementation of the hot column detection algorithm.
    - **`Optimization_hot_columns.py`**: In this script, we obtain the optimal value for sigma to optimize hot column detection.
    - **`NN_muons.py`**: This script is used for training and prediction with the DNN.
    - **`results_file.py`**: This file should be replaced with `results.py` from the Ultralytics package for better visualization of the detected clusters.

