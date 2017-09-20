FROM python:2.7

RUN apt-get update && apt-get  -y --no-install-recommends install python-pip build-essential tcsh \
python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
#update && apt-get install -y python3.5 && apt-get install -y apt-utils
#RUN /bin/bash -c "source activate /root/env/environment && pip install nltk==3.2.1"
#RUN /bin/bash -c "source activate /root/env/environment && python -m nltk.downloader punkt"
#RUN /bin/bash -c "source activate /root/env/environment && pip install tensorflow-gpu==0.12.1"
RUN pip install numpy theano protobuf nltk

WORKDIR /dynet-base/

RUN git clone https://github.com/clab/dynet.git
RUN hg clone https://bitbucket.org/eigen/eigen -r 346ecdb
WORKDIR /dynet-base/dynet
RUN mkdir build
WORKDIR /dynet-base/dynet/build
RUN cmake .. -DEIGEN3_INCLUDE_DIR=/dynet-base/eigen -DPYTHON=`which python`
RUN make -j 2
WORKDIR /dynet-base/dynet/build/python
RUN python setup.py install
RUN export DYLD_LIBRARY_PATH=/path/to/dynet/build/dynet/:$DYLD_LIBRARY_PATH

RUN mkdir /output

WORKDIR /root/

#RUN cd /dynet-base/dynet/examples/python

WORKDIR /opt/

COPY FileTools.py FileTools.py
COPY run_hinge.sh run_hinge.sh
COPY hinge_code.py hinge_code.py

#ENTRYPOINT  ["python" , "-u", "hinge_code.py"]
ENTRYPOINT  ["/opt/run_hinge.sh"]

