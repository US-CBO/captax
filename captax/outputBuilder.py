import copy
import numpy as np
from captax.constants import *


class OutputBuilder:
    """Define the object used to calculate and store aggregated results.

    Attributes
    ----------
    agg : Aggregator object
        Includes aggregates used in the calculations below.
    c_corp_tax_wedges : np.ndarray
        C corporation tax wedges.
    total_tax_wedges: np.ndarray
        Total tax wedges.
    c_corp_EMTRs : np.ndarray
        C corporation effective marginal tax rates.
    total_EMTRs: np.ndarray
        Total effective marginal tax rates.

    """

    def __init__(self, agg):
        """Initialize OutputBuilder object.

        Parameters
        ----------
        agg : Aggregator object
            Includes aggregates used in the calculations below.

        Returns
        -------
        None
            Method initializes attributes of OutputBuilder object.

        """
        self.agg = agg
        self.c_corp_tax_wedges = None
        self.total_tax_wedges = None
        self.c_corp_EMTRs = None
        self.total_EMTRs = None

        return None

    def build_all(self):
        """Build all the model outputs.

        This method calls three other methods:
            * _calc_c_corp_tax_wedges()
            * _calc_total_tax_wedges()
            * _calc_effective_marginal_tax_rates()

        The first method is used to calculate C corp tax wedges, which are equal to
        the difference between before-tax rates of return and after-tax rates of return
        required by investors.

        The second method is used to calculate total tax wedges, which are equal to
        the difference between before-tax rates of return and after-tax rates of return
        required by savers.

        The third method is used to calculate effective marginal tax rates, which are
        equal to tax wedges divided by the before-tax rates of return.

        Parameters
        ----------
        None
            Parameters are specified in the methods nested within this method.

        Returns
        -------
        None
            This method nests other methods.

        """
        print("Begin aggregate calculations")

        self.c_corp_tax_wedges = self._calc_c_corp_tax_wedges(
            self.agg.req_before_tax_returns, self.agg.req_after_tax_returns_investors
        )
        self.total_tax_wedges = self._calc_total_tax_wedges(
            self.agg.req_before_tax_returns, self.agg.req_after_tax_returns_savers
        )

        print("* Tax wedges calculated")

        self.c_corp_EMTRs = self._calc_effective_marginal_tax_rates(
            self.c_corp_tax_wedges, self.agg.req_before_tax_returns
        )
        self.total_EMTRs = self._calc_effective_marginal_tax_rates(
            self.total_tax_wedges, self.agg.req_before_tax_returns
        )

        print("* Effective marginal tax rates calculated")
        print("Finished aggregate calculations\n")

        return None

    def _calc_c_corp_tax_wedges(
        self, req_before_tax_returns, req_after_tax_returns_investors
    ):
        """Calculate tax wedge for C corporations by industry, asset type, financing
        source, and year. The C corporation tax wedge is equal to the required
        before-tax rate of return minus the required after-tax rate of return to
        investors.

        Parameters
        ----------
        req_before_tax_returns : np.ndarray
            Required before-tax rates of return.
        req_after_tax_returns_investors : np.ndarray
            Real after-tax required rate of returns to investors.

        Returns
        -------
        c_corp_tax_wedges : np.ndarray
            Array of C corporation tax wedges, with dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        """
        # Initialize array
        c_corp_tax_wedges = np.zeros(
            (LEN_INDS, LEN_ASSETS, LEN_LEGAL_FORMS, LEN_FINANCING_SOURCES, NUM_YEARS)
        )

        c_corp_tax_wedges[:] = np.nan

        # Fill values by financing source
        c_corp_tax_wedges[
            :LEN_INDS,
            :LEN_ASSETS,
            LEGAL_FORMS["c_corp"],
            :LEN_FINANCING_SOURCES,
            :NUM_YEARS,
        ] = (
            req_before_tax_returns[
                :LEN_INDS,
                :LEN_ASSETS,
                LEGAL_FORMS["c_corp"],
                :LEN_FINANCING_SOURCES,
                :NUM_YEARS,
            ]
            - req_after_tax_returns_investors[
                :LEN_INDS,
                :LEN_ASSETS,
                LEGAL_FORMS["c_corp"],
                :LEN_FINANCING_SOURCES,
                :NUM_YEARS,
            ]
        )

        return c_corp_tax_wedges

    def _calc_total_tax_wedges(
        self, req_before_tax_returns, req_after_tax_returns_savers
    ):
        """Calculate total tax wedge by industry, asset type, legal form, financing
        source and year.

        The total tax wedge is equal to the required before-tax rates of return minus
        the required after-tax rates of return to savers.

        Parameters
        ----------
        req_before_tax_returns : np.ndarray
            Required before-tax rates of return.
        req_after_tax_returns_savers : np.ndarray
            Required after-tax rates of return to savers.

        Returns
        -------
        total_tax_wedges: np.ndarray
            Array of total tax wedges, with dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        """
        assert req_before_tax_returns.shape == req_after_tax_returns_savers.shape

        total_tax_wedges = req_before_tax_returns - req_after_tax_returns_savers

        return total_tax_wedges

    def _calc_effective_marginal_tax_rates(self, tax_wedges, req_before_tax_returns):
        """Calculate effective marginal tax rates (EMTRs) on investments.

        The EMTR is calculated by the tax wedge divided by the required before-tax
        rate of return.

        Parameters
        ----------
        tax_wedges : np.ndarray
            Tax wedges.
        req_before_tax_returns : np.ndarray
            Required before-tax rates of return.

        Returns
        -------
        effective_marginal_tax_rates : np.ndarray
            Array of effective marginal tax rates, with dimensions:
                [LEN_INDS,
                 LEN_ASSETS,
                 LEN_LEGAL_FORMS,
                 LEN_FINANCING_SOURCES,
                 NUM_YEARS]

        Note
        ----------
        Only make calculation if required before-tax rate of return is > 0.0,
        otherwise set the effective marginal tax rate equal to nan.

        """
        assert tax_wedges.shape == req_before_tax_returns.shape

        effective_marginal_tax_rates = np.zeros(
            (LEN_INDS, LEN_ASSETS, LEN_LEGAL_FORMS, LEN_FINANCING_SOURCES, NUM_YEARS)
        )

        # Suppress RunTimeWarnings for division by zero or 0/0
        with np.errstate(divide="ignore", invalid="ignore"):

            effective_marginal_tax_rates = np.where(
                req_before_tax_returns != 0.0,
                tax_wedges / req_before_tax_returns,
                np.nan,
            )

        return effective_marginal_tax_rates
