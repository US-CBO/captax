import copy
import numpy as np
from captax.constants import *


np.seterr(divide="ignore", invalid="ignore")


class Aggregator:
    """Define the object used to aggregate variables created by a Calculator object.

    Attributes
    ----------
    env : Environment object
        Economic environment parameters.
    wgt : Weights object
        Weights used in calculations.
    pol : Policy object
        Policy parameters.
    calc : Calculator object
        Non-aggregates values used in aggregation.
    weights : np.ndarray
        Aggregate weights.
    req_before_tax_returns : np.ndarray
        Aggregate required before-tax rates of return.
    req_after_tax_returns_savers : np.ndarray
        Aggregate required after-tax rates of return to savers.
    req_after_tax_returns_investors : np.ndarray
        Aggregate required after-tax rates of return to investors.

    """

    def __init__(self, env, wgt, pol, calc):
        """Initialize Aggregator object.

        Parameters
        ----------
        env : Environment object
            Economic environment parameters.
        wgt : Weights object
            Weights used in calculations.
        pol : Policy object
            Policy parameters.
        calc : Calculator object
            Non-aggregates values used in aggregation.

        Returns
        -------
        None
            Method initializes attributes of Aggregator object.

        """
        self.env = env
        self.wgt = wgt
        self.pol = pol
        self.calc = calc
        self.weights = None
        self.req_before_tax_returns = None
        self.req_after_tax_returns_savers = None
        self.req_after_tax_returns_investors = None

        return None

    def aggregate_all(self):
        """Aggregate weights, before-tax rates of return, after-tax rates of return
        required by savers and after-tax rates of return required by investors.

        This method calls self._aggregate_variable(), which is used to aggregate
        weights, before-tax rates of return and after-tax rates of return required by
        savers and by investors.

        Parameters
        ----------
        None
            Parameters are specified in the methods nested within this method.

        Returns
        -------
        None
            This method nests other methods.

        """
        print("Begin aggregating results")

        self.weights = self._aggregate_variable(self.wgt.weights, ASSET_AGGS)

        self.req_before_tax_returns = self._aggregate_variable(
            self.calc.req_before_tax_returns, ASSET_AGGS, self.weights
        )

        self.req_after_tax_returns_savers = self._aggregate_variable(
            self.calc.req_after_tax_returns_savers[
                :NUM_INDS,
                :NUM_ASSETS,
                :NUM_FOR_PROFIT_LEGAL_FORMS,
                :NUM_EQUITY_DEBT,
                ACCOUNT_CATEGORIES["typical"],
                :NUM_YEARS,
            ],
            ASSET_AGGS,
            self.weights,
        )

        self.req_after_tax_returns_investors = self._aggregate_variable(
            self.calc.req_after_tax_returns_investors, ASSET_AGGS, self.weights
        )

        print("Finished aggregating results\n")

        return None

    def _create_empty_array(self, nans_or_ones):
        """Initialize array with NaNs or ones for storing values.

        Parameters
        ----------
        nans_or_ones : str
            Whether to create an empty array of "NaNs" or "ones".

        Returns
        -------
        ndarray : np.ndarray
            Array of NaNs or ones, with dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        """
        if nans_or_ones == "nans":
            ndarray = np.zeros(
                (
                    LEN_INDS,
                    LEN_ASSETS,
                    LEN_LEGAL_FORMS,
                    LEN_FINANCING_SOURCES,
                    NUM_YEARS,
                )
            )
            ndarray[:] = np.nan

        elif nans_or_ones == "ones":
            ndarray = np.ones(
                (
                    LEN_INDS,
                    LEN_ASSETS,
                    LEN_LEGAL_FORMS,
                    LEN_FINANCING_SOURCES,
                    NUM_YEARS,
                )
            )

        else:
            raise ValueError("nans_or_ones must be either 'nans' or 'ones'.")

        return ndarray

    def _aggregate_variable(self, in_var, asset_aggs, weights=None):
        """Aggregate variable using weights by industry, asset type, legal form,
        and financing source. If weights are not specified, an empty array of
        ones is created and used as weights.

        1) If weights parameter is not specified:
        Method calculates aggregates using the comprehensive perspective. Two
        other methods are called to perform that calculation:
            * self._calc_values_by_asset_type_comprehensive()
            * self._calc_values_by_asset_agg_comprehensive()
        The first method calculates aggregates by asset type, while the second
        method calculates aggregates by asset group (e.g. non-residential equipment)
        for the asset aggregates specified in the asset_aggs parameter.

        2) If weights parameter is specified:
        Method calculates aggregates for the in_var variable.
        When using the comprehensive perspective, those two other methods are called:
            * self._calc_values_by_asset_type_comprehensive()
            * self._calc_values_by_asset_agg_comprehensive()
        When using the uniformity perspective, those two other methods are called:
            * self._calc_values_by_asset_type_uniformity()
            * self._calc_values_by_asset_agg_uniformity()
        In each case the first method calculates aggregates by asset type, while
        the second method calculates aggregates by asset group (e.g. non-residential
        equipment) for the asset aggregates specified in the asset_aggs parameter.

        Parameters
        ----------
        inv_var : np.ndarray
            Variable for which aggregate weighted averages will be calculated.
        asset_aggs : tuple
            Asset aggregates considered in aggregation.
        weights : np.ndarray
            Weights used to calculate weighted averages when aggregating.

        Returns
        -------
        aggregate_variable : np.ndarray
            Array with values of in_var in the non-aggregate dimensions and
            aggregated values filled at the end of each dimension, with
            dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        """
        if weights is None:
            # Expand weight variable and create array of 1s for weight aggregation
            wgts = (np.tile(in_var, (NUM_YEARS, 1, 1, 1, 1))).transpose((1, 2, 3, 4, 0))
            ones = self._create_empty_array("ones")

            # Aggregate values
            values_by_asset_type = self._calc_values_by_asset_type_comprehensive(
                wgts, ones
            )
            values_by_asset_agg = self._calc_values_by_asset_agg_comprehensive(
                wgts, ones, asset_aggs
            )

        else:
            # Copy array values
            var = copy.deepcopy(in_var)

            # Aggregate values
            if self.pol.perspective == "comprehensive":
                values_by_asset_type = self._calc_values_by_asset_type_comprehensive(
                    var, weights
                )
                values_by_asset_agg = self._calc_values_by_asset_agg_comprehensive(
                    var, weights, asset_aggs
                )

            elif self.pol.perspective == "uniformity":
                values_by_asset_type = self._calc_values_by_asset_type_uniformity(
                    var, weights
                )
                values_by_asset_agg = self._calc_values_by_asset_agg_uniformity(
                    var, weights, asset_aggs
                )

        # Initialize array, then fill with aggregate values
        # ------------------------------------------------------------------------------
        aggregate_variable = self._create_empty_array("nans")

        assets = [ALL_ASSETS, ALL_ASSET_AGGS]
        values = [values_by_asset_type, values_by_asset_agg]
        assets_values = zip(assets, values)

        for assets, values in assets_values:
            slice = np.ix_(
                ALL_INDS_PLUS_AGG,
                assets,
                ALL_LEGAL_FORMS,
                ALL_FINANCING_SOURCES,
                ALL_YEARS,
            )

            aggregate_variable[slice] = values[slice]

        return aggregate_variable

    def _calc_values_by_asset_type_comprehensive(self, in_var, weights):
        """Calculate values by asset type when using the comprehensive method
        and applying weights that vary by industry, asset type, legal form, and
        source of financing.

        Parameters
        ----------
        inv_var : np.ndarray
            Variable for which aggregate weighted averages will be calculated.
        weights : np.ndarray
            Weights used to calculate weighted averages when aggregating.

        Returns
        -------
        out_array : np.ndarray
            Array filled with values of in_var in the non-aggregate dimensions
            and aggregated values at the end of all dimensions other than
            the asset dimension, with dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        """
        in_var = copy.deepcopy(in_var)

        # Initialize array and store non-aggregate values
        out_array = self._create_empty_array("nans")
        out_array[
            :NUM_INDS,
            :NUM_ASSETS,
            :NUM_FOR_PROFIT_LEGAL_FORMS,
            :NUM_EQUITY_DEBT,
            :NUM_YEARS,
        ] = in_var[
            :NUM_INDS,
            :NUM_ASSETS,
            :NUM_FOR_PROFIT_LEGAL_FORMS,
            :NUM_EQUITY_DEBT,
            :NUM_YEARS,
        ]

        equity_and_debt = slice(
            FINANCING_SOURCES["typical_equity"], FINANCING_SOURCES["debt"] + 1
        )

        # Industry aggregates, by asset type, legal form, financing source and year
        # ------------------------------------------------------------------------------
        out_array[
            NUM_INDS,
            :NUM_ASSETS,
            :NUM_FOR_PROFIT_LEGAL_FORMS,
            :NUM_EQUITY_DEBT,
            :NUM_YEARS,
        ] = (
            (
                in_var[
                    :NUM_INDS,
                    :NUM_ASSETS,
                    :NUM_FOR_PROFIT_LEGAL_FORMS,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]
                * weights[
                    :NUM_INDS,
                    :NUM_ASSETS,
                    :NUM_FOR_PROFIT_LEGAL_FORMS,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]
            ).sum(axis=(0))
            / weights[
                NUM_INDS,
                :NUM_ASSETS,
                :NUM_FOR_PROFIT_LEGAL_FORMS,
                :NUM_EQUITY_DEBT,
                :NUM_YEARS,
            ]
        )

        # Legal form and financing source aggregates...
        # ------------------------------------------------------------------------------
        form_aggregates = [LEGAL_FORMS["biz"], LEGAL_FORMS["biz+ooh"]]
        form_components = [slice(0, NUM_BIZ), slice(0, NUM_FOR_PROFIT_LEGAL_FORMS)]
        financing_aggregates = [
            FINANCING_SOURCES["typical (biz)"],
            FINANCING_SOURCES["typical (biz+ooh)"],
        ]
        aggregates_components_financing = zip(
            form_aggregates, form_components, financing_aggregates
        )

        for form_agg, form_comps, financing_agg in aggregates_components_financing:

            # Legal form aggregates...
            # ...by industry, asset type, financing source and year
            out_array[
                :NUM_INDS, :NUM_ASSETS, form_agg, :NUM_EQUITY_DEBT, :NUM_YEARS
            ] = (
                (
                    in_var[
                        :NUM_INDS,
                        :NUM_ASSETS,
                        form_comps,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                    * weights[
                        :NUM_INDS,
                        :NUM_ASSETS,
                        form_comps,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                ).sum(axis=(2))
                / weights[
                    :NUM_INDS, :NUM_ASSETS, form_agg, :NUM_EQUITY_DEBT, :NUM_YEARS
                ]
            )

            # ...by asset type, financing source, and year
            out_array[
                NUM_INDS, :NUM_ASSETS, form_agg, :NUM_EQUITY_DEBT, :NUM_YEARS
            ] = (
                (
                    in_var[
                        :NUM_INDS,
                        :NUM_ASSETS,
                        form_comps,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                    * weights[
                        :NUM_INDS,
                        :NUM_ASSETS,
                        form_comps,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                ).sum(axis=(0, 2))
                / weights[
                    NUM_INDS, :NUM_ASSETS, form_agg, :NUM_EQUITY_DEBT, :NUM_YEARS
                ]
            )

            # Financing source aggregates...
            # ...by industry, asset type, legal form and year
            out_array[:NUM_INDS, :NUM_ASSETS, form_comps, financing_agg, :NUM_YEARS] = (
                (
                    in_var[
                        :NUM_INDS, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS
                    ]
                    * weights[
                        :NUM_INDS, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS
                    ]
                ).sum(axis=(3))
                / weights[:NUM_INDS, :NUM_ASSETS, form_comps, financing_agg, :NUM_YEARS]
            )

            # ...by asset type, legal form and year
            out_array[NUM_INDS, :NUM_ASSETS, form_comps, financing_agg, :NUM_YEARS] = (
                (
                    in_var[
                        :NUM_INDS, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS
                    ]
                    * weights[
                        :NUM_INDS, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS
                    ]
                ).sum(axis=(0, 3))
                / weights[NUM_INDS, :NUM_ASSETS, form_comps, financing_agg, :NUM_YEARS]
            )

            # Legal form and financing aggregates...
            # ...by industry, asset type, and year
            out_array[:NUM_INDS, :NUM_ASSETS, form_agg, financing_agg, :NUM_YEARS] = (
                (
                    in_var[
                        :NUM_INDS, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS
                    ]
                    * weights[
                        :NUM_INDS, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS
                    ]
                ).sum(axis=(2, 3))
                / weights[:NUM_INDS, :NUM_ASSETS, form_agg, financing_agg, :NUM_YEARS]
            )

            # ...by asset type and year
            out_array[NUM_INDS, :NUM_ASSETS, form_agg, financing_agg, :NUM_YEARS] = (
                (
                    in_var[
                        :NUM_INDS, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS
                    ]
                    * weights[
                        :NUM_INDS, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS
                    ]
                ).sum(axis=(0, 2, 3))
                / weights[NUM_INDS, :NUM_ASSETS, form_agg, financing_agg, :NUM_YEARS]
            )

        return out_array

    def _calc_values_by_asset_agg_comprehensive(self, in_var, weights, asset_aggs):
        """Calculate values by asset aggregate when using the comprehensive method
        and applying weights by industry, asset type, legal form, and financing source.

        Parameters
        ----------
        in_var : np.ndarray
            Variable for which aggregate weighted averages will be calculated.
        weights : np.ndarray
            Weights used to calculate weighted averages when aggregating.
        asset_aggs : tuple
            Asset aggregates considered.

        Returns
        -------
        out_array : np.ndarray
            Array filled with values of in_var in the non-aggregate dimensions
            and aggregated values at the end of the asset dimension, with dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        """
        equity_and_debt = slice(
            FINANCING_SOURCES["typical_equity"], FINANCING_SOURCES["debt"] + 1
        )

        # Initialize array and output position
        out_array = self._create_empty_array("nans")
        output_position = 0

        # Fill aggregates
        # ------------------------------------------------------------------------------
        for asset_agg_range in asset_aggs:

            # Asset aggregates, by industry, legal form, financing source and year
            out_array[
                :NUM_INDS,
                NUM_ASSETS + output_position,
                :NUM_FOR_PROFIT_LEGAL_FORMS,
                :NUM_EQUITY_DEBT,
                :NUM_YEARS,
            ] = (
                (
                    in_var[
                        :NUM_INDS,
                        asset_agg_range,
                        :NUM_FOR_PROFIT_LEGAL_FORMS,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                    * weights[
                        :NUM_INDS,
                        asset_agg_range,
                        :NUM_FOR_PROFIT_LEGAL_FORMS,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                ).sum(axis=(1))
                / weights[
                    :NUM_INDS,
                    NUM_ASSETS + output_position,
                    :NUM_FOR_PROFIT_LEGAL_FORMS,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]
            )

            # Industry and asset aggregates, by legal form, financing source and year
            out_array[
                NUM_INDS,
                NUM_ASSETS + output_position,
                :NUM_FOR_PROFIT_LEGAL_FORMS,
                :NUM_EQUITY_DEBT,
                :NUM_YEARS,
            ] = (
                (
                    in_var[
                        :NUM_INDS,
                        asset_agg_range,
                        :NUM_FOR_PROFIT_LEGAL_FORMS,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                    * weights[
                        :NUM_INDS,
                        asset_agg_range,
                        :NUM_FOR_PROFIT_LEGAL_FORMS,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                ).sum(axis=(0, 1))
                / weights[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    :NUM_FOR_PROFIT_LEGAL_FORMS,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]
            )

            # Asset, legal form and financing aggregates...
            form_aggregates = [LEGAL_FORMS["biz"], LEGAL_FORMS["biz+ooh"]]
            form_components = [slice(0, NUM_BIZ), slice(0, NUM_FOR_PROFIT_LEGAL_FORMS)]
            financing_aggregates = [
                FINANCING_SOURCES["typical (biz)"],
                FINANCING_SOURCES["typical (biz+ooh)"],
            ]
            aggregates_components_financing = zip(
                form_aggregates, form_components, financing_aggregates
            )

            for form_agg, form_comps, financing_agg in aggregates_components_financing:

                # Asset and legal form aggregates...
                # ...by industry, financing source and year
                out_array[
                    :NUM_INDS,
                    NUM_ASSETS + output_position,
                    form_agg,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ] = (
                    (
                        in_var[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            :NUM_EQUITY_DEBT,
                            :NUM_YEARS,
                        ]
                        * weights[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            :NUM_EQUITY_DEBT,
                            :NUM_YEARS,
                        ]
                    ).sum(axis=(1, 2))
                    / weights[
                        :NUM_INDS,
                        NUM_ASSETS + output_position,
                        form_agg,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                )

                # ...by financing source and year
                out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    form_agg,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ] = (
                    (
                        in_var[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            :NUM_EQUITY_DEBT,
                            :NUM_YEARS,
                        ]
                        * weights[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            :NUM_EQUITY_DEBT,
                            :NUM_YEARS,
                        ]
                    ).sum(axis=(0, 1, 2))
                    / weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        form_agg,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                )

                # Asset and financing source aggregates...
                # ...by industry, legal form and year
                out_array[
                    :NUM_INDS,
                    NUM_ASSETS + output_position,
                    form_comps,
                    financing_agg,
                    :NUM_YEARS,
                ] = (
                    (
                        in_var[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                        * weights[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                    ).sum(axis=(1, 3))
                    / weights[
                        :NUM_INDS,
                        NUM_ASSETS + output_position,
                        form_comps,
                        financing_agg,
                        :NUM_YEARS,
                    ]
                )

                # ...by legal form and year
                out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    form_comps,
                    financing_agg,
                    :NUM_YEARS,
                ] = (
                    (
                        in_var[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                        * weights[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                    ).sum(axis=(0, 1, 3))
                    / weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        form_comps,
                        financing_agg,
                        :NUM_YEARS,
                    ]
                )

                # Asset, legal form and financing source aggregates...
                # ...by industry and year
                out_array[
                    :NUM_INDS,
                    NUM_ASSETS + output_position,
                    form_agg,
                    financing_agg,
                    :NUM_YEARS,
                ] = (
                    (
                        in_var[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                        * weights[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                    ).sum(axis=(1, 2, 3))
                    / weights[
                        :NUM_INDS,
                        NUM_ASSETS + output_position,
                        form_agg,
                        financing_agg,
                        :NUM_YEARS,
                    ]
                )

                # ...by year
                out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    form_agg,
                    financing_agg,
                    :NUM_YEARS,
                ] = (
                    (
                        in_var[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                        * weights[
                            :NUM_INDS,
                            asset_agg_range,
                            form_comps,
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                    ).sum(axis=(0, 1, 2, 3))
                    / weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        form_agg,
                        financing_agg,
                        :NUM_YEARS,
                    ]
                )

            # Reset output position
            output_position = output_position + 1

        return out_array

    def _calc_values_by_asset_type_uniformity(self, in_var, weights):
        """Calculate values by asset type when using the tax uniformity method
        and applying aggregate weights that vary by industry, asset type, legal
        form, and financing source.

        Parameters
        ----------
        in_var : np.ndarray
            Variable for which aggregate weighted averages will be calculated.
        weights : np.ndarray
            Weights used to calculate weighted averages when aggregating.

        Returns
        -------
        out_array : np.ndarray
            Array filled with values of in_var in the non-aggregate dimensions
            and aggregated values at the end of all dimensions other than
            the asset dimension, with dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        """
        # Initialize array, then fill values with non-aggregates
        out_array = self._create_empty_array("nans")
        out_array[
            :NUM_INDS,
            :NUM_ASSETS,
            :NUM_FOR_PROFIT_LEGAL_FORMS,
            :NUM_EQUITY_DEBT,
            :NUM_YEARS,
        ] = in_var[
            :NUM_INDS,
            :NUM_ASSETS,
            :NUM_FOR_PROFIT_LEGAL_FORMS,
            :NUM_EQUITY_DEBT,
            :NUM_YEARS,
        ]

        asset_agg_name = "All equipment, structures, IPP, inventories, and land"

        equity_and_debt = slice(
            FINANCING_SOURCES["typical_equity"], FINANCING_SOURCES["debt"] + 1
        )
        len_equity_and_debt = (
            equity_and_debt.indices(LEN_FINANCING_SOURCES)[1]
            - equity_and_debt.indices(LEN_FINANCING_SOURCES)[0]
        )

        # Industry aggregates, by asset type, legal form, financing source and year
        # ------------------------------------------------------------------------------
        # Businesses
        out_array[
            NUM_INDS, :NUM_ASSETS, :NUM_BIZ, :NUM_EQUITY_DEBT, :NUM_YEARS
        ] = (
            in_var[
                :NUM_BIZ_INDS, :NUM_ASSETS, :NUM_BIZ, :NUM_EQUITY_DEBT, :NUM_YEARS
            ]
            * (
                np.tile(
                    weights[
                        :NUM_BIZ_INDS,
                        ASSET_TYPE_INDEX[asset_agg_name],
                        LEGAL_FORMS["biz"],
                        FINANCING_SOURCES["typical (biz)"],
                        :NUM_YEARS,
                    ],
                    (NUM_ASSETS, NUM_BIZ, NUM_EQUITY_DEBT, 1, 1),
                )
            ).transpose((3, 0, 1, 2, 4))
        ).sum(
            axis=(0)
        ) / np.tile(
            weights[
                NUM_INDS,
                ASSET_TYPE_INDEX[asset_agg_name],
                LEGAL_FORMS["biz"],
                FINANCING_SOURCES["typical (biz)"],
                :NUM_YEARS,
            ],
            (NUM_ASSETS, NUM_BIZ, NUM_EQUITY_DEBT, 1),
        )

        # Owner-occupied housing
        # NaNs because owner-occupied housing cannot be aggregated across industries

        # Other aggregates
        # ------------------------------------------------------------------------------
        ind_components = [slice(0, NUM_BIZ_INDS), slice(0, NUM_INDS)]
        form_aggregates = [LEGAL_FORMS["biz"], LEGAL_FORMS["biz+ooh"]]
        form_components = [slice(0, NUM_BIZ), slice(0, NUM_FOR_PROFIT_LEGAL_FORMS)]
        financing_aggregates = [
            FINANCING_SOURCES["typical (biz)"],
            FINANCING_SOURCES["typical (biz+ooh)"],
        ]
        ind_form_financing = zip(
            ind_components, form_aggregates, form_components, financing_aggregates
        )

        for ind_comps, form_agg, form_comps, financing_agg in ind_form_financing:

            len_ind_comps = (
                ind_comps.indices(NUM_INDS)[1] - ind_comps.indices(NUM_INDS)[0]
            )

            len_form_comps = (
                form_comps.indices(LEN_LEGAL_FORMS)[1]
                - form_comps.indices(LEN_LEGAL_FORMS)[0]
            )

            # Legal form aggregates, by industry, asset type, financing source and year
            # --------------------------------------------------------------------------
            out_array[
                ind_comps, :NUM_ASSETS, form_agg, :NUM_EQUITY_DEBT, :NUM_YEARS
            ] = (
                in_var[
                    ind_comps,
                    :NUM_ASSETS,
                    form_comps,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_comps,
                            financing_agg,
                            :NUM_YEARS,
                        ],
                        (len_ind_comps, NUM_ASSETS, NUM_EQUITY_DEBT, 1, 1),
                    )
                ).transpose((0, 1, 3, 2, 4))
            ).sum(
                axis=(2)
            ) / np.tile(
                weights[
                    NUM_INDS,
                    ASSET_TYPE_INDEX[asset_agg_name],
                    form_agg,
                    financing_agg,
                    :NUM_YEARS,
                ],
                (len_ind_comps, NUM_ASSETS, NUM_EQUITY_DEBT, 1),
            )

            # Financing source aggregates, by industry, asset type, legal form and year
            # --------------------------------------------------------------------------
            out_array[ind_comps, :NUM_ASSETS, form_comps, financing_agg, :NUM_YEARS] = (
                in_var[ind_comps, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS]
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            equity_and_debt,
                            :NUM_YEARS,
                        ],
                        (len_ind_comps, NUM_ASSETS, len_form_comps, 1, 1),
                    )
                )
            ).sum(axis=(3)) / np.tile(
                weights[
                    NUM_INDS,
                    ASSET_TYPE_INDEX[asset_agg_name],
                    form_agg,
                    financing_agg,
                    :NUM_YEARS,
                ],
                (len_ind_comps, NUM_ASSETS, len_form_comps, 1),
            )

            # Legal form and financing source aggregates, by industry, asset type and year
            # --------------------------------------------------------------------------
            out_array[ind_comps, :NUM_ASSETS, form_agg, financing_agg, :NUM_YEARS] = (
                in_var[ind_comps, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS]
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_comps,
                            financing_agg,
                            :NUM_YEARS,
                        ],
                        (len_ind_comps, NUM_ASSETS, len_equity_and_debt, 1, 1),
                    )
                ).transpose((0, 1, 3, 2, 4))
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            equity_and_debt,
                            :NUM_YEARS,
                        ],
                        (len_ind_comps, NUM_ASSETS, len_form_comps, 1, 1),
                    )
                )
            ).sum(axis=(2, 3)) / (
                np.tile(
                    np.square(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            financing_agg,
                            :NUM_YEARS,
                        ]
                    ),
                    (len_ind_comps, NUM_ASSETS, 1),
                )
            ).transpose(
                (0, 1, 2)
            )

            # Industry and financing source aggregates, by asset type, legal form and year
            # --------------------------------------------------------------------------
            out_array[NUM_INDS, :NUM_ASSETS, form_comps, financing_agg, :NUM_YEARS] = (
                in_var[ind_comps, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS]
                * (
                    np.tile(
                        weights[
                            ind_comps,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            financing_agg,
                            :NUM_YEARS,
                        ],
                        (NUM_ASSETS, len_form_comps, len_equity_and_debt, 1, 1),
                    )
                ).transpose((3, 0, 1, 2, 4))
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            equity_and_debt,
                            :NUM_YEARS,
                        ],
                        (len_ind_comps, NUM_ASSETS, len_form_comps, 1, 1),
                    )
                )
            ).sum(axis=(0, 3)) / (
                np.tile(
                    np.square(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            financing_agg,
                            :NUM_YEARS,
                        ]
                    ),
                    (len_form_comps, NUM_ASSETS, 1),
                )
            ).transpose(
                (1, 0, 2)
            )

            # Industry and legal form aggregates, by asset type, financing source and year
            # --------------------------------------------------------------------------
            out_array[
                NUM_INDS, :NUM_ASSETS, form_agg, :NUM_EQUITY_DEBT, :NUM_YEARS
            ] = (
                in_var[
                    ind_comps,
                    :NUM_ASSETS,
                    form_comps,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]
                * (
                    np.tile(
                        weights[
                            ind_comps,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            financing_agg,
                            :NUM_YEARS,
                        ],
                        (NUM_ASSETS, len_form_comps, NUM_EQUITY_DEBT, 1, 1),
                    )
                ).transpose((3, 0, 1, 2, 4))
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_comps,
                            financing_agg,
                            :NUM_YEARS,
                        ],
                        (len_ind_comps, NUM_ASSETS, NUM_EQUITY_DEBT, 1, 1),
                    )
                ).transpose((0, 1, 3, 2, 4))
            ).sum(
                axis=(0, 2)
            ) / (
                np.tile(
                    np.square(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            financing_agg,
                            :NUM_YEARS,
                        ]
                    ),
                    (NUM_EQUITY_DEBT, NUM_ASSETS, 1),
                )
            ).transpose(
                (1, 0, 2)
            )

            # Industry, legal form, and financing source aggregates, by asset type and year
            # --------------------------------------------------------------------------
            out_array[NUM_INDS, :NUM_ASSETS, form_agg, financing_agg, :NUM_YEARS] = (
                in_var[ind_comps, :NUM_ASSETS, form_comps, equity_and_debt, :NUM_YEARS]
                * (
                    np.tile(
                        weights[
                            ind_comps,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            financing_agg,
                            :NUM_YEARS,
                        ],
                        (NUM_ASSETS, len_form_comps, len_equity_and_debt, 1, 1),
                    )
                ).transpose((3, 0, 1, 2, 4))
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_comps,
                            financing_agg,
                            :NUM_YEARS,
                        ],
                        (len_ind_comps, NUM_ASSETS, len_equity_and_debt, 1, 1),
                    )
                ).transpose((0, 1, 3, 2, 4))
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            equity_and_debt,
                            :NUM_YEARS,
                        ],
                        (len_ind_comps, NUM_ASSETS, len_form_comps, 1, 1),
                    )
                )
            ).sum(axis=(0, 2, 3)) / (
                np.tile(
                    np.power(
                        weights[
                            NUM_INDS,
                            ASSET_TYPE_INDEX[asset_agg_name],
                            form_agg,
                            financing_agg,
                            :NUM_YEARS,
                        ],
                        3,
                    ),
                    (NUM_ASSETS, 1),
                )
            ).transpose(
                (0, 1)
            )

        return out_array

    def _calc_values_by_asset_agg_uniformity(self, in_var, weights, asset_aggs):
        """Calculate values by asset aggregate when using the tax uniformity method
        and applying weights that vary by industry, asset, legal form, and financing
        source.

        Parameters
        ----------
        in_var : np.ndarray
            Variable for which aggregate weighted averages will be calculated.
        weights : np.ndarray
            Weights used to calculate weighted averages when aggregating.
        asset_aggs : tuple
            Asset aggregates considered.

        Returns
        -------
        out_array : np.ndarray
            Array filled with values of in_var in the non-aggregate dimensions
            and aggregated values at the end of the asset dimension, with dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        """
        # Initialize array and output position
        out_array = self._create_empty_array("nans")
        output_position = 0

        equity_and_debt = slice(
            FINANCING_SOURCES["typical_equity"], FINANCING_SOURCES["debt"] + 1
        )
        len_equity_and_debt = (
            equity_and_debt.indices(LEN_FINANCING_SOURCES)[1]
            - equity_and_debt.indices(LEN_FINANCING_SOURCES)[0]
        )

        # Filling aggregates
        # ------------------------------------------------------------------------------
        for asset_agg_range in asset_aggs:

            # Asset aggregates, by industry, legal form, financing source, and year
            # --------------------------------------------------------------------------
            # Businesses
            out_array[
                :NUM_BIZ_INDS,
                NUM_ASSETS + output_position,
                :NUM_BIZ,
                :NUM_EQUITY_DEBT,
                :NUM_YEARS,
            ] = (
                (
                    in_var[
                        :NUM_BIZ_INDS,
                        asset_agg_range,
                        :NUM_BIZ,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                asset_agg_range,
                                LEGAL_FORMS["biz"],
                                FINANCING_SOURCES["typical (biz)"],
                                :NUM_YEARS,
                            ],
                            (NUM_BIZ_INDS, NUM_BIZ, NUM_EQUITY_DEBT, 1, 1),
                        )
                    ).transpose((0, 3, 1, 2, 4))
                ).sum(axis=(1))
                / weights[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["biz"],
                    FINANCING_SOURCES["typical (biz)"],
                    :NUM_YEARS,
                ]
            )

            # Owner-occupied housing
            if (
                ASSET_TYPE_INDEX["Land"] in asset_agg_range
                and ASSET_TYPE_INDEX["Residential buildings"] in asset_agg_range
            ):
                out_array[
                    OOH_IND,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["ooh"],
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ] = (
                    in_var[
                        OOH_IND,
                        ALL_OOH_ASSETS,
                        LEGAL_FORMS["ooh"],
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                ALL_OOH_ASSETS,
                                LEGAL_FORMS["biz+ooh"],
                                FINANCING_SOURCES["typical (biz+ooh)"],
                                :NUM_YEARS,
                            ],
                            (NUM_EQUITY_DEBT, 1, 1),
                        )
                    ).transpose((1, 0, 2))
                ).sum(
                    axis=(0)
                ) / np.tile(
                    (
                        weights[
                            NUM_INDS,
                            ALL_OOH_ASSETS,
                            LEGAL_FORMS["biz+ooh"],
                            FINANCING_SOURCES["typical (biz+ooh)"],
                            :NUM_YEARS,
                        ]
                    ).sum(axis=(0)),
                    (NUM_EQUITY_DEBT, 1),
                )

            elif ASSET_TYPE_INDEX["Residential buildings"] in asset_agg_range:
                out_array[
                    OOH_IND,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["ooh"],
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ] = in_var[
                    OOH_IND,
                    ASSET_TYPE_INDEX["Residential buildings"],
                    LEGAL_FORMS["ooh"],
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]

            else:
                out_array[
                    OOH_IND,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["ooh"],
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ] = np.nan

            # Asset and financing source aggegates, by industry, legal form, and year
            # --------------------------------------------------------------------------
            # Businesses
            for legal_form, financing_source in [
                ("biz", "typical (biz)"),
                ("biz+ooh", "typical (biz+ooh)"),
            ]:
                out_array[
                    :NUM_BIZ_INDS,
                    NUM_ASSETS + output_position,
                    :NUM_BIZ,
                    FINANCING_SOURCES[financing_source],
                    :NUM_YEARS,
                ] = (
                    in_var[
                        :NUM_BIZ_INDS,
                        asset_agg_range,
                        :NUM_BIZ,
                        equity_and_debt,
                        :NUM_YEARS,
                    ]
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                asset_agg_range,
                                LEGAL_FORMS[legal_form],
                                FINANCING_SOURCES[financing_source],
                                :NUM_YEARS,
                            ],
                            (NUM_BIZ_INDS, NUM_BIZ, len_equity_and_debt, 1, 1),
                        )
                    ).transpose((0, 3, 1, 2, 4))
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                NUM_ASSETS + output_position,
                                LEGAL_FORMS[legal_form],
                                equity_and_debt,
                                :NUM_YEARS,
                            ],
                            (NUM_BIZ_INDS, len(asset_agg_range), NUM_BIZ, 1, 1),
                        )
                    )
                ).sum(
                    axis=(1, 3)
                ) / np.tile(
                    np.square(
                        weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS[legal_form],
                            FINANCING_SOURCES[financing_source],
                            :NUM_YEARS,
                        ]
                    ),
                    (NUM_BIZ_INDS, NUM_BIZ, 1),
                )

            # Owner-occupied housing
            if (
                ASSET_TYPE_INDEX["Land"] in asset_agg_range
                and ASSET_TYPE_INDEX["Residential buildings"] in asset_agg_range
            ):
                out_array[
                    OOH_IND,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["ooh"],
                    FINANCING_SOURCES["typical (biz+ooh)"],
                    :NUM_YEARS,
                ] = (
                    in_var[
                        OOH_IND,
                        ALL_OOH_ASSETS,
                        LEGAL_FORMS["ooh"],
                        equity_and_debt,
                        :NUM_YEARS,
                    ]
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                ALL_OOH_ASSETS,
                                LEGAL_FORMS["biz+ooh"],
                                FINANCING_SOURCES["typical (biz+ooh)"],
                                :NUM_YEARS,
                            ],
                            (len_equity_and_debt, 1, 1),
                        )
                    ).transpose((1, 0, 2))
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                NUM_ASSETS + output_position,
                                LEGAL_FORMS["biz+ooh"],
                                equity_and_debt,
                                :NUM_YEARS,
                            ],
                            (len(ALL_OOH_ASSETS), 1, 1),
                        )
                    )
                ).sum(
                    axis=(0, 1)
                ) / (
                    weights[
                        NUM_INDS,
                        ALL_OOH_ASSETS,
                        LEGAL_FORMS["biz+ooh"],
                        FINANCING_SOURCES["typical (biz+ooh)"],
                        :NUM_YEARS,
                    ].sum(axis=(0))
                    * weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        LEGAL_FORMS["biz+ooh"],
                        FINANCING_SOURCES["typical (biz+ooh)"],
                        :NUM_YEARS,
                    ]
                )

            elif ASSET_TYPE_INDEX["Residential buildings"] in asset_agg_range:
                out_array[
                    OOH_IND,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["ooh"],
                    FINANCING_SOURCES["typical (biz+ooh)"],
                    :NUM_YEARS,
                ] = (
                    (
                        in_var[
                            OOH_IND,
                            ASSET_TYPE_INDEX["Residential buildings"],
                            LEGAL_FORMS["ooh"],
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                        * weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz+ooh"],
                            equity_and_debt,
                            :NUM_YEARS,
                        ]
                    ).sum(axis=(0))
                    / weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        LEGAL_FORMS["biz+ooh"],
                        FINANCING_SOURCES["typical (biz+ooh)"],
                        :NUM_YEARS,
                    ]
                )

            else:
                out_array[
                    OOH_IND,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["ooh"],
                    FINANCING_SOURCES["typical (biz+ooh)"],
                    :NUM_YEARS,
                ] = np.nan

            # Asset and legal form aggregates, by industry, financing source, and year
            # --------------------------------------------------------------------------
            for legal_form in ["biz", "biz+ooh"]:
                out_array[
                    :NUM_BIZ_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS[legal_form],
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ] = (
                    in_var[
                        :NUM_BIZ_INDS,
                        asset_agg_range,
                        :NUM_BIZ,
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                asset_agg_range,
                                LEGAL_FORMS["biz"],
                                FINANCING_SOURCES["typical (biz)"],
                                :NUM_YEARS,
                            ],
                            (NUM_BIZ_INDS, NUM_BIZ, NUM_EQUITY_DEBT, 1, 1),
                        )
                    ).transpose((0, 3, 1, 2, 4))
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                NUM_ASSETS + output_position,
                                :NUM_BIZ,
                                FINANCING_SOURCES["typical (biz)"],
                                :NUM_YEARS,
                            ],
                            (
                                NUM_BIZ_INDS,
                                len(asset_agg_range),
                                NUM_EQUITY_DEBT,
                                1,
                                1,
                            ),
                        )
                    ).transpose((0, 1, 3, 2, 4))
                ).sum(
                    axis=(1, 2)
                ) / np.tile(
                    np.square(
                        weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ]
                    ),
                    (NUM_BIZ_INDS, NUM_EQUITY_DEBT, 1),
                )

            # Asset, legal form and financing source aggregates, by industry and year
            # --------------------------------------------------------------------------
            for legal_form, financing_source in [
                ("biz", "typical (biz)"),
                ("biz+ooh", "typical (biz+ooh)"),
            ]:
                out_array[
                    :NUM_BIZ_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS[legal_form],
                    FINANCING_SOURCES[financing_source],
                    :NUM_YEARS,
                ] = (
                    in_var[
                        :NUM_BIZ_INDS,
                        asset_agg_range,
                        :NUM_BIZ,
                        equity_and_debt,
                        :NUM_YEARS,
                    ]
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                asset_agg_range,
                                LEGAL_FORMS["biz"],
                                FINANCING_SOURCES["typical (biz)"],
                                :NUM_YEARS,
                            ],
                            (NUM_BIZ_INDS, NUM_BIZ, len_equity_and_debt, 1, 1),
                        )
                    ).transpose((0, 3, 1, 2, 4))
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                NUM_ASSETS + output_position,
                                :NUM_BIZ,
                                FINANCING_SOURCES["typical (biz)"],
                                :NUM_YEARS,
                            ],
                            (
                                NUM_BIZ_INDS,
                                len(asset_agg_range),
                                len_equity_and_debt,
                                1,
                                1,
                            ),
                        )
                    ).transpose((0, 1, 3, 2, 4))
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                NUM_ASSETS + output_position,
                                LEGAL_FORMS["biz"],
                                equity_and_debt,
                                :NUM_YEARS,
                            ],
                            (NUM_BIZ_INDS, len(asset_agg_range), NUM_BIZ, 1, 1),
                        )
                    )
                ).sum(
                    axis=(1, 2, 3)
                ) / np.tile(
                    np.power(
                        weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        3,
                    ),
                    (NUM_BIZ_INDS, 1),
                )

            # Industry and asset aggregates, by legal form, financing source, and year
            # --------------------------------------------------------------------------
            # Businesses
            out_array[
                NUM_INDS,
                NUM_ASSETS + output_position,
                :NUM_BIZ,
                :NUM_EQUITY_DEBT,
                :NUM_YEARS,
            ] = (
                in_var[
                    :NUM_BIZ_INDS,
                    asset_agg_range,
                    :NUM_BIZ,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            asset_agg_range,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        (NUM_BIZ_INDS, NUM_BIZ, NUM_EQUITY_DEBT, 1, 1),
                    )
                ).transpose((0, 3, 1, 2, 4))
                * (
                    np.tile(
                        weights[
                            :NUM_BIZ_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        (len(asset_agg_range), NUM_BIZ, NUM_EQUITY_DEBT, 1, 1),
                    )
                ).transpose((3, 0, 1, 2, 4))
            ).sum(
                axis=(0, 1)
            ) / np.tile(
                np.square(
                    weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        LEGAL_FORMS["biz"],
                        FINANCING_SOURCES["typical (biz)"],
                        :NUM_YEARS,
                    ]
                ),
                (NUM_BIZ, NUM_EQUITY_DEBT, 1),
            )

            # Owner-occupied housing
            # NaNs because owner-occupied housing cannot be aggregated across industries

            # Industry, asset, and financing source aggregates, by legal form and year
            # --------------------------------------------------------------------------
            # Businesses
            for legal_form, financing_source in [
                ("biz", "typical (biz)"),
                ("biz+ooh", "typical (biz+ooh)"),
            ]:
                out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    :NUM_BIZ,
                    FINANCING_SOURCES[financing_source],
                    :NUM_YEARS,
                ] = (
                    in_var[
                        :NUM_BIZ_INDS,
                        asset_agg_range,
                        :NUM_BIZ,
                        equity_and_debt,
                        :NUM_YEARS,
                    ]
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                asset_agg_range,
                                LEGAL_FORMS[legal_form],
                                FINANCING_SOURCES[financing_source],
                                :NUM_YEARS,
                            ],
                            (NUM_BIZ_INDS, NUM_BIZ, len_equity_and_debt, 1, 1),
                        )
                    ).transpose((0, 3, 1, 2, 4))
                    * (
                        np.tile(
                            weights[
                                :NUM_BIZ_INDS,
                                NUM_ASSETS + output_position,
                                LEGAL_FORMS[legal_form],
                                FINANCING_SOURCES[financing_source],
                                :NUM_YEARS,
                            ],
                            (len(asset_agg_range), NUM_BIZ, len_equity_and_debt, 1, 1),
                        )
                    ).transpose((3, 0, 1, 2, 4))
                    * (
                        np.tile(
                            weights[
                                NUM_INDS,
                                NUM_ASSETS + output_position,
                                LEGAL_FORMS[legal_form],
                                equity_and_debt,
                                :NUM_YEARS,
                            ],
                            (NUM_BIZ_INDS, len(asset_agg_range), NUM_BIZ, 1, 1),
                        )
                    )
                ).sum(
                    axis=(0, 1, 3)
                ) / np.tile(
                    np.power(
                        weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS[legal_form],
                            FINANCING_SOURCES[financing_source],
                            :NUM_YEARS,
                        ],
                        3,
                    ),
                    (NUM_BIZ, 1),
                )

            # Owner-occupied housing
            # NaNs because owner-occupied housing cannot be aggregated across industries

            # Industry, asset, and legal forms values, by financing source and year
            # --------------------------------------------------------------------------
            # All businesses
            out_array[
                NUM_INDS,
                NUM_ASSETS + output_position,
                LEGAL_FORMS["biz"],
                :NUM_EQUITY_DEBT,
                :NUM_YEARS,
            ] = (
                in_var[
                    :NUM_BIZ_INDS,
                    asset_agg_range,
                    :NUM_BIZ,
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            asset_agg_range,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        (NUM_BIZ_INDS, NUM_BIZ, NUM_EQUITY_DEBT, 1, 1),
                    )
                ).transpose((0, 3, 1, 2, 4))
                * (
                    np.tile(
                        weights[
                            :NUM_BIZ_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        (len(asset_agg_range), NUM_BIZ, NUM_EQUITY_DEBT, 1, 1),
                    )
                ).transpose((3, 0, 1, 2, 4))
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            :NUM_BIZ,
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        (
                            NUM_BIZ_INDS,
                            len(asset_agg_range),
                            NUM_EQUITY_DEBT,
                            1,
                            1,
                        ),
                    )
                ).transpose((0, 1, 3, 2, 4))
            ).sum(
                axis=(0, 1, 2)
            ) / np.tile(
                np.power(
                    weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        LEGAL_FORMS["biz"],
                        FINANCING_SOURCES["typical (biz)"],
                        :NUM_YEARS,
                    ],
                    3,
                ),
                (NUM_EQUITY_DEBT, 1),
            )

            # All businesses + owner-occupied housing
            if (
                ASSET_TYPE_INDEX["Land"] in asset_agg_range
                or ASSET_TYPE_INDEX["Residential buildings"] in asset_agg_range
            ):
                out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["biz+ooh"],
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ] = (
                    (
                        out_array[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            :NUM_EQUITY_DEBT,
                            :NUM_YEARS,
                        ]
                        * weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            :NUM_EQUITY_DEBT,
                            :NUM_YEARS,
                        ]
                        + out_array[
                            OOH_IND,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["ooh"],
                            :NUM_EQUITY_DEBT,
                            :NUM_YEARS,
                        ]
                        * weights[
                            OOH_IND,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["ooh"],
                            :NUM_EQUITY_DEBT,
                            :NUM_YEARS,
                        ]
                    )
                    / weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        LEGAL_FORMS["biz+ooh"],
                        :NUM_EQUITY_DEBT,
                        :NUM_YEARS,
                    ]
                )
            else:
                out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["biz+ooh"],
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ] = out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["biz"],
                    :NUM_EQUITY_DEBT,
                    :NUM_YEARS,
                ]

            # Industry, legal form, financing source, and asset aggregates, by year
            # --------------------------------------------------------------------------
            # All businesses, when accounting for weights across all businesses
            out_array[
                NUM_INDS,
                NUM_ASSETS + output_position,
                LEGAL_FORMS["biz"],
                FINANCING_SOURCES["typical (biz)"],
                :NUM_YEARS,
            ] = (
                in_var[
                    :NUM_BIZ_INDS,
                    asset_agg_range,
                    :NUM_BIZ,
                    equity_and_debt,
                    :NUM_YEARS,
                ]
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            asset_agg_range,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        (NUM_BIZ_INDS, NUM_BIZ, len_equity_and_debt, 1, 1),
                    )
                ).transpose((0, 3, 1, 2, 4))
                * (
                    np.tile(
                        weights[
                            :NUM_BIZ_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        (len(asset_agg_range), NUM_BIZ, len_equity_and_debt, 1, 1),
                    )
                ).transpose((3, 0, 1, 2, 4))
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            :NUM_BIZ,
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ],
                        (NUM_BIZ_INDS, len(asset_agg_range), len_equity_and_debt, 1, 1),
                    )
                ).transpose((0, 1, 3, 2, 4))
                * (
                    np.tile(
                        weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            equity_and_debt,
                            :NUM_YEARS,
                        ],
                        (NUM_BIZ_INDS, len(asset_agg_range), NUM_BIZ, 1, 1),
                    )
                )
            ).sum(
                axis=(0, 1, 2, 3)
            ) / np.power(
                weights[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["biz"],
                    FINANCING_SOURCES["typical (biz)"],
                    :NUM_YEARS,
                ],
                4,
            )

            # All businesses + owner-occupied housing, when accounting for weights
            # across all businesses + owner-occupied housing
            if (
                ASSET_TYPE_INDEX["Land"] in asset_agg_range
                or ASSET_TYPE_INDEX["Residential buildings"] in asset_agg_range
            ):
                out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["biz+ooh"],
                    FINANCING_SOURCES["typical (biz+ooh)"],
                    :NUM_YEARS,
                ] = (
                    (
                        out_array[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ]
                        * weights[
                            NUM_INDS,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["biz"],
                            FINANCING_SOURCES["typical (biz)"],
                            :NUM_YEARS,
                        ]
                        + out_array[
                            OOH_IND,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["ooh"],
                            FINANCING_SOURCES["typical (biz+ooh)"],
                            :NUM_YEARS,
                        ]
                        * weights[
                            OOH_IND,
                            NUM_ASSETS + output_position,
                            LEGAL_FORMS["ooh"],
                            FINANCING_SOURCES["typical (biz+ooh)"],
                            :NUM_YEARS,
                        ]
                    )
                    / weights[
                        NUM_INDS,
                        NUM_ASSETS + output_position,
                        LEGAL_FORMS["biz+ooh"],
                        FINANCING_SOURCES["typical (biz+ooh)"],
                        :NUM_YEARS,
                    ]
                )
            else:
                out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["biz+ooh"],
                    FINANCING_SOURCES["typical (biz+ooh)"],
                    :NUM_YEARS,
                ] = out_array[
                    NUM_INDS,
                    NUM_ASSETS + output_position,
                    LEGAL_FORMS["biz"],
                    FINANCING_SOURCES["typical (biz)"],
                    :NUM_YEARS,
                ]

            # Reset output position
            output_position = output_position + 1

        return out_array
