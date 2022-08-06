import urllib
import requests
def CheckStream(HostRadioTech: str,mountpoint: str) -> bool:
    try:
        url = "{}{}".format(HostRadioTech,mountpoint)
        #print("check links {}".format(url))
        with requests.get(url, stream=True) as response:
            try:
                response.raise_for_status()
                #print("{} streaming".format(mountpoint))
                return True
            except requests.exceptions.HTTPError:
                return False
    except requests.exceptions.ConnectionError:
        return False