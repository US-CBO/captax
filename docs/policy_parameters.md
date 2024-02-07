# Policy Parameters for CBO's Capital Tax Model (CapTax)

Policy parameters files are located in `/captax/captax/data/inputs/policy_parameters/`.

That directory contains:
* `CapTax_policy_parameters.xlsx`: This is a template tool to generate new policy parameters `*.csv` files. (Or you may edit the `*.csv` files directly.) There is additional documentation about the policy parameters in that file.
* `policies.yml`: This file contains the list of policies the model will simulate.
* `policy_parameters_Current-Law_comprehensive.csv`: This file contains policy parameters with values set to simulate `Current-Law` using the `comprehensive` perspective.
* `policy_parameters_Current-Law_uniformity.csv`: This file contains policy parameters with values set to simulate `Current-Law` using the tax `uniformity` perspective.
* `policy_parameters_permitted_ranges.csv`: This file contains the permitted ranges for all the policy parameters used in the CapTax model. If a policy parameter is set outside of this range, the model will produce an error and will not run.

The policy parameters in `policy_parameters_Current-Law_comprehensive.csv` and `policy_parameters_Current-Law_uniformity.csv` are organized into the following categories:
* [Tax rate parameters—profits and imputed rent](#tax-rate-parametersprofits-and-imputed-rent)
* [Tax rate parameters—investment income](#tax-rate-parametersinvestment-income)
* [Tax rate parameters—itemized deductions](#tax-rate-parametersitemized-deductions)
* [Deduction parameters](#deduction-parameters)
* [Timing adjustment parameters reflecting fluctuating rates of return](#timing-adjustment-parameters-reflecting-fluctuating-rates-of-return)
* [Annual changes to holding period parameters](#annual-changes-to-holding-period-parameters)
* [Policy suffix parameters](#policy-suffix-parameters)
* [Account category parameters](#account-category-parameters)

**Note**: The [policy suffix parameters](#policy-suffix-parameters) in `policy_parameters_Current-Law_comprehensive.csv` and `policy_parameters_Current-Law_uniformity.csv` are character strings that represent suffixes for files containing larger policy parameter matrices, which are in the following subdirectories:
* [`/depreciation_adjustments/`](#depreciation_adjustments-parameter-files)
* [`/investment_tax_credit_adjustments/`](#investment_tax_credit_adjustments-parameter-files)
* [`/production_tax_credit_adjustments/`](#production_tax_credit_adjustments-parameter-files)
* [`/tax_rate_adjustments/`](#tax_rate_adjustments-parameter-files)

Each subdirectory contains `*.csv` files with values set to simulate current law.

### Tax rate parameters—profits and imputed rent
#### `c_corp_tax_rate`
> **Description**: Marginal tax rate on the profits of C corporations
>
> **Units**: Rate (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Year
>
> **Source**: Internal Revenue Code
>
> **Note**: 0.2100 by statute

#### `pass_thru_tax_rate`
>**Description**: Average marginal income tax rate on the profits of pass-through entities
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Notes**: </br> 1. Should be calculated with the Section 199A deduction in place. That will capture the interaction of the deduction with the marginal rate brackets but will not capture the deduction itself. </br> 2. Under the tax uniformity perspective, this should have the same value as other tax rates estimated using the standard rate schedule

#### `seca_tax_rate`
>**Description**: Average marginal SECA tax rate on the profits of pass-through entities
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Must account for zero rate on S corporations and many partnerships

#### `repurchases_tax_rate`
>**Description**: Marginal excise tax rate on stock repurchases
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: Internal Revenue Code
>
>**Note**: 0.0100 by statute

#### `ooh_tax_rate`
>**Description**: Marginal tax rate on the imputed rent from owner-occupied housing
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: Internal Revenue Code
>
>**Note**: 0.0000 by statute

### Tax rate parameters—investment income
#### `dividend_inc_tax_rate`
>**Description**: Average marginal tax rate on dividends paid by domestic C corporations
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Under the tax uniformity perspective, this should have the same value as other tax rates subject to a maximum rate of 20 percent

#### `cap_gains_short_term_tax_rate`
>**Description**: Average marginal tax rate on capital gains accrued on domestic C corporation stock and realized within one year of purchase
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Under the tax uniformity perspective, this should have the same value as other tax rates estimated using the standard rate schedule

#### `cap_gains_long_term_tax_rate`
>**Description**: Average marginal tax rate on capital gains accrued on domestic C corporation stock and realized more than one year after purchase
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO individual income tax model
>
>**Note**: Under the tax uniformity perspective, this should have the same value as other tax rates subject to a maximum rate of 20 percent

#### `cap_gains_at_death_tax_rate`
>**Description**: Average marginal tax rate on capital gains accrued on domestic C corporation stock and not realized during purchaser’s lifetime
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Income tax rate is zero by statute. CBO did not estimate an estate tax rate

#### `interest_inc_from_biz_tax_rate`
>**Description**: Average marginal tax rate on interest received from domestic businesses
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Under the tax uniformity perspective, this should have the same value as other tax rates estimated using the standard rate schedule

#### `interest_inc_from_ooh_tax_rate`
>**Description**: Average marginal tax rate on interest received from homeowners
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Should be the same as `tax_rates[‘interest_inc’][‘biz’]` unless owner-occupied housing is being removed from the tax code altogether, in which case it should be 0.0000

#### `ret_plan_deferred_tax_rate`
>**Description**: Average marginal tax rate on withdrawals from whole life insurance policies and distributions from nonqualified annuities
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Under the tax uniformity perspective, this should have the same value as other tax rates estimated using the standard rate schedule

#### `ret_plan_nontaxable_tax_rate`
>**Description**: Average marginal tax rate on investment income of nonprofits and withdrawals from IRAs and qualified retirement plans
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Note**: Income tax rate is zero by statute. CBO did not estimate rates for unrelated business income tax or penalty tax on early withdrawals from retirement plans

### Tax rate parameters—itemized deductions
#### `mortg_interest_deduction_tax_rate`
>**Description**: Average marginal tax rate that applies to home mortgage interest payments
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Value should account for imputed home mortgage interest of nonitemizers. If it assigns a rate of zero to nonitemizers, then `mortg_interest_deductible_share` must be 1.0000

#### `prop_tax_deduction_tax_rate`
>**Description**: Average marginal tax rate that applies to property taxes paid on owner-occupied housing
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Value should account for imputed property taxes of nonitemizers. If it assigns a rate of zero to nonitemizers, then `prop_tax_deductible_share` must be 1.0000

### Deduction parameters
#### `pass_thru_inc_shares_below_thresholds`
>**Description**: Share of pass-through entity profits that falls below the income threshold above which the Section 199A deduction is limited for certain industries
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: In addition to the amounts below the phaseout range, the value should account for amounts in the phaseout range that have not been phased out

#### `pass_thru_eligibility_below_thresholds`
>**Description**: Share of pass-through income below income thresholds for calculation of Section 199A deduction adjustments that is eligible for the deduction
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO's Microsimulation Tax Model
>
>**Note**: Accounts for portion of Section 199A deduction disallowed below income threshold because of taxable income limit

#### `c_corp_interest_deductible_share`
>**Description**: Share of interest paid by C Corporations that can be deducted in the year it is paid
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Note**: Because differences between legal forms is driven by firm size, both `c_corp_interest_deductible_share` and `pass_thru_interest_deductible_share` should contain the same values under the tax uniformity perspective

#### `pass_thru_interest_deductible_share`
>**Description**: Share of interest paid by pass-through entities that can be deducted in the year it is paid
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Note**: Because differences between legal forms is driven by firm size, both `c_corp_interest_deductible_share` and `pass_thru_interest_deductible_share` should contain the same values under the tax `uniformity` perspective

#### `mortg_interest_deductible_share`
>**Description**: Share of interest paid by homeowners that can be deducted in the year it is paid
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO’s Microsimulation Tax Model
>
>**Note**: Value must account for zero share for nonitemizers unless that was factored into `mortg_interest_deduction_tax_rate`, in which case this value must be 1.0000

#### `prop_tax_deductible_share`
>**Description**: Share of property taxes paid by homeowners that can be deducted in the year it is paid
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO’s Microsimulation Tax Model
>
>**Note**: Value must account for zero share for nonitemizers unless that was factored into `prop_tax_deduction_tax_rate`, in which case this value must be 1.0000

### Timing adjustment parameters reflecting fluctuating rates of return
#### `c_corp_net_inc_timing_adjustment`
>**Description**: Present value divided by nominal value of C corporation net income
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Available to account for the consequences of fluctuating rates of return. Set to 1.0000

#### `pass_thru_net_inc_timing_adjustment`
>**Description**: Present value divided by nominal value of pass-through entity net income
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Available to account for the consequences of fluctuating rates of return. Set to 1.0000

#### `seca_net_inc_timing_adjustment`
>**Description**: Present value divided by nominal value of SECA net income
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Available to account for the consequences of fluctuating rates of return. Set to 1.0000

#### `c_corp_deductions_timing_adjustment`
>**Description**: Present value divided by nominal value of C corporation deductions
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Available to account for the consequences of fluctuating rates of return. Set to 1.0000

#### `pass_thru_deductions_timing_adjustment`
>**Description**: Present value divided by nominal value of pass-through entity deductions
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Available to account for the consequences of fluctuating rates of return. Set to 1.0000

#### `seca_deductions_timing_adjustment`
>**Description**: Present value divided by nominal value of SECA deductions
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Available to account for the consequences of fluctuating rates of return. Set to 1.0000

#### `c_corp_credits_timing_adjustment`
>**Description**: Present value divided by nominal value of C corporation credits
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Available to account for the consequences of fluctuating rates of return. Set to 1.0000

#### `pass_thru_credits_timing_adjustment`
>**Description**: Present value divided by nominal value of pass-through entity credits
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Available to account for the consequences of fluctuating rates of return. Set to 1.0000

### Annual changes to holding period parameters
#### `change_cap_gains_short_term_share`
>**Description**: Additive change to the value of `cap_gains_short_term_share` in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Notes**: Automatically adjusts residual "long-term" share. Available to simulate proposals to tax carried interest as regular income. Set to 0.0000

#### `change_cap_gains_at_death_share`
>**Description**: Additive change to the value of `cap_gains_at_death_share` in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Year
>
>**Source**: CBO
>
>**Note**: Set to 0.0000

#### `change_cap_gains_short_term_holding_period`
>**Description**: Additive change to the value of `cap_gains_short_term_holding_period` in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`
>
>**Units**: Years
>
>**Permitted Range**: No limits
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Notes**: Available to simulate proposals to change the one-year threshold dividing short-term gains from long-term gains. Set to 0.0000

#### `change_cap_gains_long_term_holding_period`
>**Description**: Additive change to the value of `cap_gains_long_term_holding_period` in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`
>
>**Units**: Years
>
>**Permitted Range**: No limits
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Notes**: Available to simulate proposals to change the one-year threshold dividing short-term gains from long-term gains. Set to 0.0000

#### `change_cap_gains_at_death_holding_period`
>**Description**: Additive change to the value of `cap_gains_at_death_holding_period` in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`
>
>**Units**: Years
>
>**Permitted Range**: No limits
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Set to 0.0000

#### `change_ret_plan_deferred_holding_period`
>**Description**: Additive change to the value of `ret_plan_deferred_holding_period` in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`
>
>**Units**: Years
>
>**Permitted Range**: No limits
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Set to 0.0000

#### `change_ret_plan_nontaxable_holding_period`
>**Description**: Additive change to the value of `ret_plan_nontaxable_holding_period` in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`
>
>**Units**: Years
>
>**Permitted Range**: No limits
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Notes**: Available to simulate proposals to change the age before which withdrawals from retirement plans are subject to penalty tax. Set to 0.0000

#### `change_inventories_holding_period`
>**Description**: Additive change to the value of `inventories_holding_period` in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`
>
>**Units**: Years
>
>**Permitted Range**: No limits
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Set to 0.0000

### Policy suffix parameters
The following set of parameters are character strings that represent suffixes for files containing larger policy parameter matrices. Those larger policy parameter matrices are in the following subdirectories:
* [`/depreciation_adjustments/`](#depreciation_adjustments-parameter-files)
* [`/investment_tax_credit_adjustments/`](#investment_tax_credit_adjustments-parameter-files)
* [`/production_tax_credit_adjustments/`](#production_tax_credit_adjustments-parameter-files)
* [`/tax_rate_adjustments/`](#tax_rate_adjustments-parameter-files)

#### `recovery_periods`
>**Description**: Policy suffix of file containing depreciation recovery periods by detailed industry and asset type
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
> **Note**: Go to documentation for [`/depreciation_adjustments/recovery_periods_[POLICY_SUFFIX].csv`](#depreciation_adjustmentsrecovery_periods_policy_suffixcsv)

#### `acceleration_rates`
>**Description**: Policy suffix of file containing depreciation acceleration rates by detailed industry and asset type
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
> **Note**: Go to documentation for [`/depreciation_adjustments/acceleration_rates_[POLICY_SUFFIX].csv`](#depreciation_adjustmentsacceleration_rates_policy_suffixcsv)

#### `straight_line_flags`
>**Description**: Policy suffix of file containing flags by detailed industry and asset type that signal (a) whether declining-balance depreciation should switch to straight-line depreciation when it becomes advantageous and (b) whether tax depreciation should be set equal to economic depreciation
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
> **Note**: Go to documentation for [`/depreciation_adjustments/straight_line_flags_[POLICY_SUFFIX].csv`](#depreciation_adjustmentsstraight_line_flags_policy_suffixcsv)

#### `inflation_adjustments`
>**Description**: Policy suffix of file containing shares of undepreciated basis to be indexed for inflation by detailed industry and asset type
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
> **Note**: Go to documentation for [`/depreciation_adjustments/inflation_adjustments_[POLICY_SUFFIX].csv`](#depreciation_adjustmentsinflation_adjustments_policy_suffixcsv)

#### `c_corp_sec_179_expens_shares`
>**Description**: Policy suffix of files containing shares of investment by detailed industry and asset type eligible for expensing by c corporations under Section 179
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/depreciation_adjustments/sec_179_expens_shares_[POLICY_SUFFIX].csv`](#depreciation_adjustmentssec_179_expens_shares_policy_suffixcsv)

#### `pass_thru_sec_179_expens_shares`
>**Description**: Policy suffix of files containing shares of investment by detailed industry and asset type eligible for expensing by pass-through entities under Section 179
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/depreciation_adjustments/sec_179_expens_shares_[POLICY_SUFFIX].csv`](#depreciation_adjustmentssec_179_expens_shares_policy_suffixcsv)

#### `other_expens_shares`
>**Description**: Policy suffix of file containing shares of investment by detailed industry and asset type eligible for expensing under sections other than 179
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/depreciation_adjustments/other_expens_shares_[POLICY_SUFFIX].csv`](#depreciation_adjustmentsother_expens_shares_policy_suffixcsv)

#### `itc_rates`
>**Description**: Policy suffix of file containing investment tax credit rates by standard industry and asset type
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/investment_tax_credit_adjustments/itc_rates_[POLICY_SUFFIX].csv`](#investment_tax_credit_adjustmentsitc_rates_policy_suffixcsv)

#### `itc_nondeprcbl_bases`
>**Description**: Policy suffix of file containing shares of investment by standard industry and asset type for which an investment tax credit was claimed that cannot also be depreciated
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y`
characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/investment_tax_credit_adjustments/itc_nondeprcbl_bases_[POLICY_SUFFIX].csv`](#investment_tax_credit_adjustmentsitc_nondeprcbl_bases_policy_suffixcsv)

#### `ptc_rates`
>**Description**: Policy suffix of file containing production tax credit rates by standard industry and asset type
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/production_tax_credit_adjustments/ptc_rates_[POLICY_SUFFIX].csv`](#production_tax_credit_adjustmentsptc_rates_policy_suffixcsv)

#### `sec_199A_adjustments`
>**Description**: Policy suffix of file containing parameters controlling Section 199A deductions by detailed industry
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: The parameters in the selected file are applied only to pass-through entities
>
>**Note**: Go to documentation for [`/tax_rate_adjustments/sec_199A_adjustments_[POLICY_SUFFIX].csv`](#tax_rate_adjustmentssec_199A_adjustments_policy_suffixcsv)

#### `c_corp_industry_adjustments`
>**Description**: Policy suffix of file containing parameters controlling indirect and targeted tax adjustments for C corporations by detailed industry
>
>**Permitted** Range: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y`
characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/tax_rate_adjustments/industry_adjustments_[POLICY_SUFFIX].csv`](#tax_rate_adjustmentsindustry_adjustments_policy_suffixcsv)

#### `pass_thru_industry_adjustments`
>**Description**: Policy suffix of file containing parameters controlling indirect and targeted tax adjustments for pass-through entities by detailed industry
>
>**Permitted** Range: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y`
characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/tax_rate_adjustments/industry_adjustments_[POLICY_SUFFIX].csv`](#tax_rate_adjustmentsindustry_adjustments_policy_suffixcsv)

#### `c_corp_asset_adjustments`
>**Description**: Policy suffix of file containing parameters controlling indirect and targeted tax adjustments for C corporations by asset type
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/tax_rate_adjustments/asset_adjustments_[POLICY_SUFFIX].csv`](#tax_rate_adjustmentsasset_adjustments_policy_suffixcsv)

#### `pass_thru_asset_adjustments`
>**Description**: Policy suffix of file containing parameters controlling indirect and targeted tax adjustments for pass-through entities by asset type
>
>**Permitted Range**: 9 characters (files supplied follow a `xxxx_yyyy` format, in which the four `x` characters identify the law being simulated and the four `y` characters identify the time period to which they apply)
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: Go to documentation for [`/tax_rate_adjustments/asset_adjustments_[POLICY_SUFFIX].csv`](#tax_rate_adjustmentsasset_adjustments_policy_suffixcsv)

### Account category parameters
The following 18 parameters represent the shares of marginal savings directed to a specific account category (`taxable`, `deferred`, or `nontaxable`) by legal form (`c_corp`, `pass_thru`, or `ooh`) and financing source (`equity` or `debt`).

#### `c_corp_equity_account_category_share_taxable`
>**Description**: Share of marginal C corporation equity directed to taxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `c_corp_equity_account_category_share_deferred`
>**Description**: Share of marginal C corporation equity directed to temporarily deferred accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `c_corp_equity_account_category_share_nontaxable`
>**Description**: Share of marginal C corporation equity directed to nontaxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `c_corp_debt_account_category_share_taxable`
>**Description**: Share of marginal C corporation debt directed to taxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `c_corp_debt_account_category_share_deferred`
>**Description**: Share of marginal C corporation debt directed to temporarily deferred accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `c_corp_debt_account_category_share_nontaxable`
>**Description**: Share of marginal C corporation debt directed to nontaxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `pass_thru_equity_account_category_share_taxable`
>**Description**: Share of marginal pass-through equity directed to taxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `pass_thru_equity_account_category_share_deferred`
>**Description**: Share of marginal pass-through equity directed to temporarily deferred accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `pass_thru_equity_account_category_share_nontaxable`
>**Description**: Share of marginal pass-through equity directed to nontaxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `pass_thru_debt_account_category_share_taxable`
>**Description**: Share of marginal pass-through debt directed to taxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `pass_thru_debt_account_category_share_deferred`
>**Description**: Share of marginal pass-through debt directed to temporarily deferred accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `pass_thru_debt_account_category_share_nontaxable`
>**Description**: Share of marginal pass-through debt directed to nontaxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `ooh_equity_account_category_share_taxable`
>**Description**: Share of marginal owner-occupied equity directed to taxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `ooh_equity_account_category_share_deferred`
>**Description**: Share of marginal owner-occupied equity directed to temporarily deferred accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `ooh_equity_account_category_share_nontaxable`
>**Description**: Share of marginal owner-occupied equity directed to nontaxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `ooh_debt_account_category_share_taxable`
>**Description**: Share of marginal owner-occupied debt directed to taxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `ooh_debt_account_category_share_deferred`
>**Description**: Share of marginal owner-occupied debt directed to temporarily deferred accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

#### `ooh_debt_account_category_share_nontaxable`
>**Description**: Share of marginal owner-occupied debt directed to nontaxable accounts
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Years
>
>**Source**: CBO
>
>**Note**: For each legal-form/source-of-financing combination, the sum of the three account category values must equal 1.0000

### `/depreciation_adjustments/` parameter files
The files in this directory contain parameter matrices with policy suffixes in their filenames. Which parameter matrix file gets used for any given year in the model is specified by the `POLICY_SUFFIX` set in the [Policy suffix parameters](#policy-suffix-parameters) in `policy_parameters_Current-Law_comprehensive.csv` and `policy_parameters_Current-Law_uniformity.csv`.

#### `/depreciation_adjustments/recovery_periods_[POLICY_SUFFIX].csv`
>**Description**: Depreciation recovery periods
>
>**Units**: Years
>
>**Permitted Range**: 0.0 – 100.0
>
>**File(s) Supplied**: </br>`recovery_periods_CLaw_perm.csv` (all years, reflecting 5-year amortization of R&D)
>
>**Dimensions**: Detailed industry (rows) by asset type (columns)
>
>**Source**: CBO, based on IRS Publication 946, Appendix B
>
>**Note**: A value of 100000.0 can be used for nondepreciable assets, such as land. Inventory values are ignored in the model

#### `/depreciation_adjustments/acceleration_rates_[POLICY_SUFFIX].csv`
>**Description**: Depreciation acceleration rates for declining-balance method
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 - 5.0000
>
>**File(s) Supplied**: `acceleration_rates_CLaw_perm.csv` (all years)
>
>**Dimensions**: Detailed industry (rows) by asset type (columns)
>
>**Source**: CBO, based on IRS Publication 946
>
>**Note**: Use 1.0 for straight-line depreciation. Inventory values are ignored in the model

#### `/depreciation_adjustments/straight_line_flags_[POLICY_SUFFIX].csv`
>**Description**: Flags that signal whether declining-balance depreciation should switch to straight-line depreciation when it becomes advantageous and whether to conform tax depreciation to economic depreciation
>
>**Permitted Range**: </br>-1 to conform tax depreciation to economic depreciation </br>&nbsp;1 to switch from declining-balance to straight-line depreciation when it becomes advantageous to do so </br>&nbsp;0 otherwise
>
>**File(s) Supplied**: `straight_line_flags_CLaw_perm.csv` (all years)
>
>**Dimensions**: Detailed industry (rows) by asset type (columns)
>
>**Source**: CBO, based on Internal Revenue Code
>
>**Note**: Inventory values are ignored in the model

#### `/depreciation_adjustments/inflation_adjustments_[POLICY_SUFFIX].csv`
>**Description**: Shares of undepreciated basis to be indexed for inflation
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**: `inflation_adjustments_CLaw_perm.csv` (all years)
>
>**Dimensions**: Detailed industry (rows) by asset type (columns)
>
>**Source**: CBO, based on Internal Revenue Code
>
>**Note**: Inventory values reflect share using LIFO. Otherwise, use 1.0000 when conforming tax depreciation to economic depreciation

#### `/depreciation_adjustments/sec_179_expens_shares_[POLICY_SUFFIX].csv`
>**Description**: Shares of investment eligible for expensing under Section 179
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**:</br>`sec_179_expens_CLPT_perm.csv` (all years, pass-through entities only—for use under the comprehensive perspective)
</br>`sec_179_expens_CLCC_perm.csv` (all years, C corporations only—for use under the comprehensive perspective)
</br>`sec_179_expens_CLaw_perm.csv` (all years, all businesses—for use under the tax uniformity perspective)
>
>**Dimensions**: Detailed industry (rows) by asset type (columns)
>
>**Source**: CBO
>
>**Notes**: Under the comprehensive perspective, values vary by legal form and industry to reflect differences in firm sizes. Under the tax uniformity perspective, all legal forms and industries receive the same value. Variation by asset type reflects statutory eligibility that is reflected under both perspectives

#### `/depreciation_adjustments/other_expens_shares_[POLICY_SUFFIX].csv`
>**Description**: Shares of investment eligible for expensing under sections other than 179
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**: </br>`other_expens_share_CLaw_2024.csv` (reflecting 5-year amortization of R&D and 40% phaseout of bonus depreciation)
</br>`other_expens_share_CLaw_2025.csv` (also reflecting 60% phaseout of bonus depreciation)
</br>`other_expens_share_CLaw_2026.csv` (also reflecting 80% phaseout of bonus depreciation)
</br>`other_expens_share_CLaw_perm.csv` (2027 and beyond, reflecting full phaseout of bonus depreciation)
>
>**Dimensions**: Detailed industry (rows) by asset type (columns)
>
>**Source**: CBO, based on Internal Revenue Code

### `/investment_tax_credit_adjustments/` parameter files
The files in this directory contain parameter matrices with policy suffixes in their filenames. Which parameter matrix file gets used for any given year in the model is specified by the `POLICY_SUFFIX` set in the [Policy suffix parameters](#policy-suffix-parameters) in `policy_parameters_Current-Law_comprehensive.csv` and `policy_parameters_Current-Law_uniformity.csv`.

#### `/investment_tax_credit_adjustments/itc_rates_[POLICY_SUFFIX].csv`
>**Description**: Investment tax credit rates
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**: </br>`itc_rates_CLaw_2024.csv` (2024 values for the solar and wind energy ITC, the advanced manufacturing ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2025.csv` (2025 values for the solar and wind energy ITC, the advanced manufacturing ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2026.csv` (2026 values for the solar and wind energy ITC, the advanced manufacturing ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2027.csv` (2027 values for the solar and wind energy ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2028.csv` (2028 values for the solar and wind energy ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2029.csv` (2029 values for the solar and wind energy ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2030.csv` (2030 values for the solar and wind energy ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2031.csv` (2031 values for the solar and wind energy ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2032.csv` (2032 values for the solar and wind energy ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2033.csv` (2033 values for the solar and wind energy ITC, and the full R&E and orphan drug credits)
</br>`itc_rates_CLaw_2034.csv` (2034 values for the solar and wind energy ITC, and the full R&E and orphan drug credits)
>
>**Dimensions**: Standard industry (rows) by asset type (columns)
>
>**Source**: CBO, based on SOI Tables for Form 6765
>
>**Note**: Currently used for R&E credit, orphan drug credit, advanced manufacturing ITC, and solar and wind ITC

#### `/investment_tax_credit_adjustments/itc_nondeprcbl_bases_[POLICY_SUFFIX].csv`
>**Description**: Shares of investment for which an investment tax credit was claimed that cannot also be depreciated
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**: </br>`itc_nondeprcbl_bases_CLaw_full.csv` (values of 1.0 in all cells other than for the solar and wind energy ITC, which reduces cost recovery deductions by a factor of 0.5)
>
>**Dimensions**: Standard industry (rows) by asset type (columns)
>
>**Source**: CBO

### `/production_tax_credit_adjustments/` parameter files
The files in this directory contain parameter matrices with policy suffixes in their filenames. Which parameter matrix file gets used for any given year in the model is specified by the `POLICY_SUFFIX` set in the [Policy suffix parameters](#policy-suffix-parameters) in `policy_parameters_Current-Law_comprehensive.csv` and `policy_parameters_Current-Law_uniformity.csv`.

#### `/production_tax_credit_adjustments/ptc_rates_[POLICY_SUFFIX].csv`
>**Description**: Production tax credit rates
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**: </br>`ptc_rates_CLaw_2024.csv` (2024 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2025.csv` (2025 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2026.csv` (2026 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2027.csv` (2027 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2028.csv` (2028 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2029.csv` (2029 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2030.csv` (2030 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2031.csv` (2031 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2032.csv` (2032 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2033.csv` (2033 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
</br>`ptc_rates_CLaw_2034.csv` (2034 values for the solar and wind energy PTC, and the advanced manufacturing PTC)
>
>**Dimensions**: Standard industry (rows) by asset type (columns)
>
>**Source**: CBO
>
>**Note**: Currently used for solar and wind energy PTC, and advanced manufacturing PTC

### `/tax_rate_adjustments/` parameter files
The files in this directory contain parameter matrices with policy suffixes in their filenames. Which parameter matrix file gets used for any given year in the model is specified by the `POLICY_SUFFIX` set in the [Policy suffix parameters](#policy-suffix-parameters) in `policy_parameters_Current-Law_comprehensive.csv` and `policy_parameters_Current-Law_uniformity.csv`.

#### `/tax_rate_adjustments/sec_199A_adjustments_[POLICY_SUFFIX].csv`
>**Description**: Two different parameters:</br>1. Share of qualified business income (above the taxable income threshold) eligible for Section 199A deduction
</br>2. Rate of Section 199A deduction
>
>**Units**:</br>1. Share (in decimal format) </br>2. Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**: </br>`sec_199A_adjustments_CLaw_temp.csv` (2024-2025, reflecting Section 199A deduction of 20%)
</br>`sec_199A_adjustments_CLaw_perm.csv` (2026 and beyond, reflecting expiration of Section 199A)
>
>**Dimensions**: Detailed industry
>
>**Source**: CBO, based on Internal Revenue Code

#### `/tax_rate_adjustments/industry_adjustments_[POLICY_SUFFIX].csv`
>**Description**: Two different parameters: </br>1. Share of net business income eligible for other industry-specific adjustment
</br>2. Rate of other industry-specific adjustment
>
>**Units**: </br>1. Share (in decimal format)
</br>2. Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**: </br>`industry_adjustments_CLaw_perm.csv` (values of 0.0 in all cells)
>
>**Dimensions**: Detailed industry
>
>**Source**: CBO, based on Internal Revenue Code
>
>**Note**: Available for simulating the pre-2017 deduction for domestic production activities

#### `/tax_rate_adjustments/asset_adjustments_[POLICY_SUFFIX].csv`
>**Description**: Two different parameters: </br>1. Share of net business income eligible for asset-type-specific adjustment
</br>2. Rate of asset-type-specific adjustment
>
>**Units**:</br> 1. Share (in decimal format)
</br>2. Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**File(s) Supplied**: `asset_adjustments_CLaw_perm.csv` (values of 0.0 in all cells)
>
>**Dimensions**: Asset type
>
>**Source**: CBO, based on Internal Revenue Code
>
>**Note**: Available for simulating a patent box or other special tax rate targeted to specific asset types
