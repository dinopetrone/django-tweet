from setuptools import setup, find_packages

setup(
    name='django-tweet',
    version='0.0.1',
    description='Django app for sending mass tweets.',
    author='Dino Petrone',
    author_email='dinopetrone@gmail.com',
    url='https://github.com/dinopetrone/django-tweet',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['gevent==0.13.8', 'celery==3.0.12', 
                      'django-celery==3.0.11'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
