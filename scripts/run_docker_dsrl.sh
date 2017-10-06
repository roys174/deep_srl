#!/usr/bin/env bash

v=`echo "$MIN_THR < $MAX_THR" | bc`;
if [ $v -eq 1 ]; then
    echo "$MIN_THR < $MAX_THR"
    echo "{" > /output/metrics.json
    for i in A0 A1 A2 A3; do
        echo "\"$i\": -1," >> /output/metrics.json
    done

    echo "\"Overall\": -1" >> /output/metrics.json
    echo "}" >> /output/metrics.json
    exit 0
#else
#    echo "$MIN_THR >= $MAX_THR ($v)! great"
fi

emb_file=${PREFIX}_${MIN_THR}_${MAX_THR}.dat.gz

scripts/run_predict_conll05.sh ${TEST_FILE} \
                ${MODEL_DIR} "--embeddings $emb_file $ADDITIONAL_PARAMS" | tee out.log

ret_val=$?
echo $out

echo $ret_val

function write_val {
    local w=$1
    local suf=$2

    val=`grep " ${w} " out.log | awk '{print $7}'`

    echo "  \"${w}\": ${val}$suf" >> /output/metrics.json


}
if [ $ret_val -eq 0 ]; then
    echo "{" > /output/metrics.json
    for i in A0 A1 A2 A3 AM-LOC AM-TMP; do
        write_val $i ","
    done

    write_val "Overall" ""
    echo "}" >> /output/metrics.json
fi

/bin/rm out.log

