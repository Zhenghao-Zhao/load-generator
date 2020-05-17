
# Instaload
A collaboration project between [Instaclustr](https://www.instaclustr.com/) and the [ANU TechLauncher initiative](https://cs.anu.edu.au/TechLauncher/).

## About
Instaload is an application which can emulate metrics data generated from a large number of Instaclustr user database nodes. This mock data can then be used to performance test Instaclustr's internal cloud monitoring system.

Instaload will allow Instaclustr developers to generate large amounts of mock data with minimal cost and manual labor. Allowing much faster and easier performance testing of their monitoring system.

## Quick Access
* [ZenHub Issue Board](https://app.zenhub.com/login)
    * Login with your GitHub account and select our repo to see the board.
* [Latest Release](https://github.com/Zhenghao-Zhao/Instaload/tree/master)
    * Note that "Latest Release" refers to the latest version of the code with no experimental/work-in-progress features. For our latest work, check the `develop` branch.
* [Documentation](https://drive.google.com/drive/folders/1xwgVBDAqbR-0H-oAxnSYZ9wgkiJFF5hS)
	* [Audit 1](https://drive.google.com/open?id=1LJdIqN4f_QtRiAGmNa--DRuzeKxTupYX)
	* [Audit 3](https://drive.google.com/open?id=1eeeyvOxhVNCOs0OE0pj5PrS7LTvF5LVY)
	* [Project Schedule](https://drive.google.com/open?id=13r4F3HSRC7zvWvQ7C5R0khaqGytzV6Yw)
	* [Decision Log](https://drive.google.com/open?id=1yDMyS0m3fL1ZBKwTFMU8WYMf0t8xxzgGl6DG04nO-s4)
	* [Risk Analysis](https://docs.google.com/document/d/1SslevcaDcjy7WK0WpOBv-2qWQspq_Bn9gxxTzi80Gss/edit?usp=sharing)


## Team Members

Name | Contact | Roles |
------------ | ------------- | ------------- | 
Zhenghao (Gregg) Zhao | u5746425@anu.edu.au | Assistant manager, research lead, GitHub and Google Drive admin |
Ziwei (David) Liu	 | u6380075@anu.edu.au | Technical manager, Google Drive management, audit speaker and preparation, meeting coordinator |
Utkarsh Pandey | u6018954@anu.edu.au | Business manager, client engagement, audit speaker and preparation |
Wei (Phillip) Xing	 | u5656487@anu.edu.au | Developer, ZenHub management |
Yongchao (Laurence) Lyu	 | u6874539@anu.edu.au | Developer, meeting organiser |
Yi Liu	 | u6641740@anu.edu.au | Developer |

## Installation

### Instaload 
Language: **Python 3.7**

For Google's Snappy library and its Python binding:
1. For *nix users (including MacOS users):
    1. Install Snappy C libs, following instructions [here](https://stackoverflow.com/a/20678150/9479242)
    <br>*Note: you might also be required to install gcc libraries that those instructions were based on, possibly refer to
    [here](https://stackoverflow.com/questions/11912878/gcc-error-gcc-error-trying-to-exec-cc1-execvp-no-such-file-or-directory)*
    2. Install the Python binding following [here](https://stackoverflow.com/a/41707800/9479242)
2. For Windows users:
    * Follow instructions in [here](https://stackoverflow.com/a/43756412/9479242)
    
For other libraries: 
* Install libraries from requirements.txt (instaload\requirements.txt)

### Monitoring app
Language: **Java 14**
* We use Maven for managing libraries and dependencies for this application
<br>Find the pom.xml file via mock_services/moni_app/pom.xml

### RabbitMQ
* Download the RabbitMQ server for your system [here](https://www.rabbitmq.com/download.html)

### Riemann
1. For *nix users (including MacOS), simply follow the instructions [here](http://riemann.io/quickstart.html)
2. For Windows users, the easiest way is to download the standalone .jar file from their [git releases](https://github.com/riemann/riemann/releases) 

## Running the application
1. Make sure both RabbitMQ and Riemann servers are running
2. Run the application from **main.py** (instaload\main.py) (e.g. *python main.py*)
3. Optional: specify config file paths in commandline: **--input_config_file**, **--input_json_file** (e.g. *python main.py --input_config_file path1 --input_json_file path2*)
    * **--input_config_file** is the path to the .json file that configures the connection from Instaload to your destined rabbitMQ server. By default it uses **data/configs/rmq.json**.
    * **--input_json_file** is the path to the .json file that describes the format of the load you want to generate. By default it uses **data/metrics/nodes.json**.

## Configuration
You are allowed to supply additional configuration files

1. To configure rabbitMQ's initial settings, you can either add your own rmq.cfg file to instaload/data/configs, and specify the path at cmd (see Running the application) or modify the existing rmq.cfg file.
2. To configure Instaload, you can either modify the existing nodes.json file at data/metrics/nodes.json or add your own 
A Cluster has properties of id, schema, table, metrics and nodes. 
id: the unique identifier for that cluster. 
schema: 