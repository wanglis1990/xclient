import setuptools

setuptools.setup(
    version='0.2.5',
    name='xclient',
    author='wanglis1990',
    author_email='wanglis1990@gmail.com',
    maintainer='wanglis1990',
    maintainer_email='wanglis1990@gmail.com',
    description='xclient',
    long_description='README.md',
    long_description_content_type='text/markdown',
    packages=['xclient', 'xclient.client', 'xclient.session'],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.21.0',
        'six>=1.15.0',
        'Werkzeug>=1.0.1',  # Werkzeug实现了thead local 和协程local, 借用
    ]
)
