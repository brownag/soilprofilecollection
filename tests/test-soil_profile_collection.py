import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from soilprofilecollection import SoilProfileCollection

# Create sample data similar to aqp examples
# Profile 1
p1_horizons = pd.DataFrame({
    'id': ['P1'] * 4,
    'hzid': ['H1', 'H2', 'H3', 'H4'],
    'top': [0, 10, 25, 50],
    'bottom': [10, 25, 50, 80],
    'hzname': ['A', 'Bt1', 'Bt2', 'C'],
    'clay': [15, 35, 40, 20],
    'color': ['#A0522D', '#8B4513', '#8B4513', '#D2B48C'] # Sienna, SaddleBrown, Tan
})

# Profile 2
p2_horizons = pd.DataFrame({
    'id': ['P2'] * 3,
    'hzid': ['H5', 'H6', 'H7'],
    'top': [0, 15, 40],
    'bottom': [15, 40, 100],
    'hzname': ['Ap', 'Bw', 'BC'],
    'clay': [20, 28, 25],
    'color': ['#654321', '#A0522D', '#CD853F'] # DarkBrown, Sienna, Peru
})

# Profile 3 (Shallow)
p3_horizons = pd.DataFrame({
    'id': ['P3'] * 2,
    'hzid': ['H8', 'H9'],
    'top': [0, 5],
    'bottom': [5, 20],
    'hzname': ['O', 'R'],
    'clay': [5, 2], # Low clay
    'color': ['#000000', '#808080'] # Black, Gray
})


all_horizons = pd.concat([p1_horizons, p2_horizons, p3_horizons], ignore_index=True)

# Site data (optional, can be inferred)
site_data = pd.DataFrame({
    'id': ['P1', 'P2', 'P3'],
    'x': [100, 150, 120],
    'y': [200, 210, 190],
    'site_name': ['Site Alpha', 'Site Beta', 'Site Gamma']
})

# --- Create SoilProfileCollection ---
try:
    spc = SoilProfileCollection(
        horizons=all_horizons,
        site=site_data,
        idname='id',
        hzidname='hzid',
        depthcols=('top', 'bottom'),
        hzdesgncol='hzname',
        metadata={'project': 'Demo', 'location': 'Test Area'},
        crs='EPSG:4326' # Example CRS
    )

    # --- Demonstrate Methods ---
    print("--- SPC Object ---")
    print(spc)
    print("\n--- Length (Number of Profiles) ---")
    print(len(spc))

    print("\n--- Profile IDs ---")
    print(spc.profile_ids)

    print("\n--- Site Data ---")
    print(spc.site)

    print("\n--- Horizon Data (first 5 rows) ---")
    print(spc.horizons.head())

    print("\n--- Max Depths per Profile ---")
    print(spc.depths())
    
    print("\n--- Horizon Thicknesses (first 5) ---")
    print(spc.thickness().head())

    print("\n--- Get Horizons for Profile 'P1' ---")
    print(spc.get_profile('P1'))

    print("\n--- Subsetting ---")
    spc_subset1 = spc[0] # First profile by index
    print(f"Subset by index 0:\n{spc_subset1}")

    spc_subset2 = spc[['P1', 'P3']] # Profiles by ID
    print(f"\nSubset by IDs ['P1', 'P3']:\n{spc_subset2}")
    
    spc_subset3 = spc[1:3] # Slice of profiles
    print(f"\nSubset by slice [1:3]:\n{spc_subset3}")
    
    # Boolean mask - select profiles where site_name contains 'Beta' or 'Gamma'
    mask = spc.site['site_name'].str.contains('Beta|Gamma')
    spc_subset4 = spc[mask]
    print(f"\nSubset by boolean mask (site name contains Beta or Gamma):\n{spc_subset4}")


    print("\n--- Profile Apply (Example: Mean Clay per Profile) ---")
    def mean_clay(hz_df):
         if 'clay' in hz_df.columns and not hz_df['clay'].empty:
             return hz_df['clay'].mean()
         return np.nan

    mean_clay_per_profile = spc.profile_apply(mean_clay)
    print(mean_clay_per_profile)
    
    print("\n--- Plotting ---")
    # Plot all profiles using the 'color' column
    ax1 = spc.plot(color='color', label_hz=True, figsize=(8, 6))
    plt.suptitle("Plot of All Profiles (Using 'color' column)")
    plt.show()

    # Plot only the first 2 profiles with a fixed color
    ax2 = spc_subset2.plot(color='sandybrown', label_hz=False, figsize=(5, 5))
    plt.suptitle("Plot of Subsetted Profiles (P1, P3) - Fixed Color")
    plt.show()


except (ValueError, KeyError, TypeError) as e:
    print(f"\nError creating or using SoilProfileCollection: {e}")

# Example of validation error: Overlapping horizons
print("\n--- Example Validation Error (Overlap) ---")
p_overlap_horizons = pd.DataFrame({
    'id': ['P_overlap'] * 2,
    'hzid': ['HO1', 'HO2'],
    'top': [0, 10],
    'bottom': [15, 20], # Overlap: H01 ends at 15, HO2 starts at 10
    'hzname': ['A','B']
})
try:
     spc_overlap = SoilProfileCollection(p_overlap_horizons, idname='id', hzidname='hzid')
except ValueError as e:
     print(f"Caught expected error: {e}")
     
# Example of validation error: Gap
print("\n--- Example Validation Error (Gap) ---")
p_gap_horizons = pd.DataFrame({
    'id': ['P_gap'] * 2,
    'hzid': ['HG1', 'HG2'],
    'top': [0, 20], # Gap: HG1 ends at 10, HG2 starts at 20
    'bottom': [10, 30],
    'hzname': ['A','B']
})
try:
     spc_gap = SoilProfileCollection(p_gap_horizons, idname='id', hzidname='hzid')
except ValueError as e:
     print(f"Caught expected error: {e}")
     
p1_horizons = pd.DataFrame({
    'id': ['P1'] * 4, 'hzid': ['H1', 'H2', 'H3', 'H4'], 'top': [0, 10, 25, 50],
    'bottom': [10, 25, 50, 80], 'hzname': ['A', 'Bt1', 'Bt2', 'C'],
    'clay': [15, 35, 40, 20], 'color': ['#A0522D', '#8B4513', '#8B4513', '#D2B48C']
})
p2_horizons = pd.DataFrame({
    'id': ['P2'] * 3, 'hzid': ['H5', 'H6', 'H7'], 'top': [0, 15, 40],
    'bottom': [15, 40, 100], 'hzname': ['Ap', 'Bw', 'BC'],
    'clay': [20, 28, 25], 'color': ['#654321', '#A0522D', '#CD853F']
})
p3_horizons = pd.DataFrame({
    'id': ['P3'] * 2, 'hzid': ['H8', 'H9'], 'top': [0, 5], 'bottom': [5, 20],
    'hzname': ['O', 'R'], 'clay': [5, 2], 'color': ['#000000', '#808080']
})
all_horizons = pd.concat([p1_horizons, p2_horizons, p3_horizons], ignore_index=True)
site_data = pd.DataFrame({'id': ['P1', 'P2', 'P3'], 'x': [100,150,120], 'y': [200,210,190]})


try:
    spc = SoilProfileCollection(
         horizons=all_horizons, site=site_data, idname='id', hzidname='hzid',
         depthcols=('top', 'bottom'), hzdesgncol='hzname'
    )
    print("\n--- Original Horizons (Showing hzname, clay, color) ---")
    print(spc.horizons[['id', 'hzname', 'top', 'bottom', 'clay', 'color']])

    standard_intervals = [0, 15, 30, 60, 100]

    print("\n--- Glom: Dominant Horizon Name ('hzname') ---")
    # This variable is categorical
    glom_dom_name = spc.glom(intervals=standard_intervals, v='hzname', agg_fun='dominant')
    print(glom_dom_name)

    print("\n--- Glom: Dominant Clay Value ('clay') ---")
    # This variable is numeric, result should match the clay value of the dominant hzname above
    glom_dom_clay = spc.glom(intervals=standard_intervals, v='clay', agg_fun='dominant')
    print(glom_dom_clay)

    print("\n--- Glom: Dominant Color ('color') ---")
    # Another categorical example
    glom_dom_color = spc.glom(intervals=standard_intervals, v='color', agg_fun='dominant')
    print(glom_dom_color)

    print("\n--- Glom: Dominant (Auto-detect columns, fill=False) ---")
    # Will run dominant on 'hzname', 'clay', 'color'
    glom_dom_auto = spc.glom(intervals=[0, 20, 50], agg_fun='dominant', v=None, fill=False)
    print(glom_dom_auto)


except Exception as e:
    import traceback
    print(f"\nAn unexpected error occurred: {e}")
    traceback.print_exc()
