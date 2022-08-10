import numpy as np

def garch_filter(delta, alpha, v_r, mu, sigma2_inf, sigma2_0):
    '''
    input:
    delta, alpha: garch(1,1) delta & alpha
    v_r: historical return
    mu: drift
    sigma2_inf: sigma_inf squared squared
    sigma2_0: the initial sigma squared
    
    output: dictionary of
    eps: vector of residuals
    sigma2: vector of sigma squared
    sigma2_next: next sigma squared
    '''
    
    mr = sigma2_inf * (1 - delta - alpha)
    v_eps = np.ones_like(v_r)
    v_sigma2 = np.ones_like(v_r)

    sigma2_nxt = sigma2_0

    for n in range(len(v_r)):
        v_sigma2[n] = sigma2_nxt
        v_eps[n] = (v_r[n] - mu)/np.sqrt(sigma2_nxt)
        sigma2_nxt = mr + delta * v_sigma2[n] + alpha * v_sigma2[n] * (v_eps[n]**2)
    
    return {'eps':v_eps, 'sigma2':v_sigma2, 'sigma2_next':sigma2_nxt}

def garch_return_simulation(delta, alpha, mu, sigma2_inf, sigma2_0, v_eps):

    v_r = np.zeros_like(v_eps)
    v_sigma2 = np.zeros_like(v_eps)

    sigma2_t = sigma2_0

    a = sigma2_inf * (1.0 - delta - alpha)
    for t in range(v_eps.size):
        eps = v_eps[t]
        v_r[t] = mu + np.sqrt(sigma2_t) * eps
        v_sigma2[t] = sigma2_t
        sigma2_t = a + delta * sigma2_t + alpha * sigma2_t * (eps**2)
    return {'r':v_r, 'sigma2': v_sigma2 }

def garch_mle_obj(v_r, mu, v_sigma2):
    return - np.sum(np.log(v_sigma2) + (v_r-mu)**2/v_sigma2)

def garch_exp_variance(sigma2_1, sigma2_inf, delta, alpha, v_t):
    return sigma2_inf + (1.0 - (delta+alpha)**v_t)/(1-(delta+alpha)) * (sigma2_1 - sigma2_inf)/v_t
