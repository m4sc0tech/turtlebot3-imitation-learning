from setuptools import find_packages, setup

package_name = 'turtlebot3_logger'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='matias',
    maintainer_email='m4sc0tech@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'logger_node = turtlebot3_logger.logger_node:main',
            'teleop_node = turtlebot3_logger.teleop_node:main',
            'inference_node = turtlebot3_logger.inference_node:main',
        ],
    },
)
