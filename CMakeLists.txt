
cmake_minimum_required(VERSION 3.12)

enable_language(CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
if(MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
else()
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -g")
endif()

project(delfem2)

# cpp & cmake setting
##########################################################
# dependencies setting

# eigen
FIND_PACKAGE(Eigen3 REQUIRED)
get_target_property(EIGEN_INCLUDE_DIR Eigen3::Eigen INTERFACE_INCLUDE_DIRECTORIES)
message(STATUS "eigen include dir: ${EIGEN_INCLUDE_DIR}")

# pybind11
If(EXISTS ${PROJECT_SOURCE_DIR}/external/pybind11/CMakeLists.txt)
  set(PYBIND11_DIR ${PROJECT_SOURCE_DIR}/external/pybind11)
ELSEIF(EXISTS ${PROJECT_SOURCE_DIR}/../pybind11/CMakeLists.txt)
  set(PYBIND11_DIR ${PROJECT_SOURCE_DIR}/../pybind11)
ENDIF()
message(STATUS "pybind11 dir: ${PYBIND11_DIR}")

# delfem2
If(EXISTS ${PROJECT_SOURCE_DIR}/external/delfem2/include)
  set(DELFEM2_DIR ${PROJECT_SOURCE_DIR}/external/delfem2)
ELSEIF(EXISTS ${PROJECT_SOURCE_DIR}/../delfem2/include)
  set(DELFEM2_DIR ${PROJECT_SOURCE_DIR}/../delfem2)
ENDIF()
message(STATUS "delfem2 dir: ${DELFEM2_DIR}")

##########################################################
# build setting

include_directories(
    ${DELFEM2_DIR}/include
    ${EIGEN_INCLUDE_DIR}
    ${PROJECT_SOURCE_DIR}/external/glad3/include
)

file(GLOB SRC_FILES
    ${PROJECT_SOURCE_DIR}/src/*.cpp)
set(INPUT_SRC
    ${SRC_FILES}
    ${PROJECT_SOURCE_DIR}/external/glad3/src/glad.c
    )

message(STATUS "src paths: ${SRC_FILES}")

add_subdirectory(${PYBIND11_DIR} build)
pybind11_add_module(${PROJECT_NAME}
    ${INPUT_SRC} )

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
