#!/usr/bin/env bash

o_dir=/output/
o_file=$o_dir/metrics.json

v=`echo "$MIN_THR < $MAX_THR" | bc`;
if [ $v -eq 1 ]; then
    echo "$MIN_THR < $MAX_THR"
    echo "{" > $o_file
    for i in A0 A1 A2 A3; do
        echo "\"$i\": -1," >> $o_file
    done

    echo "\"Overall\": -1" >> $o_file
    echo "}" >> $o_file
    exit 0
#else
#    echo "$MIN_THR >= $MAX_THR ($v)! great"
fi

emb_file=${PREFIX}_${MIN_THR}_${MAX_THR}.dat.gz

scripts/run_predict_conll05.sh ${TEST_FILE} \
                ${MODEL_DIR} "--embeddings $emb_file -d $o_dir $ADDITIONAL_PARAMS --ouptput $o_dir/output.dat" | tee out.log

ret_val=$?
echo $out

echo $ret_val

function write_val {
    local w=$1
    local suf=$2

    val=`grep " ${w} " out.log | awk '{print $7}'`

    echo "  \"${w}\": ${val}$suf" >> $o_file


}
if [ $ret_val -eq 0 ]; then
    echo "{" > $o_file
    for i in A0 A1 A2 A3 AM-LOC AM-TMP; do
        write_val $i ","
    done

    write_val "Overall" ""
    echo "}" >> $o_file
fi

/bin/rm out.log

