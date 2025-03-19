# ComfyUI-VideoTagger

## Introduction
ComfyUI-VideoTagger is a video tagging assistant tool that helps users easily manage and tag video and image files. Through a simple interface, it enables users to browse and organize media files.
![Example Workflow](./example_workflows/workflow.png)

## Main Features

### Video/Image Address List Node
- Automatically scans and outputs a list of video or image files in the input directory
- Generates corresponding text file lists based on filenames
- Outputs absolute file paths for subsequent processing

### Save Node
- Copy media files to specified locations using the input directory, media filename, and tagging prompt content
- Simultaneously generates and records tagging text files
- Facilitates subsequent management and retrieval

### Zhipu GLM Video Analysis
API key required: https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys

## Installation Method
Install via ComfyUI-Manager or manually using the following steps:
1. Clone or download this project to the ComfyUI custom_nodes directory
   ```
   cd ComfyUI/custom_nodes/ComfyUI-VideoTagger
   pip install -r requirements.txt
   ```
2. Restart ComfyUI
3. Find VideoTagger related nodes in the node list to use

## Usage Example
- [VideoTagger Example](./example_workflows/workflow.png)

## Special Thanks
- [@yolain](https://github.com/yolain/ComfyUI-Easy-Use) - Created the ComfyUI-Easy-Use project, providing various optimizations and integrations to make ComfyUI easier to use

## Contributions
Welcome to submit issue reports and feature suggestions!

![NiceJob](./nicejob.jpg) 