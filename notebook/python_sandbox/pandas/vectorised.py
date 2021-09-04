#%%
import pandas as pd
import numpy as np



#%%
r = pd.DataFrame(data=np.random.randn(100, 10), index=np.random.randint(), columns=['c' + str(x) for x in range(10)])
r.loc[[2,2,3],['c0','c1']]
#%%
