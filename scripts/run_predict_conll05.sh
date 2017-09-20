#!/bin/bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda:/usr/local/cuda/lib64:/opt/OpenBLAS/lib

INPUT_PATH=$PWD/data/srl/conll05.devel.txt
#GOLD_PATH="${data_pref}.props.gold.txt"
MODEL_PATH=$PWD/conll05_model

if [ "$#" -gt 0 ]; then
	if [ "$1" == '-h' ]; then
		echo "Usage $0 <input_path=$INPUT_PATH> <model_path=$MODEL_PATH> <extra args (or -)> <use gpus>"
		exit -1
	fi
	INPUT_PATH=$1
	if [ "$#" -gt 1 ]; then
		MODEL_PATH=$2
		if [ "$#" -gt 2 ] && [ "$3" != "-" ]; then
			EXTRA_ARGS="$3"
		fi
	fi
fi
	
name=`echo $data_pref | awk -F . '{print $(NF)}'`
echo $name


OUTPUT_PATH="temp/conll05.${name}2.out"

if [ "$#" -gt 3 ]
then
echo bla
exit
THEANO_FLAGS="optimizer=fast_compile,device=gpu$1,floatX=float32,lib.cnmem=0.8" python python/predict.py \
  --model="$MODEL_PATH" \
  --input="$INPUT_PATH" \
  --output="$OUTPUT_PATH" \
  $EXTRA_ARGS
else
THEANO_FLAGS="optimizer=fast_compile,floatX=float32" python -u python/predict.py \
  --model="$MODEL_PATH" \
  --input="$INPUT_PATH" \
  --output="$OUTPUT_PATH" \
  $EXTRA_ARGS
fi

