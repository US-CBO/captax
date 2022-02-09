# CBO's Capital Tax Model (CapTax) Parameters Documentation

The CBO Capital Tax (CapTax) Model accepts about 40 files containing a variety of data and parameter values read into the model.

There are numerous abbreviations used throughout the CapTax model code and the documentation. A listing of those abbreviations are in [abbreviations.md](abbreviations.md).

The parameter files and weights data are organized into the following directories:
* `/captax/captax/data/inputs/environment_parameters/` </br>Detailed descriptions of the environment parameters are in [environment_parameters.md](environment_parameters.md)

* `/captax/captax/data/inputs/policy_parameters/` </br>Detailed descriptions of the policy parameters are in [policy_parameters.md](policy_parameters.md)
* `/captax/captax/data/inputs/weights_data` </br>Detailed descriptions of the weights data are in [weights_data.md](weights_data.md)

Some of the parameters are scalars, but others are matrices.  
The possible dimensions of those matrices are as follows:

1.	**Industry**  
Two levels of detail are used:
	* Standard industry (61 categories fully reflected in the model’s output)
	* Detailed industry (88 categories needed to accommodate the variation in depreciation rules, but not reflected in the model’s output)

2. **Asset type**
    * 83 categories, including five placeholders for additional asset types not recognized in BEA Fixed Asset tables

3. **Legal form**
    * C corporations,
    * pass-through entities, and
    * owner-occupied housing

     (Nonprofits are present as a residual, but no calculations are done on them.)

4. **Source of financing**
    * debt, or
    * equity

5. **Account category**
    * fully taxable,
    * temporarily deferred, and
    * nontaxable
