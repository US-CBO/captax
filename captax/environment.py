import os
import numpy as np
import pandas as pd
from captax.constants import *


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


class Environment:
    """Define the object used to read and store economic environment parameters.

    Attributes
    ----------
    environment_path : str
        String describing the folder path where environment parameters input files are
        stored.
    environment_parameters_permitted_ranges_file : str
        String describing the file path of file storing permitted ranges for environment
        parameters.
    env : pd.DataFrame
        DataFrame with environment parameters specified in 'environment_parameters.csv'.
    agg_debt_share : dict
        Aggregate debt shares.
    inflation_rate : np.float
        Inflation rate.
    rate_of_return : dict
        Nominal and real rates of return on equity and debt.
    avg_local_prop_tax_rate : np.float
        Average local property tax rate.
    cap_gains_share_held : dict
        Parameters distributing capital gains by duration class.
    cap_gains_holding_period : dict
        Parameters defining capital gain holding periods by duration class.
    ret_plan_holding_period : dict
        Parameters defining retirement plans holding periods.
    inventories_holding_period : np.float
        Parameter defining inventories baseline holding period.
    econ_depreciation_detailed_industry : np.ndarray
        Economic depreciation rates by detailed industry and asset type.
    debt_shares_df : pd.DataFrame
        DataFrame with unscaled debt-financing shares by legal form (C corps,
        pass-throughs, and owner-occupied housing).
    shares : dict
        Dictionary including rescaled equity and debt-financing shares for businesses
        and owner-occupied housing, and shares of C corp equity investments financed by
        new equity and retained earnings.
    permitted_ranges : dict
        Permitted ranges for environment parameters used in the model.

    """

    def __init__(self):
        """Initialize Environment object.

        This method calls six other methods:
            * self._read_economic_environment()
              Reads in the economic environment parameters.
              
            * self._read_econ_depreciation()
              Reads economic depreciation rates by detailed industry and asset type.
            
            * self._read_debt_shares() 
              Reads shares of investment financed with debt, by industry and
              legal form.
            
            * self._calc_debt_share_rescaling_factors()
              Calculates rescaling factors applied to debt-financing shares by 
              industry and legal form.
            
            * self._rescale_debt_shares()
              Rescales debt-financing shares by industry and legal form using 
              aggregate rescaling factors returned by calc_debt_share_rescaling_factors() 
              method.
            
            * self._check_environment_parameter_ranges()
              Checks that all environment parameters are within permitted ranges.

        Parameters
        ----------
        None
            Method reads in environment parameters input file.

        Returns
        -------
        None
            Method stores environment parameters as attributes of Environment object.

        """
        self.environment_path = f"{CURRENT_PATH}/data/inputs/environment_parameters/"
        self.environment_parameters_permitted_ranges_file = (
            f"{self.environment_path}/environment_parameters_permitted_ranges.csv"
        )

        # Read in scalar economic environment parameters
        # ------------------------------------------------------------------------------
        self.env = self._read_economic_environment("environment_parameters.csv")

        # Aggregate debt shares
        self.agg_debt_share = {
            "financial_sector": self.env.iloc[0]["financial_sector_debt_share"].round(
                decimals=4
            ),
            "nonfin_c_corp": self.env.iloc[0]["nonfinancial_c_corp_debt_share"].round(
                decimals=4
            ),
            "nonfin_pass_thru": self.env.iloc[0][
                "nonfinancial_pass_thru_debt_share"
            ].round(decimals=4),
            "ooh": self.env.iloc[0]["ooh_debt_share"].round(decimals=4),
        }

        ooh_shares = {
            "debt": self.env.iloc[0]["ooh_debt_share"].round(decimals=4),
            "typical_equity": 1.0
            - self.env.iloc[0]["ooh_debt_share"].round(decimals=4),
        }

        # C corp equity financing and profit use shares
        c_corp_equity_shares = {
            "retained_earnings": self.env.iloc[0][
                "c_corp_equity_retained_earnings_share"
            ],
            "new_equity": 1.0
            - self.env.iloc[0]["c_corp_equity_retained_earnings_share"],
            "stock_repurchases": self.env.iloc[0]["c_corp_equity_repurchases_share"],
            "dividends": 1.0 - self.env.iloc[0]["c_corp_equity_repurchases_share"],
        }

        # Rates of return
        nominal_rate_of_return_equity = self.env.iloc[0][
            "nominal_rate_of_return_equity"
        ]
        nominal_rate_of_return_debt = self.env.iloc[0]["nominal_rate_of_return_debt"]
        self.inflation_rate = self.env.iloc[0]["inflation_rate"]

        self.rate_of_return = {
            "nominal": {
                "equity": nominal_rate_of_return_equity,
                "debt": nominal_rate_of_return_debt,
            },
            "real": {
                "equity": nominal_rate_of_return_equity - self.inflation_rate,
                "debt": nominal_rate_of_return_equity - self.inflation_rate,
            },
        }

        # Average local property tax rate
        self.avg_local_prop_tax_rate = self.env.iloc[0]["avg_local_prop_tax_rate"]

        # Holding period parameters
        self.cap_gains_share_held = {
            "short_term": self.env.iloc[0]["cap_gains_short_term_share"],
            "at_death": self.env.iloc[0]["cap_gains_at_death_share"],
        }

        self.cap_gains_holding_period = {
            "short_term": self.env.iloc[0]["cap_gains_short_term_holding_period"],
            "long_term": self.env.iloc[0]["cap_gains_long_term_holding_period"],
            "at_death": self.env.iloc[0]["cap_gains_at_death_holding_period"],
        }

        if not (
            self.cap_gains_holding_period["long_term"]
            > self.cap_gains_holding_period["short_term"]
        ):
            raise ValueError(
                f"Parameter value of cap_gains_long_term_holding_period has to be larger "
                f"than value of cap_gains_short_term_holding_period"
            )

        if not (
            self.cap_gains_holding_period["at_death"]
            > self.cap_gains_holding_period["long_term"]
        ):
            raise ValueError(
                f"Parameter value of cap_gains_at_death_term_holding_period has to be larger "
                f"than value of cap_gains_long_term_holding_period"
            )

        self.ret_plan_holding_period = {
            "deferred": self.env.iloc[0]["ret_plan_deferred_holding_period"],
            "nontaxable": self.env.iloc[0]["ret_plan_nontaxable_holding_period"],
        }

        self.inventories_holding_period = self.env.iloc[0]["inventories_holding_period"]

        # Read in other environment parameters that are stored in matrices
        # ------------------------------------------------------------------------------
        self.econ_depreciation_detailed_industry = self._read_econ_depreciation(
            "economic_depreciation.csv"
        )

        # Financing shares by legal form and industries
        self.debt_shares_df = self._read_debt_shares("debt_shares.csv")
        rescaling_factors = self._calc_debt_share_rescaling_factors(self.agg_debt_share)

        debt_shares = self._rescale_debt_shares(self.debt_shares_df, rescaling_factors)
        equity_shares = 1.0 - debt_shares
        equity_shares[:NUM_BIZ_INDS, :NUM_ASSETS, LEGAL_FORMS["ooh"]] = np.zeros(
            (NUM_BIZ_INDS, NUM_ASSETS)
        )

        financing_shares = {"debt": debt_shares, "typical_equity": equity_shares}

        # Pull all shares dictionaries together
        self.shares = {
            "financing": financing_shares,
            "ooh": ooh_shares,
            "c_corp_equity": c_corp_equity_shares,
        }

        # Convert permitted ranges into a dictionary, and then check that all parameter
        # values are valid (that is, within the permitted range)
        # ------------------------------------------------------------------------------
        self.permitted_ranges = pd.read_csv(
            self.environment_parameters_permitted_ranges_file,
            index_col="environment_parameter",
        ).to_dict("index")
        self._check_environment_parameter_ranges(self.env, self.permitted_ranges)

        print("* Environment parameters read")

        return None

    def _read_economic_environment(self, filename):
        """Read in the economic environment parameters.

        Data read in are organized as two columns: 'parameter' and 'value'.
        DataFrame returned is transposed version of the csv data.

        Parameters
        ----------
        filename : str
            Name of csv file to read.

        Returns
        --------
        df : pd.DataFrame
            DataFrame with a single row and each column containing an economic
            environment parameter.

        """
        assert filename.endswith(".csv")

        df = pd.read_csv(
            self.environment_path + filename, index_col="parameter"
        ).transpose()

        return df

    def _read_econ_depreciation(self, filename):
        """Read economic depreciation rates by detailed industry and asset type.

        Parameters
        ----------
        filename : str
            Name of csv file to be read.

        Returns
        -------
        ndarray : np.ndarray
            Array with economic depreciation rates by detailed industry and asset type,
            rounded to 4 decimal places.

        """
        assert filename.endswith(".csv")

        file = self.environment_path + filename
        df = pd.read_csv(file, skiprows=1, index_col="Industries/Asset types")
        ndarray = df.round(decimals=4).to_numpy()

        return ndarray

    def _read_debt_shares(self, filename):
        """Read shares of investment financed with debt, by industry and legal form.

        Parameters
        ----------
        filename : str
            Name of csv file to be read.

        Returns
        -------
        df : pd.DataFrame
            DataFrame with debt shares by industry and legal form.

        """
        assert filename.endswith(".csv")

        df = pd.read_csv(self.environment_path + filename)

        return df

    def _calc_debt_share_rescaling_factors(self, agg_debt_share):
        """Calculate rescaling factors applied to debt-financing shares by industry and
        legal form.

        Rescaling factors are calculated at an aggregate level for:
            1) financial sector,
            2) nonfinancial C corps, and
            3) nonfinancial pass-throughs
        by dividing the aggregate debt-financing shares specified in the environment
        parameters input file by the hard-coded values for aggregate debt shares
        specified at the bottom of constants.py.

        Parameters
        ----------
        agg_debt_share : dict
            Aggregate debt-financing shares.

        Returns
        -------
        rescaling_factors : dict
            Aggregate rescaling factors applied to the financial sector, nonfinancial
            C corps, and nonfinancial pass-throughs.

        """
        rescaling_factors = {
            "financial_sector": agg_debt_share["financial_sector"]
            / AGG_DEBT_SHARE["financial_sector"],
            "nonfin_c_corp": agg_debt_share["nonfin_c_corp"]
            / AGG_DEBT_SHARE["nonfin_c_corp"],
            "nonfin_pass_thru": agg_debt_share["nonfin_pass_thru"]
            / AGG_DEBT_SHARE["nonfin_pass_thru"],
        }

        return rescaling_factors

    def _rescale_debt_shares(self, debt_shares, rescaling_factors):
        """Rescale debt-financing shares by industry and legal form using aggregate
        rescaling factors returned by self._calc_debt_share_rescaling_factors() method.

        Parameters
        ----------
        debt_shares : pd.DataFrame
            DataFrame containing debt-financing shares by industry and legal form.
        rescaling_factors : dict
            Dictionary containing rescaling factors to apply to the debt shares.

        Returns
        -------
        rescaled_debt_shares : np.ndarray
            Array containing debt-financing shares by industry and legal form, after
            rescaling.

        Note
        ----
        Only rescales debt-financing shares if agg_debt_share parameters have changed
        relative to the hard-coded values at the bottom of `constants.py`.

        """
        # Only rescale debt-financing shares if self.agg_debt_share is different from
        # AGG_DEBT_SHARE
        if self.agg_debt_share != AGG_DEBT_SHARE:

            # Rescale debt shares by industry based scaling factors.
            debt_shares.loc[ALL_FINANCIAL_INDS, "c_corp"] *= rescaling_factors[
                "financial_sector"
            ]
            debt_shares.loc[ALL_NONFINANCIAL_INDS, "c_corp"] *= rescaling_factors[
                "nonfin_c_corp"
            ]
            debt_shares.loc[ALL_FINANCIAL_INDS, "pass_thru"] *= rescaling_factors[
                "financial_sector"
            ]
            debt_shares.loc[ALL_NONFINANCIAL_INDS, "pass_thru"] *= rescaling_factors[
                "nonfin_pass_thru"
            ]

            # Make sure debt shares do not exceed 1.0 after applying the rescaling
            # factors
            debt_shares["c_corp"].clip(upper=1.0, inplace=True)
            debt_shares["pass_thru"].clip(upper=1.0, inplace=True)

        # Save debt shares by industry and legal form as an np.ndarray
        rescaled_debt_shares = np.zeros(
            (NUM_INDS, NUM_ASSETS, NUM_FOR_PROFIT_LEGAL_FORMS)
        )

        for legal_form in ["c_corp", "pass_thru", "ooh"]:
            rescaled_debt_shares[
                :NUM_INDS, :NUM_ASSETS, LEGAL_FORMS[legal_form]
            ] = np.tile(debt_shares[legal_form], (NUM_ASSETS, 1)).transpose()

        # Round debt shares to four decimal points
        rescaled_debt_shares = np.round(rescaled_debt_shares, decimals=4)

        return rescaled_debt_shares

    def _check_environment_parameter_ranges(
        self, environment_parameters, permitted_ranges
    ):
        """Check that all environment parameters are within permitted ranges.

        Parameters
        ----------
        environment_parameters : pd.DataFrame
            DataFrame containing all the environment parameters that are dimensioned by
            year.
        permitted_ranges : dict
            Dictionary containing the min and max permitted values for each parameter.

        Returns
        -------
        None

        Raises
        ------
        ValueErrors if a parameter is out of permitted range.

        """
        suffix_dict = {
            "econ_depreciation_detailed_industry": self.econ_depreciation_detailed_industry,
            "c_corp_debt_shares": self.debt_shares_df["c_corp"],
            "pass_thru_debt_shares": self.debt_shares_df["pass_thru"],
            "ooh_debt_shares": self.debt_shares_df["ooh"],
        }

        for key in permitted_ranges:
            # Skip (continue) checking any parameters with min and max values set to 'NA'
            # Note: 'NA' in the data gets read in as float('nan')
            if np.isnan(permitted_ranges[key]["min_value"]) and np.isnan(
                permitted_ranges[key]["max_value"]
            ):
                continue

            permitted_range_str = f"[{permitted_ranges[key]['min_value']}, {permitted_ranges[key]['max_value']}]"

            # First check parameter values already stored in numpy arrays
            if key in suffix_dict.keys():
                if not (
                    (permitted_ranges[key]["min_value"] <= suffix_dict[key]).all()
                    & (suffix_dict[key] <= permitted_ranges[key]["max_value"]).all()
                ):
                    raise ValueError(
                        f"One of the parameter values in {key} is not within the permitted "
                        f"range {permitted_range_str}"
                    )

            # Otherwise, skip parameter values that are strings containing names of file
            # suffixes and then process the remaining parameters
            elif key not in suffix_dict.keys():
                for val in environment_parameters[key].values:
                    if not (
                        # Note: use float() to deal with '-inf' and 'inf' in the data
                        (float(permitted_ranges[key]["min_value"]) <= val)
                        & (val <= float(permitted_ranges[key]["max_value"]))
                    ):
                        raise ValueError(
                            f"The value for {key} ({val}) is not within the permitted range "
                            f"{permitted_range_str}"
                        )

        return None
