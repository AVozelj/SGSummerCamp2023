import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 14})

cols=['node','x','y','z']
df = pd.read_csv('data/nodes.lst', delim_whitespace=True, names=cols)
x = df['x'].values
fi = df['y'].values
z = df['z'].values

X = -z
Y = x * np.sin(np.radians(fi))
Z = x * np.cos(np.radians(fi))

names = df['node'].values

# Set up a figure twice as tall as it is wide
fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle('NODES MAPPER')

# First subplot
ax = fig.add_subplot(1, 2, 1)
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

ax.set_title('Cylindrical surface nodes unfolded into a plane\n(mouseover node to get its data)')

ax2 = fig.add_subplot(1, 2, 2, projection='3d')

active = ax2.text(0,0,0,'o', color='red',va='center',ha='center')
active.set_visible(False)

def motion_hover(event):
    annotation_visbility = annotation.get_visible()
    if event.inaxes == ax:
        is_contained, annotation_index = scatter.contains(event)
        if is_contained:
            data_point_location = scatter.get_offsets()[annotation_index['ind'][0]]
            annotation.xy = data_point_location
            idx = annotation_index['ind'][0]
            text_label = 'Node {0}\n(z={1:.1f}mm\n$\\varphi=${2:.1f}$^{{o}}$)\nANSYS\n(X={3:.1f},Y={4:.1f},Z={5:.1f})'.format(names[idx], z[idx], fi[idx], X[idx], Y[idx], Z[idx])
            annotation.set_text(text_label)
            annotation.set_alpha(0.4)
            active.set_position((X[idx],Y[idx]))
            active.set_z(Z[idx])
            active.set_visible(True)
            annotation.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if annotation_visbility:
                annotation.set_visible(False)
                active.set_visible(False)
                fig.canvas.draw_idle()
                
fig.canvas.mpl_connect('motion_notify_event', motion_hover)
ax.set_xlabel('Z (mm)')
ax.set_ylabel('$\\varphi$ ($^{{o}}$)')


ax2.set_title('Nodes in ANSYS global coordinate system')

ax2.scatter(X, Y, Z)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.view_init(60,0,90)
ax2.set_aspect('equal')
plt.tight_layout()
plt.show()