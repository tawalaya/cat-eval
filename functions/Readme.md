# Functions

Each folder contains a synsetic serverless function with a know performance profile.

## Requrimetnes
 - python3.7+
 - pip
 - node12+
 - npm
 - zip
 - make
 - envsubst
 - git
 - gcloud: fully configured google cli tool
 - aws: fully configured aws cli tool 

## Usage

For deployment of each function, go into the folder of the given function, set envorment variables as needed and run `make <VENDOR>` where VENDOR can be `AWS or GCF`. 

For cleanup run `make clean`, this will always undeploy both aws and gcf.

## Functions

### Lloyd
This function is inspiered by Lloyd et al.<sup>[1](#cite1)</sup> an can exsibit either CPU or memory intensive workloads by tuning the variables `OPSIZE, ITTER,DEPTH` of the deployment.

### Prime
This function implements a primality test function using the Sieve of Eratosthenes algorithm<sup>[2](#cite2)</sup> in Node.js 14 without any dependencies. It is good for mildy stessing a CPU while consuming time based on the size of the input number.

### Text2Speech
This function converts a provided text into speech using the `gtts` libary. A similar function has been used by Eisman et al.<sup>[3](#cite3)</sup>. This functions writes the generated mp3 to a cloud object store, you can configure the bucket-name using the `BUCKET` variable.


# References
<a name="cite1">1</a>: [2018 Serverless Computing: An Investigation of Factors Influencing Microservice Performance by Lloyd, W and Ramesh, S and Chinthalapati, S and Ly, L and Pallickara, S](http://ieeexplore.ieee.org/abstract/document/8360324)

<a name="cite2">1</a>: [2019 Benchmarking Elasticity of FaaS Platforms as a Foundation for Objective-driven Design of Serverless Applications by Kuhlenkamp J. and Werner S. and Borges M. and Ernst D. and Wenzel D.](https://www.ise.tu-berlin.de/fileadmin/fg308/publications/2020/Online_Preprint___SAC_2020__Benchmarking_Elasticity_of_FaaS_Platforms_as_a_Foundation_for_Objective_driven_Design_of_Serverless_Applications.pdf)

<a name="cite3">1</a>: [2021 Sizeless: Predicting the optimal size of serverless functions by Eismann S. and Bui L. and Grohmann J and Abad C. and Herbst N. and Kounev S.](https://arxiv.org/pdf/2010.15162.pdf)