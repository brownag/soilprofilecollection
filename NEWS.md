# soilprofilecollection 0.2.1

- Pinned pandas version to `>=2.2.3` to ensure access to modern APIs.
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
