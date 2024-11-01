<div align="center">

# Envsion - Cuztomizable AI Image Generation Tool
## Envision is a fork of the program Invoke which is a creative engine built on top of Stable Diffusion, Envision houses more customizable features which allows users to complete control over resulting models.

</div>

<div align="center">

# Disclaimer
## "This program uses the Invoke engine, which is the property of its respective owner(s). Invoke is a registered trademark and copyrighted material; all rights are reserved to the original copyright holder. This project does not claim ownership of Invoke or its affiliated intellectual property, nor does it intend to infringe on the rights of the copyright or trademark owner(s). The use of Invoke within this application is solely for its intended functionality and is used in accordance with applicable licenses."

</div>

# Documentation
| **Quick Links**                                                                                                      | 
|----------------------------------------------------------------------------------------------------------------------------|
|  [Installation and Updates][installation docs] - [Documentation and Tutorials][docs home]  | 

</div>

## Quick Start

1. Download and unzip the installer from the bottom of the [latest release][latest  release link].
2. Run the installer script.

   - **Windows**: Double-click on the `install.bat` script.
   - **macOS**: Open a Terminal window, drag the file `install.sh` from Finder into the Terminal, and press enter.
   - **Linux**: Run `install.sh`.

3. When prompted, enter a location for the install and select your GPU type.
4. Once the install finishes, find the directory you selected during install. The default location is `C:\Users\Username\invokeai` for Windows or `~/invokeai` for Linux/macOS.
5. Run the launcher script (`invoke.bat` for Windows, `invoke.sh` for macOS and Linux) the same way you ran the installer script in step 2.
6. Select option 1 to start the application. Once it starts up, open your browser and go to <http://localhost:9090>.
7. Open the model manager tab to install a starter model and then you'll be ready to generate.

More detail, including hardware requirements and manual install instructions, are available in the [installation documentation][installation docs].

### Generate!


### DIY

Build your own image and customize the environment to match your needs using our `docker-compose` stack. See [README.md](./docker/README.md) in the [docker](./docker) directory.

## Troubleshooting, FAQ and Support

Please review our [FAQ][faq] for solutions to common installation problems and other issues.

## Features

Full details on features can be found in [our documentation][features docs].

### Web Server & UI

Invoke runs a locally hosted web server & React UI with an industry-leading user experience.

### Unified Canvas

The Unified Canvas is a fully integrated canvas implementation with support for all core generation capabilities, in/out-painting, brush tools, and more. This creative tool unlocks the capability for artists to create with AI as a creative collaborator, and can be used to augment AI-generated imagery, sketches, photography, renders, and more.

### Workflows & Nodes

Invoke offers a fully featured workflow management solution, enabling users to combine the power of node-based workflows with the easy of a UI. This allows for customizable generation pipelines to be developed and shared by users looking to create specific workflows to support their production use-cases.

### Board & Gallery Management

Invoke features an organized gallery system for easily storing, accessing, and remixing your content in the Invoke workspace. Images can be dragged/dropped onto any Image-base UI element in the application, and rich metadata within the Image allows for easy recall of key prompts or settings used in your workflow.

### Other features

- Support for both ckpt and diffusers models
- SD1.5, SD2.0, SDXL, and FLUX support
- Upscaling Tools
- Embedding Manager & Support
- Model Manager & Support
- Workflow creation & management
- Node-Based Architecture

Original portions of the software are Copyright © 2024 by respective contributors.

[features docs]: https://invoke-ai.github.io/InvokeAI/features/database/
[faq]: https://invoke-ai.github.io/InvokeAI/faq/
[docs home]: https://invoke-ai.github.io/InvokeAI
[installation docs]: https://invoke-ai.github.io/InvokeAI/installation/