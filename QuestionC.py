# At Ormuco, we want to optimize every bits of software we write. Your goal is to write a new
# library that can be integrated to the Ormuco stack. Dealing with network issues everyday,
# latency is our biggest problem. Thus, your challenge is to write a new Geo Distributed LRU
# (Least Recently Used) cache with time expiration. This library will be used extensively by
# many of our services so it needs to meet the following criteria:
#
#     1 - Simplicity. Integration needs to be dead simple.
#     2 - Resilient to network failures or crashes.
#     3 - Near real time replication of data across Geolocation. Writes need to be in real time.
#     4 - Data consistency across regions
#     5 - Locality of reference, data should almost always be available from the closest region
#     6 - Flexible Schema
#     7 - Cache can expire
#
# As a hint, we are not looking for quantity, but rather quality, maintainability, scalability,
# testability and a code that you can be proud of.
import time


class LRU(object):
    num_slots = 1
    time_to_expiry = 300
    region = None
    region_list = []
    dataset = []

    def __init__(self, region, num_slots=1, time_to_expiry=300):
        self.num_slots = num_slots
        self.time_to_expiry = time_to_expiry
        self.region = region

    def write(self, data_id, data):
        # Remove expired cached data
        for i in range(len(self.dataset)):
            # Check if expired, if reached expired data, if reach data thats not expired, break cause rest of data
            # isn't expired
            if self.dataset[i][0] + self.time_to_expiry < time.time():
                del self.dataset[i]
            else:
                break

        if len(self.dataset) < self.num_slots:
            self.dataset.append([time.time(), data_id, data])
        else:
            # TODO: Start to replace in LRU fashion, unless there are expired places to use first
            pass

    def read(self, data_id):
        # Look for data in local cache, starting at most recently used
        for i in range(len(self.dataset)):
            index = len(self.dataset)-1-i

            # Check if expired, if reached expired data, break because rest of data is also expired
            if self.dataset[index][0] + self.time_to_expiry < time.time():
                break

            # if data is read, refresh the time and return it to user
            if data_id == self.dataset[index][1]:
                temp = self.dataset[index]
                temp[0] = time.time()

                # delete old entry before appending new one to not exceed memory limit
                del self.dataset[index]
                self.dataset.append(temp)

                return temp[2]

        # TODO: Else search other regions

        pass

    def add_new_region(self, region):
        # TODO: Figure out how I want to connect regions such that they all know that each other exist
        #  so that they can ensure data consistency across the regions
        # LRU(region='North America', num_slots=self.num_slots, time_to_expiry=self.time_to_expiry)
        pass

    def synchronize(self):
        pass


geo_lru = LRU(region='North America', num_slots=10, time_to_expiry=1)

for j in range(0, 11):
    time.sleep(0.3)
    geo_lru.write(j, j*10 + 5)

read_data = geo_lru.read(0)

hi = 1