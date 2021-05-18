from numpy.core.numeric import full_like, zeros_like
from scipy.stats import mvn
from numpy import array, zeros, int32,broadcast_to, Inf,full
from joblib import Parallel, delayed


class ParameterBox:
    pass

integration = ParameterBox() # Will contain all module-level values.
integration.maxpts = None # global in module # "maxpts=None" means maxpts = d*1000
integration.abseps = 1e-6 # global in module
integration.releps = 1e-6
integration.n_jobs = 1
# TODO : allow more joblib control
# TODO : forbid typos! like "integration.relesp"

def integrate(l,u,m,c):
    return mvn.mvnun(l, u, m, c, integration.maxpts, integration.abseps, integration.releps)

def parallel_integration(l,u,m,c):
    N = c.shape[0]
    if N==0:
        return tuple(), tuple()
    p = Parallel(n_jobs=integration.n_jobs)(
        delayed(integrate)(l[j,...], u[j,...], m[j,...], c[j,...]) for j in range(N)) 
    v, i = zip(*p)
    return v, i


def prod(tup):
    a = 1
    for i in tup:
        a *= i
    return a

def hyperrectangle_integration(mean,covariance,lower=None,upper=None,info=False):
    # parallel batch version of scipy.stats.mvn
    # no pytorch here
    # default: integration over the first orthant (for all i, Y_i<0)
    ms = mean.shape
    batch_shape = ms[:-1]
    d = ms[-1]

    N = prod(batch_shape)
    m = mean.reshape(N,d)
    l = full_like(m,-Inf) if lower is None else lower.reshape(N,d)
    u = zeros_like(m) if upper is None else upper.reshape(N,d)
    c = covariance.reshape(N,d,d)


    v, i = parallel_integration(l,u,m,c)
    values = array(v).reshape(batch_shape)
    if info :
        infos  = array(i, dtype = int32).reshape(batch_shape)
        return (values,infos)
    else:
        return values

