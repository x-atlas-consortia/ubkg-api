#!/bin/bash
set -e
set -u

#########
# FULL SYSTEM TEST SCRIPT
# This script calls endpoints of the ubkg-api to validate the environment, including 
# responses to large response payloads or timeouts.
# Use the unit test script to check endpoints in all scenarios, such as bad parameters.
##########


###########
# Help function
##########
Help()
{
   # Display Help
   echo ""
   echo "****************************************"
   echo "HELP: UBKG API SYSTEM TEST SCRIPT"
   echo | tee
   echo "Syntax: ./ubkg_api-system-test.sh [-option]..."
   echo "option" | tee
   echo "-v     test environment: l (local), d (DEV), or p (PROD)"
   echo "NOTE: This script writes output to a file named ubkg_system_test.out."
}

#####
# Get options
while getopts ":hv:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      v) # environment
         env=$OPTARG;;
      \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done


UBKG_URL_PROD=https://ontology.api.hubmapconsortium.org
UBKG_URL_DEV=https://ontology-api.dev.hubmapconsortium.org
UBKG_URL_TEST=https://ontology-api.test.hubmapconsortium.org
UBKG_URL_LOCAL=http://127.0.0.1:5002

# Map to selected API environment.
case "$env" in
  l) # local
    UBKG_URL="${UBKG_URL:-$UBKG_URL_LOCAL}";;
  d) # DEV
    UBKG_URL="${UBKG_URL:-$UBKG_URL_DEV}";;
  p) # PROD
    UBKG_URL="${UBKG_URL:-$UBKG_URL_PROD}";;
  \?) # default to local machine
    UBKG_URL="${UBKG_URL:-$UBKG_URL_LOCAL}";;

esac

# UBKG_URL=$UBKG_URL_LOCAL
echo "Using UBKG at: ${UBKG_URL}" | tee ubkg_system_test.out
echo "Only the first 60 characters of output from HTTP 200 returns displayed."

#--------------------------------------------


echo "/codes/SNOMEDCT_US%3A254837009/codes?sab=CHV,DOID"| tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?sab=CHV,DOID" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/codes/SNOMEDCT_US%3A254837009/concepts" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/codes/SNOMEDCT_US%3A254837009/terms?term_type=PT" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/terms?term_type=PT" \
 --header "Accept: application/json" | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/C0678222/codes" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/C0010346/concepts" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C4722518/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/C0678222/definitions" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/definitions" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=0&limit=10" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/C0006142/paths/subgraph/sequential?relsequence=NCI%3Ais_marked_by_gene_product,NCI%3Agene_product_encoded_by_gene&skip=0&limit=5" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0006142/paths/subgraph/sequential?relsequence=NCI:is_marked_by_gene_product,NCI:gene_product_encoded_by_gene&skip=0&limit=5" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/arm/nodeobjects" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/arm/nodeobjects" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&skip=0&limit=10" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=1&limit=10" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=1&limit=10" \
--header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/node-types GET" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/node-types" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/node-types/Code/counts GET" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/node-types/Code/counts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/node-types/Code/counts-by-sab?sab=SNOMEDCT_US GET " | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/node-types/Code/counts-by-sab?sab=SNOMEDCT_US" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/property-types GET" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/property-types" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/relationship-types GET" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/relationship-types" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/sabs GET" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/sabs" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/sabs/codes/counts?skip=5&limit=10" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/codes/counts?skip=5&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/sabs/SNOMEDCT_US/codes/counts?skip=0&limit=10" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/counts?skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/sabs/SNOMEDCT_US/codes/details?skip=0&limit=10" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/details?skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/sabs/SNOMEDCT_US/term-types" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/term-types" \
 --header "Accept: application/json"  | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/semantics/semantic-types" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic-types?skip=1&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "semantics/semantic-types/Anatomical%20Structure?&skip=0&limit=10" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic-types/Anatomical%20Structure?&skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo | tee -a ubkg_system_test.out
echo "/semantics/semantic-types/Anatomical%20Structure/subtypes?skip=1&limit=10" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic-types/Anatomical%20Structure/subtypes?skip=1&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/terms/codes/Breast%20cancer GET" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/codes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/terms/Breast%20cancer/concepts GET" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out

echo "/sources GET" | tee -a ubkg_system_test.out
curl --request GET \
 --url "${UBKG_URL}/sources" \
 --header "Accept: application/json" | cut -c1-60 | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out
echo | tee -a ubkg_system_test.out


