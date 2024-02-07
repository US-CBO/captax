# Weights Data for CBO's Capital Tax Model (CapTax)

There are four components to the weights used in CBO's CapTax model:
* [Asset values](#asset-values)
* [Legal form shares](#legal-form-shares)
* [Detailed industry weights](#detailed-industry-weights)
* [Debt shares](environment_parameters.md#debt-shares)

Weights data files for the first three components ([Asset values](#asset-values), [Legal form shares](#legal-form-shares), and [Detailed industry weights](#detailed-industry-weights)) are in `/captax/captax/data/inputs/weights_data/`. The last component ([Debt shares](environment_parameters.md#debt-shares)), however, also factors directly into the tax calculations in the model. Those weights data are located in `/captax/captax/data/inputs/environment_parameters`.

## Asset values
The primary weight values used in the CapTax model consist of asset values by industry and asset type.

### `assets.csv`
>**Description**: Net stock of fixed assets, current cost
>
>**Units**: Millions of dollars
>
>**Permitted Range**: All positive numbers
>
>**Dimensions**: Standard industry (rows) by asset type (columns)
>
>**Source**:
</br>2021 BEA Detailed Fixed Asset tables (Equipment, Structures, Intellectual Property) </br>2021 BLS Detailed Capital Measures tables (Inventories and Land)
</br>CBO estimates based on data from the U.S. Census Bureau, the Independent Petroleum Association of America, the U.S. Geological Survey, and the Energy Information Administration (tangible mining structures, mineral exploration, mine and well development) </br> CBO estimates based on 2019 data from the Internal Revenue Service and BEA Detailed Fixed Asset tables (R&D and own-account software eligible and not eligible for R&E credit)

## Legal form shares
There are three files used to allocate total asset values by industry and asset type among the legal forms used in the CapTax model (C corporations, pass-through entities, and owner-occupied housing). Those shares do not sum to 1.0000; the residual share is attributable to nonprofit organizations.
### `asset_shares_c_corps.csv`
>**Description**: Share of assets held by C corporations
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000 (sum of legal forms, including nonprofits, must equal 1.0000)
>
>**Dimensions**: Standard industry (rows) by asset type (columns)
>
>**Source**: CBO estimates based on data from the Internal Revenue Service (2017-2019)

### `asset_shares_pass_throughs.csv`
>**Description**: Share of assets held by pass-through entities
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.0000 to 1.0000 (sum of legal forms, including nonprofits, must equal 1.0000)
>
>**Dimensions**: Standard industry (rows) by asset type (columns)
>
>**Source**: CBO estimates based on data from the Internal Revenue Service (2017-2019)

### `asset_shares_ooh.csv`
>**Description**: Share of assets held by owner-occupied housing
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 1.0000 for Residential Structures and Land in the Owner-occupied Housing industry, 0.0000 otherwise
>
>**Dimensions**: Standard industry (rows) by asset type (columns)
>
>**Source**: By definition

## Detailed industry weights
There is just a single file weights that are used to apportion values between detailed industry and standard industry categories.

### `detailed_industry_weights.csv`
>**Description**: Share of detailed industry for each standard industry category
>
>**Units**: Share (in decimal format)
>
>**Permitted Range**: 0.000 to 1.0000
>
>**Dimensions**: Detailed industry
>
>**Source**: CBO, based on data from the U.S. Census Bureau, the Energy Information Administration, and the Federal Reserve (2017-2020)
>
>**Note**: Weights sum to 1 for each standard industry category
