import types
from matplotlib.pyplot import sca
import numpy as np
from scipy.interpolate import splev, splrep

from shapely.geometry import Point
import geopandas

R_earth = 6371.0

def circle_distance(lon1: np.ndarray, lat1: np.ndarray, lon2: float, lat2: float, in_deg = True):
    '''
        haversine based formula
        https://en.wikipedia.org/wiki/Great-circle_distance
    '''
    # rename to match the formula, and convert to radian if necessary
    lam1, phi1, lam2, phi2 = lon1, lat1, lon2, lat2
    if in_deg:
        to_rad = np.pi/180.0
        lam1, phi1, lam2, phi2 = [a * to_rad for a in [lam1, phi1, lam2, phi2]]
    dlam = lam1 - lam2
    dphi = phi1 - phi2
    
    cd  = 2.0*np.arcsin(
        np.sqrt(
        (np.sin(dphi/2.0))**2 + (1.0-(np.sin(dphi/2.0))**2-(np.sin((phi1+phi2)/2.0))**2)*
        ((np.sin(dlam/2.0))**2))
    )
    return cd

def sort_by_distance(lon, lat, lon_i, lat_i, in_deg=True):
    '''
        order (lon, lat) pairs based on the circle distance
    '''
    cd = circle_distance(lon, lat, lon_i, lat_i, in_deg)
    i_s = np.argsort(cd)
    return i_s, cd[i_s]


def sort_by_distance_lat_scaled(lon, lat, lon_i, lat_i, in_deg=True):
    '''
        the longitude is scaled by cos(lat). 
    '''
    dlat = lat - lat_i
    dlon = (lon - lon_i) * (np.cos(lat) + np.cos(lat_i))/2.0
    dls = np.sqrt(dlat**2 + dlon**2)
    i_s = np.argsort(dls)
    return i_s, dls[i_s]

def get_neighbours(lon: np.ndarray, lat: np.ndarray, K: int, type: str = "circle", in_deg=True):
    """get indices and metrics of neighbouring points (up to K)

    Args:
        lon (np.ndarray): lon
        lat (np.ndarray): lat
        K (int): number of neighbours
        type (str, optional): "circle" or "lat_scaled". Defaults to "circle".
        in_deg (bool, optional): whether in degree or radian
    """

    num_data = len(lon)
    nhb_idx, nhb_mtc = [], []
    for i in range(num_data):
        lon_i, lat_i = lon[i], lat[i]
        if type == "circle":
            idx, mtc = sort_by_distance(lon, lat, lon_i, lat_i, in_deg)
        elif type == "lat_scaled":
            idx, mtc = sort_by_distance_lat_scaled(lon, lat, lon_i, lat_i, in_deg)
        else:
            raise Exception("unknown type: " + type)

        nhb_idx.append(idx[:K])
        nhb_mtc.append(mtc[:K])
    
    return nhb_idx, nhb_mtc

def spline_fit_lat(lat, Z, num_knots=9, in_deg=True):

    # convert it to radians first
    if in_deg:
        lat = np.deg2rad(lat)

    i_s = np.argsort(lat)
    # put x in radian
    x, y = lat[i_s], Z[i_s]
    
    knots = np.arcsin(np.linspace(np.sin(x[0]), np.sin(x[-1]), num_knots+2))
    spl = splrep(x, y, t = knots[1:-1])
    f = splev(lat, spl)
    return f

def combine_bands(bands: np.ndarray, scales: list, agg_funcs: list =[np.mean, np.mean, np.mean]):
    if type(scales) is float:
        scales = [scales] * len(bands) 
    if isinstance(agg_funcs, types.FunctionType):
        agg_funcs = [agg_funcs] * 3

    scaled_bands = []
    for band, scale in zip(bands, scales):
        lmu = scale_band(band, scale) # this would create (lmu=3) x (num pts) matrix
        scaled_bands.append(lmu)
    scaled_bands = np.array(scaled_bands).transpose((1,0,2)) # (lmu=3) x (num_bands) x (num pts)
    return np.array([fn(sb, axis=0) for sb, fn in zip(scaled_bands, agg_funcs)])
        
def scale_band(band, scale):
    l, m, u = band
    return np.array([m+scale*(l-m), m, m+scale*(u-m)])

def average_over_sphere(lon, lat, Z, lon_a, lat_a, kernel_width, in_deg=True):

    is_scalar = np.isscalar(lon_a)
    if is_scalar:
        lon_a = np.array([lon_a])
        lat_a = np.array([lat_a])
    
    z_a = np.empty_like(lon_a)
    for i, (lon_i, lat_i) in enumerate(zip(lon_a, lat_a)):
        z_a[i] = _average_over_sphere(lon, lat, Z, lon_i, lat_i, kernel_width, in_deg)
    
    if is_scalar:
        return z_a[0]
    else:
        return z_a

def _average_over_sphere(lon, lat, Z, lon_i, lat_i, kernel_width, in_deg=True):

    kernel = lambda d: np.exp(-(d/kernel_width)**2)

    cd = circle_distance(lon, lat, lon_i, lat_i, in_deg)
    min_cd = np.min(cd)
    if min_cd > kernel_width:
        cd *= kernel_width/min_cd
    kcd = kernel(cd)
    z_i = np.sum(kcd * Z) / np.sum(kcd)
    return z_i

def geo_projection(lon, lat, crs="ESRI:54012"):

    is_scalar = np.isscalar(lon)
    if is_scalar:
        lon = np.array([lon])
        lat = np.array([lat])
    
    col = 'geometry'
    gdf = geopandas.GeoDataFrame({col: [Point(lon_i, lat_i) for lon_i, lat_i in zip(lon, lat)]}, crs="EPSG:4326")
    # convert
    px = gdf.to_crs(crs)
    xy = np.array([[px.loc[i][col].x, px.loc[i][col].y] for i in range(px.shape[0])])

    x, y = xy[:,0], xy[:,1]
    if is_scalar:
        return x[0], y[0]
    else:
        return x, y