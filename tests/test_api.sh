#!/bin/bash
set -e
set -u

###########
# Help function
##########
Help()
{
   # Display Help
   echo ""
   echo "****************************************"
   echo "HELP: UBKG API test script"
   echo | tee -a test.out
   echo "Syntax: ./test_api.sh [-option]..."
   echo "option" | tee -a test.out
   echo "-v     test environment: l (local), d (DEV), or p (PROD)"
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

UBKG_URL=$UBKG_URL_LOCAL
echo "Using UBKG at: ${UBKG_URL}" | tee test.out
echo "Only the first 60 characters of output from HTTP 200 returns printed."

echo "TESTS FOR: codes/<code_id/codes GET" | tee -a test.out
echo "1. /codes/SNOMEDCT_US%3A254837009/codes?test=test =>invalid parameter; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?test=test" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. codes/SNOMEDCT_US%3A254837009/codes?sab=999 =>non-existent sab; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?sab=999" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. codes/SNOMEDCT_US%3A254837009X/codes => non-existent code; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009X/codes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. codes/SNOMEDCT_US%3A254837009/codes?sab=CHV,DOID => with sab as comma-delimited list of existing SABs; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?sab=CHV,DOID" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "5. /codes/SNOMEDCT_US%3A254837009/codes?sab=CHV&sab=DOID => with individual sabs; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?sab=CHV&sab=DOID" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: codes/<code_id>/concepts" | tee -a test.out
echo "1. codes/SNOMEDCT_US%3A254837009X/concepts => with invalid code; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009X/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. SNOMEDCT_US%3A254837009/concepts => valid code; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: concepts/<concept_id>/codes GET" | tee -a test.out
echo "1. concepts/C0678222/codes?test=x => invalid parameter; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes?test=x" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C0678222x/codes => invalid concept; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222x/codes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C0678222/codes => valid concept; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: concepts/<concept_id>/concepts GET" | tee -a test.out
echo "1. concepts/C0678222X/concepts => invalid concept; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222X/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C0678222/concepts => valid concept; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR:  concepts/<concept_id>/definitions" | tee -a test.out
echo "1. concepts/C0678222x/definitions => invalid concept; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222x/definitions" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C0678222/definitions => valid concept; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/definitions" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: concepts/<concept_id>/expand GET" | tee -a test.out
echo "1. concepts/C2720507/expand => missing required parameters; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/expand" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C2720507/expand?sab=SNOMEDCT_US&rel=isa&depth2=2 => invalid parameter name; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/expand?sab=SNOMEDCT_US&rel=isa&depth2=2" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C2720507Z/expand?sab=SNOMEDCT_US&rel=isa&depth=2 => invalid concept id; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/expand?sab=SNOMEDCT_US&rel=isa&depth=2" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "4. concepts/C2720507Z/expand?sab=SNOMEDCT_US&rel=isa&depth=z => non-numeric depth; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/expand?sab=SNOMEDCT_US&rel=isa&depth=z" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "5. concepts/C2720507/expand?sab=SNOMEDCT_US&rel=isa&depth=2 => valid parameters; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/expand?sab=SNOMEDCT_US&rel=isa&depth=2" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: concepts/<concept_id>/paths GET " | tee -a test.out
echo "1. concepts//C2720507/paths => missing parameters; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts//C2720507/paths?sab=SNOMEDCT_US&rel2=isa => invalid parameter name; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths?sab=SNOMEDCT_US&rel2=isa" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C2720507z/paths?sab=SNOMEDCT_US&rel=isa => invalid concept_id; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507z/paths?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "4. concepts/C2720507/paths?sab=SNOMEDCT_US&rel=isa => valid parameters; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: concepts/<concept_id>/shortestpaths GET" | tee -a test.out
echo "1. concepts/C2720507/shortestpaths => missing parameters; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/shortestpaths" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C2720507/shortestpaths?target_concept_id=C1272753&sab=SNOMEDCT_US&rel2=isa => invalid parameter name; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/shortestpaths?target_concept_id=C1272753&sab=SNOMEDCT_US&rel2=isa" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C2720507Z/shortestpaths?target_concept_id=C1272753&sab=SNOMEDCT_US&rel=isa => invalid concept_id; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/shortestpaths?target_concept_id=C1272753&sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "4. concepts/C2720507/shortestpaths?target_concept_id=C1272753&sab=SNOMEDCT_US&rel=isa => valid parameters; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/shortestpaths?target_concept_id=C1272753&sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: concepts/<concept_id>/trees GET" | tee -a test.out
echo "1. concepts/C2720507/trees => missing parameters: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/trees" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C2720507/trees?sab2=SNOMEDCT_US&rel=isa&depth=2 => invalid parameter: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/trees?sab2=SNOMEDCT_US&rel=isa&depth=2" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C2720507/trees?sab=SNOMEDCT_US&rel=isa&depth=z => non-numeric depth: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/trees?sab=SNOMEDCT_US&rel=isa&depth=z" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "4. concepts/C2720507/trees?sab=SNOMEDCT_US&rel=isa&depth=3 => depth > 2: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/trees?sab=SNOMEDCT_US&rel=isa&depth=3" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "5. concepts/C2720507Z/trees?sab=SNOMEDCT_US&rel=isa&depth=2 => invalid concept_id: should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/trees?sab=SNOMEDCT_US&rel=isa&depth=2" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "6. concepts/<C2720507/trees?sab=SNOMEDCT_US&rel=isa&depth=2 => valid parameters: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/trees?sab=SNOMEDCT_US&rel=isa&depth=2" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: terms/<term_id>/codes GET" | tee -a test.out
echo "1. terms/Breast%20cancerz/codes => no match; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancerz/codes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. terms/Breast%20cancer/codes GET with match: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/codes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: terms/Breast%20cancerz/concepts GET" | tee -a test.out
echo "1. terms/<term_id>/concepts GET with no match; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancerz/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. terms/Breast%20cancer/concepts GET with match; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

