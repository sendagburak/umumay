# SPDX-License-Identifier: GPL-3.0-or-later
from setuptools import setup

setup(
    name='umumay', version='0.1.4',
    description='Umumay: offline modular desktop utilities',
    packages=['umumay'],
    package_data={'umumay': ['privacy_tr.txt', 'privacy_en.txt', 'umumay.png', '*.desktop']},
    url='https://github.com/sendagburak/umumay',
    python_requires='>=3.9', license='GPL-3.0-or-later',
    entry_points={'console_scripts': ['umumay=umumay.__main__:main']},
)
