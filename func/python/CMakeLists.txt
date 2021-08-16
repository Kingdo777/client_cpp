set(PYTHON_LIBRARIES ${CMAKE_SYSROOT}/lib/wasm32-wasi/libpython3.8.a)
set(PYTHON_INCLUDE_DIRS ${CMAKE_SYSROOT}/include/python3.8)

add_executable(py_func pyinit.c pyinit.h py_func.cpp)


target_link_libraries(py_func rfit c-printscan-long-double)
target_link_libraries(py_func ${PYTHON_LIBRARIES})
target_include_directories(py_func PUBLIC ${PYTHON_INCLUDE_DIRS})
# Need to export all symbols to support dynamic linking C-extensions
set_target_properties(py_func PROPERTIES
        LINK_FLAGS "-Xlinker --export-all -Xlinker --no-gc-sections"
        )
