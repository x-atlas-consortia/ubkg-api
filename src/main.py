from ubkg_api.app import UbkgAPI

config = {
          'SERVER': 'bolt://34.234.131.112:7688',
          'USERNAME': 'neo4j',
          'PASSWORD': 'HappyG0at'
    }

# For local standalone (non-docker) development/testing
if __name__ == "__main__":
    UbkgAPI(config).app.run(host='0.0.0.0', debug=True, port=8080)
