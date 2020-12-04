A package to make your uni clases better

Created by Eduardo Atonatiuh Camarena Santamaría and Diego Salvador Gonzales Camacho

To install project with CUDA support use the following commands before installing (requires conda):
conda install cudatoolkit=10.0
conda install cudnn=7.6
and change the first requirement from the requirements.txt file to tensorflow-gpu==1.15
Then you can install the package with the following command: "pip install -e ."

If you're not going to use a CUDA enabled GPU just install the package normally

after installing the package install the cocoapi with (requires Visual C++ 2015 Build Tools): pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI

then clone the matterport mask-rcnn repo to a different folder: git clone https://github.com/matterport/Mask_RCNN.git,
go to: https://github.com/matterport/Mask_RCNN/releases 
download the mask_rcnn_coco.h5 file to the root of the mask-rcnn repo
install the package with the command "pip install ." (your console needs to be in the root of the mask-rcnn repo)