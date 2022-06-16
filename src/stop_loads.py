from drivers.Load.Shelly import ShellyLoad

loads = [
    ShellyLoad('192.168.100.131'),
    ShellyLoad('192.168.100.132'),
]

if __name__ == '__main__':
    for i, load in enumerate(loads):
        print(f'Load{i} status: {load.get_status()} \n setting it off')
        load.set_status(False)