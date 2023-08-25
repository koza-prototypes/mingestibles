#!/bin/bash

rm output/monarch-kg.db || true
echo "Decompressing tsv files..."
tar zxf output/monarch-kg.tar.gz -C output
gunzip output/qc/monarch-kg-dangling-edges.tsv.gz
gunzip output/monarch-kg-denormalized-edges.tsv.gz

echo "Loading nodes..."
sqlite3 -cmd ".mode tabs" output/monarch-kg.db ".import output/monarch-kg_nodes.tsv nodes"
echo "Loading edges..."
sqlite3 -cmd ".mode tabs" output/monarch-kg.db ".import output/monarch-kg_edges.tsv edges"
echo "Loading dangling edges..."
sqlite3 -cmd ".mode tabs" output/monarch-kg.db ".import output/qc/monarch-kg-dangling-edges.tsv dangling_edges"
echo "Loading denormalized edges..."
sqlite3 -cmd ".mode tabs" output/monarch-kg.db ".import output/monarch-kg-denormalized-edges.tsv denormalized_edges"

sqlite3 output/monarch-kg.db "CREATE TABLE closure (subject TEXT, predicate TEXT, object TEXT)"
sqlite3 -cmd ".mode tabs" output/monarch-kg.db ".import data/monarch/phenio-relation-graph.tsv closure"

echo "Cleaning up..."
rm output/monarch-kg_*.tsv
gzip --force output/qc/monarch-kg-dangling-edges.tsv
gzip --force output/monarch-kg-denormalized-edges.tsv

echo "Compressing database"
gzip --force output/monarch-kg.db
