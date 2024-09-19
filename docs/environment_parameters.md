# Economic Environment Parameters for CBO's Capital Tax Model (CapTax)

Parameters pertaining to the underlying economic environment for the CapTax model are located in the  
`/captax/captax/data/inputs/environment_parameters/` directory.

Within that directory, there are three files:
* [debt_shares.csv](#debt_sharescsv)
* [economic_depreciation.csv](#economic_depreciationcsv)
* [environment_parameters.csv](#environment_parameterscsv)

Details of the parameters in each of those files are provided, below.

## environment_parameters.csv
The parameters in `environment_parameters.csv` can be grouped into four categories:
* [Financing share parameters](#financing-share-parameters)
* [Rate of return parameters](#rate-of-return-parameters)
* [Owner-occupied housing parameters](#owner-occupied-housing-parameters)
* [Holding period parameters](#holding-period-parameters)

Details for each parameter within those groups are provided, below.

### Financing share parameters
#### `financial_sector_debt_share`
> **Description**: Share of investment in fixed assets funded by debt (*C corporations and pass-through entities, "Finance" and "Management of Companies" sectors only*)
>
> **Units**: Share (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar (industry-specific values are in `/captax/captax/data/inputs/environment_parameters/debt_shares.csv`)
>
> **Source**: CBO, based on the Financial Accounts of the United States (2001-2023)
>
> **Note**: Changing this value will adjust the corresponding industry-specific values read in from `/captax/captax/data/inputs/environment_parameters/debt_shares.csv`

####  `nonfinancial_c_corp_debt_share`
> **Description**: Share of investment in fixed assets funded by debt (*C corporations only, all sectors except "Finance" and "Management of Companies"*)
>
> **Units**: Share (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar (industry-specific values are in `/captax/captax/data/inputs/environment_parameters/debt_shares.csv`)
>
> **Source**: CBO, based on the Financial Accounts of the United States (2001-2023)
>
> **Note**: Changing this value will automatically adjust the corresponding industry-specific values read in from `/captax/captax/data/inputs/environment_parameters/debt_shares.csv`

#### `nonfinancial_pass_thru_debt_share`
> **Description**: Share of investment in fixed assets funded by debt (*Pass-through entities only, all sectors except "Finance" and "Management of Companies"*)
>
> **Units**: Share (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar (industry-specific values are in `/captax/captax/data/inputs/environment_parameters/debt_shares.csv`)
>
> **Source**: CBO, based on the Financial Accounts of the United States (2001-2023)
>
> **Note**: Changing this value will automatically adjust the corresponding industry-specific values read in from `/captax/captax/data/inputs/environment_parameters/debt_shares.csv`

#### `ooh_debt_share`
> **Description**: Share of investment in fixed assets funded by debt (*Owner-occupied housing only*)
>
> **Units**: Share (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar (industry-specific values do not apply)
>
> **Source**: CBO, based on the Financial Accounts of the United States (2001-2023)

#### `c_corp_equity_retained_earnings_share`
> **Description**: Share of equity-financed investment in fixed assets funded with retained earnings (*C corporations only*)
>
> **Units**: Share (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar
>
> **Source**: CBO
>
> **Note**: The difference between 1.0000 and this parameter represents the share of equity-financed investment in fixed assets funded with new shares

#### `c_corp_equity_repurchases_share`
> **Description**: Share of returns from equity-financed investment in fixed assets paid out as stock repurchases (*C corporations only*)
>
> **Units**: Share (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar
>
> **Source**: CBO
>
> **Note**: The difference between 1.0000 and this parameter represents the share of returns from equity-financed investment in fixed assets paid out as dividends

### Rate of return parameters

#### `nominal_rate_of_return_equity`
> **Description**: Nominal rate of return on equity-financed investment in fixed assets
>
> **Units**: Rate (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000 (although values in excess of 0.1000 would be unusual)
>
> **Dimensions**: Scalar
>
> **Source**: CBO (Interest rate on 10-year Treasury bonds plus an equity premium)

####  `nominal_rate_of_return_debt`
> **Description**: Nominal rate of return on debt-financed investment in fixed assets
>
> **Units**: Rate (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000 (although values in excess of 0.1000 would be unusual)
>
> **Dimensions**: Scalar
>
> **Source**: CBO (Interest rate on corporate bonds rated Baa)

#### `inflation_rate`
> **Description**: Rate of inflation
>
> **Units**: Rate (in decimal format)
>
> **Permitted Range**: Unlimited (although negative values and values in excess of 0.1000 would be unusual)
>
> **Dimensions**: Scalar
>
> **Source**: CBO (Consumer price index for all urban consumers)

### Owner-occupied housing parameters

#### `avg_local_prop_tax_rate`
> **Description**: Property tax rate that applies to owner-occupied housing
>
> **Units**: Rate (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar
>
> **Source**: CBO, based on the 2021 American Housing Survey

### Holding period parameters

#### `cap_gains_short_term_share`
> **Description**: Share of capital gains accruals realized within one year of purchase
>
> **Units**: Rate (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar (year-by-year changes can be made in `/captax/captax/data/inputs/policy_parameters/policy_parameters_Current-Law_[PERSPECTIVE].csv`)
>
> **Source**: CBO, based on SOI Sale of Capital Assets (2007-2015)
>
> **Note**: The "long_term" share (realized during the purchaser’s lifetime but more than one year after purchase) is the difference between 1.0000 and the sum of the "short_term" and "at_death" shares

#### `cap_gains_at_death_share`
> **Description**: Share of capital gains accruals not realized during purchaser’s lifetime
>
> **Units**: Rate (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar (year-by-year changes can be made in `/captax/captax/data/inputs/policy_parameters/policy_parameters_Current-Law_[PERSPECTIVE].csv`)
>
> **Source**: CBO, based on SOI Sale of Capital Assets (2007-2015) and SOI Estate Tax Returns (2007-2016)
>
> **Note**: The "long_term" share (realized during the purchaser’s lifetime but more than one year after purchase) is the difference between 1.0000 and the sum of the "short_term" and "at_death" shares

#### `cap_gains_short_term_holding_period`
> **Description**: Average holding period of capital gains realized within one year of purchase
>
> **Units**: Years
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Scalar (year-by-year changes can be made in `/captax/captax/data/inputs/policy_parameters/policy_parameters_Current-Law_[PERSPECTIVE].csv`)
>
> **Source**: CBO, based on SOI Sale of Capital Assets (2007-2015)

#### `cap_gains_long_term_holding_period`
> **Description**: Average holding period of capital gains realized more than one year after purchase
>
> **Units**: Years
>
> **Permitted Range**: 1.0001 to 100.0000 (higher values imply implausibly long lifespans)
>
> **Dimensions**: Scalar (year-by-year changes can be made in `/captax/captax/data/inputs/policy_parameters/policy_parameters_Current-Law_[PERSPECTIVE].csv`)
>
> **Source**: CBO, based on SOI Sale of Capital Assets (2007-2015)

#### `cap_gains_at_death_holding_period`
> **Description**: Average holding period of capital gains not realized during purchaser’s lifetime
>
> **Units**: Years
>
> **Permitted Range**: 2.0000 to 100.0000 (higher values imply implausibly long lifespans)
>
> **Dimensions**: Scalar (year-by-year changes can be made in `/captax/captax/data/inputs/policy_parameters/policy_parameters_Current-Law_[PERSPECTIVE].csv`)
>
> **Source**: CBO, based on SOI Sale of Capital Assets (2007-2015) and SOI Estate Tax Returns (2007-2016)

#### `ret_plan_deferred_holding_period`
> **Description**: Average holding period of assets in whole life insurance policies and nonqualified annuities
>
> **Units**: Years
>
> **Permitted Range**: 1.0000 to 100.0000 (higher values imply implausibly long lifespans)
>
> **Dimensions**: Scalar (year-by-year changes can be made in `/CapTax/captax/data/inputs/policy_parameters/policy_parameters_Current-Law_[PERSPECTIVE].csv`)
>
> **Source**: CBO

#### `ret_plan_nontaxable_holding_period`
> **Description**: Average holding period of assets held 1. by nonprofit organizations, and 2. in IRAs and qualified retirement accounts
>
> **Units**: Years
>
> **Permitted Range**: 1.0000 to 100.0000 (higher values imply implausibly long lifespans)
>
> **Dimensions**: Scalar
>
> **Source**: CBO
>
> **Note**: Set to minimum

#### `inventories_holding_period`
> **Description**: Average holding period of inventories
>
> **Units**: Years
>
> **Permitted Range**: Positive values (although values in excess of 1.0000 would be unusual)
>
> **Dimensions**: Scalar
>
> **Source**: CBO

## debt_shares.csv
There is just a single parameter matrix in this file.

#### `debt_shares`
> **Description**: Share of investment in fixed assets funded by debt
>
> **Units**: Share (in decimal format)
>
> **Permitted Range**: 0.0000 to 1.0000
>
> **Dimensions**: Standard industry (rows) by legal form (columns)
>
> **Source**: CBO, based on SOI Nonfarm Sole Proprietorship, Partnership, and Corporate Returns (2018-2020)
>
>**Note**: The values for C corporations and pass-through entities read in from this file will be adjusted if any of the first three “Financing share parameters” in `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv` (`financial_sector_debt_share`, `nonfinancial_c_corp_debt_share`, or `nonfinancial_pass_thru_debt_share`) are modified. Directly modifying values in this array, however, will have no impact on the values read in from `/captax/captax/data/inputs/environment_parameters/environment_parameters.csv`

## economic_depreciation.csv
There is just a single parameter matrix in this file.

#### `economic_depreciation`
>**Description**: Annual rate of reduction in the value of a fixed asset due to wear and tear or obsolescence
>
>**Units**: Rate (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000
>
>**Dimensions**: Detailed industry (rows) by asset type (columns)
>
>**Source**: CBO, based on 2022 BEA Detailed Fixed Asset tables (Depreciation, current cost/Net stocks, current cost)
