
cmake_minimum_required(VERSION 3.12)

enable_language(CXX)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
if(MSVC)
  set(CMAKE_CXX_FLAGS "/W4")
else()
  set(CMAKE_CXX_FLAGS "-Wall -g")
endif()

project(delfem2)

# cpp & cmake setting
##########################################################
# dependencies setting

# pybind11
set(PYBIND11_DIR "${PROJECT_SOURCE_DIR}/external/pybind11")
add_subdirectory(${PYBIND11_DIR} pybind11)

# glfw
# set(GLFW_ROOT "${PROJECT_SOURCE_DIR}/external/libglfw")
# include(${CMAKE_CURRENT_SOURCE_DIR}/external/FindGLFW.cmake)

##########################################################
# build setting

include_directories(
    ${PROJECT_SOURCE_DIR}/external/delfem2/include
    ${PROJECT_SOURCE_DIR}/external/eigen
    ${PROJECT_SOURCE_DIR}/external/glad3/include
#    ${GLFW_INCLUDE_DIR}
)

file(GLOB SRC_FILES
    ${PROJECT_SOURCE_DIR}/src/*.cpp)
set(INPUT_SRC
    ${SRC_FILES}
    ${PROJECT_SOURCE_DIR}/external/glad3/src/glad.c
    )

message(STATUS "src paths: ${SRC_FILES}")

pybind11_add_module(${PROJECT_NAME}
    ${INPUT_SRC} )

#target_link_libraries(${PROJECT_NAME} PRIVATE
#    ${GLFW_LIBRARIES})

# build & link
###########################################
# post build

file(TO_NATIVE_PATH "${PROJECT_BINARY_DIR}" NATIVE_PROJECT_BINARY_DIR)
file(TO_NATIVE_PATH "${PROJECT_SOURCE_DIR}" NATIVE_PROJECT_SOURCE_DIR)

if(MSVC)
  add_custom_command(TARGET ${PROJECT_NAME}
  POST_BUILD
    COMMAND copy 
      "${NATIVE_PROJECT_BINARY_DIR}\\${CMAKE_CFG_INTDIR}\\${PROJECT_NAME}.*.pyd"   
      ${NATIVE_PROJECT_SOURCE_DIR}\\delfem2
    COMMENT "Post Event"
  )
else()
  add_custom_command(TARGET ${PROJECT_NAME}
  POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy 
      ${PROJECT_BINARY_DIR}/${CMAKE_CFG_INTDIR}/${PROJECT_NAME}.*
      ${PROJECT_SOURCE_DIR}/delfem2
    COMMENT "Post Event"
  )
endif()
