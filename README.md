# CBO’s CapTax Model

CBO uses its Capital Tax model (CBO-CapTax) to estimate the effects of federal taxes on capital income from new investment. Specifically, CBO uses the model to estimate federal effective marginal tax rates (EMTRs) on marginal investments for the U.S. economy and in finer detail by industry, asset type, legal form of organization (C corporations versus pass-through entities, for example), and source of financing (debt versus equity). The model uses two separate analytical perspectives:

* A **comprehensive perspective**, which analyzes the effects of federal taxes on capital income by incorporating differences in how assets are deployed or financed and differences in rates of return among sources of financing;

* A **uniformity perspective**, under which differences in aggregate EMTRs (say between C corporations and pass-through entities) only reflect how those groups are treated by the tax system, holding everything else equal. This latter perspective requires a different approach to weighting EMTRs, establishing the values of policy parameters, and determining appropriate after-tax rates of return.

## Documentation

More detailed documentation for the model can be found in a CBO Working Paper: [“CBO’s Model for Estimating the Effect of Federal Taxes on Capital Income from New Investment"](https://cbo.gov/publication/57429). A short description of modeling changes made after the release of the paper can be found [here](docs/updates_to_model.md).

The [`/captax/docs/`](docs/) directory contains files with useful information pertaining to parameters and data used in the CapTax model.

Furthermore, the file `/captax/captax/data/inputs/policy_parameters/CapTax_policy_parameters.xlsx` contains all current law policy parameters in one Excel workbook, allows users to generate new `*.csv` files with policy changes, and provides additional documentation on each parameter.

## How to Install the CapTax Model

Follow these three steps to install CBO’s CapTax model:

1) **Install the Anaconda distribution of Python**   
The Anaconda distribution of Python contains many useful Python packages for data analysis and statistical modeling. You can download and install the Anaconda distribution of Python from Anaconda's [Installation page](https://docs.anaconda.com/anaconda/install/index.html).
</br></br>CBO's CapTax model was developed using Python 3.8 on computers running Windows 10 operating systems, although the model should run on other operating systems as well.
</br></br>CBO also used Anaconda's built-in package manager, `conda`, to manage the external packages used by the model. To replicate results from CBO's CapTax model, you will need to use `conda` to create a virtual environment that loads the appropriate version of Python and has all the same versions of the external packages CBO used when developing the model. All the external packages (and their versions) are documented in the `environment.yml` file in the project’s root directory. That file is used to create an virtual environment that matches the one CBO used to develop the CapTax model. This is done in step 3, below.

2) **Download the CapTax model from GitHub**  
There are several options for how to get the code from GitHub to your computer:  

    * If you have git installed on your computer, you can clone a copy of the repo to your computer. This is done through git with the command: `git clone https://github.com/us-cbo/captax.git`

    * If you have a GitHub account, you can fork a copy of the repo first to your own GitHub account and then clone it to your computer.

    * If you don’t have git installed on your computer, you can download a zipped file containing the entire repo and then unzip it.

3) **Create the CBO-CapTax virtual environment**  
Once you have installed the Anaconda distribution of Python and you have downloaded a copy of the repo to your computer, follow these steps to create a virtual environment that will make sure you have all the appropriate dependencies to run the model:

    * Open the `Anaconda Prompt` application, which comes as part of the Anaconda installation  
(**Note**: If you cloned or downloaded the model to a network drive, you will need to use the `Anaconda PowerShell Prompt` application instead of the `Anaconda Prompt` application.)

    * Navigate to the root directory where the model was cloned or downloaded on your computer using the change directory (`cd`) command:  
`cd your/path/to/CapTax_model`</br>(**Note**: If you have spaces in any of the directory names in the path, the path string will need to be inside quotation marks.)

    * Create a virtual environment that matches the one used to develop the CBO CapTax model by typing:  
`conda env create -f environment.yml`  
(**Note**: This may take several minutes to complete.)

    * Activate the newly created virtual environment by typing:  
`conda activate CBO-CapTax`  
To replicate CBO's CapTax model results, the model needs to be run from within this virtual environment.

    * When finished working with the CapTax model, deactivate the virtual environment from the Anaconda Prompts by typing:  
`conda deactivate`

## How to Run the Model Using Current Law Parameters

Current law policy parameters for the CapTax model are in:  
`/captax/captax/data/inputs/policy_parameters/`

That directory includes a `policies.yml` file, which is **the main driver file** for the CapTax model, as it is the file the model reads in to determine which policy parameter file(s) to read in for producing simulations. The `policies.yml` file provided has two policy parameters files listed:

* `policy_parameters_Current-Law_comprehensive.csv`, and
* `policy_parameters_Current-Law_uniformity.csv`

Without any changes to policy parameters files or `policies.yml`, the model will run two policy simulations: both under current law, but one for each of the two analytical perspectives.

Each of policy parameters files listed in `policies.yml` contains numerous model parameters that determine how and which calculations are made in the model.  
(See [`/captax/docs/policy_parameters.md`](docs/policy_parameters.md) for more details on what each policy parameter represents.)

The model flow is in `run_captax.py`, which is in the root of the cloned or downloaded project directory.

To run the model from the Anaconda Prompt, type:  
**(CBO-CapTax) your/path/to/CapTax_model>**`python run_captax.py`

Then hit `Enter` to run the model.

Text will scroll by documenting the progress as the model proceeds.

The output from the model using current law parameters is stored in the following directories:

* `/captax/captax/data/outputs/Current-Law/comprehensive`, and
* `/captax/captax/data/outputs/Current-Law/uniformity`

When the model is running, you will be prompted to overwrite the contents of the output directories if those directories already exist. (You will be prompted twice -- once for the comprehensive results and another time for the uniformity results.)

You should type `Yes` to the prompts that ask you if you'd like to overwrite the results stored in those directories. If you type `No`, the model run will end and you will be asked to specify a set of policy parameters files in `policies.yml` (discussed in more detail below) and to rerun the model.

A successful first run of the model will overwrite the output using `Current-Law` parameters, but there should be no changes in the values. Because the `Current-Law` results are included in the repo, users who have cloned the git repo can verify that the results haven’t changed by checking the status of the git directory with the `git status` command. (If a user is not using git, then they will have to verify the results of the initial run manually.)

## How to Specify a Policy Change

Most policy parameters are annual values that can be directly edited when performing a simple policy change, as discussed below. There are, however, policy parameters that are stored in separate files and are used to model the effect of the tax system on investment through:

* depreciation adjustments,
* investment tax credit adjustments,
* production tax credit adjustments, and
* marginal tax rate adjustments

Files used to estimate depreciation adjustments include parameter values that vary by detailed industry and asset type. Files used to estimate investment tax credit adjustments and production tax credit adjustments include parameters that vary by industry and asset type. Files used to estimate marginal tax rate adjustments include parameter values that vary by detailed industry or by asset type.

Making policy changes related to one or more of those three sets of adjustment parameters is slightly more complex and requires changes in at least two places, as discussed below.

### A Simple Policy Change

To make a simple policy change, that is a change to parameters defining tax rates and other general policy choices, follow these steps:

1) Make a copy of the `policy_parameters_Current-Law_comprehensive.csv` file.

2) Rename the `Current-Law` portion of the filename with a new policy suffix; for example:   
`policy_parameters_My-Policy-Name_comprehensive.csv`.

3) Open that renamed file and make your desired parameter changes.

4) Save and close the `policy_parameters_My-Policy-Name_comprehensive.csv` file with your parameter changes.

If also interested in the uniformity perspective for the same policy change, follow these steps:

1) Make a copy of the `policy_parameters_Current-Law_uniformity.csv` file.

2) Rename the `Current-Law` portion of the filename with a new policy suffix; for example: `policy_parameters_My-Policy-Name_uniformity.csv`.

3) Open that renamed file and make your desired parameter changes following the instructions in the `Readme_Part_1` worksheet of the `CapTax_policy_parameters.xlsx` documentation file on how to estimate parameter values that are consistent with the uniformity perspective.

4) Save and close the `policy_parameters_My-Policy-Name_uniformity.csv` file with your parameter changes.

Once you’ve made your desired policy changes and saved them in new files, you need to add your new policy parameters files to the `policies.yml` file for the CapTax model to simulate them.

Open `policies.yml`, which includes the following text:

```
# Enter the policy files for the CapTax model to run.
# Each line must start with '-' followed by a space, and then the filename:
- policy_parameters_Current-Law_comprehensive.csv
- policy_parameters_Current-Law_uniformity.csv  
```

Add names of new policy parameter file(s) to existing list if interested in both current law and new policy output:

```
# Enter the policy files for the CapTax model to run.
# Each line must start with '-' followed by a space, and then the filename:
- policy_parameters_Current-Law_comprehensive.csv
- policy_parameters_Current-Law_uniformity.csv
- policy_parameters_My-Policy-Name_comprehensive.csv
- policy_parameters_My-Policy-Name_uniformity.csv
```

Alternatively, replace list of current law policy parameters files with list of new policy parameters files:

```
# Enter the policy files for the CapTax model to run.
# Each line must start with '-' followed by a space, and then the filename:
- policy_parameters_My-Policy-Name_comprehensive.csv
- policy_parameters_My-Policy-Name_uniformity.csv
```

Save and close the `policies.yml` file.

### A More Complex Policy Change

A more complex policy change, that is a change to parameters defining depreciation rules, investment tax credit rules, production tax credit rules, and marginal tax rate adjustments, involves changing one or more policy parameters stored in more complex data structures and requires making changes in at least two places.

To make a more complex policy change, follow these steps:

1) Identify the parameter file with the parameters you want to change. That parameter file is located in one of these directories:

    * `/captax/captax/data/inputs/policy_parameters/depreciation_adjustments/`
    * `/captax/captax/data/inputs/policy_parameters/investment_tax_credit_adjustments/`
    * `/captax/captax/data/inputs/policy_parameters/production_tax_credit_adjustments/`
    * `/captax/captax/data/inputs/policy_parameters/tax_rate_adjustments/`

2) Make a copy of the relevant file; for example:   
`acceleration_rates_CLaw_perm.csv`

3) Rename the `Current-Law` portion of the filename with a new policy suffix; for example:   
`acceleration_rates_My-Policy-Name.csv`

4) Open the renamed file and make the desired parameter changes.

5) Save and close the file.

Repeat those steps for each file if there are multiple files that need to be changed.

Make changes in the appropriate parameters files that include parameters defining tax rates and other general policy choices (In those files there are fourteen policy parameters specifying policy name suffixes associated with parameter files with more complex data structures):

1) Make a copy of the `policy_parameters_Current-Law_comprehensive.csv` file  

2) Rename the `Current-Law` portion of the filename with a new policy suffix; for example:  
`policy_parameters_My-Policy-Name_comprehensive.csv`

3) Modify the policy name suffix(es) referencing the policy parameter file(s) with depreciation rules, investment tax credit rules, production tax credit rules, or marginal tax rate adjustments modified by the user; for example: change the policy name suffix for the `acceleration_rates` parameter for the appropriate years from `CLaw_perm` to `My-Policy-Name`.

Repeat the same steps for `policy_parameters_Current-Law_uniformity.csv` if also interested in running the CapTax model with a policy simulation using the uniformity perspective.

Finally, add the names of new policy parameters file(s) to list of policy parameter files included in `policies.yml`, as discussed for simple policy changes.

## How to Run the CapTax Model with a Policy Change

After making changes to the appropriate policy parameter files and adding them to the `policies.yml` file, the user can run the model with the policy changes from the Anaconda Prompt by typing:

`(CBO-CapTax) user/specific/path/to/project/CapTax_model> python run_captax.py`

For each `policy_parameters_My-Policy-Name_perspective.csv` file listed in `policies.yml`, a new directory will be created to store the model outputs:

`/captax/captax/data/outputs/My-Policy-Name/perspective`

The first model run for a given `My-Policy-Name` and `perspective` will not prompt the user for input on whether to over-write the results in that directory, because that directory will not yet have any output stored.

Subsequent model runs with the same `My-Policy-Name` and `perspective`, however, will prompt the user for input on whether to over-write the results already stored in that directory.

## Acknowledgements

The [original version of the model](https://www.cbo.gov/system/files/2022-02/corrected_etrs.xls) was developed in Excel by **Paul Burnham** and **Larry Ozanne (formerly of CBO)**  and was released along with the CBO Background paper [Computing Effective Tax Rates on Capital Income](https://www.cbo.gov/publication/18259) (2006). That model was subsequently extended and converted to Fortran. **Cody Kallen (formerly of CBO)** made significant contributions towards converting the model from Fortran to its current state in Python.

**Dorian Carloni** and **Kevin Perese** made further structural changes to the model in Python. **Madeleine Fox** and **Jennifer Shand** did research and constructed parameters for the model. **Omar Morales**, **Charles Pineles-Mark**, and **F. Matthew Woodward** provided useful feedback on the source code and ran model tests. **John McClelland** and **Joseph Rosenberg** supervised the most recent model development.


## Contact

If you have questions about the data or computer code in this repository, you can contact CBO’s Office of Communications at [communications@cbo.gov](mailto:communications@cbo.gov?subject=Question%20about%20CBO's%20CapTax%20model%20on%20GitHub.com) or [create a new issue](https://github.com/us-cbo/captax/issues). (If you are interested in making a pull request to this repo, please create a new issue before doing so.)

CBO will respond to all questions, issues, and pull requests as its workload permits.
