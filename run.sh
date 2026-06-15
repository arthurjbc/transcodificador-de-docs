#!/bin/bash
mkdir -p stubs
python3 -m grpc_tools.protoc -I./protos --python_out=./stubs --grpc_python_out=./stubs ./protos/transcoder.proto
