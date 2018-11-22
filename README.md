# Helpers for data loaded from http://stat.gibdd.ru

| Before             |  After |
:-------------------------:|:-------------------------:
![](https://github.com/grisme/dtp_stat_helpers/blob/master/pictures/before.jpg)  |  ![](https://github.com/grisme/dtp_stat_helpers/blob/master/pictures/after.jpg)
![](https://github.com/grisme/dtp_stat_helpers/blob/master/pictures/before1.jpg)  |  ![](https://github.com/grisme/dtp_stat_helpers/blob/master/pictures/after1.jpg)

`address_coordinate_cleaning.py` - replace coordinates of accident by address coordinates (with help of Yandex Geocoder).

`addresses_to_street_projection.py` - project coordinates of address to the nearest street.

### Dependencies
For `address_coordinate_cleaning.py`:
  * pandas
  * yandex_geocoder
  * tqdm
  
For `addresses_to_street_projection.py`:
  * pandas
  * numpy
  * osmnx
  * networkx
  * shapely
  * tqdm
  
### Running
Fix fields in scripts (`csv_path` and `city`) for running.

### Known problems
* `addresses_to_street_projection.py` failed with error `Connection refused` - turn on VPN for loading of graph of streets.
