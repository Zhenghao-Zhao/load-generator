
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
1. For *nix users, you need to download extra C libs. Follow instructions in https://stackoverflow.com/questions/11416024/error-installing-python-snappy-snappy-c-h-no-such-file-or-directory
<br>You also need to install python-snappy as the binding after you have attained the c libs
2. For Windows users, follow instructions in https://stackoverflow.com/questions/42979544/how-to-install-snappy-c-libraries-on-windows-10-for-use-with-python-snappy-in-an
<br>Note: we use python 3.7
3. Install libraries from requirements.txt (instaload\requirements.txt)

### Monitoring app (.java)
1. We use Maven for managing libraries and dependencies for this application
You can find the pom.xml file via mock_services/moni_app/pom.xml

### RabbitMQ
1. Download the RabbitMQ server for your system
(https://www.rabbitmq.com/download.html)

### Riemann
1. For *nix users, simply follow the instructions here
(http://riemann.io/quickstart.html)
2. For Windows users, the easiest way is to download the standalone.jar file from their git repo releases 
(https://github.com/riemann/riemann/releases) 

### Running the application
1. Make sure both RabbitMQ and Riemann servers are running
2. Run the application from main.py (instaload\main.py)