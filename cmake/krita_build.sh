#!/bin/bash

export PYTHONHOME=/home/kinow/Development/python/anaconda3/bin/

cmake -G "Eclipse CDT4 - Unix Makefiles" ../krita -DCMAKE_INSTALL_PREFIX=/home/kinow/Development/cpp/workspace/krita_install/ -DWITH_GMIC=ON -DPACKAGERS_BUILD=OFF -DBUILD_TESTING=OFF -DKDE4_TEST_OUTPUT=OFF -DCMAKE_CXX_FLAGS_KRITADEVS="-O0 -g" -DKDE_SKIP_UNINSTALL_TARGET=ON -DCMAKE_CXX_FLAGS="-O0 -g" -DCFLAGS="-O0 -g" -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_DEBUG="-O0 -g"

make -j8

exit 0
