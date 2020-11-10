#!/usr/bin/env bash

cd ..
BASEDIR=$(pwd)

EX_HOME=$(cat config.json | jq .EX_HOME)
EX_HOME=${EX_HOME:1:-1}

DATA_DIR=$(cat config.json | jq .DATA_HOME)
DATA_DIR=${DATA_DIR:1:-1}
TMP_DIR=${EX_HOME}/tmp_data

mkdir -p $DATA_DIR $TMP_DIR

FILECNT=$(ls $TMP_DIR | wc -l)

if [ $FILECNT = 0 ] ; then
    echo '>>>> Start Datagen for Training.'

    python datagen.py \
      --data_dir=$DATA_DIR \
      --data=dishes.xlsx

    echo '>>>> End Datagen for Training.'
else
    echo '>>>> Dataset files are already exist in target dir. Check and try datagen again.'
fi