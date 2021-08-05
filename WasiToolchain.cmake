cmake_minimum_required(VERSION 3.4.0)

# -----------------------------------------
# A useful reference for this file is the wasi-sdk equivalent:
# https://github.com/WebAssembly/wasi-sdk/blob/master/wasi-sdk.cmake
#
# BUT there are lots of crucial modifications in here and it's
# used all over the place in this project, so be **very** careful
# when changing it.
# -----------------------------------------

set(INSTALL_DIR /home/kingdo/CLionProjects/client_cpp/runtime/toolchain/bin)
set(RFIT_SYSROOT /home/kingdo/CLionProjects/client_cpp/runtime/llvm-sysroot)

set(EXE_SUFFIX "")

set(UNIX 1)

# Note that system name and processor here are crucial
# Setting system name automatically switches on cross-compiling
set(CMAKE_SYSTEM_NAME Wasm)
set(CMAKE_SYSTEM_VERSION 1)
set(CMAKE_SYSTEM_PROCESSOR wasm32)

if(RFIT_BUILD_SHARED)
    message(STATUS "Faasm building SHARED libraries")

    # See note in README about shared libraries targeting Emscripten
    set(WASM_TRIPLE wasm32-unknown-emscripten)
else()
    message(STATUS "Faasm building STATIC libraries")

    set(WASM_TRIPLE wasm32-wasi)
endif()

set(CMAKE_C_COMPILER_TARGET ${WASM_TRIPLE} CACHE STRING "faasm build")
set(CMAKE_CXX_COMPILER_TARGET ${WASM_TRIPLE} CACHE STRING "faasm build")
message(STATUS "Faasm building target ${CMAKE_CXX_COMPILER_TARGET}")

# Specify LLVM toolchain
set(CMAKE_C_COMPILER ${INSTALL_DIR}/clang)
set(CMAKE_CXX_COMPILER ${INSTALL_DIR}/clang++)
set(CMAKE_AR ${INSTALL_DIR}/llvm-ar CACHE STRING "faasm build")
set(CMAKE_NM ${INSTALL_DIR}/llvm-nm CACHE STRING "faasm build")
set(CMAKE_RANLIB ${INSTALL_DIR}/llvm-ranlib CACHE STRING "faasm build")

# We define dynamic linking functions in Faasm
unset(CMAKE_DL_LIBS CACHE)

# Add definition for flagging Faasm
add_definitions(-D__faasm)

# Note: see Clang wasm-specific flags at
# https://clang.llvm.org/docs/ClangCommandLineReference.html#webassembly Note
# the optimisation level. We want to keep vectorization so stick with O3 Also
# note that the optimisation is crucial to getting any kind of decent
# performance.
#
# We must explicitly exclude atomics here just in case we've accidentally
# introduced them upstream. Use of atomics means we can't link things together:
# https://reviews.llvm.org/D59281
#
# The stack-first here is really important to help detect stack overflow
# issues. Without it the stack will overflow into the global data.
# stack-size is also crucial to bigger functions not messing up

# 23/09/2020 - Remove SIMD
# set(RFIT_COMPILER_FLAGS "-O3 -msimd128 -mno-atomics --sysroot=${RFIT_SYSROOT}")
set(RFIT_COMPILER_FLAGS " \
    -O3 -mno-atomics \
    --sysroot=${RFIT_SYSROOT} \
    -m32 \
    -DANSI \
    -Xlinker --stack-first \
    ")

if(RFIT_BUILD_SHARED)
    set(RFIT_COMPILER_FLAGS "${RFIT_COMPILER_FLAGS} \
        -fPIC \
        -nostdlib \
        -nostdlib++ \
    ")
endif()

set(CMAKE_SYSROOT ${RFIT_SYSROOT} CACHE STRING "faasm build")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${RFIT_COMPILER_FLAGS}" CACHE STRING "faasm build")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${RFIT_COMPILER_FLAGS}" CACHE STRING "faasm build")

# Shared library flags
# See notes in README about WebAssembly and shared libraries
SET(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} \
    -Xlinker --no-entry \
    -Xlinker --shared \
    -Xlinker --export-all \
    -Xlinker --no-gc-sections \
    " CACHE STRING "faasm build")


# This needs to be included to support libcxx with atomics
# -Xlinker --shared-memory 
SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} \
    -Xlinker --stack-first \
    -Xlinker --no-check-features \
    -Xlinker --threads \
    -Xlinker --max-memory=4294901760 \
    " CACHE STRING "faasm build")

# This is important to ensure the right search path
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

set(CMAKE_C_COMPILER_WORKS ON)
set(CMAKE_CXX_COMPILER_WORKS ON)

# Note - order very important here
SET(RFIT_BLAS_LIBS lapack blas f2c)

