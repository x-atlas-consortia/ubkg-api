#!/bin/bash
set -e
set -u

INGESTAPI_URL_PROD=https://ingest.api.hubmapconsortium.org
INGESTAPI_URL_DEV=https://ingest-api.dev.hubmapconsortium.org
INGESTAPI_URL_TEST=https://ingest-api.test.hubmapconsortium.org
INGESTAPI_URL_LOCAL=http://localhost:8484
INGESTAPI_URL=$INGESTAPI_URL_DEV

UBKG_URL_PROD=https://ontology.api.hubmapconsortium.org
UBKG_URL_DEV=https://ontology-api.dev.hubmapconsortium.org
UBKG_URL_LOCAL=http://127.0.0.1:5002
UBKG_URL=$UBKG_URL_LOCAL

SEARCH_URL_DEV=https://search-api.dev.hubmapconsortium.org
SEARCH_URL_TEST=https://search-api.test.hubmapconsortium.org
SEARCH_URL=$SEARCH_URL_DEV

UUID_URL_DEV=https://uuid-api.dev.hubmapconsortium.org
UUID_URL=$UUID_URL_DEV

# Note: this must be a "Data Admin" token and only Bill or Joe can generate one...
TOKEN=OBVrztSx2PEQrgDhoSr5MtIGTHE0n2CQOnY0XzlIk

# https://github.com/x-atlas-consortia/ubkg-api

#echo "search-api ..."
#curl --request GET \
# --url "${SEARCH_URL}/v3/assaytype/bulk-RNA" \
# --header "Authorization: Bearer ${TOKEN}"
#echo
#
#echo "ubkg-api GET ..."
#curl --request GET \
# --url "${UBKG_URL}/assaytype/bulk-RNA?application_context=HUBMAP" \
# --header "Authorization: Bearer ${TOKEN}"
#echo
#
#echo "ubkg-api POST..."
#curl --request POST \
# --url "${UBKG_URL}/assayname?application_context=HUBMAP" \
# --header "Content-Type: application/json" \
# --header "Authorization: Bearer ${TOKEN}" \
# --data '{"name": "bulk-RNA"}'
#echo
#
#echo "search-spi POST array..."
#curl --request POST \
# --url "${SEARCH_URL}/v3/assayname" \
# --header "Content-Type: application/json" \
# --header "Authorization: Bearer ${TOKEN}" \
# --data '{"name": ["PAS", "PAS microscopy"]}'
#echo
#
#echo "ubkg-api POST array..."
#curl --request POST \
# --url "${UBKG_URL}/assayname" \
# --header "Content-Type: application/json" \
# --header "Accept: application/json" \
# --header "Authorization: Bearer ${TOKEN}" \
# --data '{"name": ["ATACseq-bulk"], "application_context": "HUBMAP"}'
#echo
#
#curl --request GET \
# --url "${UBKG_URL}/relationships/hgnc-id/HGNC%3A7178" \
# --header "Accept: application/json" \
# --header "Authorization: Bearer ${TOKEN}"
#echo



echo "Using HGNC ID (HGNC:7178)..."
curl --request GET \
 --url "${UBKG_URL}/relationships/gene/HGNC%3A7178" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "Using Approved Name (multimerin 1)..."
curl --request GET \
 --url "${UBKG_URL}/relationships/gene/multimerin%201" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "Using Symbol Alias (EMILIN4)..."
curl --request GET \
 --url "${UBKG_URL}/relationships/gene/EMILIN4" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "Using Symbol Alias (GPIa*)..."
curl --request GET \
 --url "${UBKG_URL}/relationships/gene/GPIa*" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "Using Symbol Alias (ECM)..."
curl --request GET \
 --url "${UBKG_URL}/relationships/gene/ECM" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "Using Approved Symbol (MMRN1)..."
curl --request GET \
 --url "${UBKG_URL}/relationships/gene/MMRN1" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "Using Previous Symbol (MMRN)..."
curl --request GET \
 --url "${UBKG_URL}/relationships/gene/MMRN" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "Using Previous Symbol (mmrn)..."
curl --request GET \
 --url "${UBKG_URL}/relationships/gene/mmrn" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo
#  --data '{"name": ["ATACseq-bulk"], "application_context": "HUBMAP"}'
#  --data '{"name": []}'
#  --data '{"name": ["PAS", "PAS microscopy"]}'
#  --data '{"name": ["PAS"], "application_context": "hubmap"}'

