#!/bin/bash
set -e
set -u

UBKG_URL_PROD=https://ontology.api.hubmapconsortium.org
UBKG_URL_DEV=https://ontology-api.dev.hubmapconsortium.org
UBKG_URL_TEST=https://ontology-api.test.hubmapconsortium.org
UBKG_URL_LOCAL=http://127.0.0.1:5002

UBKG_URL=$UBKG_URL_LOCAL
echo "Using UBKG at: ${UBKG_URL}"

echo "codes/<code_id>/codes GET"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%20254837009/codes?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "codes/<code_id>/concepts GET"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%20254837009/concepts?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "concepts/<concept_id>/codes GET"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "concepts/<concept_id>/concepts GET"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/concepts?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "concepts/<concept_id>/definitions GET"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/definitions?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "concepts/<concept_id>/semantics GET"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/semantics?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "concepts/expand POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/expand" \
 --header "Content-Type: application/json" \
 --data '{"query_concept_id": "C2720507", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "isa"], "depth": 2}'
echo

echo "concepts/paths POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/paths" \
 --header "Content-Type: application/json" \
 --data '{"query_concept_id": "C2720507", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "isa"]}'
echo

echo "concepts/shortestpaths POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/shortestpaths" \
 --header "Content-Type: application/json" \
 --data '{"query_concept_id": "C2720507", "target_concept_id": "C1272753", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "part_of"]}'
echo

echo "concepts/trees POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/trees" \
 --header "Content-Type: application/json" \
 --data '{"query_concept_id": "C2720507", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "isa"], "depth": 2}'
echo

echo "semantics/<semantic_id>/semantics GET"
curl --request GET \
 --url "${UBKG_URL}/semantics/Physical%20Object/semantics?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "terms/<term_id>/codes GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/codes?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "terms/<term_id>/concepts GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "terms/<term_id>/concepts/terms GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts/terms?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "tui/<tui_id>/semantics GET"
curl --request GET \
 --url "${UBKG_URL}/tui/T200/semantics?application_context=HUBMAP" \
 --header "Accept: application/json"
echo
