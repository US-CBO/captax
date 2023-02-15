import datetime
import os
import itertools
import pandas as pd
from captax.constants import *


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


class Writer:
    """Define the object used to write out model results.

    Attributes
    ----------
    env : Environment object
        Economic environment parameters.
    pol : Policy object
        Policy parameters.
    agg : Aggregator object
        Aggregates included in output files.
    output : OutputBuilder object
        Tax wedges and effective marginal tax rates (EMTRs) included in output files.
    include_land : bool
        Boolean for whether to include land in model output.
    disp : Dispersion object
        Dispersion statistics.
    output_path : str
        String describing the folder path where output files for a given policy and
        perspective are stored.
    metrics : dict
        Dictionary including output variables, variables' names, variables' labels and
        variables' units.
    """

    def __init__(self, env, pol, agg, output, include_land=False, disp=None):
        """Initialize the Writer object.

        Parameters
        ----------
        env : Environment object
            Economic environment parameters.
        pol : Policy object
            Policy parameters.
        agg : Aggregator object
            Aggregates included in output files.
        output : OutputBuilder object
            Tax wedges and effective marginal tax rates (EMTRs) included in output
            files.
        include_land : bool, default False
            Boolean for whether to include land in model output.
        disp : Dispersion object, default None
            If present (not None), write out dispersion statistics.

        Returns
        -------
        None
            Method initializes attributes of Writer object.

        """
        self.env = env
        self.pol = pol
        self.agg = agg
        self.output = output
        self.include_land = include_land
        self.disp = disp

        # Use this as the directory to actually write out to
        self.output_path = f"{CURRENT_PATH}/data/outputs/{self.pol.policy_name}/{self.pol.perspective}/"

        # Build a dictionary of model metrics, with string labels, and units
        vars = [
            self.agg.req_before_tax_returns,
            self.agg.req_after_tax_returns_savers,
            self.output.total_tax_wedges,
            self.output.total_EMTRs,
            self.agg.req_after_tax_returns_investors,
            self.output.c_corp_tax_wedges,
            self.output.c_corp_EMTRs,
            self.agg.weights,
        ]

        scaled_vars = [
            self.agg.req_before_tax_returns * 100,
            self.agg.req_after_tax_returns_savers * 100,
            self.output.total_tax_wedges * 100,
            self.output.total_EMTRs * 100,
            self.agg.req_after_tax_returns_investors * 100,
            self.output.c_corp_tax_wedges * 100,
            self.output.c_corp_EMTRs * 100,
            self.agg.weights,
        ]

        var_names = [
            "req_before_tax_returns",
            "req_after_tax_returns_savers",
            "total_tax_wedges",
            "total_EMTRs",
            "req_after_tax_returns_investors",
            "c_corp_tax_wedges",
            "c_corp_EMTRs",
            "weights",
        ]

        var_labels = [
            "Required Before-tax Returns",
            "Required After-tax Returns to Savers",
            "Total Tax Wedges",
            "Total EMTRs",
            "Required After-tax Returns to Investors",
            "C Corporation Tax Wedges",
            "C Corporation EMTRs",
            "Weights (Asset Values)",
        ]

        units = [
            "Percent",
            "Percent",
            "Percentage Points",
            "Percent",
            "Percent",
            "Percentage Points",
            "Percent",
            "Millions of Dollars",
        ]

        self.metrics = {}

        for var, scaled_var, var_name, var_label, unit in zip(
            vars, scaled_vars, var_names, var_labels, units
        ):
            # Use the memory id of the _var object as the key, becuase it's immutable
            self.metrics[id(var)] = {}
            self.metrics[id(var)]["var"] = scaled_var
            self.metrics[id(var)]["var_name"] = var_name
            self.metrics[id(var)]["var_label"] = var_label
            self.metrics[id(var)]["units"] = unit

        return None

    def write_all(self):
        """Write all results.

        This method calls five other methods:
            * self._write_supplemental_table_EMTRs()
              Writes out an Excel file containing CBO's baseline supplemental table
              for effective marginal tax rates (EMTRs) on capital income.

            * self._write_summary_metrics()
            Writes out values for all asset types or asset aggregates in the first year,
            or for all asset types by year.

            * self._write_values_biz()
              Writes out values for a given variable by either industry or asset type
                (but always also include by legal form, and financing source as well)
                for businesses.

            * self._write_values_by_industry_asset_agg()
              Writes out values for a given variable by industry and asset aggregates.

            * self._write_supplemental_table_tax_wedges()
              Writes out an Excel file containing CBO's baseline supplemental table for
              differences in total tax wedges.

        All methods called write out csv output files.

        Parameters
        ----------
        None
            Parameters are specified in the methods nested within this method.

        Returns
        -------
        None

        """
        print("Begin writing results")

        if (
            self.pol.policy_name == "Current-Law"
            and self.pol.perspective == "comprehensive"
        ):
            self._write_supplemental_table_EMTRs(
                self.metrics[id(self.output.total_EMTRs)]
            )

        self._write_summary_metrics(self.metrics)

        if self.pol.perspective == "comprehensive":
            self._write_values_biz(
                self.metrics[id(self.agg.weights)], by_var="asset_type"
            )

        self._write_values_biz(
            self.metrics[id(self.output.total_EMTRs)], by_var="asset_type"
        )
        self._write_values_biz(
            self.metrics[id(self.output.total_EMTRs)], by_var="industry"
        )

        self._write_values_by_industry_asset_agg(
            self.metrics[id(self.output.total_EMTRs)],
            asset_aggs=[
                "Nonresidential equipment",
                "Nonresidential structures",
                "Residential property",
                "R&D and own-account software",
                "Other intellectual property products",
                "Inventories",
                "All equipment, structures, IPP, and inventories",
                "Land",
                "All equipment, structures, IPP, inventories, and land",
            ],
            legal_form_key="biz",
            financing_key="typical (biz)",
        )

        # Only write out tax wedge supplemental table for Current-Law under the
        # uniformity perspective
        if (
            self.pol.policy_name == "Current-Law"
            and self.pol.perspective == "uniformity"
        ):
            disp_metrics = {}
            disp_metrics["wgtd_avg_abs_diffs"] = self.disp.total_tax_wedge[
                "wgtd_avg_abs_diffs"
            ]
            disp_metrics["wgtd_avg_abs_diffs"]["wgtd_avg_abs_diff"] = (
                disp_metrics["wgtd_avg_abs_diffs"]["wgtd_avg_abs_diff"] * 100
            ).round(decimals=2)
            self._write_supplemental_table_tax_wedges(
                self.metrics[id(self.output.total_tax_wedges)],
                disp_metrics["wgtd_avg_abs_diffs"],
            )

        return None

    def _write_out_csv(
        self, df=None, filename=None, header_str=None, years=None, write_index=False
    ):
        """Write out csv files with standard naming convention.

        Parameters
        ----------
        df : pd.DataFrame, default None
            DataFrame to be written out to csv file.
        filename : str, default None
            Root file name for new csv file.
        header_str : str, default None
            String to be written in first row of csv file, for documentation.
        years : list, default None
            Year(s) that are being written out.
        write_index : bool, default False
            Whether to write out the pd.DataFrame index values.

        Returns
        -------
        None
            Method writes out a csv file.

        """
        if len(years) == 1:
            years_str = str(years[0])
        elif len(years) == 2:
            years_str = f"{years[0]}_{years[1]}"

        full_filename = (
            f"{filename}_{years_str}_{self.pol.policy_name}_{self.pol.perspective}.csv"
        )
        output_file = f"{self.output_path}{full_filename}"

        with open(output_file, "w") as out_file:
            out_file.write(header_str + "\n")

        df.to_csv(
            output_file, mode="a", index=write_index, na_rep="NA", line_terminator="\n"
        )

        return None

    def _write_summary_metrics(self, metrics=None):
        """Write out a csv file with summary metrics.

        Method calls:
            * self._make_summary_df()
              Makes a DataFrame containg summary output for key model metrics.

            * self._write_out_csv()
              Writes out the csv output file.

        Parameters
        ----------
        metrics : dict
            A dictionary of model metrics to write out.

        Returns
        -------
        None
            Method writes out a csv file.

        """
        # Store data into DataFrame
        summary_df = self._make_summary_df(metrics)
        header_str = (
            f'"Key Model Metrics, by Asset Aggregate, Legal Form, and Financing Source, {START_YEAR} - {END_YEAR} '
            f'(returns and EMTRs are in percent; tax wedges are in percentage points; weights are in millions of dollars)"'
        )
        filename = "summary"
        years = [START_YEAR, END_YEAR]

        # Write out file
        self._write_out_csv(
            df=summary_df,
            filename=filename,
            header_str=header_str,
            years=years,
            write_index=False,
        )

        return None

    def _make_summary_df(self, metrics):
        """Make a DataFrame containg summary output for key model metrics.

        Parameters
        ----------
        metrics : OrderedDict
            Ordered dictionary of metric_labels:metrics to be written out.

        Returns
        -------
        df_out : pd.DataFrame
            DataFrame to be passed to self._write_out_csv()
            The DataFrame will have the following columns:
                weighting_method
                asset_aggs,
                legal_forms,
                financing,
                year,
                [metrics]

        """
        # Select relevant data
        names_dims = np.r_[NUM_ASSETS : NUM_ASSETS + NUM_ASSET_AGGS - 2]
        i_years = np.arange(NUM_YEARS)

        slice = np.ix_(
            [NUM_INDS],
            names_dims,
            [x for x in ALL_LEGAL_FORMS if x not in [LEGAL_FORMS["non_profit"]]],
            ALL_FINANCING_SOURCES,
            i_years,
        )

        # Set up category columns
        asset_aggs_labels = ASSET_TYPE_LABELS[names_dims].tolist()

        year_labels = []
        for i_year in i_years:
            year_labels.append(str(START_YEAR + i_year))

        category_labels = [
            asset_aggs_labels,
            [x for x in LEGAL_FORMS.keys() if x not in ["non_profit"]],
            FINANCING_SOURCES.keys(),
            year_labels,
        ]

        # Get cartesian product of category labels
        category_combos = list(itertools.product(*category_labels))

        category_column_labels = ["asset_aggs", "legal_forms", "financing", "year"]

        # Create a list that will contain a DataFrame with the method used and all the
        # category labels
        dfs = []
        df = pd.DataFrame(data=category_combos, columns=category_column_labels)
        df.insert(0, column="weighting_method", value=self.pol.perspective)

        # Then add columns for each of the variables in the metrics list
        for key in metrics.keys():
            df[metrics[key]["var_name"]] = (
                metrics[key]["var"][slice].flatten().round(decimals=4)
            )

        dfs.append(df)

        # Concatenate the two frames and return
        df_out = pd.concat(dfs, axis=0).round(decimals=2)

        return df_out

    def _write_values_biz(self, var_dict, by_var, year=START_YEAR):
        """Write out a csv file with values by either industry or asset type
        (but always also include by legal form, and financing source as well) for
        businesses.

        Method calls two other methods:
            * self._set_index_year()
            * self._write_out_csv()

        The first method sets i_year based on year - START_YEAR. The second method
        writes out the csv output file.

        Parameters
        ----------
        var_dict : dict
            Contains 4 keys: 'var', 'var_name', 'var_label', and 'units'
            'variable' key contains a np.ndarray object, indexed by:
                industry,
                asset_type,
                legal_form,
                financing_source, and
                year
        by_var : str
            String determining whether values get written by industry or asset type.
        year : int
            Year to be written out. Default value = START_YEAR.

        Returns
        -------
        None
            Method writes out a csv file.

        """
        i_year = self._set_index_year(year)

        # Set up labels for legal form and financing source
        legal_form_abbreviations = ["c_corp", "pass_thru", "biz"]
        legal_form_labels = ["C Corporations", "Pass-through Entities", "Businesses"]
        legal_forms_zip = zip(legal_form_abbreviations, legal_form_labels)
        financing_labels = ["Equity", "Debt", "Typical (Biz)"]

        # Set up industry- or asset type-specific variables
        if by_var == "industry":
            if self.include_land == True:
                asset_agg_name = "All equipment, structures, IPP, inventories, and land"
            else:
                asset_agg_name = "All equipment, structures, IPP, and inventories"

        # Create DataFrame to store output
        dfs = []
        for legal_form_abbreviation, legal_form_label in legal_forms_zip:
            cols = pd.MultiIndex.from_product([[legal_form_label], financing_labels])

            # Create appropriate slice depending on by_var
            if by_var == "industry":
                var_slice = var_dict["var"][
                    ALL_INDS_PLUS_AGG,
                    ASSET_TYPE_INDEX[asset_agg_name],
                    LEGAL_FORMS[legal_form_abbreviation],
                    FINANCING_SOURCES["typical_equity"] : FINANCING_SOURCES[
                        "typical (biz)"
                    ]
                    + 1,
                    i_year,
                ]
                df_index = INDUSTRY_LABELS

            elif by_var == "asset_type":
                var_slice = var_dict["var"][
                    NUM_INDS,
                    ALL_ASSETS_PLUS_AGGS,
                    LEGAL_FORMS[legal_form_abbreviation],
                    FINANCING_SOURCES["typical_equity"] : FINANCING_SOURCES[
                        "typical (biz)"
                    ]
                    + 1,
                    i_year,
                ]
                df_index = ASSET_TYPE_LABELS

            df = pd.DataFrame(var_slice, index=df_index, columns=cols)
            dfs.append(df)

        df_out = pd.concat(dfs, axis=1).round(decimals=2)

        if by_var == "industry":
            title = "Industry"
        elif by_var == "asset_type":
            title = "Asset Type"

        self._write_out_csv(
            df=df_out,
            filename=f"{var_dict['var_name']}_by_{by_var}_legal_form_financing",
            header_str=f"\"{var_dict['var_label']} by {title}, Legal Form, and Financing Source, "
            f"{YEARS[i_year]} ({var_dict['units']})\"",
            years=[year],
            write_index=True,
        )

        return None

    def _write_values_by_industry_asset_agg(
        self, var_dict, asset_aggs, legal_form_key, financing_key, year=START_YEAR
    ):
        """Write out a csv file with values by industry and asset aggregate.

        Method calls two other methods:
            * self._set_index_year()
            * self._write_out_csv()

        The first method sets i_year based on year - START_YEAR. The second method
        writes out the csv output file.

        Parameters
        ----------
        var_dict : dict
            Contains 5 keys: 'var', 'scaled_var', 'var_name', 'var_label', and 'units'
            'var' key contains a np.ndarray object, indexed by:
                industry,
                asset_type,
                legal_form,
                financing, and
                year
        asset_aggs : np.ndarray
            Asset aggregates considered.
        legal_form_key : str
            String with key for legal form dictionary (defined in constants.py).
        financing_key : str
            String with key for financing source dictionary (defined in constants.py).
        year : int
            Year to be written out. Default value = START_YEAR.

        Returns
        -------
        None
            Method writes out a csv file.

        """
        i_year = self._set_index_year(year)

        # Combine information into one DataFrame
        dfs = []
        for asset_agg in asset_aggs:
            cols = pd.Index([asset_agg])
            df = pd.DataFrame(
                var_dict["var"][
                    ALL_INDS_PLUS_AGG,
                    ASSET_TYPE_INDEX[asset_agg],
                    LEGAL_FORMS[legal_form_key],
                    FINANCING_SOURCES[financing_key],
                    i_year,
                ],
                index=INDUSTRY_LABELS,
                columns=cols,
            )
            dfs.append(df)
        df_out = pd.concat(dfs, axis=1).round(decimals=2)

        self._write_out_csv(
            df=df_out,
            filename=f"{var_dict['var_name']}_by_industry_asset_agg",
            header_str=f'"Values by Industry and Asset Aggregate, '
            f"{YEARS[i_year]} ({var_dict['units']})\"",
            years=[year],
            write_index=True,
        )

        return None

    def _write_supplemental_table_EMTRs(self, EMTRs_dict):
        """Write out an Excel file containing CBO's baseline supplemental table for
        effective marginal tax rates (EMTRs) on capital income.

        This method calls other two methods:
            * self._create_supplemental_EMTRs_df()
            * self._create_formats()

        Parameters
        ----------
        EMTRs_dict : dict
            Dictionary containing information on EMTRs to be written out.

        Returns
        -------
        None
            Writes out an Excel file.

        """
        filename = f"{self.output_path}supplemental_table_EMTRs_{self.pol.policy_name}_{self.pol.perspective}.xlsx"
        writer = pd.ExcelWriter(filename, engine="xlsxwriter")
        workbook = writer.book

        (
            supplemental_df,
            small_positives_exist,
            small_negatives_exist,
        ) = self._create_supplemental_EMTRs_df(EMTRs_dict)

        supplemental_df.to_excel(
            writer,
            sheet_name="EMTR on Capital Income",
            startrow=9,
            startcol=1,
            header=False,
            index=False,
        )

        formats = self._create_formats(workbook)

        worksheet = writer.sheets["EMTR on Capital Income"]

        if small_positives_exist:
            worksheet.conditional_format(
                "B12:L38",
                {
                    "type": "cell",
                    "criteria": "between",
                    "minimum": 0.001,
                    "maximum": 0.049,
                    "format": formats["asterisk"],
                },
            )
        if small_negatives_exist:
            worksheet.conditional_format(
                "B12:L38",
                {
                    "type": "cell",
                    "criteria": "between",
                    "minimum": -0.049,
                    "maximum": -0.001,
                    "format": formats["double_asterisk"],
                },
            )

        # Rows and columns are zero-indexed
        worksheet.set_column(0, 0, 65)  # Set column A to a width of 65
        worksheet.set_column(
            1, NUM_YEARS + 1, 9, formats["data"]
        )  # Set columns B:L to a width of 9

        worksheet.write(
            4,
            0,
            "Effective Marginal Tax Rates on Capital Income, by Tax Year",
            formats["bold"],
        )
        worksheet.write(5, 0, "Percent", formats["normal"])

        years = [x for x in range(START_YEAR, START_YEAR + NUM_YEARS)]
        for col_num, year in enumerate(years):
            worksheet.write(8, 1 + col_num, year, formats["col_label"])

        worksheet.write(
            10, 0, "All Assets Arising From New Investment", formats["bold"]
        )

        worksheet.write(11, 0, "Overall", formats["normal"])

        worksheet.write(13, 0, "Business Assets", formats["normal"])
        worksheet.write(14, 0, "By asset type", formats["indent"])
        worksheet.write(15, 0, "Nonresidential equipment", formats["indent2"])
        worksheet.write(16, 0, "Nonresidential structures", formats["indent2"])
        worksheet.write(17, 0, "Residential property", formats["indent2"])
        worksheet.write(18, 0, "R&D and own-account software", formats["indent2"])
        worksheet.write(
            19, 0, "Other intellectual property products", formats["indent2"]
        )
        worksheet.write(20, 0, "Inventories", formats["indent2"])
        worksheet.write(21, 0, "By source of financing", formats["indent"])
        worksheet.write(22, 0, "Equity-financed", formats["indent2"])
        worksheet.write(23, 0, "Debt-financed", formats["indent2"])
        worksheet.write(24, 0, "By legal form of organization", formats["indent"])
        worksheet.write(25, 0, "C corporations", formats["indent2"])
        worksheet.write(26, 0, "Pass-through entities", formats["indent2"])

        worksheet.write(28, 0, "Owner-Occupied Housing Structures", formats["normal"])
        worksheet.write(29, 0, "By source of financing", formats["indent"])
        worksheet.write(30, 0, "Equity-financed", formats["indent2"])
        worksheet.write(31, 0, "Debt-financed", formats["indent2"])

        worksheet.write(33, 0, "Memorandum", formats["bold"])
        worksheet.write(34, 0, "Overall, Including Land", formats["normal"])
        worksheet.write(35, 0, "Business Assets, Including Land", formats["normal"])
        worksheet.write(36, 0, "Business land", formats["indent"])
        worksheet.write(
            37, 0, "Owner-Occupied Housing, Including Land", formats["normal"]
        )

        worksheet.write(
            40, 0, "Data source: Congressional Budget Office.", formats["normal"]
        )

        if small_positives_exist and small_negatives_exist:
            worksheet.write(
                42,
                0,
                "* = between zero and 0.05 percentage points; ** = between -0.05 percentage points and zero.",
                formats["normal"],
            )
        elif small_positives_exist:
            worksheet.write(
                42, 0, "* = between zero and 0.05 percentage points.", formats["normal"]
            )
        elif small_negatives_exist:
            worksheet.write(
                42,
                0,
                "** = between -0.05 percentage points and zero.",
                formats["normal"],
            )

        # Add lines
        for row in [6, 9, 39, 44]:
            for col in range(NUM_YEARS + 1):
                worksheet.write(row, col, "", formats["top_border"])

        # Set a fixed creation date, so each run doesn't produce differences in the binary Excel file.
        workbook.set_properties({"created": datetime.date(2021, 9, 2)})
        workbook.close()

        return None

    def _create_supplemental_EMTRs_df(self, EMTRs_dict):
        """Create a DataFrame with the effective marginal tax rates (EMTRs) to be
        written to the supplemental table file.

        This method calls self._get_values().

        Parameters
        ----------
        EMTRs_dict : dict
            Dictionary containing information on EMTRs to be written out.

        Returns
        -------
        supplemental_df : pd.DataFrame
            DataFrame containing the values to write out for the supplemental data file.
        small_positives_exist : Boolean
            True if any values in supplemental_df are between 0.001 and 0.049
        small_negatives_exist : Boolean
            True if any values in supplemental_df are between -0.049 and -0.001

        """
        all_assets_agg_with_land = (
            "All equipment, structures, IPP, inventories, and land"
        )
        all_assets_agg_without_land = "All equipment, structures, IPP, and inventories"

        dfs_out = []

        ## All Assets Arising From New Investment

        # Overall
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                NUM_INDS,
                all_assets_agg_without_land,
                "biz+ooh",
                "typical (biz+ooh)",
            )
        )

        # Business assets
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                NUM_INDS,
                all_assets_agg_without_land,
                "biz",
                "typical (biz)",
            )
        )

        # Business assets, by asset type
        asset_aggs = [
            "Nonresidential equipment",
            "Nonresidential structures",
            "Residential property",
            "R&D and own-account software",
            "Other intellectual property products",
            "Inventories",
        ]

        for asset_agg in asset_aggs:
            dfs_out.append(
                self._get_values(
                    EMTRs_dict, NUM_INDS, asset_agg, "biz", "typical (biz)"
                )
            )

        # Business assets, by financing source
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                NUM_INDS,
                all_assets_agg_without_land,
                "biz",
                "typical_equity",
            )
        )
        dfs_out.append(
            self._get_values(
                EMTRs_dict, NUM_INDS, all_assets_agg_without_land, "biz", "debt"
            )
        )

        # Business assets, by legal form of organization
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                NUM_INDS,
                all_assets_agg_without_land,
                "c_corp",
                "typical (biz)",
            )
        )
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                NUM_INDS,
                all_assets_agg_without_land,
                "pass_thru",
                "typical (biz)",
            )
        )

        # Owner-occupied housing, by source of financing
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                OOH_IND,
                all_assets_agg_without_land,
                "ooh",
                "typical (biz+ooh)",
            )
        )
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                OOH_IND,
                all_assets_agg_without_land,
                "ooh",
                "typical_equity",
            )
        )
        dfs_out.append(
            self._get_values(
                EMTRs_dict, OOH_IND, all_assets_agg_without_land, "ooh", "debt"
            )
        )

        ## Memorandum

        # Overall, including land
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                NUM_INDS,
                all_assets_agg_with_land,
                "biz+ooh",
                "typical (biz+ooh)",
            )
        )

        # Business assets, including land
        dfs_out.append(
            self._get_values(
                EMTRs_dict, NUM_INDS, all_assets_agg_with_land, "biz", "typical (biz)"
            )
        )

        # Business land
        dfs_out.append(
            self._get_values(EMTRs_dict, NUM_INDS, "Land", "biz", "typical (biz)")
        )

        # Owner-occupied housing, including land
        dfs_out.append(
            self._get_values(
                EMTRs_dict,
                OOH_IND,
                all_assets_agg_with_land,
                "ooh",
                "typical (biz+ooh)",
            )
        )

        supplemental_df = pd.concat(dfs_out, axis=1)

        small_positives_exist = (
            (supplemental_df > 0.001) & (supplemental_df < 0.049)
        ).any(axis=None)
        small_negatives_exist = (
            (supplemental_df < -0.001) & (supplemental_df > -0.049)
        ).any(axis=None)

        supplemental_df = supplemental_df.round(decimals=2)

        # Insert empty columns
        for col_pos in [0, 1, 3, 5, 12, 15, 18, 20, 23, 24]:
            supplemental_df.insert(col_pos, 0, "", allow_duplicates=True)

        # Transpose the DataFrame to get years as column labels
        supplemental_df = supplemental_df.transpose()

        return supplemental_df, small_positives_exist, small_negatives_exist

    def _write_supplemental_table_tax_wedges(
        self, total_tax_wedges_dict, wgtd_avg_abs_diffs_dict
    ):
        """Write out an Excel file containing CBO's baseline supplemental table with
        differences in tax wedges as uniformity measures.

        This method calls other two methods:
            * self._create_supplemental_tax_wedges_df()
            * self._create_formats()

        Parameters
        ----------
        total_tax_wedges_dict : dict
            Dictionary containing information on total tax wedges to be written out.
        wgtd_avg_abs_diffs_dict : dict
            Dictionary containing information on weighted average of absolute
            differences in tax wedges to be written out.

        Returns
        -------
        None
            Writes out an Excel file.

        """
        filename = f"{self.output_path}supplemental_table_tax_wedges_{self.pol.policy_name}_{self.pol.perspective}.xlsx"
        writer = pd.ExcelWriter(filename, engine="xlsxwriter")
        workbook = writer.book

        (
            supplemental_df,
            small_positives_exist,
            small_negatives_exist,
        ) = self._create_supplemental_tax_wedges_df(
            total_tax_wedges_dict, wgtd_avg_abs_diffs_dict
        )

        supplemental_df.to_excel(
            writer,
            sheet_name="Differences in Tax Wedges",
            startrow=9,
            startcol=1,
            header=False,
            index=False,
        )

        formats = self._create_formats(workbook)

        worksheet = writer.sheets["Differences in Tax Wedges"]

        if small_positives_exist:
            worksheet.conditional_format(
                "B11:L38",
                {
                    "type": "cell",
                    "criteria": "between",
                    "minimum": 0.001,
                    "maximum": 0.049,
                    "format": formats["asterisk"],
                },
            )

        if small_negatives_exist:
            worksheet.conditional_format(
                "B11:L38",
                {
                    "type": "cell",
                    "criteria": "between",
                    "minimum": -0.049,
                    "maximum": -0.001,
                    "format": formats["double_asterisk"],
                },
            )

        # Set column widths
        worksheet.set_column(0, 0, 65)  # Set column A to a width of 65
        worksheet.set_column(
            1, NUM_YEARS + 1, 9, formats["data"]
        )  # Set columns B:L to a width of 9

        # Set row heights for select rows
        worksheet.set_row(15, 3.75)
        worksheet.set_row(21, 3.75)
        worksheet.set_row(33, 3.75)
        worksheet.set_row(39, 3.75)

        # Write out table title and units
        worksheet.write(
            4,
            0,
            "Differences in Tax Wedges Among Types of New Investment, by Tax Year",
            formats["bold"],
        )
        worksheet.write(5, 0, "Percentage Points", formats["normal"])

        # Write year column labels
        years = [year for year in range(START_YEAR, START_YEAR + NUM_YEARS)]
        for col_num, year in enumerate(years):
            worksheet.write(8, 1 + col_num, year, formats["col_label"])

            # Also write out "____"s for differences
            worksheet.write(15, 1 + col_num, "____", formats["normal_right"])
            worksheet.write(21, 1 + col_num, "____", formats["normal_right"])
            worksheet.write(33, 1 + col_num, "____", formats["normal_right"])
            worksheet.write(39, 1 + col_num, "____", formats["normal_right"])

        # Write out table stubs
        worksheet.write(10, 0, "Tax Wedge for Business Assets", formats["bold"])

        worksheet.write(12, 0, "By source of financing", formats["indent"])
        worksheet.write(13, 0, "Equity-financed", formats["indent2"])
        worksheet.write(14, 0, "Debt-financed", formats["indent2"])
        worksheet.write(
            16, 0, "Difference between sources of financing", formats["italic_indent"]
        )

        worksheet.write(18, 0, "By legal form of organization", formats["indent"])
        worksheet.write(19, 0, "C corporations", formats["indent2"])
        worksheet.write(20, 0, "Pass-through entities", formats["indent2"])
        worksheet.write(
            22,
            0,
            "Difference between legal forms of organization",
            formats["italic_indent"],
        )

        worksheet.write(
            24,
            0,
            "Weighted mean absolute difference between all asset pairs",
            formats["italic_indent"],
        )
        worksheet.write(
            25,
            0,
            "Weighted mean absolute difference between all industry pairs",
            formats["italic_indent"],
        )

        worksheet.write(27, 0, "Tax Wedge for Owner-Occupied Housing", formats["bold"])
        worksheet.write(
            28,
            0,
            "Difference between owner-occupied housing and business assets",
            formats["italic_indent"],
        )

        worksheet.write(30, 0, "By source of financing", formats["indent"])
        worksheet.write(31, 0, "Equity-financed", formats["indent2"])
        worksheet.write(32, 0, "Debt-financed", formats["indent2"])
        worksheet.write(
            34, 0, "Difference between sources of financing", formats["italic_indent"]
        )

        worksheet.write(36, 0, "Memorandum", formats["bold"])
        worksheet.write(
            37, 0, "Tax Wedge for Owner-Occupied Housing Structures", formats["normal"]
        )
        worksheet.write(
            38, 0, "Tax Wedge for Renter-Occupied Housing Structures", formats["normal"]
        )
        worksheet.write(
            40,
            0,
            "Difference between owner- and renter-occupied housing structures",
            formats["italic_indent"],
        )

        worksheet.write(
            43, 0, "Data source: Congressional Budget Office.", formats["normal"]
        )

        if small_positives_exist and small_negatives_exist:
            worksheet.write(
                45,
                0,
                "* = between zero and 0.05 percentage points; ** = between -0.05 percentage points and zero.",
                formats["normal"],
            )
        elif small_positives_exist:
            worksheet.write(
                45, 0, "* = between zero and 0.05 percentage points.", formats["normal"]
            )
        elif small_negatives_exist:
            worksheet.write(
                45,
                0,
                "** = between -0.05 percentage points and zero.",
                formats["normal"],
            )

        # Add lines
        for row in [6, 9, 42, 47]:
            for col in range(NUM_YEARS + 1):
                worksheet.write(row, col, "", formats["top_border"])

        # Set a fixed creation date, so each run doesn't produce differences in the
        # binary Excel file.
        workbook.set_properties({"created": datetime.date(2021, 9, 2)})
        workbook.close()

        return None

    def _create_supplemental_tax_wedges_df(
        self, total_tax_wedges_dict, wgtd_avg_abs_diffs_dict
    ):
        """Create a DataFrame with the variables to be written to the supplemental
        table file with differences in tax wedges as measures of tax uniformity.

        This method calls two other methods:
            * self._get_values()
            * self._get_values_wgtd_avg_abs_diffs()

        Parameters
        ----------
        total_tax_wedges_dict : dict
            Dictionary containing information on total tax wedges to be written out.
        wgtd_avg_abs_diffs_dict : dict
            Dictionary containing information on weighted average of absolute
            differences to be written out.

        Returns
        -------
        supplemental_df : pd.DataFrame
            DataFrame containing the values to write out for the supplemental data file.
        small_positives_exist : Boolean
            True if any values in supplemental_df are between 0.001 and 0.049
        small_negatives_exist : Boolean
            True if any values in supplemental_df are between -0.049 and -0.001

        """
        all_assets_agg = "All equipment, structures, IPP, inventories, and land"
        industry_dim_name = "industries (including land)"

        dfs_out = []

        ## Tax wedge for business assets
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict, NUM_INDS, all_assets_agg, "biz", "typical (biz)"
            )
        )

        # Tax wedge for business assets, by source of financing
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict, NUM_INDS, all_assets_agg, "biz", "typical_equity"
            )
        )
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict, NUM_INDS, all_assets_agg, "biz", "debt"
            )
        )
        diff_biz_equity_debt = pd.DataFrame(
            (
                self._get_values(
                    total_tax_wedges_dict,
                    NUM_INDS,
                    all_assets_agg,
                    "biz",
                    "typical_equity",
                ).values
                - self._get_values(
                    total_tax_wedges_dict, NUM_INDS, all_assets_agg, "biz", "debt"
                ).values
            ),
            index=YEARS,
        )
        dfs_out.append(diff_biz_equity_debt)

        # Tax wedge for business assets, by legal form of organization
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict,
                NUM_INDS,
                all_assets_agg,
                "c_corp",
                "typical (biz)",
            )
        )
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict,
                NUM_INDS,
                all_assets_agg,
                "pass_thru",
                "typical (biz)",
            )
        )
        diff_c_corp_pass_thru = pd.DataFrame(
            (
                self._get_values(
                    total_tax_wedges_dict,
                    NUM_INDS,
                    all_assets_agg,
                    "c_corp",
                    "typical (biz)",
                ).values
                - self._get_values(
                    total_tax_wedges_dict,
                    NUM_INDS,
                    all_assets_agg,
                    "pass_thru",
                    "typical (biz)",
                ).values
            ),
            index=YEARS,
        )
        dfs_out.append(diff_c_corp_pass_thru)

        # Tax wedge for business assets, weighted average of absolute differences
        dfs_out.append(
            self._get_values_wgtd_avg_abs_diffs(
                wgtd_avg_abs_diffs_dict, "biz", "assets", all_assets_agg
            )
        )
        dfs_out.append(
            self._get_values_wgtd_avg_abs_diffs(
                wgtd_avg_abs_diffs_dict, "biz", industry_dim_name
            )
        )

        ## Tax wedge for owner-occupied housing
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict,
                OOH_IND,
                all_assets_agg,
                "ooh",
                "typical (biz+ooh)",
            )
        )

        # Difference between owner-occupied housing and business assets
        diff_ooh_biz = pd.DataFrame(
            (
                self._get_values(
                    total_tax_wedges_dict,
                    OOH_IND,
                    all_assets_agg,
                    "ooh",
                    "typical (biz+ooh)",
                ).values
                - self._get_values(
                    total_tax_wedges_dict,
                    NUM_INDS,
                    all_assets_agg,
                    "biz",
                    "typical (biz)",
                ).values
            ),
            index=YEARS,
        )
        dfs_out.append(diff_ooh_biz)

        # Tax wedge for owner-occupied housing, by source of financing
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict, OOH_IND, all_assets_agg, "ooh", "typical_equity"
            )
        )
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict, OOH_IND, all_assets_agg, "ooh", "debt"
            )
        )
        diff_ooh_equity_debt = pd.DataFrame(
            (
                self._get_values(
                    total_tax_wedges_dict,
                    OOH_IND,
                    all_assets_agg,
                    "ooh",
                    "typical_equity",
                ).values
                - self._get_values(
                    total_tax_wedges_dict, OOH_IND, all_assets_agg, "ooh", "debt"
                ).values
            ),
            index=YEARS,
        )
        dfs_out.append(diff_ooh_equity_debt)

        ## Memorandum
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict,
                OOH_IND,
                "Residential buildings",
                "ooh",
                "typical (biz+ooh)",
            )
        )
        dfs_out.append(
            self._get_values(
                total_tax_wedges_dict,
                REAL_ESTATE_IND,
                "Residential buildings",
                "biz",
                "typical (biz)",
            )
        )
        diff_ooh_roh = pd.DataFrame(
            (
                self._get_values(
                    total_tax_wedges_dict,
                    OOH_IND,
                    "Residential buildings",
                    "ooh",
                    "typical (biz+ooh)",
                ).values
                - self._get_values(
                    total_tax_wedges_dict,
                    REAL_ESTATE_IND,
                    "Residential buildings",
                    "biz",
                    "typical (biz)",
                ).values
            ),
            index=YEARS,
        )
        dfs_out.append(diff_ooh_roh)

        supplemental_df = pd.concat(dfs_out, axis=1)

        small_positives_exist = (
            (supplemental_df > 0.001) & (supplemental_df < 0.049)
        ).any(axis=None)
        small_negatives_exist = (
            (supplemental_df < -0.001) & (supplemental_df > -0.049)
        ).any(axis=None)

        supplemental_df = supplemental_df.round(decimals=2)

        # Insert empty columns
        for col_pos in [0, 2, 3, 6, 8, 9, 12, 14, 17, 20, 21, 24, 26, 27, 30]:
            supplemental_df.insert(col_pos, 0, "", allow_duplicates=True)

        # Transpose the DataFrame to get years as column labels
        supplemental_df = supplemental_df.transpose()

        return supplemental_df, small_positives_exist, small_negatives_exist

    def _get_values(
        self, var_dict, industry_index, asset_agg, legal_form, financing_source
    ):
        """Get values to write out by asset aggregation, legal form, and financing
        source.

        All values contain all years.

        Parameters
        ----------
        var_dict : dict
            Dictionary containing information on variable to be written out.
        industry_index : np.float
            Index of industry to select values by.
        asset_agg : str
            Name of asset type aggregation to select values by.
        legal_form : str
            Name of legal form of organization to select values by.
        financing_source : str
            Name of finaincing source to select values by.

        Returns
        -------
        col : pd.DataFrame
            A single column pandas DataFrame with a 3 row header indicating the asset
            type aggregation, legal form, and financing source.

        """
        col_names = pd.MultiIndex.from_product(
            [[asset_agg], [legal_form], [financing_source]]
        )

        col = pd.DataFrame(
            var_dict["var"][
                industry_index,
                ASSET_TYPE_INDEX[asset_agg],
                LEGAL_FORMS[legal_form],
                FINANCING_SOURCES[financing_source],
                :NUM_YEARS,
            ].transpose(),
            index=YEARS,
            columns=col_names,
        )

        return col

    def _get_values_wgtd_avg_abs_diffs(
        self, var_dict, legal_form, dimension, asset_agg=None
    ):
        """Get values to write out by legal form and dimension along which weighted
        average of absolute differences is calculated.

        All values contain all years.

        Parameters
        ----------
        var_dict : dict
            Dictionary containing information on variable to be written out.
        legal_form : str
            Name of legal form of organization to select values by.
        dimension : str
            Dimension considered for weighted average. Can take values 'assets',
            'industries (excluding land)', or 'industries (including land)'.
        asset_agg : str
            Name of asset type aggregation to select values by. Default is None, which
            is used when dimension = 'industries'.

        Returns
        -------
        col : pd.DataFrame
            A single column pandas DataFrame with a 3 row header indicating the
            dimension along which to get weighted average of absolute differences, the
            legal form, and a label for the weighted average considered.

        """
        if dimension == "assets":
            if asset_agg is None:
                raise ValueError(
                    'Asset aggregate must be specified when dimension = "assets"'
                )
            agg_name = asset_agg
            label = "Difference Among Asset Types"
        elif dimension in [
            "industries (excluding land)",
            "industries (including land)",
        ]:
            agg_name = "All Industries"
            label = "Difference Among Industries"
        else:
            raise ValueError(
                'dimension must be equal to "assets", "industries (excluding land)" '
                'or "industries (including land)"'
            )

        var = var_dict[(var_dict["dimension"] == dimension)]

        col_names = pd.MultiIndex.from_product([[agg_name], [legal_form], [label]])

        col = pd.DataFrame(
            data=np.array(
                [
                    var.loc[
                        (var["aggregation"] == agg_name)
                        & (var["legal_form"] == legal_form),
                        "wgtd_avg_abs_diff",
                    ]
                ]
            ).transpose(),
            index=YEARS,
            columns=col_names,
        )

        return col

    def _create_formats(self, workbook):
        """Create format objects for xlsxwriter.

        Parameters
        ----------
        workbook : xlsxwriter.Workbook
            Excel workbook to be written out.

        Returns
        -------
        formats : dict

        """
        formats = {
            "normal": workbook.add_format({"font": "Arial", "size": 11}),
            "normal_right": workbook.add_format(
                {"font": "Arial", "size": 11, "align": "right"}
            ),
            "bold": workbook.add_format({"bold": True, "font": "Arial", "size": 11}),
            "italic_indent": workbook.add_format(
                {"italic": True, "font": "Arial", "size": 11, "indent": 1}
            ),
            "indent": workbook.add_format({"font": "Arial", "size": 11, "indent": 1}),
            "indent2": workbook.add_format({"font": "Arial", "size": 11, "indent": 2}),
            "top_border": workbook.add_format({"top": 1, "bottom": 0}),
            "data": workbook.add_format(
                {
                    "bold": False,
                    "valign": "top",
                    "align": "right",
                    "font": "Arial",
                    "size": 11,
                    "num_format": "#,##0.0",
                }
            ),
            "col_label": workbook.add_format(
                {
                    "bold": False,
                    "font": "Arial",
                    "size": 11,
                    "align": "right",
                    "num_format": "0_)",
                    "top": None,
                    "right": None,
                    "left": None,
                }
            ),
            "asterisk": workbook.add_format({"num_format": '"*";"*"'}),
            "double_asterisk": workbook.add_format({"num_format": '"**";"**"'}),
        }

        return formats

    def _set_index_year(self, year):
        """Set i_year based on year - START_YEAR.

        Parameters
        ----------
        year : int
            Year of data to write out.

        Returns
        -------
        i_year : int
            0-based index, starting at START_YEAR = 0.

        """
        if year < START_YEAR:
            raise ValueError("year must be >= START_YEAR")
        else:
            i_year = year - START_YEAR

        return i_year
