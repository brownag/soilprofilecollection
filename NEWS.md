# soilprofilecollection 0.3.1
- Bug fix in `.from_dataframe()`:                                                                                                                               
  - Changed inference to check if standard names exist in the schema, and raise a ValueError if they don't (instead of silently defaulting), but allowing user-provided idname/hzidname/depthcols to pass through to the constructor.                                                                                                                                                  
# soilprofilecollection 0.3.0

- **BREAKING**: matplotlib is now an optional dependency. Install with `pip install soilprofilecollection[plot]` to use the `.plot()` method.
  - Updated README with installation instructions for both basic and plotting modes
- mkdocstrings-python moved to dev dependencies (only needed for building documentation)
- Improved `.from_dataframe()`: now automatically infers standard column names from schema template
  - No need to repeat `idname`, `hzidname`, `depthcols`, and `hzdesgncol` parameters
- Fixed slicing bug in `__getitem__` where profile ID column was dropped when selecting specific horizons within profiles


# soilprofilecollection 0.2.1

- Resolved a `FutureWarning` in `pandas` by explicitly setting `include_groups=False` in a `groupby().apply()` call.

# soilprofilecollection 0.2.0

-  Added pytest test suite with fixtures and test coverage for core functionality
-  Added `.from_dataframe()` utility function for schema-based data import
-  Removed debug print statements throughout the codebase and streamlined error handling

# soilprofilecollection 0.1.0

- Basic implementation of SoilProfileCollection object
  - Site and Horizon Data
  - Profile and Horizon IDs
  - CRS information and Metadata
  - Indexing with `[i,j]`
  
- Added SoilProfileCollection `.profile_apply()` `.glom()` and `.plot()` methods
  - `.glom()` method does both slicing/intersection and aggregation
