
# Summarizer

  
  

This is a .net Framework based automation tool for summarization built using RPA developing software UiPath. It utilizes textrank and nod2vec algorithms to summarize and visualize text as clipboard-copied, document or emails. The activity is composed by three parts:

  

* Installer: One time installation of python runtime and dependencies necessary to run the activity.

* User Interface: HTML Custom Input interface to retrieve user options: mode, graphic visualization and Google Translate.

* Processing: Python code retrieves and processes input text. Outputs are saved either as report (.docx) and/or graphic display (.html) of key concepts at output folder.

  

It generates summarized text report of three types of input: Clipboard, Document and Email. Allows visualization of key concepts and relations from the targeted inputs. Email mode allows to target folder and number of threads to be summarized.

  


### Break down into end to end tests

  

Explain what these tests test and why

  

```
Give an example
```

  



  ## Getting Started

  

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

  

### Prerequisites

This project can be run directly as a python activity

*  [UiPath Studio](https://www.uipath.com/) - RPA developing tool
* Python environment with the following dependencies

```
- chardet=3.0.4=py36_1003
- cryptography=2.7=py36h7a1dbc1_0
- cython-blis=0.2.4=py36hfa6e2cd_1
- ggtrans=2.4.0=py36_0
- intel-openmp=2019.4=245
- jsonschema=3.0.2=py36_0
- langdetect=1.0.7=py_0
- numpy=1.17.0=py36hc71023c_0
- openssl=1.1.1c=hfa6e2cd_0
- requests=2.22.0=py36_0
- scipy=1.3.0=py36h29ff71c_0
- spacy=2.1.7=py36he980bc4_0
- sqlite=3.29.0=he774522_0
- summa=1.2.0=py36_0
- tqdm=4.32.2=py_0
- urllib3=1.24.3=py36_0
- wasabi=0.2.2=py_0
- wheel=0.33.4=py36_0

- pip:
-- en-core-web-sm==2.1.0
-- ginza==2.0.0
-- ja-ginza==2.1.0
-- sortedcontainers==2.1.0
-- sudachidict-core==20190531
-- sudachipy==0.3.3
```

For the complete list of dependencies refer to *miniconda.yml* file.


> **Note:** The *wasabi* dependencies *ginza and ja-ginza modules* are not necessary but required if you are to interested in Japanese language compatibility, whereas [*SpaCy*](https://github.com/explosion/spaCy) and the *en-core-web-sm* module are required for English.
  

## Deployment
  

To run it on another windows machine you can pack the python runtime and enviroment with the requirements especified at [miniconda.yml](miniconda.yml) with:

  

*  [Conda-Pack](https://conda.github.io/conda-pack/)
*  [Embedded Python](https://docs.python.org/3/extending/embedding.html)

  

> **Note:** The main xaml of this project has a *installer* section. Therefore the xaml can be runned and work out-of-the-box, downloading the packed environment and runtime (only on the first run).

  
## Sample Input and Outputs
  
As the main xaml is runned

## Authors

  

*  **Pablo Morales** - [pdmorale](https://github.com/pdmorale)

  

## License

  

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details