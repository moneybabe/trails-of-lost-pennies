# Trail of Lost Pennies

This project contains computations for the "Trail of Lost Pennies" problem,
specifically pertaining to lowering bounding the value $\lambda =
\inf\{\mathcal{M}(x):x\in(0,\infty)\}$ by approximation through the finite
counterpart to get $\lambda \geq \inf\{\mathcal{M}_{5,4}(x): x\in[1/3, 3]\} - 6.3\times
10^{-7}$. You can verify the computations by
running the `verify.ipynb`
Jupyter notebook.

## Setup
If you are not familiar with command line interface, you can go to the Google Colab 
notebook
[here](https://colab.research.google.com/drive/1Whg0Gip34kKrnB-VTfhF524NNhN-H2WD?usp=sharing)
and make a copy to directly run the verifying computations on broswer.

Otherwise, if you are familiar with the command line and would like to run the 
verifying notebook locally, or even run the entire computation for the proof
from scratch (which might take hours depending on your hardware), 
follow the instructions below.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of [Python](https://www.python.org/downloads/).

## Setup for users familiar with command line

1. Clone the repository or simply by click the green "Code" button on right top
   corner and download the zip file.:
```
git clone https://github.com/moneybabe/trails-of-lost-pennies.git
```

2. Navigate to the project directory or unzip the downloaded file and navigate to the directory:
```
cd trails-of-lost-pennies
```

##### From here, you have to use the command line interface to run the following commands.
3. Create a virtual environment:
```
python3 -m venv env
```

4. Activate the virtual environment:
On macOS and Linux:
```
source env/bin/activate
```
On Windows:
```
.\env\Scripts\activate
```

5. Install the required packages:
```
pip install -r requirements.txt
```

6. Run the notebook:
```
jupyter notebook verify.ipynb
```

7. [Optional] Run the entire computation for the proof (might take hours), which would output a comma separated
   value file `results.csv` containing the values of
   $\mathcal{M}_{5,4}^\downarrow[a,b]$ and the corresponding $a, b$ for
   $[a, b]\subseteq[1/3, 3]$:
```
python main.py
```
