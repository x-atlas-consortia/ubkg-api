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
   echo | tee
   echo "Syntax: ./test_api.sh [-option]..."
   echo "option" | tee
   echo "-v     test environment: l (local), d (DEV), or p (PROD)"
   echo "NOTE: This script writes output to a file named test.out."
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
echo "Only the first 60 characters of output from HTTP 200 returns displayed."

#--------------------------------------------
echo "TESTS FOR: codes/<code_id/codes GET" | tee -a test.out
echo "SIGNATURE: /codes/<code_id>/codes?sab=<SAB>" | tee -a test.out
echo | tee -a test.out
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

#--------------------------------------------
echo "TESTS FOR: codes/<code_id>/concepts" | tee -a test.out
echo "SIGNATURE: /codes/<code_id>/concepts" | tee -a test.out
echo | tee -a test.out
echo "1. codes/SNOMEDCT_US%3A254837009X/concepts => with invalid code; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009X/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. /codes/SNOMEDCT_US%3A254837009/concepts => valid code; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<concept_id>/codes GET" | tee -a test.out
echo "SIGNATURE: /concepts/<concept_id>/codes"| tee -a test.out
echo | tee -a test.out
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

#--------------------------------------------
echo "TESTS FOR: concepts/<concept_id>/concepts GET" | tee -a test.out
echo "SIGNATURE: /concepts/<concept_id>/concepts" | tee -a test.out
echo | tee -a test.out

echo "1. concepts/C0678222Z/concepts => invalid concept; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222Z/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. concepts/C0678222/concepts => valid concept; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR:  concepts/<concept_id>/definitions" | tee -a test.out
echo "SIGNATURE: /concepts/<concept_id>/definitions" | tee -a test.out
echo | tee -a test.out

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

#--------------------------------------------
echo "TESTS FOR: concepts/paths/subgraph" | tee -a test.out
echo "SIGNATURE: /concepts/paths/subgraph?sab=<sab>&rel=<relationship type>&skip=<number>&limit=<number>" | tee -a test.out
echo "Parameters sab and rel can be %2C-delimited list or indidividual values."  | tee -a test.out

echo "1. concepts/paths/subgraph? => missing parameters: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=-1&limit=1 => negative skip: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=-1&limit=1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=1&limit=-1 => negative limit: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=1&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=z&limit=1 => non-numeric skip: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=Z&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=1&limit=Z => non-numeric limit: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=1&limit=Z" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "6. concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isaZ=> invalid parameter value: should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isaz" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "7. concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=0&limit=10 => valid parameters, single sab, single rel: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "8. concepts/paths/subgraph?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of&skip=0&limit=10 => valid parameters, multiple individual sab, rel: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&sab=UBERON&rel=isa&skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "9. concepts/paths/subgraph?sab=SNOMEDCT_US%2CUBERON&rel=isa%2Cpart_of&skip=0&limit=10 => valid parameters,list sab, rel: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/paths/subgraph?sab=SNOMEDCT_US&rel=isa&skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<identifier>/nodes GET" | tee -a test.out
echo "SIGNATURE: /conepts/<identifier>/nodes" | tee -a test.out
echo | tee -a test.out
echo "1. concepts/Cellsz/nodes => invalid identifier; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/CellsZ/nodes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. concepts/Cells/nodes => valid identifier; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/Cells/nodes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<concept_id>/paths/expand GET" | tee -a test.out
echo "SIGNATURE: /concepts/<concept_id>/paths/expand?sab=<SAB>&rel=<relationship type>&mindepth=<number>&maxedepth=<number>&skip=<number>&limit=<number>" | tee -a test.out
echo "Parameters sab and rel can be %2C-delimited list or indidividual values."  | tee -a test.out

echo "1. concepts/C2720507/paths/expand => missing required parameters; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepthZ=2&maxdepth=3&skip=1&limit=10 => invalid parameter name; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepthZ=2&maxdepth=3&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=Z&maxdepth=3&skip=1&limit=10 => non-numeric mindepth; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=Z&maxdepth=3&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=Z&skip=1&limit=10 => non-numeric maxdepth; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=Z&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=-1&maxdepth=3&skip=1&limit=10 => negative mindepth; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=-1&maxdepth=3&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "6. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=-1&skip=1&limit=10 => negative maxdepth; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "7. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=3&maxdepth=2&skip=1&limit=10 => parameter order invalid; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=3&maxdepth=2&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "8. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=-1&limit=10 => negative skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "9. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=1&limit=-1 => negative limit; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=1&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "10. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=Z&limit=10 => non-numeric skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=Z&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "11. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=1&limit=Z => non-numeric limit; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=1&limit=Z" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "12. concepts/C2720507Z/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&skip=1&limit=10 => invalid concept id; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "13. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=1&limit=10 => long query; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "14. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&skip=0&limit=10 => valid parameters, single sab, rel; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "15. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of&mindepth=2&maxdepth=3&skip=0&limit=10 => valid parameters, delimited lists for sab, rel; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of&mindepth=2&maxdepth=3&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "16. concepts/C2720507/paths/expand?sab=SNOMEDCT_US%2CUBERON&rel=isa%2Cpart_of&mindepth=2&maxdepth=3&skip=0&limit=10 => valid parameters, URL-encoded lists for sab, rel; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of&mindepth=2&maxdepth=3&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<concept_id>/paths/trees GET" | tee -a test.out
echo "SIGNATURE: /concepts/<concept_id>/paths/trees?sab=<SAB>&rel=<relationship type>&mindepth=<number>&maxdepth=<number>&skip=<number>&limit=<number>"
echo "Parameters sab and rel can be %2C-delimited list or indidividual values."  | tee -a test.out

echo "1. concepts/C2720507/paths/trees => missing parameters: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&relZ=isa&mindepth=-1&maxdepth=3&skip=1&limit=10  => invalid parameter name: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&relZ=isa&mindepth=-1&maxdepth=3&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=-1&maxdepth=3&skip=1&limit=10 => negative mindepth: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=-1&maxdepth=3&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=-1&skip=1&limit=10 => negative maxdepth: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=-1&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=Z&maxdepth=1&skip=1&limit=10 => non-numeric mindepth: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=Z&maxdepth=-1&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "6. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=Z&skip=1&limit=10 => non-numeric maxdepth: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=Z&maxdepth=-1&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "7. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=3&maxdepth=2&skip=1&limit=10 => invalid range: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=3&maxdepth=2&skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "8. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=-1&limit=10 => negative skip: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=Z&maxdepth=3&skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "9. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=1&limit=-10 => negative limit: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=Z&maxdepth=3&skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "10. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=Z&limit=10 => non-numeric skip: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=Z&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "11. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=1&limit=Z => non-numeric limit: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=1&limit=Z" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "12. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=1&limit=10 => valid, single sab, rel: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=1&maxdepth=3&skip=1&limit=10" \
--header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "13. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of&mindepth=1&maxdepth=3&skip=1&limit=10 => valid, multiple sab, rel: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of&mindepth=1&maxdepth=3&skip=1&limit=10" \
--header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "14. concepts/C2720507/paths/trees?sab=SNOMEDCT_US%2CUBERON&rel=isa%2Cpart_of&mindepth=1&maxdepth=3&skip=1&limit=10 => valid, list sab, rel: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of&mindepth=1&maxdepth=3&skip=1&limit=10" \
--header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<origin_concept_id>/paths/shortestpath/<terminus_concept_id> GET" | tee -a test.out
echo "SIGNATURE: /concepts/<origin_concept_id>/paths/shortestpath/<terminus_concept_id>?sab=<SAB>&rel=<relationship types" | tee -a test.out
echo "Parameters sab and rel can be %2C-delimited list or indidividual values."  | tee -a test.out

echo "1. concepts/C2720507/paths/shortestpath/C1272753 => missing parameters; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/shortestpath/C1272753" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&relZ=isa => invalid parameter name; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel2=isa" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. concepts/C2720507Z/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa => invalid concept_id; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa => valid parameters, single sab, rel; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "5. concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of => valid parameters, multiple sab, rel; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&sab=UBERON&rel=isa&rel=part_of" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "6. concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US%2CUBERON&rel=isa%2Cpart_of => valid parameters, multiple sab, rel; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US%2CUBERON&rel=isa%2Cpart_of" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: node_types/counts GET" | tee -a test.out
echo "SIGNATURE: /node_types/counts" | tee -a test.out
echo | tee -a test.out

echo "1. node_types/counts GET => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/counts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: node_types/<node_type>/counts GET" | tee -a test.out
echo "SIGNATURE: /node_types/<node_type>/counts" | tee -a test.out
echo | tee -a test.out
echo "1. node_types/Codez/counts GET => no match; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/Codez/counts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. node_types/Code/counts GET => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/Code/counts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out


#--------------------------------------------
echo "TESTS FOR: node_types/counts_by_sab GET" | tee -a test.out
echo "SIGNATURE: /node_types/counts_by_sab" | tee -a test.out

echo "1. node_types/counts_by_sab GET => blocked because of likely timeout; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/counts_by_sab?test=test" \
 --header "Accept: application/json" | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: node_types/<node_type>/counts_by_sab GET" | tee -a test.out
echo "SIGNATURE: /node_types/<node_type>/counts?sab=<SAB>" | tee -a test.out
echo "Parameters sab and rel can be %2C-delimited list or indidividual values."  | tee -a test.out
echo | tee -a test.out

echo "1. node_types/Codez/counts_by_sab?sab=SNOMEDCT_US GET => invalid parameter; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/Codez/counts_by_sab?sab=SNOMED_US" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. node_types/Code/counts_by_sab?sab=SNOMEDCT_US GET => valid, single sab; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/Code/counts_by_sab?sab=SNOMED_US" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "3. node_types/Code/counts_by_sab?sab=SNOMEDCT_US&sab=NCI GET => valid, multiple sab; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/Code/counts_by_sab?sab=SNOMEDCT_US&sab=NCI" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "4. node_types/Code/counts_by_sab?sab=SNOMEDCT_US%2CNCI GET => valid, list sab; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/Code/counts_by_sab?sab=SNOMEDCT_US%2CNCI" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: property_types GET" | tee -a test.out
echo "SIGNATURE: /property_types" | tee -a test.out
echo "1. property_types GET => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/property_types" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: relationship_types GET" | tee -a test.out
echo "SIGNATURE: /relationship_types" | tee -a test.out
echo "1. relationship_types GET => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/relationship_types" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out


#--------------------------------------------
echo "TESTS FOR: sabs/codes/counts GET" | tee -a test.out
echo "SIGNATURE: /sabs/codes/count?skip=<number>&limit=<number>" | tee -a test.out

echo "1. sabs/codes/counts?test=test => invalid parameter: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/codes/counts?test=test" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. sabs/codes/counts?skip=-1&limit=10 => negative skip value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/codes/counts?skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. sabs/codes/counts?skip=1&limit=-1 => negative limit value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/codes/counts?skip=1&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. sabs/codes/counts?skip=a&limit=10 => nonnumeric skip value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/codes/counts?skip=a&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. sabs/codes/counts?skip=1&limit=a => nonnumeric limit value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/codes/counts?skip=1&limit=a" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. sabs/codes/counts?skip=5&limit=10 => valid: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/codes/counts?skip=5&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out


#--------------------------------------------
echo "TESTS FOR: sabs/<sab>/codes/counts  GET" | tee -a test.out
echo "SIGNATURE: /sabs/<SAB>/codes/counts?skip=<number>&limit=<number>" | tee -a test.out
echo | tee -a test.out

echo "1. sabs/SNOMEDCT_US/codes/counts?test=test => invalid parameter: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/counts?test=test" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. sabs/SNOMEDCT_US/codes/counts?skip=-1&limit=10 => negative skip value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/counts?skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. sabs/SNOMEDCT_US/codes/counts?skip=1&limit=-1 => negative limit value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/counts?skip=0&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. sabs/SNOMEDCT_US/codes/counts?skip=a => nonnumeric skip value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/counts?skip=a&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. sabs/SNOMEDCT_US/codes/counts?skip=a => nonnumeric limit value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/counts?skip=0&limit=a" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. sabs/SNOMEDCT_USA/codes/counts?skip=0&limit=10 => invalid SAB: should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_USA/codes/counts?skip=0&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "5. sabs/SNOMEDCT_US/codes/counts?skip=0&limit=10 => valid: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/counts?skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: sabs/codes/details GET" | tee -a test.out
echo "SIGNATURE: /sabs/codes/details" | tee -a test.out
echo | tee -a test.out

echo "1. sabs/codes/details => blocked; return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/codes/details" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: sabs/<SAB>/codes/details GET" | tee -a test.out
echo "SIGNATURE: /sabs/<SAB>/codes/details?skip=<number>&limit=<number>"
echo | tee -a test.out

echo "1. sabs/SNOMEDCT_US/codes/details?test=test => invalid parameter: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/details?test=test" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. sabs/SNOMEDCT_US/codes/details?skip=-1&limit=10 => negative skip value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/details?skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. sabs/SNOMEDCT_US/codes/details?skip=1&limit=-1 => negative limit value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/details?skip=1&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. sabs/SNOMEDCT_US/codes/details?skip=a&limit=10 => nonnumeric skip value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/details?skip=a&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. sabs/SNOMEDCT_US/codes/details?skip=1&limit=a => nonnumeric limit value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/details?skip=1&limit=a" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. sabs/SNOMEDCT_USA/codes/details => invalid SAB: should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_USA/codes/details" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. sabs/SNOMEDCT_US/codes/details?skip=0&limit=10 => valid: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/codes/details?skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: sabs/term_types GET" | tee -a test.out
echo "SIGNATURE: /sabs/term_types" | tee -a test.out
echo | tee -a test.out

echo "1. sabs/term_types => blocked; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/term_types" \
 --header "Accept: application/json"  | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: sabs/<sab>/term_types GET" | tee -a test.out
echo "SIGNATURE: /sabs/<sab>term_types" | tee -a test.out
echo | tee -a test.out

echo "1. sabs/SNOMEDCT_USA/term_types => invalid sab; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_USA/term_types" \
 --header "Accept: application/json"  | tee -a test.out
echo | tee -a test.out

echo "2. sabs/SNOMEDCT_US/term_types => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/sabs/SNOMEDCT_US/term_types" \
 --header "Accept: application/json"  | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: semantics/semantic_types GET" | tee -a test.out
echo "SIGNATURE: /semantics/semantic_types?skip=<number>&limit=<number>" | tee -a test.out
echo | tee -a test.out

echo "1. semantics/semantic_types?test=test => invalid parameter; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types?test=test" \
 --header "Accept: application/json"  | tee -a test.out
echo | tee -a test.out

echo "2. semantics/semantic_types?skip=-1&limit=10 => negative skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types?skip=-1&limit=10" \
 --header "Accept: application/json"  | tee -a test.out
echo | tee -a test.out

echo "3. semantics/semantic_types?skip=1&limit=-1 => negative limit; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types?skip=1&limit=-1" \
 --header "Accept: application/json"  | tee -a test.out
echo | tee -a test.out

echo "4. semantics/semantic_types?skip=a&limit=10 => non-numeric skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types?skip=a&limit=10" \
 --header "Accept: application/json"  | tee -a test.out
echo | tee -a test.out

echo "5. semantics/semantic_types?skip=1&limit=a => non-numeric limit; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types?skip=1&limit=a" \
 --header "Accept: application/json"  | tee -a test.out
echo | tee -a test.out

echo "6. semantics/semantic_types => should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types?skip=1&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: semantics/<semantic_types>/semantic_types GET" | tee -a test.out
echo "SIGNATURE: /semantics/<semantic_type>/semantic_types?skip=<number>&limit=<number>" | tee -a test.out
echo | tee -a test.out

echo "1. semantics/Anatomical%20Structure/semantic_types?skip=1&limit=10&test=test => invalid parameter; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_types?skip=1&limit=10&test=test" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "1. semantics/Anatomical%20Structure/semantic_types?skip=-1&limit=10 => negative skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_types?skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. semantics/Anatomical%20Structure/semantic_types?skip=1&limit=-1 => negative limit; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_types?skip=1&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. semantics/Anatomical%20Structure/semantic_types?skip=a&limit=10 => non-numeric skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_types?skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. semantics/Anatomical%20Structure/semantic_types?skip=1&limit=a => non-numeric limit; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_types?skip=1&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. semantics/Anatomical%20Structurez/semantic_types?skip=1&limit=10 => invalid semantic type; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structurez/semantic_types?skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. semantics/Anatomical%20Structure/semantic_types?&skip=1&limit=10 => valid semantic type; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_types?&skip=1&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: semantics/<semantic_type>/subtypes GET" | tee -a test.out
echo "SIGNATURE: /semantics/<semantic_type>/subtypes?skip=<number>&limit=<number>" | tee -a test.out
echo | tee -a test.out

echo "1. semantics/Anatomical%20Structure/subtypes?test=test => invalid parameter; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/subtypes?test=test" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. semantics/Anatomical%20Structure/subtypes?skip=-1&limit=10 => negative skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/subtypes?skip=-1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. semantics/Anatomical%20Structure/subtypes?skip=1&limit=-1 => negative limit; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_subtypes?skip=1&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. semantics/Anatomical%20Structure/subtypes?skip=a&limit=10 => non-numeric skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_subtypes?skip=a&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "5. semantics/Anatomical%20Structure/subtypes?skip=1&limit=a => non-numeric limit; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_subtypes?skip=1&limit=a" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "6. semantics/Anatomical%20Structurez/subtypes?skip=1&limit=10 => invalid semantic type; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structurez/semantic_subtypes?skip=1&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo | tee -a test.out
echo "7. semantics/Anatomical%20Structure/subtypes?skip=1&limit=10 => valid parameters; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/Anatomical%20Structure/semantic_subtypes?skip=1&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: terms/<term_id>/codes GET" | tee -a test.out
echo "SIGNATURE: /terms/<term_id>/codes" | tee -a test.out
echo | tee -a test.out

echo "1. terms/Breast%20cancerz/codes => no match; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancerz/codes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. terms/codes/Breast%20cancer GET with match: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/codes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: terms/<concept_id>/concepts GET" | tee -a test.out
echo "SIGNATURE: /terms/<concept_id>/concepts"
echo "1. terms/concepts/Breast%20cancerz GET with no match; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancerz/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. terms/Breast%20cancer/concepts GET with match; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out