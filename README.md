# Instaload
## Quick Access
* [Issue Board](https://github.com/Zhenghao-Zhao/Instaload#workspaces/project-board-5e5efa7668d1b55158247a50/board?repos=244576663)
* [Documentation](https://drive.google.com/drive/folders/1xwgVBDAqbR-0H-oAxnSYZ9wgkiJFF5hS)
* [Develop](https://github.com/Zhenghao-Zhao/Instaload/tree/develop)

## Overview
At Instaclustr, we provide a managed service which delivers Kafka, Cassandra and Elasticsearch as-a-service to some of the biggest names in Tech. We manage enterprise scale solutions which are relied upon by critical business services.
We have hundreds of clusters, and over 3000 instances (nodes) running at any time. As well as automated systems for provisioning and configuring clusters, a component of our management system is a comprehensive automated monitoring system which alerts our support staff of any potential issues. Our monitoring system is itself a large, distributed system comprising over 60 servers (some up to 36 CPU's, 72 Gb RAM, 2TB Storage). It receives 450,00 events/metrics per second, with periodic peaks up to 200% of average load.

Our plans for growth plans mean that we need better ways to test the performance of our very large system operating at much greater scale than we are able to currently. The requirement is for a system which enables us to generate realistic loads for our monitoring system. We are looking for a scalable solution which enables us to simulate metrics and state events from up to 10,000 unique nodes. This could involve technologies including docker, kubernetes, kafka, rabbitmq etc. You will also develop an understanding of the Open Source technologies we support, including Cassandra, Kafka, and Elasticsearch.

Emphasis will be put on the ability to quickly and automatically stand up, and tear down the test environment in cloud environments for performance tests.

The largest challenges of the project will be the orchestration of the multiple servers that will be required to generate the required load.
Ideally, the system will be able to generate different metrics and load per simulated instance, taking input and direction from user input into the system. This will help us simulate the different load different customers can produce on the system. You will also need to be able automatically collect the results collected while performance testing, so we are able to evaluate performance impacts of system improvements.

## Team Members
- Zhenghao Zhao (u5746425@anu.edu.au)
- Ziwei (David) Liu (u6380075@anu.edu.au)
- Utkarsh (u6018954@anu.edu.au)
- Wei (Phillip) Xing (u5656487@anu.edu.au)
- Yongchao (Laurence) Lyn (u6018954@anu.edu.au)
- Yi Liu (u6641740@anu.edu.au)
