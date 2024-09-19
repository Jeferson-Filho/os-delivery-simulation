[![Contributors][contributors-shield]][contributors-url]

<div align="center">
  <h1 align="center">Concurrent Delivery Network Simulation</h1>
</div>

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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
This project focuses on implementing and comparing two well-known algorithms for finding Minimum Spanning Trees (MST) in graphs: Prim's Algorithm and Kruskal's Algorithm. The graphs used in the comparison are generated using the Erdős-Rényi random graph model.

### Statement
For simplification purposes, consider that the redistribution points are organized sequentially.

* In your implementation, assume that:
    * There are S redistribution points.
    * There are C vehicles representing the means of transport.
    * There are P packages to be delivered.
    * Each vehicle has A cargo spaces (each package occupies exactly one space).
    * Ensure that P >> A >> C.
* The program should accept input arguments determining S, C, P, and A when starting the application. The main thread should receive these arguments and create a thread for each of the P packages, each of the C vehicles, and each of the S redistribution points (label them sequentially for identification).
* Vehicles may start from distinct and random points, defined when initializing their threads. The distribution network allows only one vehicle to be processed at a redistribution point at a time. If a point is empty (no packages waiting for dispatch), the vehicle moves to the next redistribution point.
* When packages arrive at a redistribution point, they are organized in a queue controlled by the point. Once the package reaches its destination, it is unloaded (random time) and its thread terminates.
* The travel time between one redistribution point and another is random and not fixed for all vehicles. A vehicle can overtake another during the journey and arrive at the next redistribution point first.
* As long as there are packages to be delivered, vehicles continue circulating between points. When a vehicle reaches the last point, it is directed back to the first point (a circular queue).
* Input arguments provided to the package threads indicate their origin and destination points. These arguments are randomly determined when the threads are created for each package.
* Once all packages have been delivered, the vehicles stop circulating, and the application ends.
* The program outputs should be:

    1. A real-time monitoring screen showing the packages, redistribution points, and vehicles.
    2. Log files of the packages saved to disk. a. Each package generates a log file containing the package number, its origin and destination points, the time it arrived at the origin point, the time it was loaded onto a vehicle, the identifier of the vehicle, and the time it was unloaded at the destination point.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Next][Python]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Descrever como rodar o projeto no ambiente local

### Prerequisites

### Installation

Instalação de ferramentas necessárias para rodar o projeto (verificar se será necessário)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Create a repository on GitHub

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributors

<a href="https://github.com/Jeferson-Filho/os-delivery-simulation/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Jeferson-Filho/os-delivery-simulation" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Quem quiser colocar um meio de contato, escreve aqui

Jeferson Filho - [LinkedIn](https://www.linkedin.com/in/jdietrichfho/)

Project Link: [https://github.com/Jeferson-Filho/os-delivery-simulation](https://github.com/Jeferson-Filho/os-delivery-simulation)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Colocar aqui as fontes ou páginas/coisas que julguem interessante para compor o projeto

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Jeferson-Filho/os-delivery-simulation.svg?style=for-the-badge
[contributors-url]: https://github.com/Jeferson-Filho/os-delivery-simulation/graphs/contributors
[Python]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[Python-url]: https://docs.python.org/3/
