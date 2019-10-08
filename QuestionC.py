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
import os


class LRU(object):
    num_slots = 1
    time_to_expiry = 300
    region = None
    region_list = []
    dataset = []

    def __init__(self, region, num_slots=1, time_to_expiry=300, region_list=[]):
        self.num_slots = num_slots
        self.time_to_expiry = time_to_expiry
        self.region = region
        self.dataset = []

        if not os.path.exists(self.region):
            os.makedirs(self.region)

        self.region_list = region_list
        self.synchronize()

    def write(self, data_id, data, local_region=True):
        # Remove expired cached data
        for i in range(len(self.dataset)):
            # Check if expired, if reached expired data, if reach data thats not expired, break cause rest of data
            # isn't expired
            if self.dataset[i][0] + self.time_to_expiry < time.time():
                del self.dataset[i]
            else:
                break

        # if there is room left over, add new data else remove oldest data and add new data
        if len(self.dataset) < self.num_slots:
            self.dataset.append([time.time(), data_id, data])
        else:
            del self.dataset[0]
            self.dataset.append([time.time(), data_id, data])

        file = open(self.region + '/' + str(data_id) + '.txt', 'w')
        file.write(str(data))

        # Write to other regions
        if local_region:
            for region in self.region_list:
                region.write(data_id, data, local_region=False)

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

        # Look for file in local region
        # if os.path.exists(self.region + '/' + str(data_id) + '.txt'):
        #     file = open(self.region + '/' + str(data_id) + '.txt', 'r')
        #     data = file.read()
        #
        #     # Add to cache
        #     if len(self.dataset) < self.num_slots:
        #         self.dataset.append([time.time(), data_id, data])
        #     else:
        #         del self.dataset[0]
        #         self.dataset.append([time.time(), data_id, data])
        #
        #     return data

        # Look in the databases of all the other regions
        for region in self.region_list:
            if os.path.exists(region.region + '/' + str(data_id) + '.txt'):
                file = open(region.region + '/' + str(data_id) + '.txt', 'r')
                data = file.read()

                # Add to cache
                if len(self.dataset) < self.num_slots:
                    self.dataset.append([time.time(), data_id, data])
                else:
                    del self.dataset[0]
                    self.dataset.append([time.time(), data_id, data])

                return data

        return print('File not found!')

    def add_new_region(self, region):
        temp_region_list = self.region_list.copy()
        temp_region_list.append(self)
        new_region = LRU(region=region, num_slots=self.num_slots, time_to_expiry=self.time_to_expiry,
                         region_list=temp_region_list)

        for other_region in self.region_list.copy():
            other_region.add_to_region_list(new_region)

        self.region_list.append(new_region)

        return new_region

    def add_to_region_list(self, region):
        self.region_list.append(region)

    def synchronize(self):
        for region in self.region_list:
            for file_name in os.path(region.region): # TODO: Figure out how to do this
                file = open(self.region.region + '/' + file_name, 'r')
                data = file.read()
            file.write(str(data))

# TODO: After crash recovery, literally just del and reinstantiate with same name

geo_lru = LRU(region='North America', num_slots=10, time_to_expiry=1)

geo_lru.write(100, 0)

eu_lru = geo_lru.add_new_region('Europe')

la_lru = geo_lru.add_new_region('Latin America')

af_lru = geo_lru.add_new_region('Africa')


for j in range(0, 11):
    time.sleep(0.3)
    geo_lru.write(j, j*10 + 5)

read_data = geo_lru.read(0)

hi = 1