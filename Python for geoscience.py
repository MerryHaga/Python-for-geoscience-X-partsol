#!/usr/bin/env python
# coding: utf-8

# In[38]:


import warnings
warnings.filterwarnings('ignore')


# ## Petrophysics calculation

# In[39]:


pip install lasio


# In[40]:


import lasio
las=lasio.read('well-1.las')

#convert the las file to pandas dataframe, this will automatically retain the logname and made the depth as index column
well=las.df() ## convert the las file to pd dataframe
print (well)


# In[41]:


KujungFM=well.loc[3337.79:3751.5]
print (KujungFM)


# In[42]:


#this code is adapted from andy mcdonald

def shale_volume(gamma_ray, gamma_ray_max, gamma_ray_min): #specify the arguments
    vshale = (gamma_ray - gamma_ray_min) / (gamma_ray_max - gamma_ray_min) #use the argument to the equation using math operators
    return round(vshale, 4)

def density_porosity(input_density, matrix_density, fluid_density):
    denpor = (matrix_density - input_density) / (matrix_density - fluid_density)
    return round(denpor, 4)


# In[43]:


mDens= 2.65
fDens= 1
KujungFM['VSHALE']=shale_volume(KujungFM['GR'], KujungFM['GR'].quantile(q=0.99),
                             KujungFM['GR'].quantile(q=0.01))
KujungFM['PHI']=density_porosity(KujungFM['RHOB'], mDens, fDens)
KujungFM.head()


# ### Calculate RW and SW
# 
# **Apparent water formation resistivity using Hingle method**
# <img src="rw.png">
# 
# **SW:**
# <img src="sw_archie.png">

# In[44]:


#this code is adapted from andy mcdonald

def shale_volume(gamma_ray, gamma_ray_max, gamma_ray_min): #specify the arguments
    vshale = (gamma_ray - gamma_ray_min) / (gamma_ray_max - gamma_ray_min) #use the argument to the equation using math operators
    return round(vshale, 4)

def density_porosity(input_density, matrix_density, fluid_density):
    denpor = (matrix_density - input_density) / (matrix_density - fluid_density)
    return round(denpor, 4)


# In[45]:


mDens= 2.65
fDens= 1
KujungFM['VSHALE']=shale_volume(KujungFM['GR'], KujungFM['GR'].quantile(q=0.99),
                             KujungFM['GR'].quantile(q=0.01))
KujungFM['PHI']=density_porosity(KujungFM['RHOB'], mDens, fDens)
KujungFM.head()


# In[46]:


#Calculate RW and SW


# In[47]:


def rw_app(porosity, archieA, archieM, rt):
    rw= ((porosity ** archieM)*(rt/archieA))
    return rw

def sw_archie(porosity, rt, rw, archieA, archieM, archieN):
    sw = ((archieA / (porosity ** archieM)) * (rw/rt))**(1/archieN)
    return sw

archieA= 1
archieM= 2
archieN= 2


# In[61]:


KujungFM['rw']=rw_app(KujungFM['NPHI_LS'], archieA, archieM, KujungFM['ILD'])
KujungFM['SW'] = sw_archie(KujungFM['NPHI_LS'], KujungFM['ILD'], KujungFM['rw'], archieA, archieM, archieN)


# In[62]:


well.describe()


# In[63]:


KujungFM.head()


# In[64]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# ## Data Handling

# - ***explore the statistical information of the SW and RW log***
# - ***compare the mean and the standard deviation of each log from the pandas result***
# - ***visualize using histogram, boxplot, etc***

# In[51]:


# statistical information of the all variables in KujungFM

print('mean for all variables in KujungFM: \n' + str(KujungFM.mean()) + '\n')
print('median for all variables in KujungFM: \n' + str(KujungFM.median()) + '\n')
print('range for all variables in KujungFM: \n' + str(KujungFM.max() - KujungFM.min()) + '\n')
print('variance for all variables in KujungFM: \n' + str(KujungFM.var()) + '\n')
print('standard deviation for all variables in KujungFM: \n' + str(KujungFM.std()))


# In[52]:


print(KujungFM.describe())


# In[65]:


# Visualize using boxplot

# rw value
red_square = dict(markerfacecolor='r', marker='s')
fig1, ax1 = plt.subplots()
ax1.set_title('Water apparent resistivity (rw) in Kujung FM.')
ax1.boxplot(KujungFM['rw'], vert=False, flierprops=red_square)

# SW value
green_diamond = dict(markerfacecolor='g', marker='D')
fig2, ax2 = plt.subplots()
ax2.set_title('Water saturation (SW) in Kujung FM.')
ax2.boxplot(KujungFM['SW'], vert=False, flierprops=green_diamond)


# In[66]:


# Creating dataset
data = [KujungFM['rw'], KujungFM['SW']]

fig = plt.figure(figsize =(10, 7)) 
ax = fig.add_subplot(111) 
  
# Creating axes instance 
bp = ax.boxplot(data, patch_artist = True, 
                notch ='True', vert = 0) 
  
colors = ['#0000FF', '#00FF00'] 
  
for patch, color in zip(bp['boxes'], colors): 
    patch.set_facecolor(color) 
  
# changing color and linewidth of 
# whiskers 
for whisker in bp['whiskers']: 
    whisker.set(color ='#8B008B', 
                linewidth = 1.5, 
                linestyle =":") 
  
# changing color and linewidth of 
# caps 
for cap in bp['caps']: 
    cap.set(color ='#8B008B', 
            linewidth = 2) 
  
# changing color and linewidth of 
# medians 
for median in bp['medians']: 
    median.set(color ='red', 
               linewidth = 3) 
  
# changing style of fliers 
for flier in bp['fliers']: 
    flier.set(marker ='D', 
              color ='#e7298a', 
              alpha = 0.5) 
      
# x-axis labels 
ax.set_yticklabels(['rw', 'SW']) 
  
# Adding title  
plt.title("rw and SW value in Kujung FM.") 
  
# Removing top axes and right axes 
# ticks 
ax.get_xaxis().tick_bottom() 
ax.get_yaxis().tick_left() 
      
# show plot 
plt.show(bp) 


# In[67]:


# Visualize using histogram

# rw
sns.distplot(KujungFM['rw'], bins=10)
plt.show()

# SW : The central tendency of the data is strong,
# There is no variation/spread in SW value
# sns.distplot(KujungFM['rw'], bins=5)
# plt.show()


# In[68]:


fig, ax = plt.subplots(figsize=(10,10))

ax1 = plt.subplot2grid((2,2), (0,0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((2,2), (0,1), rowspan=1, colspan=1)


ax1.scatter(x= "SW", y= "PHI", data= KujungFM, marker="s", alpha= 0.2)
ax1.set_ylim(0.3, 0)
ax1.set_ylabel("PHI")
ax1.set_xlabel("SW")


ax2.scatter(x= "VSHALE", y= "PHI", data= KujungFM, marker="p", alpha= 0.2)
ax1.set_ylim(0.4, 0)
ax2.set_ylabel("PHI")
ax2.set_xlabel("VSHALE")


# In[69]:


KujungFM.plot(kind="scatter", x="VSHALE", y="SW", c="rw", 
          colormap="YlOrRd_r", ylim=(3,1), xlim=(0,1))


# In[71]:


from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(KujungFM["VSHALE"], KujungFM["SW"], KujungFM["rw"], alpha= 0.3,) 


# In[70]:


fig, ax = plt.subplots(figsize=(10,10))

ax1 = plt.subplot2grid((2,2), (0,0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((2,2), (0,1), rowspan=1, colspan=1)


ax1.scatter(x= "SW", y= "PHI", data= KujungFM, marker="s", alpha= 0.2)
ax1.set_ylim(0.3, 0)
ax1.set_ylabel("PHI")
ax1.set_xlabel("SW")


ax2.scatter(x= "VSHALE", y= "PHI", data= KujungFM, marker="p", alpha= 0.2)
ax1.set_ylim(0.4, 0)
ax2.set_ylabel("PHI")
ax2.set_xlabel("VSHALE")


# In[ ]:




