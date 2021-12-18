

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
  -DBUILD_SHARED_LIBS=OFF \
  -DBUILD_TESTING=OFF
cmake --build .
cmake --install . --prefix ../../Imathlib
cd ../../../

echo "################################"
echo "build alembic"
echo "################################"

git submodule update --init -- external/alembic
cd external/alembic || exit
git checkout master
git pull origin master
mkdir build
cd build || exit
Imath_dir=$(pwd)/../../Imathlib
echo "Imath_dir: ${Imath_dir}"
cmake .. \
  -DALEMBIC_SHARED_LIBS=OFF \
  -DBUILD_TESTING=OFF \
  -DCMAKE_PREFIX_PATH=${Imath_dir} \
  -DUSE_PYALEMBIC=OFF\
  -DPYALEMBIC_PYTHON_MAJOR=3
cmake --build . --config Release
cmake --install . --prefix ../../alembiclib
cd ../../../