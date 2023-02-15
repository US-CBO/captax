from collections import OrderedDict
from itertools import permutations
import numpy as np
import pandas as pd
from captax.constants import *


class Dispersion:
    """Define the object used to calculate and store dispersion statistics.

    Attributes
    ----------
    agg : Aggregator object
        Includes aggregate weights used in calculations.
    output : OutputBuilder object
        Includes total tax wedges used in calculations.
    total_tax_wedge: dict
        Dispersion statistics when focusing on total tax wedges.

    """

    def __init__(self, agg, output):
        """Initialize Dispersion object.

        Parameters
        ----------
        agg : Aggregator object
            Includes aggregate weights used in calculations.
        output : OutputBuilder object
            Includes total tax wedges used in calculations.

        Returns
        -------
        None
            Method initializes attributes of Dispersion object.

        """
        self.agg = agg
        self.output = output
        self.total_tax_wedge = None

        return None

    def calc_all(self):
        """Calculate all the dispersion statistics.

        Currently, dispersion statistics are calculated for just a single variable:
        `total_tax_wedge`. The dispersion statistics are calculated, primarily, across
        asset types within a select set of asset aggregations.

        This method calculates the average differences in total tax wedges
        (using self._calc_wgtd_avg_abs_diff() method) along four dimensions:
            * industries,
            * assets,
            * legal forms, and
            * financing source.

        For the first two dimensions, a weighted average of absolute differences is
        calculated. For the second two (because there are only two elements in
        each: C corps vs. Pass-through and Equity vs. Debt), simple differences are
        calculated.

        A Dispersion object attribute is created for disp.total_tax_wedge, which is a
        dictionary with one key:value pairs. The key is 'diffs', and the value associated
        with the key is a pandas DataFrame.

        Parameters
        ----------
        None
            Parameters are specified in the methods nested within this method.

        Returns
        -------
        None
            This method nests other methods.

        """
        print("Begin calculating dispersion statistics")

        values = self.output.total_tax_wedges
        weights = self.agg.weights

        self.total_tax_wedge = {}

        # Weighted average of absolute differences calculations
        # ------------------------------------------------------------------------------
        # Initialize list where weighted average of absolute differences are stored
        dfs = []

        # Perform calculation for specified asset aggregates
        asset_aggs_names = [
            "All equipment, structures, IPP, and inventories",
            "All equipment, structures, IPP, inventories, and land",
            "Nonresidential equipment",
            "Nonresidential structures",
            "Residential property",
            "IPP",
            "R&D and own-account software",
            "Other intellectual property products",
        ]

        asset_aggs = [
            ALL_EQUIP_STRUCT_IPP_INVENT,
            ALL_ASSETS,
            ALL_NONRES_EQUIPMENT,
            ALL_NONRES_STRUCTURES_PLUS_MINERAL,
            ALL_RESIDENTIAL,
            ALL_IPP_MINUS_MINERAL,
            ALL_RESEARCH,
            ALL_NON_RESEARCH_IPP_MINUS_MINERAL,
        ]

        names_aggs = zip(asset_aggs_names, asset_aggs)

        for asset_agg_name, asset_agg in names_aggs:
            wgtd_avg_abs_diff_asset_agg = self._calc_wgtd_avg_abs_diff(
                values, weights, "assets", asset_agg_name, asset_agg
            )

            dfs.append(wgtd_avg_abs_diff_asset_agg)

        # Perform calculation for industry aggregations
        dim_names = ["industries (excluding land)", "industries (including land)"]

        for dim_name in dim_names:
            wgtd_avg_abs_diff_ind_agg = self._calc_wgtd_avg_abs_diff(
                values, weights, dim_name, "All Industries", ALL_BIZ_INDS
            )
            dfs.append(wgtd_avg_abs_diff_ind_agg)

        # Store values
        self.total_tax_wedge["wgtd_avg_abs_diffs"] = pd.concat(dfs, ignore_index=True)

        print("* Weighted average of absolute differences calculated")

        print("Finished calculating dispersion statistics\n")

        return None

    def _calc_wgtd_avg_abs_diff(self, values, weights, dim, agg_label, agg_components):
        """Calculate the weighted average of absolute differences.

        The weighted average of absolute differences are calculated by dimension
        ('assets', 'industries (excluding land)', or 'industries (including land)'),
        a select number of aggregations within each dimension, three legal forms
        ('c_corp', 'pass-through', or 'biz'), and by year.

        This method calls other five methods:
            * self._select_values_weights() : Selects the values and weights to use.
            * self._calc_total_wgts_sq() : Calculates the sum of the weights, squared.
            * self._calc_weight_adj_factor() : Calculates a weight adjustment factor used
                in the weighted average of absolute differences calculations.
            * self._get_permutations() : Gets all the possible permutations of pairs from
                a one-dimensional array.
            * self._adjust_weights() : Adjusts the weights used in the weighted average of
                absolute differences calculation.

        Parameters
        ----------
        values : np.ndarray
            The values for which to calculate the weighted average of absolute differences.
        weights : np.ndarray
            The weights to use in the calculations.
        dim : str
            Dimension of the multi-dimensional arrays (values and weights) for which to
            perform the calculation of the weighted average of absolute differences.
            Can be either 'assets' 'industries (excluding land)', or 'industries (including land)'.
        agg_label : str
            Label for aggregate considered.
        agg_components : list
            List of the elements over which to calculate the weighted average of absolute
            differences.

        Returns
        -------
        df : pd.DataFrame
            The DataFrame has 4 categorical variables:
                * dimension
                * aggregation
                * legal_form
                * year
            and 1 metric variable: wgtd_avg_abs_diff

        """
        # Initialize list where weighted average of absolute differences is stored
        data = []

        # Perform calculation for specified aggregate
        agg_dim = [dim]
        agg_label = [agg_label]
        agg_components = [agg_components]
        agg_dim_label_components = zip(agg_dim, agg_label, agg_components)

        for dim, label, components in agg_dim_label_components:
            for legal_form in ["c_corp", "pass_thru", "biz"]:
                for i_year in range(NUM_YEARS):
                    # _vals and _wgts are returned as flattened, 1-D arrays
                    vals, wgts = self._select_values_weights(
                        values, weights, dim, agg_components, legal_form, i_year
                    )

                    total_wgts_sq = self._calc_total_wgts_sq(wgts)
                    wgt_adj_factor = self._calc_weight_adj_factor(wgts, total_wgts_sq)

                    val_perms = self._get_permutations(vals)
                    wgt_perms = self._get_permutations(wgts)

                    adjusted_wgts = self._adjust_weights(
                        wgt_perms, wgt_adj_factor, total_wgts_sq
                    )

                    wgtd_avg_abs_diff = 0
                    for val_pair, wgt in zip(val_perms, adjusted_wgts):
                        abs_diff = abs(val_pair[0] - val_pair[1])
                        wgtd_avg_abs_diff += abs_diff * wgt

                    data.append(
                        [dim, label, legal_form, START_YEAR + i_year, wgtd_avg_abs_diff]
                    )

        # Put the data list into a DataFrame
        columns = [
            "dimension",
            "aggregation",
            "legal_form",
            "year",
            "wgtd_avg_abs_diff",
        ]

        df = pd.DataFrame(data, columns=columns)

        return df

    def _select_values_weights(
        self, values, weights, dim, agg_components, legal_form, i_year
    ):
        """Select the values and weights to use.

        Parameters
        ----------
        values : np.ndarray
            Values to use in calculation of weighted average of absolute differences.
        weights : np.ndarray
            Weights to use in calculation of weighted average of absolute differences.
        dim : str
            Dimension of the multi-dimensional arrays (values and weights) for which to
            perform the calculation of the weighted average of absolute differences.
            Can be either 'assets', 'industries (excluding land)' or 'industries (including land)'.
        agg_components : list
            List of the elements over which to calculate the weighted average of absolute
            differences.
        legal_form : str
            Legal form to use for the calculation of the weighted average of absolute
            differences. Can be 'c_corp', 'pass_thru', or 'biz'.
        i_year : integer
            Year index for which to calculate the weighted average of absolute differences.

        Returns
        -------
        values, weights : np.ndarray
            Two flattened arrays, based on the parameter specifications.

        """
        if dim == "assets":
            values = values[
                NUM_INDS,
                agg_components,
                LEGAL_FORMS[legal_form],
                FINANCING_SOURCES["typical (biz)"],
                i_year,
            ].flatten()

            weights = weights[
                NUM_INDS,
                agg_components,
                LEGAL_FORMS[legal_form],
                FINANCING_SOURCES["typical (biz)"],
                i_year,
            ].flatten()

        elif dim == "industries (excluding land)":
            values = values[
                agg_components,
                ASSET_TYPE_INDEX["All equipment, structures, IPP, and inventories"],
                LEGAL_FORMS[legal_form],
                FINANCING_SOURCES["typical (biz)"],
                i_year,
            ].flatten()

            weights = weights[
                agg_components,
                ASSET_TYPE_INDEX["All equipment, structures, IPP, and inventories"],
                LEGAL_FORMS[legal_form],
                FINANCING_SOURCES["typical (biz)"],
                i_year,
            ].flatten()

        elif dim == "industries (including land)":
            values = values[
                agg_components,
                ASSET_TYPE_INDEX[
                    "All equipment, structures, IPP, inventories, and land"
                ],
                LEGAL_FORMS[legal_form],
                FINANCING_SOURCES["typical (biz)"],
                i_year,
            ].flatten()

            weights = weights[
                agg_components,
                ASSET_TYPE_INDEX[
                    "All equipment, structures, IPP, inventories, and land"
                ],
                LEGAL_FORMS[legal_form],
                FINANCING_SOURCES["typical (biz)"],
                i_year,
            ].flatten()
        else:
            raise ValueError(
                f'Dimension specified must be "assets", "industries (excluding land)" '
                f'or "industries (including land)"'
            )

        return values, weights

    def _calc_total_wgts_sq(self, weights):
        """Calculate the sum of the weights, squared.

        Because the weighting method used when calculating the weighted average of
        absolute differences is multiplicative, we need the square of the total weights
        array to normalize the weights to be between 0 and 1.

        Parameters
        ----------
        weights : np.ndarray
            Flattened (one-dimensional) array of weights.

        Returns
        -------
        total_wgts_sq : float
            Sum of weights, squared.

        """
        total_wgts_sq = sum(weights) ** 2

        return total_wgts_sq

    def _calc_weight_adj_factor(self, weights, total_wgts_sq):
        """Calculate a weight adjustment factor used in the weighted average of absolute
        differences calculations.

        The adjustment factor is used to scale up the weights that are used in the
        calculation of the weighted average of absolute difference calculations. The
        weights need to be scaled up because the diagonal pairs of an n x n matrix of
        the weights are not being used in the calculation.

        The value of the weight adjustment factor will be < 1.0.

        Parameters
        ----------
        weights : np.ndarray
            Array of weights to use in the weighted average of absolute difference
            calculations.
        total_wgts_sq : float
            The square of the sum of all the weight values. Used as the denominator to
            normalize the adjustment factor.

        Returns
        -------
        wgt_adj_factor : float
            Weight adjustment factor.

        """
        sum_wgts_sq = sum(weights ** 2)
        wgt_adj_factor = 1.0 - (sum_wgts_sq / total_wgts_sq)

        return wgt_adj_factor

    def _get_permutations(self, array):
        """Get all the possible permutations of pairs from a one-dimensional array.

        Uses the itertool.permutations() method.
        Example: permutations('ABC', 2) -> AB, AC, BA, BC, CA, CB
        The 2 parameter indicates that we are producing pairs.
        This is essentially all the non-diagonal possible pairs, that is: AA, BB, and CC
        are omitted.

        Parameters
        ----------
        array : np.ndarray
            A one-dimensional array

        Returns
        -------
        perms : itertools object
            All possible permutations of pairs from one-dimensional array.

        """
        perms = permutations(array, 2)

        return perms

    def _adjust_weights(self, weight_perms, weight_adj_factor, total_wgts_sq):
        """Adjust the weights used in the weighted average of absolute differences
        calculation.

        A multiplicative weighting scheme is used when calculating the weighted average
        of the absolute differences between any two values (Vi, and Vj).

        The weight given to each absolute difference between Vi and Vj is equal to
        Wi * Wj, scaled by the total_wgts_sq and then divided by the weight_adj_factor.
        The weight_adj_factor is < 1.0, so dividing will scale the weights up.

        Parameters
        ----------
        weight_perms : itertools object
            All the possible weight pair permutations.
        weight_adj_factor : float
            Scaling factor to account for the diagonal pairs not being included.
        total_wgts_sq : float
            Sum of the weight array, squared.

        Returns
        -------
        adjusted_wgt_perms : list
            A list of weights used to weight the abolute differences by when calculating
            the weighted average of absolute differences.

        Note
        ----
        The resulting list of adjusted weights should sum to 1.

        """
        adjusted_wgt_perms = []

        for wgt_pair in weight_perms:
            wgt = ((wgt_pair[0] * wgt_pair[1]) / total_wgts_sq) / weight_adj_factor
            adjusted_wgt_perms.append(wgt)

        return adjusted_wgt_perms
