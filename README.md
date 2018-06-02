1. Install Docker: https://docs.docker.com/install/

1. Get kaggle credential file
    - follow the instruction [here](https://github.com/Kaggle/kaggle-api#api-credentials) and get `kaggle.json`
    - place the `kaggle.json` in the same directory as `Dockerfile`

1. Kick run_tensorflow.sh

    1. `$ sh run_tensorflow.sh`

    When running on VM. Foward the port 8888 and 6006 for jupyter-notebook and tensorboard.

1. To download input data from Kaggle, run the following script inside container (e.g. from the top cell of the notebook)  
`prepare_data.sh`  
Note that downloaded files persists in `input` directory, so you don't have to run this script multiple times.