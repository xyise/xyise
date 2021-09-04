

#%%

pkg_folder = r'/home/youngsuk/repos/anylox.github.io/codes/scratch/pkg_sample'
sys.path.append(pkg_folder)

#import pkg.pack1.mod1_1
#import pkg.pack1.mod1_2
import pkg.pack1

#%%
%load_ext autoreload
%autoreload 1
%aimport pkg.pack1.mod1_1
%aimport pkg.pack1.mod1_2
%aimport pkg.pack1


#%%
pkg.pack1.mod1_1.x_1_1
#%%
pkg.pack1.mod1_2.x_1_2

#%%
import plotly.graph_objs as go
import plotly.offline as py

py.plot([go.Scatter(x=[1,2,3], y=[3,1,6])])

#%%
py.init_notebook_mode(connected=True)


#%%
py.iplot([{"x": [1, 2, 3], "y": [3, 1, 6]}])

#%%
import plotly.express as px
iris = px.data.iris()
fig = px.scatter(iris, x="sepal_width", y="sepal_length")
fig.show()

#%%
iris = px.data.iris()
fig = px.scatter_3d(iris, x='sepal_length', y='sepal_width', z='petal_width',
              color='species')
fig.show()

#%%
