#!/usr/bin/env bash

v=`echo "$MAX < $MIN" | bc`;
if [ $v -eq 1 ]; then
    echo "$MAX < $MIN"
    exit 0
else
    echo "We're all set!"
fi

emb_file=${PREFIX}_${MAX}_${MIN}.dat.gz

scripts/run_predict_conll05.sh ${TEST_FILE} \
                ${MODEL_DIR} "--embeddings $emb_file $ADDITIONAL_PARAMS" | tee out.log
ret_val=$?
echo $out

echo $ret_val

if [ $ret_val -eq 0 ]; then
    val=`grep Overall out.log | awk '{print $8}'`

    echo "{overall: $val}" >> /ouptut/metrics.json
fi

/bin/rm out.log

