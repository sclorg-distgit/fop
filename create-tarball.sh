#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-tarball.sh VERSION"
    exit 1
fi

VERSION=${1}
NAME="fop"

wget http://archive.apache.org/dist/xmlgraphics/fop/source/${NAME}-${VERSION}-src.tar.gz
tar xvf ${NAME}-${VERSION}-src.tar.gz

(
  cd ${NAME}-${VERSION}
  # non-free color profile
  find src/java/org/apache/fop/pdf/ -name "*.icm*" -delete
  find ./ -name "*.jar" -delete
  find ./ -name "*.pdf" -delete
  # serialized objects
  find ./${NAME}-${VERSION}/ -name "*.ser" -delete
  # examples, tests, ...
  rm -Rf lib/ examples/ test/ hyph/
  rm -Rf src/documentation/
  mkdir -p lib/build/
)

tar czvf ${NAME}-${VERSION}-clean.tar.gz ${NAME}-${VERSION}
rm -Rf ${NAME}-${VERSION}.tar.gz

