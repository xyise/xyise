import numpy as np

# Python must be 3.6 or higher. 

kw_rv2fnblocksize ={
    'standard_normal':(lambda rv: 2),
    'normal':(lambda rv: 2),
    'uniform':(lambda rv: 1),
    'multivariate_normal':(lambda rv: 2 * len(rv.kw_inputs['mean']))
}

class RandomVariables:

    def __init__(self, rv_type, kw_inputs = {}, transform = None):
        self.rv_type = rv_type
        self.kw_inputs = kw_inputs
        self.transform = transform
    
    def generate_samples(self, rgn, n_scen):
        str_eval = 'rgn.' + self.rv_type + '(size=size'

        if len(self.kw_inputs) > 0: 
            str_eval += ',' + ','.join([(k + '=' + k) for k in self.kw_inputs])

        str_eval += ')'

        x = eval(str_eval, {}, {**{'rgn':rgn, 'size':n_scen}, **self.kw_inputs})

        if self.transform != None:
            x = self.transform(x)
        return x

class RandomRepeat:

    def __init__(self, seed_seq, n_scens, kw_rv):

        self.__name__ = 'random_repeat'

        self._seed_seq = seed_seq
        self._n_scens = n_scens
        
        self._kw_rv = {}
        self._kw_skip = {}
        self._next_skip = 0

        for n in kw_rv:
            self._update(n, kw_rv[n])

    def _update(self, name, rv):
        self._kw_rv[name] = rv
        self._kw_skip[name] = self._next_skip
        self._next_skip += self._n_scens * kw_rv2fnblocksize[rv.rv_type](rv)

    def add(self, kw_rv_add):

        for n in kw_rv_add:
            if n not in self._kw_rv:
                self._update(n, kw_rv_add[n])

    def get_sample(self, name, n_scens = None):
        
        rv = self._kw_rv[name]
        n_skip = self._kw_skip[name]

        bit_gen = np.random.PCG64(self._seed_seq)
        bit_gen.advance(n_skip)
        rgn = np.random.Generator(bit_gen)

        n_s = self._n_scens
        if n_scens != None:
            if n_scens > self._n_scens:
                raise Exception('Can not request more than the default scenario size')
            n_s = n_scens

        x = rv.generate_samples(rgn, n_s)
        return x

    

    