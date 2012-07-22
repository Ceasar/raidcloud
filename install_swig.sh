# Install SWIG
if [ ! -d $CACHE_DIR/swig ]; then
  cd $BUILD_DIR
  echo "-----> Fetching and installing SWIG 2"
  curl -O https://s3.amazonaws.com/guybowden/swig.tar.gz >/dev/null 2>&1
  echo "-----> Installing ..."
  tar xzvf swig.tar.gz >/dev/null 2>&1
  mv swig $CACHE_DIR/swig
  rm swig.tar.gz
  echo "SWIG installed" | indent
fi

mkdir -p .paybox
cp -R $CACHE_DIR/swig .paybox

echo "updating path..." | indent
PATH=$PATH:/app/.paybox/swig/bin/
export PATH
echo $PATH | indent
echo "setting SWIG_LIB environment var"
export SWIG_LIB=/app/.paybox/swig/share/swig/2.0.5/
