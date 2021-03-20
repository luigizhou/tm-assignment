# README

## How To build

Using pip, install all the requirements by running the following command

```
pip3 install requirements.txt
```

The small cli program comes with some help text:
```
usage: cli.py [-h]
              (--get-running-services | --get-averages | --flag-services | --track-service TRACK_SERVICE)
              address

positional arguments:
  address               address of the cpx api (i.e. http://localhost:port )

optional arguments:
  -h, --help            show this help message and exit
  --get-running-services
                        challenge1, print running services
  --get-averages        challenge2, print averages for running services
  --flag-services       challenge3, print services that have less than 2
                        instance running
  --track-service TRACK_SERVICE
                        challenge4, track cpu and mem of a specificed service
```

## Discussion

**Future Improvement**

* Add Error Handling for multiple scenario where the cli tool may fail (i.e. cpx failure)
* Might make sense to add some caching if running multiple operations within seconds

