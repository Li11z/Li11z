<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:A8E6CF,50:BDE0FE,100:FFC8DD&height=200&section=header&text=Ali%20Afoud&fontSize=56&fontColor=2B2D42&animation=fadeIn&fontAlignY=38&desc=Scientific%20ML%20%C2%B7%20Health%20and%20Biology%20%C2%B7%20Interpretability&descAlignY=58&descSize=17" alt="header" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&pause=1200&color=5B9BD5&center=true&vCenter=true&width=620&lines=Hi%2C+I%27m+Ali;CS+%2B+Math+graduate%2C+UBC;Teaching+neural+networks+the+laws+of+physics;ML+and+DL+for+health+and+biology;Making+models+interpretable" alt="typing intro" />

[![arXiv](https://img.shields.io/badge/arXiv-Afoud%2C%20A-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/search/?searchtype=author&query=Afoud%2C+A)
[![Email](https://img.shields.io/badge/Email-Afoudali%40hotmail.com-5BB5E0?style=flat-square&logo=microsoftoutlook&logoColor=white)](mailto:Afoudali@hotmail.com)
![Location](https://img.shields.io/badge/Based%20in-Montreal%2C%20QC-5CC9A7?style=flat-square)
![Profile views](https://komarev.com/ghpvc/?username=Li11z&color=7ec8e3&style=flat-square&label=Profile+views)

</div>

## About me

<img align="right" width="300" src="assets/dejong.svg" alt="3D De Jong attractors assembling, rotating and morphing" />

- Computer Science + Mathematics graduate, University of British Columbia (2026)
- Interested in where machine learning meets mathematical modelling: physics-informed learning, neural differential equations and data-driven discovery of governing equations
- Machine learning and deep learning for health and biology, and making models interpretable
- Exploring quantum computing
- Building things from scratch in the open: an ML library (Python/C++) and a linear algebra library (C)
- Languages: English, French, Arabic

<br clear="right"/>

## Research interests

```mermaid
flowchart LR
    A(("Ali")) --> C["Scientific ML"]
    A --> D["ML and DL for Health and Biology"]
    A --> I["Interpretability"]
    A --> Q["Quantum (exploring)"]
    C --> C1["Physics-informed networks and neural operators"]
    C --> C2["Neural ODEs and universal differential equations"]
    C --> C3["Equation discovery: SINDy, symbolic regression"]
    D --> D1["Epidemic and PDE models"]
    D --> D2["Medical imaging and physiological signals"]
    I --> I1["Attribution methods"]
    I --> I2["Interpretable models for science"]
    classDef root fill:#FFC8DD,stroke:#FFAFCC,color:#2B2D42
    classDef area fill:#BDE0FE,stroke:#A2D2FF,color:#2B2D42
    classDef leaf fill:#E8F8F0,stroke:#A8E6CF,color:#2B2D42
    class A root
    class C,D,I,Q area
    class C1,C2,C3,D1,D2,I1,I2 leaf
```

<details>
<summary><b>The math behind these interests</b></summary>

**Physics-informed neural networks** (scientific ML). A network is trained to match measured data and, at the same time, is penalised wherever it breaks the physical law (the PDE) the system is known to obey.

```math
\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^{N}\big(u_\theta(x_i) - u_i\big)^2 + \lambda\,\frac{1}{M}\sum_{j=1}^{M}\big(\mathcal{N}[u_\theta](x_j)\big)^2
```

**Universal differential equations** (neural ODEs). Keep the physics you trust and let a neural network learn only the part you don't know. With no known part, this is a plain neural ODE.

```math
\frac{d\mathbf{h}}{dt} = f_{\text{known}}(\mathbf{h}) + \mathrm{NN}_\theta(\mathbf{h}, t)
```

**SINDy** (equation discovery). Build a library of candidate terms (x, y, xy, sin x, ...) and find the few that explain the data, so the result is a readable equation rather than a black box.

```math
\min_{\Xi}\; \big\lVert \dot{\mathbf{X}} - \Theta(\mathbf{X})\,\Xi \big\rVert_2^2 + \lambda \lVert \Xi \rVert_1
```

**SIR model** (health and biology). The starting point of my epidemic-waves work: susceptible, infected and recovered populations, with infection rate β and recovery rate γ.

```math
\frac{dS}{dt} = -\beta S I, \qquad \frac{dI}{dt} = \beta S I - \gamma I, \qquad \frac{dR}{dt} = \gamma I
```

**Integrated gradients** (interpretability). How much each input feature contributed to a model's prediction, measured along a path from a neutral baseline to the actual input.

```math
\mathrm{IG}_i(x) = (x_i - x_i') \int_0^1 \frac{\partial F\big(x' + \alpha (x - x')\big)}{\partial x_i}\, d\alpha
```

</details>

## Selected projects

![public](https://img.shields.io/badge/-public-5CC9A7?style=flat-square) ![soon](https://img.shields.io/badge/-going%20public%20soon-FFB38A?style=flat-square) ![private](https://img.shields.io/badge/-private%20(course%20or%20research)-A0AEC0?style=flat-square)

| Project | What it does | Stack | Status |
|---|---|---|:-:|
| **Epidemic waves PDE model** | Age-structured, opinion-driven prophylaxis model of COVID-19 waves using contact matrices and age-specific fatality rates | Python, NumPy | ![](https://img.shields.io/badge/-private-A0AEC0?style=flat-square) |
| **Jersey number recognition** | Broadcast soccer pipeline: image restoration, pose-based torso crops, OCR/VLM ensemble with calibrated voting | PyTorch, YOLOv8 | ![](https://img.shields.io/badge/-private-A0AEC0?style=flat-square) |
| **ML from scratch** | Classical ML algorithms behind a shared fit/predict API, validated against scikit-learn | Python, C++ | ![](https://img.shields.io/badge/-soon-FFB38A?style=flat-square) |
| **Linear algebra in C** | Matrix library with manual memory management; naive vs cache-blocked multiplication | C | ![](https://img.shields.io/badge/-soon-FFB38A?style=flat-square) |

<details>
<summary><b>More projects</b></summary>
<br>

| Project | What it does | Stack | Status |
|---|---|---|:-:|
| **Live lecture Q&A** | Real-time question answering over lecture speech and board content with tiered retrieval memory | Python, pgvector | ![](https://img.shields.io/badge/-private-A0AEC0?style=flat-square) |
| **Password analysis** | Character trigram grader and inverse generator built on 174.8M leaked passwords, tested with Hashcat | Python | ![](https://img.shields.io/badge/-private-A0AEC0?style=flat-square) |
| **Toronto safety analysis** | Neighbourhood safety scores and LightGBM crime/collision forecasts, served through a web app | PostgreSQL, LightGBM, FastAPI, Next.js | ![](https://img.shields.io/badge/-private-A0AEC0?style=flat-square) |
| **Brownian motion notes** | Expository report on Lévy's construction and path properties | LaTeX | ![](https://img.shields.io/badge/-private-A0AEC0?style=flat-square) |

</details>

## Tech stack

<p align="center">
  <img src="assets/tech-orbit.svg" width="100%" alt="Tech stack orbiting on tilted rings" />
</p>

<details>
<summary><b>Every tool, with links</b></summary>
<br>

**Languages**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org "Main language for research and ML")
[![C](https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=black)](https://en.cppreference.com/w/c "Systems work and the linear algebra library")
[![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)](https://isocpp.org "Performance-critical ML routines")
[![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)](https://dev.java "Coursework and software engineering")
[![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)](https://www.r-project.org "Statistics")
[![SQL](https://img.shields.io/badge/SQL-4169E1?style=for-the-badge)](https://www.postgresql.org/docs/ "Data pipelines and analysis")
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/docs/Web/JavaScript "Web apps")

**Machine learning and deep learning**

[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org "Deep learning")
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co "Transformers and pretrained models")
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org "Classical ML")
[![LightGBM](https://img.shields.io/badge/LightGBM-5CC9A7?style=for-the-badge)](https://lightgbm.readthedocs.io "Gradient boosting")
[![XGBoost](https://img.shields.io/badge/XGBoost-5BB5E0?style=for-the-badge)](https://xgboost.readthedocs.io "Gradient boosting")
[![SHAP](https://img.shields.io/badge/SHAP-FF85A8?style=for-the-badge)](https://shap.readthedocs.io "Model interpretability")
[![YOLOv8](https://img.shields.io/badge/YOLOv8-111F68?style=for-the-badge)](https://docs.ultralytics.com "Detection and pose estimation")

**Data and engineering**

[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org "Numerical computing")
[![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org "Data wrangling")
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org "Databases and pgvector")
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com "Model-serving APIs")
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org "Front ends")
[![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge)](https://azure.microsoft.com "Deployment")
[![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com "Version control")
[![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge)](https://learn.microsoft.com/power-bi/ "Dashboards")

</details>

<p align="center"><b>Currently studying</b></p>

<p align="center">
  <a href="https://sciml.ai" title="Scientific machine learning in Julia"><img src="https://img.shields.io/badge/Julia-SciML-9558B2?style=flat-square&logo=julia&logoColor=white" /></a>
  <a href="https://github.com/patrick-kidger/diffrax" title="Differential equation solvers in JAX"><img src="https://img.shields.io/badge/JAX-Diffrax-5BB5E0?style=flat-square" /></a>
  <a href="https://github.com/dynamicslab/pysindy" title="Sparse identification of nonlinear dynamics"><img src="https://img.shields.io/badge/PySINDy-equation%20discovery-5CC9A7?style=flat-square" /></a>
  <a href="https://github.com/MilesCranmer/PySR" title="Symbolic regression"><img src="https://img.shields.io/badge/PySR-symbolic%20regression-FFB38A?style=flat-square" /></a>
  <a href="https://github.com/Qiskit/qiskit" title="Quantum computing"><img src="https://img.shields.io/badge/Qiskit-quantum-FF85A8?style=flat-square&logo=qiskit&logoColor=white" /></a>
</p>

## Contributions

<p align="center">
  <img src="assets/contrib-3d.svg" width="100%" alt="3D contribution graph with a snake eating the bars" />
</p>

<details>
<summary><b>Publications</b></summary>
<br>

- J. Wu, A. P. Herlihy, A. S. Mirza, **A. Afoud**, F. Fard. *GrowthHacker.* ACM TOSEM, 2026. [DOI](https://doi.org/10.1145/3815588)
- **A. Afoud**, J. Wu. *VReAct.* JAWs @ IEEE/ACM ASE 2026. [arXiv](https://arxiv.org/abs/2609.31937)

</details>

<div align="center">
  <img src="https://github.com/user-attachments/assets/9487e424-740d-46ed-9abb-21a7fd8813c6" width="280" alt="kazumaup" />
  <br>
  <sub>Hello World!</sub>
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:FFC8DD,50:BDE0FE,100:A8E6CF&height=120&section=footer" alt="footer" />
</div>