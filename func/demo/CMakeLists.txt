function(demo_func exec_name dir_path)
    rfit_func(${exec_name} ${dir_path})
    set(ALL_DEMO_FUNCS ${ALL_DEMO_FUNCS} ${exec_name} PARENT_SCOPE)
endfunction(demo_func)


demo_func(hello hello.cpp)
demo_func(hello_world hello_world.cpp)

#rfit_dynamic_func(dynlink dynlink.cpp)
#set(ALL_DEMO_FUNCS ${ALL_DEMO_FUNCS} dynlink)

# Custom target to group all the demo functions
add_custom_target(demo_all_funcs DEPENDS ${ALL_DEMO_FUNCS})

