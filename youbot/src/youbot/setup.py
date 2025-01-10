import os
from glob import glob
from setuptools import find_packages, setup


package_name = 'youbot'
data_files = []
data_files.append(('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name + '/launch', ['launch/robot_launch.py']))
data_files.append(('share/' + package_name + '/worlds', ['worlds/youbot.wbt']))
data_files.append(('share/' + package_name + '/resource', ['resource/youbot.urdf']))
data_files.append(('share/' + package_name, ['package.xml']))

for root, dirs, files in os.walk('protos'):
    files_in_dir = [os.path.join(root, file) for file in files]  # 获取当前目录中的所有文件
    target_dir = os.path.relpath(root, '.')  # 相对于当前目录的路径
    data_files.append((f'share/{package_name}/{target_dir}', files_in_dir))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user.name@mail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'kuka_youbot_driver = youbot.kuka_youbot_driver:main',
        ],
    },
)
