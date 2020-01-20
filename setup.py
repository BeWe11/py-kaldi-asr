from __future__ import print_function
from setuptools import setup, Extension
import numpy
import subprocess
import sys
import os

try:
    from Cython.Distutils import build_ext
except ImportError:
	raise Exception ("*** cython is needed to build this extension.")

cmdclass = { }
ext_modules = [ ]

def getstatusoutput(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, _ = process.communicate()
    return (process.returncode, out)

def find_dependencies():

    kw = {}

    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    
    #
    # pkgconfig: kaldi-asr
    #
    
    status, output = getstatusoutput(["pkg-config", "--libs", "--cflags", "kaldi-asr"])
    
    if status != 0:
    	raise Exception("*** failed to find pkgconfig for kaldi-asr")
    
    for token in output.split():

        token = token.decode('utf8')

        prefix = token[:2]
        arg    = token[2:]

        # print(repr(token))
        # print(repr(prefix))

        kw.setdefault(flag_map.get(prefix), []).append(arg)
   
    # print (repr(kw))
 
    return kw

# CFLAGS = -Wall -pthread -std=c++11 -DKALDI_DOUBLEPRECISION=0 -Wno-sign-compare \
#          -Wno-unused-local-typedefs -Winit-self -DHAVE_EXECINFO_H=1 -DHAVE_CXXABI_H -DHAVE_ATLAS \
#          `pkg-config --cflags kaldi-asr` -g

ext_modules += [
    Extension("kaldiasr.nnet3", 
              sources  = [ "kaldiasr/nnet3.pyx", "kaldiasr/nnet3_wrappers.cpp" ],
              language = "c++", 
              extra_compile_args = [ '-Wall', '-pthread', '-std=c++11', '-DKALDI_DOUBLEPRECISION=0', '-Wno-sign-compare', '-Wno-unused-local-typedefs', '-Winit-self', '-DHAVE_EXECINFO_H=1', '-DHAVE_CXXABI_H', '-g'  ],
              **find_dependencies()),
	Extension("kaldiasr.gmm", 
			  sources  = [ "kaldiasr/gmm.pyx", "kaldiasr/gmm_wrappers.cpp" ],
			  language = "c++", 
			  extra_compile_args = [ '-Wall', '-pthread', '-std=c++11', '-DKALDI_DOUBLEPRECISION=0', '-Wno-sign-compare', '-Wno-unused-local-typedefs', '-Winit-self', '-DHAVE_EXECINFO_H=1', '-DHAVE_CXXABI_H', '-g'  ],
			  **find_dependencies()),
]
cmdclass.update({ 'build_ext': build_ext })

setup(
    name                 = 'py-kaldi-asr',
    version              = '0.5.2',
    description          = 'Simple Python/Cython interface to kaldi-asr nnet3/chain and gmm decoders',
    long_description     = open('README.md').read(),
    author               = 'Guenter Bartsch',
    author_email         = 'guenter@zamia.org',
    maintainer           = 'Guenter Bartsch',
    maintainer_email     = 'guenter@zamia.org',
    url                  = 'https://github.com/gooofy/py-kaldi-asr',
    packages             = ['kaldiasr'],
    cmdclass             = cmdclass,
    ext_modules          = ext_modules,
    include_dirs         = [numpy.get_include()],
    classifiers          = [
                               'Operating System :: POSIX :: Linux',
                               'License :: OSI Approved :: Apache Software License',
                               'Programming Language :: Python :: 2',
                               'Programming Language :: Python :: 2.7',
                               'Programming Language :: Python :: 3',
                               'Programming Language :: Python :: 3.5',
                               'Programming Language :: Cython',
                               'Programming Language :: C++',
                               'Intended Audience :: Developers',
                               'Topic :: Software Development :: Libraries :: Python Modules',
                               'Topic :: Multimedia :: Sound/Audio :: Speech'
                           ],
    license              = 'Apache',
    keywords             = 'kaldi asr',
    include_package_data = True,
    install_requires     = ['numpy', 'cython', ],
    )

