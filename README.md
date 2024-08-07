![alt text](https://raw.githubusercontent.com/kyunghoon-han/tihi/main/logo_small.png)

**Tihi** is a lightweight, minimalist GUI tool written in Python designed for identifying signal peaks and decomposing signals in chemical experiments using locally available resources.

## Installation through PyPI

One can install this package as:
```
pip install numpy scipy PyQt5 pyqtgraph 
pip install Tihi-spectral-fitter
```
where `pip` could be `pip3` and first line can be modified if some of those packages are already installed.

If you want to remove the installed package, run the following.
```
pip uninstall Tihi-spectral-fitter
```

The PyPI page on this project is https://pypi.org/project/Tihi-spectral-fitter/.

## Installation from the source

If you want to have the source code in your favorite directory so that you can modify the code for your purposes, first clone the GitHub repository as
```
git clone https://github.com/kyunghoon-han/tihi
```
then `cd` into the *tihi* directory and execute
```
pip install .
```
on your favorite terminal.

Uninstalling **Tihi** installed from the source can be done by the following command:
```
pip uninstall tihi
```

## Documentation
**Tihi** documentation is available on https://tihi.readthedocs.io/en/latest/.

## Thanks
The authors thank Tobias Henkes https://github.com/tohenkes for finding the crucial error with 8.
