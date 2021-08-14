
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

set(PYBIND11_DIR "${PROJECT_SOURCE_DIR}/external/pybind11")
add_subdirectory(${PYBIND11_DIR} pybind11)

##########################################################
# build setting

include_directories(
    ${PROJECT_SOURCE_DIR}/external/delfem2/include
    ${PROJECT_SOURCE_DIR}/external/eigen
)

file(GLOB SRC_FILES
    ${PROJECT_SOURCE_DIR}/src/*.cpp)
set(INPUT_SRC  ${SRC_FILES})

message(STATUS "src paths: ${SRC_FILES}")

pybind11_add_module(${PROJECT_NAME}
  ${INPUT_SRC} )

#target_link_libraries(${PROJECT_NAME}
#  PRIVATE ${INPUT_LIBRARY})

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
