from setuptools import setup, find_packages

with open('motogram/__init__.py', 'r') as f:
    exec(f.read())

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

with open('sp-requirements.txt', 'r') as f:
    sp_requirements = f.read().splitlines()

setup(
    name='motogram',
    version=__version__,
    author='Santhosh',
    description='Telegram MTProto bots library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bcncalling/motogram',  
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'dev': sp_requirements,
    },
    keywords=['Telegram', 'MTProto', 'bots', 'motogram', 'pyrogram', 'telethon'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)

