<div id="top"></div>



<br />

## Morion
Morion is a python framework for easily interacting with documents in a MongoDB database.


<a href="https://stgit.dcs.gla.ac.uk/team-project-h/2021/csp3/csp3-main/-/wikis/home"><strong>Read the Wiki for more information»</strong></a>

<a href="https://stgit.dcs.gla.ac.uk/team-project-h/2021/csp3/csp3-dissertation">View Dissertation</a>

<a href="https://stgit.dcs.gla.ac.uk/team-project-h/2021/csp3/csp3-main">Report Bug</a>

<a href="https://stgit.dcs.gla.ac.uk/team-project-h/2021/csp3/csp3-main">Request Feature</a>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#user-guide">User Guide</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a project that allows researchers to robustly upload documents into a MongoDB database. To download documents back out,
and to analyse their findings, all from within a python environment.


<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [MongoDB](https://www.mongodb.com/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [Pymongo](https://pypi.org/project/pymongo/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
You can find the main files of the project in `src/`, and detailed examples on how to use the project in `examples/`.

`src` can be broken down into the following sections:

1. `morion/` - The core package for uploading, downloading, and interacting with the database.
2. `UofG_PP/` - A project that uses `morion` to create models, with examples on how to create readers and writers
that show how `morion` provides functionality for robust interaction with the database.

### Prerequisites

You will need a MongoDB database with read/write access.
You can either install one on your local machine or on a server you have access to.
For more information, check out: https://docs.mongodb.com/manual/installation/

<p align="right">(<a href="#top">back to top</a>)</p>

### Installation

1. Clone the repository into your system, then run "pip install ." on the top level directory, where setup.py is located.
2. In the python commandline, run 
  from morion import setup
  setup()
3. You will be asked for a connection to a mongoDB.
4. Done! You are now connected to the database and can run morion methods from your python shell.



<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## User Guide

<p align="right">(<a href="#top">back to top</a>)</p>



Check out the docs for further explanations on individual methods.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

James McClure, Product Owner - 2385464m@student.gla.ac.uk

Danial Tariq, Tool Smith - 2460201t@student.gla.ac.uk

Ciara Losel, Quality assurance manager - 2438870l@student.gla.ac.uk

Franciszek Sowul, Chief architect - 2482997s@student.gla.ac.uk

Eren Oezveren, UX designer - 2440801o@student.gla.ac.uk


Project Link: [https://stgit.dcs.gla.ac.uk/team-project-h/2021/csp3/csp3-main](https://stgit.dcs.gla.ac.uk/team-project-h/2021/csp3/csp3-main)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Douglas Russel, for being our coach, helping us improve our software process with useful advice 

Dima Maneuski, for being a great customer

<p align="right">(<a href="#top">back to top</a>)</p>



