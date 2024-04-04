# Phone Matchup

## Overview
Welcome to _**Phone Matchup**_! _**Phone Matchup**_ is a _**ETL Pipelines**_ designed to extract and Standardize _**Smart Phone**_ data. Whether you are a developer or contributor, this _**README.md**_ will guide you through the essentials of the project.

## Table of Content
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Installation](#installation)
4. [Contribution](#contribution)

## Introduction
**Phone Matchup** crafts an advanced **ETL Pipeline** designed to efficiently **Extract**, **Standardize**, and meticulously **Process** Smart Phone Data, tailoring the results to suit the user's budget preferences and specific brand preferences, delivering a seamless experience.

## Getting Started
Before diving into the project, ensure you have the following prerequisites:
- Programming Language: [Python 3.X](https://www.python.org/)
- Package Manager: [pip](https://pypi.org/project/pip/)
- Version Control: [Git](https://git-scm.com/)
- Integrated Development Environment: [Visual Studio Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/)

## Installation
1. Clone Repository
   ```bash
   https://github.com/Arko-Sengupta/Phone-Matchup.git
   ```

2. Navigate to the Project Directory
   ```bash
   cd/<Project-Directory>
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Find `Scraper.py` follow the path `src\scraper\Scraper.py`. Find the Comment as below and Replace the Line for Testing.
   ```bash
   # Limit Products for Test
   with ThreadPoolExecutor(max_workers=4) as executor:
       product_details = list(executor.map(self.ProductDetails, list(set(products[:100]))))
   ```

5. Start the Application
   ```bash
   streamlit run App.py
   ```

## Contribution
If you'd like to contribute, follow the guidelines
- Create a branch using the format `Phone-Matchup_<YourUsername>` when contributing to the project.
- Add the label `Contributor` to your contributions to distinguish them within the project.