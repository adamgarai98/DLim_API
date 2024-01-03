
# DLim_api

**This repository contains my Deep Learning IMage (DLim) API project, which is essentialy a RESTful Python API implemented using Flask, which allows a user to upload images and run inference using pre-built models.**

Some current features: SAM, multithreading, status of tasks, Docker, CUDA, arguments parsing (log levels, host, port), automatic versioning, exception handling.

Todo: Iterative solving of CUDA out of memory errors. More models. Return masks.

Can be installed using pip or built with docker

## Docker Installation Instructions
Simply clone and enter the repository, and run `docker build -t dlim_api .` to build the project and `docker run --rm -p 5000:5000 --gpus all dlim_api -ll 10`, to run the project on localhost using all GPU's (assumed CUDA is installed) with the desired logging level you wish (please refer to Python standard logging levels). 

## CUDA
If you do not have CUDA installed and do NOT wish to use it, just run the project as normal but without the `--gpus all` flag, and your CPU will be used instead.

If you do not have CUDA installed and wish to use it, please follow the relevant guides for your operating system:
[WINDOWS](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html)
[LINUX](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)

  ## USAGE
  ### Segment Anything Model (SAM)
  
  [SAM](https://github.com/facebookresearch/segment-anything) developed by Meta AI can be used to automatically generate masks for your images.
  
  Ensure that you have the "sam_vit_h_4b8939.pth" model checkpoint downloaded from [here](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth) and placed in `src\dlim_api\utils\model_checkpoints\sam_vit_h_4b8939.pth`
  
**Endpoints:**
 - `PUT /sam/load` Loads the SAM automatic mask generator.
 - `POST /sam/segment` Post an image for segmentation. This will return a unique `<task_id>` and begin predicting segmentation masks.
 - `GET /sam/segment/status/<task_id>` Gets the status of a <task_id> for that specific image. If completed will return the segmented image, otherwise will return the status (i.e. "Not found", "Error <message>" etc) 

## Version Bumping through PR titles

My repository uses an automated versioning system that relies on the naming convention of the pull request titles. When you merge a pull request into the dev branch, the version number of the project is automatically bumped and a new tag is created, based on the prefix in your PR title.

  

The version number follows the MAJOR.MINOR.FIX format, where:

  

MAJOR version increments indicate significant changes or enhancements in the project, often including breaking changes. MINOR version increments indicate backwards-compatible new features or enhancements. FIX version increments indicate backwards-compatible bug fixes or minor changes. To specify the type of changes you have made in your pull request, prefix your PR title with one of the following:

  

major: - to increment the MAJOR version (e.g., from 1.0.0 to 2.0.0). minor: - to increment the MINOR version (e.g., from 0.1.0 to 0.2.0). fix: - to increment the FIX version (e.g., from 0.0.1 to 0.0.2). For example, if you have made a minor change, your PR title could be: minor: Add new feature XYZ.

  

If your PR title does not include any of the specified prefixes, the GitHub Action will not increment the version or create a new tag. This can be useful for non-functional changes like updates to documentation or code refactoring that don't require a version bump.

  

When your PR is merged into main, the GitHub Action will increment the version according to the prefix in the PR title and create a new tag.

  

Please ensure you follow this convention to maintain a well-structured and meaningful version history for my project.