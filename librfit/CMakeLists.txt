cmake_minimum_required(VERSION 3.0)
project(librfit)

# ------ Rfit C/C++ library ------ #

set(CMAKE_CXX_STANDARD 17)

set(PUBLIC_HEADERS
        include/core.h
        include/host_interface.h
        include/rfit.h
        include/emscripten.h
        )

set(LIB_FILES
        core.cpp
        zygote.cpp
        ping.cpp
        emscripten.c
        )


message(STATUS "Librfit WebAssembly build")

add_library(rfit STATIC ${LIB_FILES})
set_target_properties(rfit PROPERTIES PUBLIC_HEADER "${PUBLIC_HEADERS}")

# Install in WASM sysroot
install(TARGETS rfit
        ARCHIVE DESTINATION ${CMAKE_SYSROOT}/lib/wasm32-wasi
        LIBRARY DESTINATION ${CMAKE_SYSROOT}/lib/wasm32-wasi
        PUBLIC_HEADER DESTINATION ${CMAKE_SYSROOT}/include/rfit
        )

# Add allowed import files
install(
        FILES rfit.imports
        DESTINATION ${CMAKE_SYSROOT}/lib/wasm32-wasi
        RENAME librfit.imports
)


target_include_directories(rfit PUBLIC ${CMAKE_CURRENT_LIST_DIR}/include)
