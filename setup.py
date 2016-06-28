from setuptools import setup

setup(
    name="vmprof-flamegraph",
    version="0.0.1",
    author="INADA Naoki",
    description="Convert vmprof data into flamegraph format",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['vmprof'],
    scripts=["vmprof-flamegraph.py"],
)
