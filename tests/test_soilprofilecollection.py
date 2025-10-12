import pandas as pd
import numpy as np
import pytest
import matplotlib.axes

from soilprofilecollection import SoilProfileCollection
from soilprofilecollection.soil_profile_collection import import_data_sheet

# Fixture for creating a sample SPC
@pytest.fixture
def sample_spc():
    """Creates a sample SoilProfileCollection for testing."""
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
    site_data = pd.DataFrame({
        'id': ['P1', 'P2', 'P3'], 'x': [100, 150, 120], 'y': [200, 210, 190],
        'site_name': ['Site Alpha', 'Site Beta', 'Site Gamma']
    })
    return SoilProfileCollection(
        horizons=all_horizons,
        site=site_data,
        idname='id',
        hzidname='hzid',
        depthcols=('top', 'bottom'),
        hzdesgncol='hzname',
        metadata={'project': 'Demo', 'location': 'Test Area'},
        crs='EPSG:4326'
    )

def test_spc_creation_and_properties(sample_spc):
    """Tests basic attributes of the SoilProfileCollection."""
    assert isinstance(sample_spc, SoilProfileCollection)
    assert len(sample_spc) == 3
    assert sample_spc.profile_ids == ['P1', 'P2', 'P3']
    assert sample_spc.crs == 'EPSG:4326'
    assert 'site_name' in sample_spc.site.columns

def test_spc_methods(sample_spc):
    """Tests various methods of the SoilProfileCollection."""
    depths_df = sample_spc.depths(how='max').set_index('id')
    assert depths_df.loc['P1', 'max_depth'] == 80
    assert sample_spc.thickness().iloc[0] == 10
    p1_horizons = sample_spc.get_profile('P1')
    assert isinstance(p1_horizons, pd.DataFrame)
    assert p1_horizons.shape[0] == 4

def test_spc_subsetting(sample_spc):
    """Tests subsetting the SoilProfileCollection."""
    spc_subset1 = sample_spc[0]
    assert len(spc_subset1) == 1
    assert spc_subset1.profile_ids == ['P1']

    spc_subset2 = sample_spc[['P1', 'P3']]
    assert len(spc_subset2) == 2
    assert spc_subset2.profile_ids == ['P1', 'P3']

    spc_subset3 = sample_spc[1:3]
    assert len(spc_subset3) == 2
    assert spc_subset3.profile_ids == ['P2', 'P3']
    
    mask = sample_spc.site['site_name'].str.contains('Beta|Gamma')
    spc_subset4 = sample_spc[mask]
    assert len(spc_subset4) == 2
    assert spc_subset4.profile_ids == ['P2', 'P3']

def test_profile_apply(sample_spc):
    """Tests the profile_apply method."""
    def mean_clay(hz_df):
        if 'clay' in hz_df.columns and not hz_df['clay'].empty:
            return hz_df['clay'].mean()
        return np.nan
    
    mean_clay_per_profile = sample_spc.profile_apply(mean_clay)
    assert isinstance(mean_clay_per_profile, pd.Series)
    assert mean_clay_per_profile['P1'] == pytest.approx(27.5)
    assert mean_clay_per_profile['P2'] == pytest.approx(24.333333333333332)

def test_validation_errors():
    """Tests that the SPC raises errors for invalid horizon data."""
    # Overlapping horizons
    p_overlap_horizons = pd.DataFrame({
        'id': ['P_overlap'] * 2, 'hzid': ['HO1', 'HO2'],
        'top': [0, 10], 'bottom': [15, 20]
    })
    with pytest.raises(ValueError, match="has overlapping horizons"):
        SoilProfileCollection(p_overlap_horizons, idname='id', hzidname='hzid')

    # Gap in horizons
    p_gap_horizons = pd.DataFrame({
        'id': ['P_gap'] * 2, 'hzid': ['HG1', 'HG2'],
        'top': [0, 20], 'bottom': [10, 30]
    })
    with pytest.raises(ValueError, match="has depth gaps between horizons"):
        SoilProfileCollection(p_gap_horizons, idname='id', hzidname='hzid')

def test_glom(sample_spc):
    """Tests the glom method for aggregating horizon data."""
    standard_intervals = [0, 15, 30, 60, 100]
    
    glom_dom_name = sample_spc.glom(intervals=standard_intervals, v='hzname', agg_fun='dominant', output='dataframe')
    glom_dom_name_wide = glom_dom_name.pivot(index=['top', 'bottom'], columns='id', values='hzname').reset_index()
    
    assert glom_dom_name_wide.shape == (4, 5)
    assert glom_dom_name_wide.loc[0, 'P1'] == 'A'
    
    glom_dom_clay = sample_spc.glom(intervals=standard_intervals, v='clay', agg_fun='dominant', output='dataframe')
    glom_dom_clay_wide = glom_dom_clay.pivot(index=['top', 'bottom'], columns='id', values='clay').reset_index()
    assert glom_dom_clay_wide.loc[0, 'P1'] == 15

def test_plot(sample_spc):
    """Tests that the plot method runs without errors and returns an Axes object."""
    ax = sample_spc.plot(color='color')
    assert isinstance(ax, matplotlib.axes.Axes)

def test_import_data_sheet():
    """Tests importing data with a schema template."""
    source_data = pd.DataFrame({
        'profile_id': ['P1', 'P1', 'P2'],
        'h_id': [1, 2, 3],
        'd_top': [0, 10, 0],
        'd_bottom': [10, 25, 15],
        'prop': [5, 8, 9]
    })
    schema = {
        'profile_id': 'id',
        'h_id': 'hzid',
        'd_top': 'top',
        'd_bottom': 'bottom'
    }
    
    spc = import_data_sheet(source_data, schema)

    assert isinstance(spc, SoilProfileCollection)
    assert len(spc) == 2
    assert spc.idname == 'id'
    assert spc.hzidname == 'hzid'
    assert spc.depthcols == ('top', 'bottom')
    assert 'prop' in spc.horizons.columns
    assert spc.horizons.shape[0] == 3