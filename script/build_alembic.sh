brew install boost
pip3 install numpy
BOOST_ROOT=`echo $(brew --cellar boost)/$(brew list --versions boost | tr ' ' '\n' | tail -1)`
echo ${BOOST_ROOT}

echo "################################"
echo "build Imath"
echo "################################"

git submodule update --init -- external/Imath
cd external/Imath || exit
git checkout master
git pull origin master
mkdir build
cd build || exit
cmake .. \
  -DPYTHON:BOOL="1" \
  -DBOOST_ROOT:PATH=${BOOST_ROOT} 
cmake --build .
cmake --install . --prefix ../../Imathlib
cd ../../../

Imath_dir=$(pwd)/../../Imathlib
echo "Imath_dir: ${Imath_dir}"

echo "################################"
echo "build alembic"
echo "################################"

git submodule update --init -- external/alembic
cd external/alembic || exit
git checkout master
git pull origin master
mkdir build
cd build || exit
cmake .. \
  -DUSE_PYALEMBIC:BOOL="1" \
  -DBOOST_ROOT:PATH=${BOOST_ROOT} \
  -DCMAKE_PREFIX_PATH=${Imath_dir} 
cmake --build . --config Release
cmake --install . --prefix ../../alembiclib
cd ../../../