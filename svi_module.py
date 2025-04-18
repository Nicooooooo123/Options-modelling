# svi_module.py

import numpy as np
from scipy.optimize import minimize
import pandas as pd

def svi_model(k, a, b, rho, m_param, sigma):
    """Stochastic Volatility Inspired (SVI) model formula.
    
    Args:
        k: Log moneyness values
        a: Vertical shift parameter
        b: Slope/curvature parameter 
        rho: Correlation/asymmetry parameter
        m_param: Horizontal shift parameter
        sigma: Smoothness parameter
    
    Returns:
        Implied volatility values according to SVI model
    """
    return a + b * (rho * (k - m_param) + np.sqrt((k - m_param)**2 + sigma**2))

def svi_objective(params, k, v, lambda_reg=0.0):
    """Objective function for SVI model calibration.
    
    Args:
        params: Parameters [a, b, rho, m_param, sigma]
        k: Log moneyness values
        v: Market implied volatility values
        lambda_reg: Regularization weight
    
    Returns:
        Error term with regularization
    """
    a, b, rho, m_param, sigma = params
    if b < 0 or sigma <= 0 or abs(rho) >= 1:
        return 1e10  # Return large penalty for invalid parameters
    model_values = svi_model(k, a, b, rho, m_param, sigma)
    error = np.sum((model_values - v) ** 2)
    reg_penalty = lambda_reg * (b**2 + sigma**2)
    return error + reg_penalty

def calibrate_svi(k, v, lambda_reg=0.0, multi_start_count=5):
    """Calibrate SVI model to market data using multi-start optimization.
    
    Args:
        k: Log moneyness values
        v: Market implied volatility values
        lambda_reg: Regularization weight
        multi_start_count: Number of random starting points
    
    Returns:
        Best calibrated parameters
    """
    best_params = None
    best_obj_val = np.inf
    base_a = np.min(v)
    
    for _ in range(multi_start_count):
        # Random initialization within reasonable bounds
        a0 = base_a + np.random.uniform(-0.5, 0.5)
        b0 = 0.1 + np.random.uniform(-0.05, 0.05)
        rho0 = np.random.uniform(-0.9, 0.9)
        m0 = np.random.uniform(-0.1, 0.1)
        sigma0 = 0.1 + np.random.uniform(0, 0.1)
        x0 = [a0, b0, rho0, m0, sigma0]
        
        # Parameter bounds
        bounds = [
            (-np.inf, np.inf),    # a: Vertical shift
            (0, np.inf),          # b: Slope/curvature (must be positive)
            (-0.99, 0.99),        # rho: Correlation/asymmetry (must be between -1 and 1)
            (-np.inf, np.inf),    # m: Horizontal shift
            (0.001, np.inf)       # sigma: Smoothness (must be positive)
        ]
        
        try:
            result = minimize(lambda params: svi_objective(params, k, v, lambda_reg),
                            x0, bounds=bounds, method="L-BFGS-B")
            if result.fun < best_obj_val:
                best_obj_val = result.fun
                best_params = result.x
        except Exception:
            continue
            
    return best_params

def generate_svi_calibrated_data(unique_maturities, imp_vol_data, spot_price, reg_weight=0.0, multi_start_count=5, option_data_type="Both"):
    """Generate SVI calibrated volatility data for each maturity.
    
    Args:
        unique_maturities: List of unique time-to-expiry values
        imp_vol_data: DataFrame with implied volatility data
        spot_price: Current spot price
        reg_weight: Regularization weight
        multi_start_count: Number of random starting points
        option_data_type: Type of option data used ("Calls Only", "Puts Only", "Both")
    
    Returns:
        DataFrame with SVI calibrated data
    """
    svi_calibrated_data = []
    
    for maturity in unique_maturities:
        maturity_data = imp_vol_data[np.isclose(imp_vol_data["TimeToExpiry"], maturity)]
        if len(maturity_data) < 5:
            continue
            
        k = maturity_data["LogMoneyness"].values
        v = maturity_data["ImpliedVolatility"].values * 100
        params = calibrate_svi(k, v, lambda_reg=reg_weight, multi_start_count=multi_start_count)
        
        if params is None:
            continue
            
        a, b, rho, m_param, sigma = params
        k_smooth = np.linspace(min(k)-0.1, max(k)+0.1, 100)
        v_smooth = svi_model(k_smooth, a, b, rho, m_param, sigma)
        strikes_smooth = spot_price * np.exp(k_smooth)
        
        for i in range(len(k_smooth)):
            svi_calibrated_data.append({
                "TimeToExpiry": maturity,
                "LogMoneyness": k_smooth[i],
                "StrikePrice": strikes_smooth[i],
                "Moneyness": np.exp(k_smooth[i]),
                "ImpliedVolatility": v_smooth[i] / 100,
                "OptionType": option_data_type.replace(" Only", "").replace("Both Calls & Puts", "Both")
            })
    
    if svi_calibrated_data:
        return pd.DataFrame(svi_calibrated_data)
    else:
        return pd.DataFrame(columns=["TimeToExpiry", "StrikePrice", "Moneyness", "ImpliedVolatility", "OptionType"])

def filter_outliers(imp_vol_data):
    """Filter out outliers from the implied volatility data.
    
    Args:
        imp_vol_data: DataFrame with implied volatility data
    
    Returns:
        DataFrame with outliers removed
    """
    # Filter by volume if available
    if "volume" in imp_vol_data.columns:
        imp_vol_data = imp_vol_data[imp_vol_data["volume"] > 10]
        
    # Remove outliers based on IQR method
    Q1 = imp_vol_data["ImpliedVolatility"].quantile(0.25)
    Q3 = imp_vol_data["ImpliedVolatility"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 2.0 * IQR
    upper_bound = Q3 + 2.0 * IQR
    
    return imp_vol_data[(imp_vol_data["ImpliedVolatility"] >= lower_bound) &
                        (imp_vol_data["ImpliedVolatility"] <= upper_bound)]
