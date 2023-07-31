import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 14})

cols=['node','x','y','z']
df = pd.read_csv('data/nodes.lst', delim_whitespace=True, names=cols)

fi = df['y'].values
z = df['z'].values
names = df['node'].values

fig, ax = plt.subplots()
scatter = plt.scatter(
    x=z,
    y=fi)
# Step 2. Create Annotation Object
annotation = ax.annotate(
    text='',
    xy=(0, 0),
    xytext=(15, 15), # distance from x, y
    textcoords='offset points',
    bbox={'boxstyle': 'round', 'fc': 'w'},
    arrowprops={'arrowstyle': '->'}
)
annotation.set_visible(False)

def motion_hover(event):
    annotation_visbility = annotation.get_visible()
    if event.inaxes == ax:
        is_contained, annotation_index = scatter.contains(event)
        if is_contained:
            data_point_location = scatter.get_offsets()[annotation_index['ind'][0]]
            annotation.xy = data_point_location
            idx = annotation_index['ind'][0]
            text_label = 'Node {0}\n(z={1:.1f}mm\n$\\varphi=${2:.1f}$^{{o}}$)'.format(names[idx], z[idx], fi[idx])
            annotation.set_text(text_label)
            annotation.set_alpha(0.4)

            annotation.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if annotation_visbility:
                annotation.set_visible(False)
                fig.canvas.draw_idle()
                
fig.canvas.mpl_connect('motion_notify_event', motion_hover)
plt.title('Node mapper for strain gauges positions\n(mouseover node to get its data)')
ax.set_xlabel('Z (mm)')
ax.set_ylabel('$\\varphi$ ($^{{o}}$)')
plt.tight_layout()
plt.show()