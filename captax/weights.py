import copy
import os
import numpy as np
import pandas as pd
from captax.constants import *


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


class Weights():
    """Define the object used to read assets data and calculate model weights.

    Attributes
    ----------
    weights_path : str
        String describing the folder path where weights input files are stored.
    weights : np.ndarray
        Weights used in model calculations.
    detailed_industry_weights : np.ndarray
        Detailed industry weights for aggregating detailed industries into broader industries.

    """""

    def __init__(self, shares_data):
        """Initialize Weights object.

        This method calls four other methods:
            * self._read_assets_data() : Reads assets data used as the basis for calculating model weights.
            * self._read_asset_shares() : Reads in shares of total assets by industry and asset type for each
                legal form.
            * self._calc_weights() : Calculates weights by industry, asset type, legal form and financing source.
            * self._read_detailed_industry_weights() : Reads detailed industry weights to apportion industry
                data to detailed industry level.

        Parameters
        ----------
        shares_data : dict
            Dictionary including equity and debt-financing shares for businesses and owner-occupied housing, and
            shares of C corp equity investments financed by new equity and retained earnings.

        Returns
        -------
        None
            Method reads weights data and stores them as attributes of Weights object.

        """
        self.weights_path = CURRENT_PATH + '/data/inputs/weights_data/'

        _assets_data = self._read_assets_data('assets.csv')

        # Shares of total assets for each legal form, by industry and asset type
        _c_corp_shares = self._read_asset_shares('asset_shares_c_corp.csv')
        if not ((_c_corp_shares[OOH_IND, :NUM_ASSETS]==0).all()):
            raise ValueError(f'C corp shares of total assets must be equal to 0 for the OOH industry')

        _pass_thru_shares = self._read_asset_shares('asset_shares_pass_thru.csv')
        if not ((_pass_thru_shares[OOH_IND, :NUM_ASSETS]==0).all()):
            raise ValueError(f'Pass-through shares of total assets must be equal to 0 for the OOH industry')

        if not ((_c_corp_shares + _pass_thru_shares <=1).all()):
            raise ValueError(f'The sum of C corp and pass-through shares of total assets must be lower or equal to 1')
        _nonprofit_shares = 1.0 - _c_corp_shares - _pass_thru_shares

        _ooh_shares = self._read_asset_shares('asset_shares_ooh.csv')
        if not ((_ooh_shares[ALL_BIZ_INDS, :NUM_ASSETS]==0).all() & (_ooh_shares[OOH_IND, :NUM_ASSETS]==1).all()):
            raise ValueError(f'OOH shares of total assets must be equal to 0 for all industries other than the '
                             f'OOH industry, for which they must equal 1 for all asset types')

        _asset_shares = {
            'c_corp' : _c_corp_shares,
            'pass_thru' : _pass_thru_shares,
            'non_profit' : _nonprofit_shares,
            'ooh' : _ooh_shares
        }

        self.weights = self._calc_weights(_assets_data, _asset_shares, shares_data)

        print('* Assets data read, and weights calculated')

        self.detailed_industry_weights = self._read_detailed_industry_weights('detailed_industry_weights.csv')

        print('* Detailed industry weights read')

        return None


    def _read_assets_data(self, filename):
        """Read assets data used as the basis for calculating model weights.

        Parameters
        ----------
        filename : str
            Name of csv file to be read.

        Returns
        -------
        ndarray : np.ndarray
            Array of asset values (in $ millions) by industry and asset type.

        """
        assert filename.endswith('.csv')

        file = self.weights_path + filename
        df = pd.read_csv(file, skiprows=1, index_col='Industries/Asset types')
        ndarray = df.round(decimals=0).to_numpy()

        return ndarray


    def _read_asset_shares(self, filename):
        """Read in shares of total assets by industry and asset type for each legal form.

        Combined, C corps and pass-throughs comprise for-profit businesses, the residual
        of those two are the shares of assets attributable to nonprofit entities.

        The owner-occupied housing matrix is all zeros, except for the last row of the matrix, which
        includes information on assets by asset type for owner-occupied housing.

        Parameters
        ----------
        filename : str
            Name of csv file to be read.

        Returns
        -------
        ndarray : np.ndarray
            Array with asset values for each legal form, by industry and asset type.

        Note
        ----
        There are three asset shares files: C corporations, pass-throughs, and owner-occupied housing.
        Each file contains an asset type by industry matrix, which represents the share of total
        assets within that legal form.

        """
        assert filename.endswith('csv')

        file = self.weights_path + filename
        df = pd.read_csv(file, skiprows=1, index_col='Industries/Asset types')
        ndarray = df.round(decimals=4).to_numpy()

        return ndarray


    def _calc_weights(self, assets, asset_shares, shares):
        """Calculate weights to be used throughout the model.

        Weights are based on asset values by industry and asset type, adjusted for
        share parameters by financing sources (debt/equity shares and the share of C corps
        equity that is financed through new equity and retained earnings) and by legal form.

        Parameters
        ----------
        assets : np.ndarray
            Total asset values (in $ millions) by industry and asset type.
        asset_shares : dict
            Shares of total assets by legal form.
        shares : dict
            Dictionary including equity and debt-financing shares for businesses and owner-occupied housing, and
            shares of C corp equity investments financed by new equity and retained earnings.

        Returns
        -------
        weights : np.ndarray
            Four-dimensional array (by industry, asset type, legal form, and financing
            sources), of adjusted weights, which are used throughout the model.

        """
        # Initialize array
        #---------------------------------------------------------------------------------
        weights = np.zeros((NUM_INDS,
                            NUM_ASSETS,
                            LEN_LEGAL_FORMS,
                            LEN_FINANCING_SOURCES))

        weights[:] = np.nan

        # Calculate weights
        #---------------------------------------------------------------------------------
        for legal_form in ['c_corp','pass_thru','ooh','non_profit']:
            for financing_source in ['typical_equity','debt','typical (biz)']:

                # Weights for investments financed with new equity and retained earnings
                if legal_form == 'c_corp' and financing_source == 'typical_equity':
                    for equity_financing_source in ['new_equity','retained_earnings']:
                        weights[:NUM_INDS,
                                :NUM_ASSETS,
                                LEGAL_FORMS[legal_form],
                                FINANCING_SOURCES[equity_financing_source]] = (
                                    assets
                                    * asset_shares[legal_form]
                                    * shares['financing'][financing_source][:NUM_INDS,
                                                                            :NUM_ASSETS,
                                                                            LEGAL_FORMS[legal_form]]
                                    * shares['c_corp_equity'][equity_financing_source]
                        )

                # Weights for investments financed with typical equity and debt
                if legal_form in ['c_corp','pass_thru','ooh']:
                    if financing_source in ['typical_equity','debt']:
                        weights[:NUM_INDS,
                                :NUM_ASSETS,
                                LEGAL_FORMS[legal_form],
                                FINANCING_SOURCES[financing_source]] = (
                                    assets
                                    * asset_shares[legal_form]
                                    * shares['financing'][financing_source][:NUM_INDS,
                                                                            :NUM_ASSETS,
                                                                            LEGAL_FORMS[legal_form]]
                        )

                # Weights for typically financed investments (businesses)
                if financing_source == 'typical (biz)':
                    weights[:NUM_INDS,
                            :NUM_ASSETS,
                            LEGAL_FORMS[legal_form],
                            FINANCING_SOURCES[financing_source]] = (
                                assets
                                * asset_shares[legal_form]
                    )

        # Weights for typically financed investments (businesses + owner-occupied housing)
        weights[:NUM_INDS, :NUM_ASSETS, :LEN_LEGAL_FORMS, FINANCING_SOURCES['typical (biz+ooh)']] = (
            weights[:NUM_INDS, :NUM_ASSETS, :LEN_LEGAL_FORMS, FINANCING_SOURCES['typical (biz)']]
        )

        return weights


    def _read_detailed_industry_weights(self, filename):
        """Read detailed industry weights to apportion industry data to detailed industry level.

        Parameters
        ----------
        filename : str
            Name of csv file containing the data.

        Returns
        -------
        ndarray: np.ndarray
            1-dimensional array of detailed industry weights.

        """
        assert filename.endswith('csv')

        file = self.weights_path + filename
        df = pd.read_csv(file, skiprows=1, index_col='detailed_industry').round(decimals=3)

        # Check that detailed industry weights add up to 1 for each industry
        sum_detailed_industry_weights = df.groupby(['standard_industry']).sum()
        if not (np.all((sum_detailed_industry_weights == 1.0))):
            raise ValueError(f'Detailed industry weights do not add up to 1 for at least one industry')

        # Save detailed industry weights into a 1-dimensional array
        ndarray = df['detailed_industry_weights'].to_numpy()

        return ndarray
