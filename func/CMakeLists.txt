cmake_minimum_required(VERSION 3.8.0)
project(rfit-func)

set(CMAKE_CXX_STANDARD 17)

message(STATUS "Detected wasm build (sysroot=${CMAKE_SYSROOT})")

# NOTE: we have to set the max memory here but want it to be as close to the
# max (4GB) as possible. If we set it to the max though, this input is
# ignored and the function is set with no maximum memory size.  Therefore we
# set it to 4GB - 1 page, i.e.  max-memory = (4*1024*1024*1024) - (64*1024)
# = 4294901760.
#
# WARNING: the code may also set limits on the max memory size, so must be
# changed there too (IRModuleCache.h)
#
# This max memory limit can stop benchmarks working so make sure it's big
# and consider restricting in a more specific manner for certain functions.

# -Xlinker --export=_faasm_zygote \
SET(CMAKE_EXE_LINKER_FLAGS "
        -Xlinker --export=__heap_base \
        -Xlinker --export=__data_end \
        -Xlinker --export-all \
        -Xlinker --export=__wasm_call_ctors \
        -Xlinker --max-memory=4294901760 \
        -Wl,-z,stack-size=4194304 -Wl, \
    ")

SET(CMAKE_EXECUTABLE_SUFFIX ".wasm")

set(RFIT_FUNC_LIBS rfit c-printscan-long-double)

function(rfit_func func_name file_name)
    add_executable(${func_name} ${file_name})
    target_link_libraries(${func_name} ${RFIT_FUNC_LIBS})
endfunction(rfit_func)

function(rfit_dynamic_func func_name file_name)
    rfit_func(${func_name} ${file_name})

    # These are the linker flags required for functions that will also do
    # dynamic linking.
    # We need to export all symbols to make them available to the
    # dynamically loaded modules
    set_target_properties(${func_name} PROPERTIES
            LINK_FLAGS "-Xlinker --export-all -Xlinker --no-gc-sections"
            )

endfunction(rfit_dynamic_func)

add_subdirectory(demo)
