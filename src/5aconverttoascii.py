from plyfile import PlyData

# Load binary PLY
plydata = PlyData.read('point_cloud.ply')

# Set to ASCII format
plydata.text = True

# Write to ASCII PLY
plydata.write('point_cloud_ascii.ply')