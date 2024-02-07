"""Define various constants used in the model."""
import os
import numpy as np


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


# Years
# --------------------------------------------------------------------------------------
NUM_YEARS = 11
ALL_YEARS = np.arange(NUM_YEARS)
START_YEAR = 2024
END_YEAR = START_YEAR + NUM_YEARS - 1
YEARS = np.arange(START_YEAR, START_YEAR + NUM_YEARS)

# Industries
# --------------------------------------------------------------------------------------
# Industries labels
with open(CURRENT_PATH + "/data/inputs/labels/industry_labels.txt") as f:
    INDUSTRY_LABELS = np.array([line.rstrip() for line in f])

NUM_INDS = len(INDUSTRY_LABELS) - 1
NUM_DETAILED_INDS = 88

NUM_IND_AGGS = 1
LEN_INDS = NUM_INDS + NUM_IND_AGGS

# Arrays including industry indexes
ALL_INDS = np.r_[:NUM_INDS]
ALL_INDS_PLUS_AGG = np.r_[: NUM_INDS + 1]

# Financial industries:
#    Credit intermediation
#    Securities, commodity contracts, and other financial investments
#    Insurance
#    Other financial vehicles
#    Professional, scientific, and technical services
ALL_FINANCIAL_INDS = np.r_[40:44, 46]
ALL_NONFINANCIAL_INDS = np.r_[0:40, 44:46, 47 : NUM_INDS - 1]

REAL_ESTATE_IND = 44

# Businesses vs. owner-occupied housing industries
ALL_BIZ_INDS = np.r_[: NUM_INDS - 1]
NUM_BIZ_INDS = len(ALL_BIZ_INDS)

# Owner-occupied housing (OOH) is included as the last element in the industry dimension
OOH_IND = NUM_INDS - 1
OOH_IND_DETAILED = NUM_DETAILED_INDS - 1
OOH_NUM_INDS = 1

# Index positions for industries
INDUSTRY_INDEX = {}
for i in ALL_INDS_PLUS_AGG:
    INDUSTRY_INDEX[INDUSTRY_LABELS[i]] = i

# Legal forms of organizaion
# --------------------------------------------------------------------------------------
# Legal form labels
LEGAL_FORM_LABELS = np.array(
    [
        "C Corporations",
        "Pass-through Entities",
        "Owner-occupied Housing",
        "Non-Profits",
        "Businesses",
        "All Legal Forms",
    ]
)

# Legal form indexes
LEGAL_FORMS = {}
LEGAL_FORMS["c_corp"] = 0
LEGAL_FORMS["pass_thru"] = 1
LEGAL_FORMS["ooh"] = 2
LEGAL_FORMS["non_profit"] = 3
LEGAL_FORMS["biz"] = 4  # 'c_corp' and 'pass_thru'
LEGAL_FORMS["biz+ooh"] = 5  # 'c_corp', 'pass_thru', and 'ooh'

NUM_BIZ = 2  # 'c_corp' and 'pass_thru'
NUM_FOR_PROFIT_LEGAL_FORMS = 3  # 'c_corp', 'pass_thru', and 'ooh'

LEN_LEGAL_FORMS = len(LEGAL_FORMS)

# Array including legal form indexes
ALL_LEGAL_FORMS = np.arange(LEN_LEGAL_FORMS)

# Financing sources
# --------------------------------------------------------------------------------------
# Financing sources labels
FINANCING_SOURCE_LABELS = np.array(
    [
        "New Equity",
        "Retained Earnings",
        "Equity",
        "Debt",
        "Typical Financing (Businesses)",
        "Typical Financing (Businesses + OOH)",
    ]
)

# Financing sources indexes
FINANCING_SOURCES = {}
FINANCING_SOURCES["new_equity"] = 0
FINANCING_SOURCES["retained_earnings"] = 1
FINANCING_SOURCES[
    "typical_equity"
] = 2  # weighted average of new_equity and retained_earnings
FINANCING_SOURCES["debt"] = 3
FINANCING_SOURCES["typical (biz)"] = 4
FINANCING_SOURCES["typical (biz+ooh)"] = 5

NUM_EQUITY = 3
NUM_FINANCING_SOURCES = 4

LEN_FINANCING_SOURCES = len(FINANCING_SOURCES)

# Array including financing indexes
ALL_FINANCING_SOURCES = np.arange(LEN_FINANCING_SOURCES)

# Account categories
# --------------------------------------------------------------------------------------
# Account categories labels
ACCOUNT_CATEGORY_LABELS = np.array(
    ["Fully Taxable", "Temporarily Deferred", "Nontaxable", "Typical"]
)

# Account categories indexes
ACCOUNT_CATEGORIES = {}
ACCOUNT_CATEGORIES["taxable"] = 0
ACCOUNT_CATEGORIES["deferred"] = 1
ACCOUNT_CATEGORIES["nontaxable"] = 2
ACCOUNT_CATEGORIES["typical"] = 3

LEN_ACCOUNT_CATEGORIES = len(ACCOUNT_CATEGORIES)

# Asset types
# --------------------------------------------------------------------------------------
# Asset types labels
with open(CURRENT_PATH + "/data/inputs/labels/asset_type_labels.txt") as f:
    ASSET_TYPE_LABELS = np.array([line.rstrip() for line in f])

NUM_EQUIPMENT = 32
NUM_STRUCTURES = 23
NUM_IPP = 19
NUM_NON_BEA_INTANGIBLES = 2  # Place holder for Non-BEA intangibles
NUM_RESIDENTIAL = 2
NUM_INVENTORIES = 1
NUM_LAND = 1
NUM_NON_BEA_NATURAL_RESOURCES = 3  # Place holder for Non-BEA natural resources

NUM_ASSETS = (
    NUM_EQUIPMENT
    + NUM_STRUCTURES
    + NUM_IPP
    + NUM_NON_BEA_INTANGIBLES
    + NUM_RESIDENTIAL
    + NUM_INVENTORIES
    + NUM_LAND
    + NUM_NON_BEA_NATURAL_RESOURCES
)

ALL_ASSETS = np.r_[:NUM_ASSETS]

# Start and end positions for asset classes
START_EQUIPMENT = 0
END_EQUIPMENT = NUM_EQUIPMENT

START_STRUCTURES = END_EQUIPMENT
END_STRUCTURES = START_STRUCTURES + NUM_STRUCTURES

START_IPP = END_STRUCTURES
END_IPP = START_IPP + NUM_IPP + NUM_NON_BEA_INTANGIBLES

START_RESIDENTIAL = END_IPP
END_RESIDENTIAL = START_RESIDENTIAL + NUM_RESIDENTIAL
RESIDENTIAL_EQUIP = END_IPP
RESIDENTIAL_STRUCT = END_IPP + 1

START_INVENTORIES = RESIDENTIAL_STRUCT + 1
END_INVENTORIES = START_INVENTORIES + NUM_INVENTORIES

START_LAND = END_INVENTORIES
END_LAND = START_LAND + NUM_LAND + NUM_NON_BEA_NATURAL_RESOURCES

assert END_LAND == NUM_ASSETS

ALL_NONRES_EQUIPMENT = np.r_[START_EQUIPMENT:END_EQUIPMENT]
ALL_EQUIPMENT = np.r_[START_EQUIPMENT:END_EQUIPMENT, RESIDENTIAL_EQUIP]
ALL_NONRES_STRUCTURES = np.r_[START_STRUCTURES:END_STRUCTURES]
ALL_STRUCTURES = np.r_[START_STRUCTURES:END_STRUCTURES, RESIDENTIAL_STRUCT]
ALL_IPP = np.r_[START_IPP:END_IPP]
ALL_RESIDENTIAL = np.r_[START_RESIDENTIAL:END_RESIDENTIAL]
ALL_INVENTORIES = np.r_[START_INVENTORIES:END_INVENTORIES]
ALL_LAND = np.r_[START_LAND:END_LAND]

# Numbers of IPP assets
NUM_MINERAL = 8  # Mineral exploration and development
NUM_SOFTWARE = 2  # Purchased software
NUM_RESEARCH = 4  # Developed software & research and development
NUM_ENTERTAINMENT = 5  # Entertainment, literary, and artistic originals
NUM_NON_BEA_INTANGIBLES = 2  # All non-BEA intangible assets

ALL_MINERAL = np.r_[START_IPP : START_IPP + NUM_MINERAL]
ALL_SOFTWARE = np.r_[ALL_MINERAL[-1] + 1 : ALL_MINERAL[-1] + 1 + NUM_SOFTWARE]
ALL_RESEARCH = np.r_[ALL_SOFTWARE[-1] + 1 : ALL_SOFTWARE[-1] + 1 + NUM_RESEARCH]
ALL_ENTERTAINMENT = np.r_[
    ALL_RESEARCH[-1] + 1 : ALL_RESEARCH[-1] + 1 + NUM_ENTERTAINMENT
]
ALL_NON_BEA_INTANGIBLES = np.r_[
    ALL_ENTERTAINMENT[-1] + 1 : ALL_ENTERTAINMENT[-1] + 1 + NUM_NON_BEA_INTANGIBLES
]

ALL_NON_RESEARCH_IPP = np.r_[
    ALL_MINERAL, ALL_SOFTWARE, ALL_ENTERTAINMENT, ALL_NON_BEA_INTANGIBLES
]

# Define which asset aggregations to use
USE_NIPA_ASSET_AGGS = True

if USE_NIPA_ASSET_AGGS is True:
    ALL_NONRES_STRUCTURES_PLUS_MINERAL = np.r_[ALL_NONRES_STRUCTURES, ALL_MINERAL]
    ALL_STRUCTURES_PLUS_MINERAL = np.r_[ALL_STRUCTURES, ALL_MINERAL]
    ALL_IPP_MINUS_MINERAL = [x for x in ALL_IPP if x not in ALL_MINERAL]
    ALL_NON_RESEARCH_IPP_MINUS_MINERAL = [
        x for x in ALL_NON_RESEARCH_IPP if x not in ALL_MINERAL
    ]
elif USE_NIPA_ASSET_AGGS is False:
    ALL_NONRES_STRUCTURES_PLUS_MINERAL = ALL_NONRES_STRUCTURES
    ALL_STRUCTURES_PLUS_MINERAL = ALL_STRUCTURES
    ALL_IPP_MINUS_MINERAL = ALL_IPP
    ALL_NON_RESEARCH_IPP_MINUS_MINERAL = ALL_NON_RESEARCH_IPP

ALL_EQUIP_STRUCT = np.r_[ALL_EQUIPMENT, ALL_STRUCTURES_PLUS_MINERAL]
ALL_EQUIP_STRUCT_INVENT = np.r_[
    ALL_EQUIPMENT, ALL_STRUCTURES_PLUS_MINERAL, ALL_INVENTORIES
]
ALL_EQUIP_STRUCT_INVENT_LAND = np.r_[
    ALL_EQUIPMENT, ALL_STRUCTURES_PLUS_MINERAL, ALL_INVENTORIES, ALL_LAND
]
ALL_EQUIP_STRUCT_IPP = np.r_[ALL_EQUIPMENT, ALL_STRUCTURES, ALL_IPP]
ALL_EQUIP_STRUCT_IPP_INVENT = np.r_[
    ALL_EQUIPMENT, ALL_STRUCTURES, ALL_IPP, ALL_INVENTORIES
]

# Main asset aggregates
ASSET_AGGS = (
    ALL_NONRES_EQUIPMENT,
    ALL_NONRES_STRUCTURES_PLUS_MINERAL,
    ALL_RESIDENTIAL,
    ALL_RESEARCH,
    ALL_NON_RESEARCH_IPP_MINUS_MINERAL,
    ALL_EQUIP_STRUCT_IPP_INVENT,
    ALL_ASSETS,
    ALL_EQUIP_STRUCT_INVENT,
    ALL_EQUIP_STRUCT_INVENT_LAND,
)

NUM_ASSET_AGGS = len(ASSET_AGGS)
LEN_ASSETS = NUM_ASSETS + NUM_ASSET_AGGS

# Arrays including asset indexes
ALL_ASSET_AGGS = np.r_[NUM_ASSETS : NUM_ASSETS + NUM_ASSET_AGGS]
ALL_ASSETS_PLUS_AGGS = np.r_[: NUM_ASSETS + NUM_ASSET_AGGS]

# Index positions for asset types and aggregates
ASSET_TYPE_INDEX = {}
for i in ALL_ASSETS_PLUS_AGGS:
    ASSET_TYPE_INDEX[ASSET_TYPE_LABELS[i]] = i

ALL_OOH_ASSETS = np.r_[
    ASSET_TYPE_INDEX["Residential buildings"], ASSET_TYPE_INDEX["Land"]
]

# Components of asset type/industry adjustments applied to tax rates
# --------------------------------------------------------------------------------------
TAX_RATE_ADJUSTMENTS_COMPONENTS = {"eligibility": 0, "rate": 1}

NUM_TAX_RATE_ADJUSTMENTS_COMPONENTS = len(TAX_RATE_ADJUSTMENTS_COMPONENTS)

# Aggregate debt shares, derived from Federal Reserve Financial Accounts of the United 
# States (FAOTUS)
# DO NOT EDIT THESE.
# --------------------------------------------------------------------------------------
AGG_DEBT_SHARE = {
    "financial_sector": 0.4932,
    "nonfin_c_corp": 0.2750,
    "nonfin_pass_thru": 0.3054,
    "ooh": 0.4136,
}
