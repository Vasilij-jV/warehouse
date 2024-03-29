# -*- config: utf8 -*-


from multiprocessing import Process, Queue
import multiprocessing as mp


class WarehouseManager:

    def __init__(self, manager_dict):
        self.data = manager_dict

    def process_request(self, request, data):
        if request[0] in data and request[1] == 'receipt':
            data[request[0]] += request[2]
        elif request[0] in data and request[1] == 'shipment' and request[2] > 0:
            data[request[0]] -= request[2]
        else:
            data[request[0]] = request[2]

    def run(self, list_request):
        list_process_request = []
        for one_request in list_request:
            obj_request = Process(target=self.process_request,
                                  kwargs=dict(request=one_request, data=self.data, ))
            list_process_request.append(obj_request)
        for one_request_start in list_process_request:
            one_request_start.start()
        for one_request_join in list_process_request:
            one_request_join.join()


if __name__ == '__main__':
    with mp.Manager() as manager:
        my_dict = manager.dict()
        requests = [
            ("product1", "receipt", 100),
            ("product2", "receipt", 150),
            ("product1", "shipment", 30),
            ("product3", "receipt", 200),
            ("product2", "shipment", 50),
            ("product1", "receipt", 150),
            ("product2", "receipt", 350),
            ("product1", "shipment", 30),
            ("product3", "receipt", 200),
            ("product2", "shipment", 50)
        ]
        warehouse_manager = WarehouseManager(manager_dict=my_dict)
        warehouse_manager.run(list_request=requests)
        print(warehouse_manager.data)
