#!/usr/bin/env bash

WORKING_DIR=/code/tests/${TYPE}/
COVER_PACKAGE=/code/domain/

echo "
Pronto para executar testes:
dir=${WORKING_DIR}
cobertura=${COVER_PACKAGE}
filtrar_teste?=\"${TESTFILE}\"
"

# Executa os testes unitarios ou de integracao
nosetests \
    ${WORKING_DIR} \
    --with-xunit \
    --verbosity=2 \
    --with-coverage \
    --cover-erase \
    --cover-package=${COVER_PACKAGE} \
    --cover-branches \
    --exe \
    --cover-min-percentage=15 ${TESTFILE} \