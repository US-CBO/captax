import os.path
import platform
import numpy as np
import pandas as pd
import yaml
from captax.constants import *
from colorama import init, Fore

init(autoreset=True)

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def create_policies(env):
    """Create Policy objects to run through the CapTax model.

    This method calls three other methods:
        * _read_policies()
        * _validate_policy_parameters_files()
        * _produce_policy_perspective_run()

    The first method reads in the list of policies to run, included in the
    policies.yml file. The second method validates the policy parameters
    files names included in that file. The third method determines whether
    to produce model run for specified policy and perspective.

    Parameters
    ----------
    env : Environment object
        Economic environment parameters.

    Returns
    -------
    policies: list
        List of policies considered in model run.

    """
    policy_parameters_files = _read_policies()
    _validate_policy_parameters_files(policy_parameters_files)

    policies = []
    for filename in policy_parameters_files:
        start_policy_name = filename.find("_", filename.find("_") + 1)
        end_policy_name = filename.rfind("_")
        policy_name = filename[start_policy_name + 1 : end_policy_name]

        perspective = filename[filename.rfind("_") + 1 : filename.rfind(".csv")]

        produce_policy_perspective_run = _produce_policy_perspective_run(
            policy_name, perspective
        )
        if produce_policy_perspective_run == True:
            policies.append(Policy(policy_name, perspective, env))
        else:
            continue

    return policies


def _produce_policy_perspective_run(policy_name, perspective):
    """Determine whether to produce model run for specified policy and perspective.

    Model run will be produced if directory for given policy and perspective does not
    exist. If that directory already exists, users will be asked whether they want to
    produce the corresponding model run and overwrite the output already stored in the
    existing folder.

    Calls the _yes_or_no() method.

    Parameters
    ----------
    policy_name : str
        Name of policy considered.
    perspective : str
        Name of perspective considered.

    Returns
    -------
    write_output: bool
        Boolean for whether to produce policy run for specified policy and perspective.

    """
    # Set relevant paths for policy and perspective considered
    policy_path = f"{CURRENT_PATH}/data/outputs/{policy_name}"
    perspective_path = f"{policy_path}/{perspective}/"

    # If policy path does not exist, create it
    if not os.path.exists(policy_path):
        os.mkdir(policy_path)

    # Check if perspective path exists within the policy path
    # If so, prompt user to ask if results should be over-written
    if os.path.exists(perspective_path):

        # Create path string with back slashes for Windows
        if platform.system() == "Windows":
            path_str = perspective_path.replace("/", "\\")
        else:
            path_str = perspective_path

        print("\n")
        print(Fore.RED + "==============")
        print(Fore.CYAN + "   WARNING!   ")
        print(Fore.RED + "==============")
        print(f"The path: {path_str} already exists.")

        question = f"Do you want to overwrite the {perspective} output files in that directory?"
        write_output = _yes_or_no(question)

    # Otherwise, create the perspective path
    else:
        os.mkdir(perspective_path)
        write_output = True

    return write_output


def _yes_or_no(question):
    """Ask a question that requires a yes or no answer from a user.

    Parameters
    ----------
    question : str
        The question to be answered.

    Returns
    -------
    True or False

    """
    reply = str(input(question + " [Y]es or [N]o: ")).lower().strip()

    if reply == "":  # User hit Enter without typing a response
        return _yes_or_no("Please enter")
    elif reply[0] == "y":
        return True
    elif reply[0] == "n":
        return False
    else:
        return _yes_or_no("Please enter")


def _read_policies():
    """Read policies.yml file, which contains the specs for each policy to run.

    Parameters
    ----------
    None

    Returns
    -------
    policy_parameters_files : tuple
        Tuple of parameters files read in from policies.yml, which gets passed in to
        validate_policy_parameters_files().

    """
    policies_file = f"{CURRENT_PATH}/data/inputs/policy_parameters/policies.yml"
    with open(policies_file) as pf:
        policy_parameters_files = yaml.load(pf, Loader=yaml.FullLoader)
    policy_parameters_files = tuple(policy_parameters_files)

    return policy_parameters_files


def _validate_policy_parameters_files(parameters_files_list):
    """Validate the filenames in the policies.yml file.

    Check each of the policy_parameters_* file names listed in the policies.yml
    file for expected prefixes, file extentions and perspective spellings.
    Also check to make sure that the files listed actually exist.

    Parameters
    ----------
    parameters_files_list : tuple

    Returns
    -------
    None

    Raises
    ------
    ValueErrors for a variety of potential problems in parameters file names.

    """
    expected_prefix = "policy_parameters_"
    expected_file_extension = ".csv"
    expected_perspectives = ["comprehensive", "uniformity"]

    for filename in parameters_files_list:
        error_msg_part1 = f"There appears to be a problem in the name of one of your policy parameters files: \n"
        f"'{filename}'\n"

        if filename.find(expected_prefix) != 0:
            error_msg_part2 = "Your file listed in 'policies.yml' must start with the prefix: 'policy_parameters'"
            raise ValueError(error_msg_part1 + error_msg_part2)

        if filename[-4:] != expected_file_extension:
            error_msg_part2 = "Your file listed in 'policies.yml' must be a *.csv file"
            raise ValueError(error_msg_part1 + error_msg_part2)

        perspective = filename[filename.rfind("_") + 1 : filename.rfind(".csv")]
        if perspective not in expected_perspectives:
            error_msg_part2 = "Your file listed in 'policies.yml' must end with either 'comprehensive.csv' or "
            "'uniformity.csv'"
            raise ValueError(error_msg_part1 + error_msg_part2)

        full_path = f"{CURRENT_PATH}/data/inputs/policy_parameters"
        if filename not in os.listdir(full_path):
            # Create path string with back slashes for Windows
            full_path_filename = full_path + "/" + filename
            if platform.system() == "Windows":
                full_path_filename = full_path_filename.replace("/", "\\")
            error_msg_part2 = "Your file listed in 'policies.yml' doesn't seem to exist. (You could have a "
            "typo in your filename.)"
            error_msg_part3 = (
                f"\nPlease make sure this file exists:\n  {full_path_filename}"
            )
            raise ValueError(error_msg_part1 + error_msg_part2 + error_msg_part3)

    return None


class Policy:
    """Define the object used to read and store policy parameters.

    Attributes
    ----------
    policy_name : str
        String describing the policy being considered.
    perspective : str
        String describing the perspective used (must be "comprehensive" or "uniformity").
    env : Environment object
        Economic environment parameters.
    policy_path : str
        String describing the folder path where policy parameters input files are stored.
    policy_parameters_file : str
        String describing the file path of file where policy parameters are stored.
    policy_parameters_permitted_ranges_file : str
        String describing the file path of file storing permitted ranges for policy
        parameters.
    tax_rates : dict
        Tax rate parameters.
    deduction : dict
        Deduction parameters.
    biz_timing_adjustments : dict
        Timing adjustment parameters for businesses (C Corps and pass-throughs).
    cap_gains_share_held_changes : dict
        Parameters distributing capital gains by duration class.
    holding_period_changes : dict
        Changes to baseline values of holding periods by duration class.
    account_category_shares : dict
        Parameters defining account categories for equity and debt investments.
    depreciation : dict
        Policy depreciation parameters.
    itc : dict
        Investment tax credit parameters (rates and non-depreciable bases).
    tax_rate_adjustments : dict
        Tax rate adjustment parameters.

    """

    def __init__(self, policy_name, perspective, env):
        """Initialize Policy object.

        This method calls five other methods:
            * self._read_policy_parameters_file() : Reads the policy parameters file,
              which includes policy parameters that vary by year.
            * self._read_depreciation_parameters() : Reads in various policy parameters
              related to calculations of tax depreciation.
            * self._read_investment_tax_credit_parameters() : Reads in parameters
              related to the investment tax credit.
            * self._read_tax_rate_adjustment_parameters() : Reads in parameters related
              to tax rate adjustments.
            * self._check_policy_parameter_ranges() : Checks that all policy parameters
              are within permitted ranges.

        Parameters
        ----------
        policy_name : str
            String describing the policy being considered.
        perspective : str
            String describing the perspective being used (must be "comprehensive" or
            "uniformity").
        env : Environment object
            Economic environment parameters.

        Returns
        -------
        None
            Method reads policy parameters and stores them as attributes of Policy
            object.

        """
        self.policy_name = policy_name
        self.perspective = perspective
        self.env = env
        self.policy_path = f"{CURRENT_PATH}/data/inputs/policy_parameters"
        self.policy_parameters_file = f"{self.policy_path}/policy_parameters_{self.policy_name}_{self.perspective}.csv"
        self.policy_parameters_permitted_ranges_file = (
            f"{self.policy_path}/policy_parameters_permitted_ranges.csv"
        )

        # Read policy parameters to a DataFrame, then assign to numpy arrays
        # ---------------------------------------------------------------------------------
        pol = self._read_policy_parameters_file(self.policy_parameters_file)

        # Tax rate parameters
        self.tax_rates = {
            "c_corp": pol["c_corp_tax_rate"].to_numpy(),
            "pass_thru": pol["pass_thru_tax_rate"].to_numpy(),
            "seca": pol["seca_tax_rate"].to_numpy(),
            "stock_repurchases": pol["repurchases_tax_rate"].to_numpy(),
            "ooh": pol["ooh_tax_rate"].to_numpy(),
            "dividend_inc": pol["dividend_inc_tax_rate"].to_numpy(),
            "cap_gains": {
                "short_term": pol["cap_gains_short_term_tax_rate"].to_numpy(),
                "long_term": pol["cap_gains_long_term_tax_rate"].to_numpy(),
                "at_death": pol["cap_gains_at_death_tax_rate"].to_numpy(),
            },
            "interest_inc": {
                "biz": pol["interest_inc_from_biz_tax_rate"].to_numpy(),
                "ooh": pol["interest_inc_from_ooh_tax_rate"].to_numpy(),
            },
            "ret_plan": {
                "deferred": pol["ret_plan_deferred_tax_rate"].to_numpy(),
                "nontaxable": pol["ret_plan_nontaxable_tax_rate"].to_numpy(),
            },
        }

        # Deduction parameters
        self.deduction = {
            "pass_thru_inc_share_below_thresholds": pol[
                "pass_thru_inc_share_below_thresholds"
            ].to_numpy(),
            "pass_thru_eligibility_below_thresholds": pol[
                "pass_thru_eligibility_below_thresholds"
            ].to_numpy(),
            "interest_deductible_shares": {
                "c_corp": pol["c_corp_interest_deductible_share"].to_numpy(),
                "pass_thru": pol["pass_thru_interest_deductible_share"].to_numpy(),
            },
            "mortg_interest_deduction": {
                "tax_rates": pol["mortg_interest_deduction_tax_rate"].to_numpy(),
                "deductible_shares": pol["mortg_interest_deductible_share"].to_numpy(),
            },
            "prop_tax_deduction": {
                "tax_rates": pol["prop_tax_deduction_tax_rate"].to_numpy(),
                "deductible_shares": pol["prop_tax_deductible_share"].to_numpy(),
            },
        }

        # Timing adjustment parameters reflecting fluctuating rates of return
        self.biz_timing_adjustments = {
            "c_corp": {
                "net_inc": pol["c_corp_net_inc_timing_adjustment"].to_numpy(),
                "deductions": pol["c_corp_deductions_timing_adjustment"].to_numpy(),
                "credits": pol["c_corp_credits_timing_adjustment"].to_numpy(),
            },
            "pass_thru": {
                "net_inc": pol["pass_thru_net_inc_timing_adjustment"].to_numpy(),
                "deductions": pol["pass_thru_deductions_timing_adjustment"].to_numpy(),
                "credits": pol["pass_thru_credits_timing_adjustment"].to_numpy(),
            },
            "seca": {
                "net_inc": pol["seca_net_inc_timing_adjustment"].to_numpy(),
                "deductions": pol["seca_deductions_timing_adjustment"].to_numpy(),
            },
        }

        # Additive annual changes to baseline holding period parameters
        self.cap_gains_share_held_changes = {
            "short_term": pol["change_cap_gains_short_term_share"].to_numpy(),
            "at_death": pol["change_cap_gains_at_death_share"].to_numpy(),
        }

        self.holding_period_changes = {
            "cap_gains": {
                "short_term": pol[
                    "change_cap_gains_short_term_holding_period"
                ].to_numpy(),
                "long_term": pol[
                    "change_cap_gains_long_term_holding_period"
                ].to_numpy(),
                "at_death": pol["change_cap_gains_at_death_holding_period"].to_numpy(),
            },
            "ret_plan": {
                "deferred": pol["change_ret_plan_deferred_holding_period"].to_numpy(),
                "nontaxable": pol[
                    "change_ret_plan_nontaxable_holding_period"
                ].to_numpy(),
            },
            "inventories": pol["change_inventories_holding_period"].to_numpy(),
        }

        # Check that sums of "change" parameter values and corresponding base year
        # parameter values specified in environment parameter file fall within permitted
        # ranges.
        base_yr_keys = [
            "cap_gains_short_term_share",
            "cap_gains_at_death_share",
            "cap_gains_short_term_holding_period",
            "cap_gains_long_term_holding_period",
            "cap_gains_at_death_holding_period",
            "ret_plan_deferred_holding_period",
            "ret_plan_nontaxable_holding_period",
            "inventories_holding_period",
        ]

        for key in base_yr_keys:
            permitted_range_str = f"[{self.env.permitted_ranges[key]['min_value']}, "
            f"{self.env.permitted_ranges[key]['max_value']}]"
            change_key = f"change_{key}"
            if not (
                (
                    self.env.permitted_ranges[key]["min_value"]
                    <= (self.env.env[key].values + pol[change_key])
                ).all()
                & (
                    (self.env.env[key].values + pol[change_key])
                    <= self.env.permitted_ranges[key]["max_value"]
                ).all()
            ):
                raise ValueError(
                    f"One of the parameter values of {change_key} is such that the sum of ({key} + "
                    f"{change_key}) is not within the permitted range {permitted_range_str}'"
                )

        # Policy suffixes pointing to depreciation, investment tax credit & tax rate
        # adjustment parameters
        file_policy_suffixes = {
            "recovery_periods": pol["recovery_periods"].to_numpy(),
            "acceleration_rates": pol["acceleration_rates"].to_numpy(),
            "straight_line_flags": pol["straight_line_flags"].to_numpy(),
            "inflation_adjustments": pol["inflation_adjustments"].to_numpy(),
            "sec_179_expens_shares": {
                "c_corp": pol["c_corp_sec_179_expens_shares"].to_numpy(),
                "pass_thru": pol["pass_thru_sec_179_expens_shares"].to_numpy(),
            },
            "other_expens_shares": pol["other_expens_shares"].to_numpy(),
            "itc": {
                "rates": pol["itc_rates"].to_numpy(),
                "nondeprcbl_bases": pol["itc_nondeprcbl_bases"].to_numpy(),
            },
            "tax_rate_adjustments": {
                "sec_199A_adjustments": pol["sec_199A_adjustments"].to_numpy(),
                "c_corp": {
                    "asset_adjustments": pol["c_corp_asset_adjustments"].to_numpy(),
                    "industry_adjustments": pol[
                        "c_corp_industry_adjustments"
                    ].to_numpy(),
                },
                "pass_thru": {
                    "asset_adjustments": pol["pass_thru_asset_adjustments"].to_numpy(),
                    "industry_adjustments": pol[
                        "pass_thru_industry_adjustments"
                    ].to_numpy(),
                },
            },
        }

        # Account category parameters
        self.account_category_shares = {
            "c_corp": {
                "equity": {
                    "taxable": pol[
                        "c_corp_equity_account_category_share_taxable"
                    ].to_numpy(),
                    "deferred": pol[
                        "c_corp_equity_account_category_share_deferred"
                    ].to_numpy(),
                    "nontaxable": pol[
                        "c_corp_equity_account_category_share_nontaxable"
                    ].to_numpy(),
                },
                "debt": {
                    "taxable": pol[
                        "c_corp_debt_account_category_share_taxable"
                    ].to_numpy(),
                    "deferred": pol[
                        "c_corp_debt_account_category_share_deferred"
                    ].to_numpy(),
                    "nontaxable": pol[
                        "c_corp_debt_account_category_share_nontaxable"
                    ].to_numpy(),
                },
            },
            "pass_thru": {
                "equity": {
                    "taxable": pol[
                        "pass_thru_equity_account_category_share_taxable"
                    ].to_numpy(),
                    "deferred": pol[
                        "pass_thru_equity_account_category_share_deferred"
                    ].to_numpy(),
                    "nontaxable": pol[
                        "pass_thru_equity_account_category_share_nontaxable"
                    ].to_numpy(),
                },
                "debt": {
                    "taxable": pol[
                        "pass_thru_debt_account_category_share_taxable"
                    ].to_numpy(),
                    "deferred": pol[
                        "pass_thru_debt_account_category_share_deferred"
                    ].to_numpy(),
                    "nontaxable": pol[
                        "pass_thru_debt_account_category_share_nontaxable"
                    ].to_numpy(),
                },
            },
            "ooh": {
                "equity": {
                    "taxable": pol[
                        "ooh_equity_account_category_share_taxable"
                    ].to_numpy(),
                    "deferred": pol[
                        "ooh_equity_account_category_share_deferred"
                    ].to_numpy(),
                    "nontaxable": pol[
                        "ooh_equity_account_category_share_nontaxable"
                    ].to_numpy(),
                },
                "debt": {
                    "taxable": pol[
                        "ooh_debt_account_category_share_taxable"
                    ].to_numpy(),
                    "deferred": pol[
                        "ooh_debt_account_category_share_deferred"
                    ].to_numpy(),
                    "nontaxable": pol[
                        "ooh_debt_account_category_share_nontaxable"
                    ].to_numpy(),
                },
            },
        }

        # Check that shares add up to 1, within an absolute tolerance of 0.001
        for form in ["c_corp", "pass_thru", "ooh"]:
            for financing in ["equity", "debt"]:
                shares_sum = (
                    self.account_category_shares[form][financing]["taxable"]
                    + self.account_category_shares[form][financing]["deferred"]
                    + self.account_category_shares[form][financing]["nontaxable"]
                )

                np.testing.assert_allclose(shares_sum, 1, atol=0.001)

        # Read in other policy parameter files
        # ------------------------------------------------------------------------------
        # Depreciation parameters
        self.depreciation = {
            "recovery_periods": self._read_depreciation_parameters(
                "recovery_periods_", file_policy_suffixes["recovery_periods"]
            ),
            "acceleration_rates": self._read_depreciation_parameters(
                "acceleration_rates_", file_policy_suffixes["acceleration_rates"]
            ),
            "straight_line_flags": self._read_depreciation_parameters(
                "straight_line_flags_", file_policy_suffixes["straight_line_flags"]
            ),
            "inflation_adjustments": self._read_depreciation_parameters(
                "inflation_adjustments_", file_policy_suffixes["inflation_adjustments"]
            ),
            "c_corp_sec_179_expens_shares": self._read_depreciation_parameters(
                "sec_179_expens_shares_",
                file_policy_suffixes["sec_179_expens_shares"]["c_corp"],
            ),
            "pass_thru_sec_179_expens_shares": self._read_depreciation_parameters(
                "sec_179_expens_shares_",
                file_policy_suffixes["sec_179_expens_shares"]["pass_thru"],
            ),
            "other_expens_shares": self._read_depreciation_parameters(
                "other_expens_shares_", file_policy_suffixes["other_expens_shares"]
            ),
        }

        # Investment Tax Credit (itc) parameters
        self.itc = {
            "rates": self._read_investment_tax_credit_parameters(
                "itc_rates_", file_policy_suffixes["itc"]["rates"]
            ),
            "nondeprcbl_bases": self._read_investment_tax_credit_parameters(
                "itc_nondeprcbl_bases_", file_policy_suffixes["itc"]["nondeprcbl_bases"]
            ),
        }

        # Tax rate adjustment parameters
        self.tax_rate_adjustments = {
            "c_corp": {
                "asset_type": self._read_tax_rate_adjustment_parameters(
                    "asset_adjustments_",
                    file_policy_suffixes["tax_rate_adjustments"]["c_corp"][
                        "asset_adjustments"
                    ],
                ),
                "industry": self._read_tax_rate_adjustment_parameters(
                    "industry_adjustments_",
                    file_policy_suffixes["tax_rate_adjustments"]["c_corp"][
                        "industry_adjustments"
                    ],
                ),
            },
            "pass_thru": {
                "asset_type": self._read_tax_rate_adjustment_parameters(
                    "asset_adjustments_",
                    file_policy_suffixes["tax_rate_adjustments"]["pass_thru"][
                        "asset_adjustments"
                    ],
                ),
                "sec_199A": self._read_tax_rate_adjustment_parameters(
                    "sec_199A_adjustments_",
                    file_policy_suffixes["tax_rate_adjustments"][
                        "sec_199A_adjustments"
                    ],
                ),
                "industry": self._read_tax_rate_adjustment_parameters(
                    "industry_adjustments_",
                    file_policy_suffixes["tax_rate_adjustments"]["pass_thru"][
                        "industry_adjustments"
                    ],
                ),
            },
        }

        # Convert permitted ranges into a dictionary, and then check that all parameter
        # values are valid (that is, within the permitted range)
        # ------------------------------------------------------------------------------
        permitted_ranges = pd.read_csv(
            self.policy_parameters_permitted_ranges_file, index_col="policy_parameter"
        ).to_dict("index")
        self._check_policy_parameter_ranges(pol, permitted_ranges)

        print(
            f"* Policy parameters for {policy_name} with the {perspective} perspective read"
        )

        return None

    def _read_policy_parameters_file(self, filename):
        """Read the policy parameters file, which includes policy parameters that vary
        by year.

        Examples of policy parameters are tax rates on C corps income and shares of
        total interest deductible by pass-throughs.

        Parameters
        ----------
        filename : str
            Name of csv file (with full PATH) to be read.

        Returns
        -------
        policy_params : pd.DataFrame
            DataFrame with all policy parameter values selected for the number of years
            specified by the NUM_YEARS constant.

        """
        df = pd.read_csv(filename, index_col=0)

        if NUM_YEARS > len(df):
            raise ValueError(
                f"NUM_YEARS is greater than the number of rows in {filename}"
            )
        else:
            # Only select policy parameters for the number of years specified in
            # NUM_YEARS
            policy_params = df.iloc[:NUM_YEARS, :]

        return policy_params

    def _read_depreciation_parameters(self, filename, filename_suffix):
        """Read in various policy parameters related to calculations of tax
        depreciation.

        There are 7 files that are read in, each of which are matrices of
        detailed industry by asset type values:
            * recovery_periods
            * acceleration_rates
            * straight_line_flags
            * inflation_adjustments
            * c_corp_sec_179_expens_shares
            * pass_thru_sec_179_expens_shares
            * other_expens_shares

        Parameters
        ----------
        filename : str
            File name.
        filename_suffix : str
            Suffix to file name that indicates the specific policy matrix to read.

        Returns
        -------
        depreciation_parameters : np.ndarray
            Array of policy depreciation parameters by detailed industry, asset type,
            and year.

        """
        # Initialize array
        depreciation_parameters = np.zeros((NUM_DETAILED_INDS, NUM_ASSETS, NUM_YEARS))

        # Fill arrays with relevant depreciation parameters
        for i_year in range(NUM_YEARS):

            data = pd.read_csv(
                self.policy_path
                + "/depreciation_adjustments/"
                + filename
                + filename_suffix[i_year]
                + ".csv"
            )
            data.drop([0], axis=0, inplace=True)
            data.drop(data.iloc[:NUM_DETAILED_INDS, 0:2], axis=1, inplace=True)
            data.reset_index(inplace=True, drop=True)
            depreciation_parameters[
                :NUM_DETAILED_INDS, :NUM_ASSETS, i_year
            ] = data.to_numpy()

        return depreciation_parameters

    def _read_investment_tax_credit_parameters(self, filename, filename_suffix):
        """Read in parameters related to the investment tax credit.

        There are 2 files that are read in, each of which are matrices of
        industry by asset type values:
            * itc_rates
            * itc_nondeprcbl_bases

        Parameters
        ----------
        filename : str
            File name.
        filename_suffix : str
            Suffix to file name that indicates the specific policy matrix to read.

        Returns
        -------
        itc_parameters : np.ndarray
            Array of investment tax credit parameters by industry, assets, and year.

        """
        # Initialize array
        itc_parameters = np.zeros((NUM_INDS, NUM_ASSETS, NUM_YEARS))

        # Fill arrays with relevant investment tax credit parameters
        for i_year in range(NUM_YEARS):

            data = pd.read_csv(
                self.policy_path
                + "/investment_tax_credit_adjustments/"
                + filename
                + filename_suffix[i_year]
                + ".csv"
            )
            data.drop([0], axis=0, inplace=True)
            data.drop(data.iloc[:NUM_INDS, 0:2], axis=1, inplace=True)
            data.reset_index(inplace=True, drop=True)
            itc_parameters[:NUM_INDS, :NUM_ASSETS, i_year] = data.to_numpy()

        return itc_parameters

    def _read_tax_rate_adjustment_parameters(self, filename, filename_suffix):
        """Read in parameters related to tax rate adjustments.

        There are 3 files that are read in, one of which is a matrix of asset type
        values:
            * asset_adjustments
        The other two are matrices of detailed industry values:
            * sec_199A_adjustments
            * industry_adjustments

        All matrices include two columns, one for the eligibility parameters and one for
        the rate parameter.

        Parameters
        ----------
        filename : str
            File name.
        filename_suffix : str
            Suffix to file name that indicates the specific policy matrix to read.

        Returns
        -------
        tax_rate_adjustment_parameters : np.ndarray
            Array of tax rate adjustment parameters.

        """
        # Initialize array
        if filename in ["sec_199A_adjustments_", "industry_adjustments_"]:
            tax_rate_adjustment_parameters = np.zeros(
                (NUM_DETAILED_INDS, NUM_TAX_RATE_ADJUSTMENTS_COMPONENTS, NUM_YEARS)
            )
        elif filename == "asset_adjustments_":
            tax_rate_adjustment_parameters = np.zeros(
                (NUM_ASSETS, NUM_TAX_RATE_ADJUSTMENTS_COMPONENTS, NUM_YEARS)
            )
        else:
            raise ValueError(
                'tax rate adjustment file name must be equal to \
                             "sec_199A_adjustments_", "industry_adjustments_" or \
                             "asset_adjustments_"'
            )

        # Fill array with relevant tax rate adjustment parameters
        for i_year in range(NUM_YEARS):

            # Read input files
            data = pd.read_csv(
                self.policy_path
                + "/tax_rate_adjustments/"
                + filename
                + filename_suffix[i_year]
                + ".csv"
            )

            data.drop([0], axis=0, inplace=True)
            data.drop(data.iloc[:, 0:1], axis=1, inplace=True)
            data.reset_index(inplace=True, drop=True)

            tax_rate_adjustment_parameters[
                :NUM_DETAILED_INDS, :NUM_TAX_RATE_ADJUSTMENTS_COMPONENTS, i_year
            ] = data.to_numpy()

        return tax_rate_adjustment_parameters

    def _check_policy_parameter_ranges(self, policy_parameters, permitted_ranges):
        """Check that all policy parameters are within permitted ranges.

        Parameters
        ----------
        policy_parameters : pd.DataFrame
            DataFrame containing all the policy parameters that are dimensioned by year.
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
            "recovery_periods": self.depreciation["recovery_periods"],
            "acceleration_rates": self.depreciation["acceleration_rates"],
            "straight_line_flags": self.depreciation["straight_line_flags"],
            "inflation_adjustments": self.depreciation["inflation_adjustments"],
            "c_corp_sec_179_expens_shares": self.depreciation[
                "c_corp_sec_179_expens_shares"
            ],
            "pass_thru_sec_179_expens_shares": self.depreciation[
                "pass_thru_sec_179_expens_shares"
            ],
            "other_expens_shares": self.depreciation["other_expens_shares"],
            "itc_rates": self.itc["rates"],
            "itc_nondeprcbl_bases": self.itc["nondeprcbl_bases"],
            "sec_199A_adjustments": self.tax_rate_adjustments["pass_thru"]["sec_199A"],
            "c_corp_industry_adjustments": self.tax_rate_adjustments["c_corp"][
                "industry"
            ],
            "pass_thru_industry_adjustments": self.tax_rate_adjustments["pass_thru"][
                "industry"
            ],
            "c_corp_asset_adjustments": self.tax_rate_adjustments["c_corp"][
                "asset_type"
            ],
            "pass_thru_asset_adjustments": self.tax_rate_adjustments["pass_thru"][
                "asset_type"
            ],
        }

        for key in permitted_ranges:
            permitted_range_str = f"[{permitted_ranges[key]['min_value']}, {permitted_ranges[key]['max_value']}]"

            # First check parameter values already stored in numpy arrays, which are
            # populated based on parameters containing strings that reference file name
            # suffixes in the policy_parameters_* files
            if key in suffix_dict.keys():
                if key == "straight_line_flags":
                    if not (
                        (
                            (suffix_dict[key] == permitted_ranges[key]["min_value"])
                            | (suffix_dict[key] == permitted_ranges[key]["max_value"])
                            | (suffix_dict[key] == 0.0)
                        ).all()
                    ):
                        raise ValueError(
                            f"One of the parameter values in {key} is not within the set of permitted "
                            f"values [{permitted_ranges[key]['min_value']},0,"
                            f"{permitted_ranges[key]['max_value']}]"
                        )
                elif key == "recovery_periods":
                    if not (
                        (permitted_ranges[key]["min_value"] <= suffix_dict[key]).all()
                        & (
                            (suffix_dict[key] <= permitted_ranges[key]["max_value"])
                            | (suffix_dict[key] == 100000.0)
                        ).all()
                    ):
                        raise ValueError(
                            f"One of the parameter values in {key} is not within the permitted "
                            f"range {permitted_range_str}"
                        )
                else:
                    if not (
                        (permitted_ranges[key]["min_value"] <= suffix_dict[key]).all()
                        & (suffix_dict[key] <= permitted_ranges[key]["max_value"]).all()
                    ):
                        raise ValueError(
                            f"One of the parameter values in {key} is not within the permitted "
                            f"range {permitted_range_str}"
                        )

            # Otherwise, skip parameter values that are strings containing names of file
            # suffixes
            elif key not in suffix_dict.keys():
                for val in policy_parameters[key].values:
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
