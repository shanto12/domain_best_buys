from base64 import b64decode
import requests
from bs4 import BeautifulSoup
import re
import pandas
from multiprocessing import Process, Pool, Event, Value, Manager

def find_proxies_nova():
    proxy_list_url = "https://www.proxynova.com/proxy-server-list/"
    print(f"Trying proxies from nova: {proxy_list_url}")
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    # uptime = 80
    # speed = 1000

    r = requests.get(proxy_list_url)
    table = pandas.read_html(r.text)
    proxy_df = table[0]
    proxy_df.dropna(inplace=True)
    proxies_list = []
    try:
        for index, row in proxy_df.iterrows():
            proxy_speed, proxy_uptime, proxy_ip, proxy_port = [row.get(x, None) for x in ['Proxy Speed', 'Uptime', 'Proxy IP', 'Proxy Port']]
            # proxy_speed, proxy_uptime, proxy_ip, proxy_port = [x if x != 'nan' else None for x in [proxy_speed, proxy_uptime, proxy_ip, proxy_port]]
            print(f"{index}: Checking IP, Port: {proxy_ip}, {proxy_port}")
            if all([proxy_speed, proxy_uptime, proxy_ip, proxy_port]) and isinstance(proxy_speed, str) and isinstance(proxy_uptime, str):
                proxy_speed, proxy_uptime = proxy_speed.split()[0], proxy_uptime.split("%")[0]
                # if scraped_speed.isnumeric() and int(scraped_speed)<speed and scraped_uptime.isnumeric() and int(scraped_uptime)>uptime:
                proxy_ip = pattern.search(proxy_ip)[0]
                proxies = {"https": f"https://{proxy_ip}:{proxy_port}"}
                proxies_list.append(proxies)
    except Exception as e:
        print(e)

    return proxies_list

def find_proxies_spys():
    proxy_list_url = "https://free-proxy-list.net/"
    print(f"Trying proxies from spys: {proxy_list_url}")

    r = requests.get(proxy_list_url)
    table = pandas.read_html(r.text)
    proxy_df = table[0]
    proxy_df.dropna(inplace=True)
    proxies_list = []
    for index, row in proxy_df.iterrows():
        proxy_ip, proxy_port, proxy_country, proxy_https = [row.get(x, None) for x in ['IP Address', 'Port', 'Country', 'Https']]
        print(f"{index}: Checking IP, Port: {proxy_ip}, {proxy_port}")
        if all([proxy_ip, proxy_port, proxy_country, proxy_https]):
            proxy_port, proxy_protocol = int(proxy_port), "https" if proxy_https == "yes" else "http"
            proxies = {f"{proxy_protocol}": f"{proxy_protocol}://{proxy_ip}:{proxy_port}"}
            proxies_list.append(proxies)

    return proxies_list

def find_proxies_free_proxy_cz():
    url = proxy_list_url = "http://free-proxy.cz/en/proxylist/country/all/https/ping/all/"
    print(f"Trying proxies from free proxy cz: {proxy_list_url}")

    def decode_ip(x):
        result = re.search('decode\("(.*)"\)', x)
        if result:
            ip_encoded_string = result.group(1)
            decoded_ip = b64decode(ip_encoded_string).decode('ascii')
        else:
            print(f"Unable to decode for strging: {x}")
            decoded_ip = None

        return decoded_ip

    page = 1
    LIMIT = 2
    df_list = []
    while 1 and page<LIMIT:
        try:
            print(f"Getting page: {url}")
            r = requests.get(url)
            table = pandas.read_html(r.text)
            proxy_df = table[1]
            proxy_df['IP address'] = proxy_df['IP address'].apply(lambda x: decode_ip(x))

            df_list.append(proxy_df)
        except Exception as e:
            print(f"Breaking. Exception: {e}")
            break
        else:
            page += 1
            url = proxy_list_url + str(page)

    combined_proxy_df = pandas.concat(df_list)
    print(f"DataFrame shape before dropna and drop duplicates: {combined_proxy_df.shape}")
    combined_proxy_df.dropna(inplace=True)
    combined_proxy_df.drop_duplicates(inplace=True)
    print(f"DataFrame shape after dropna and drop duplicates: {combined_proxy_df.shape}")

    proxies_list = []
    for index, row in combined_proxy_df.iterrows():
        proxy_ip, proxy_port, proxy_country, proxy_protocol = [row.get(x, None) for x in ['IP address', 'Port', 'Country', 'Protocol']]
        print(f"{index}: Checking IP, Port: {proxy_ip}, {proxy_port}")
        if all([proxy_ip, proxy_port, proxy_country, proxy_protocol]) and proxy_protocol.lower() != "http":
            proxy_port = int(proxy_port)
            proxies = {"https": f"{proxy_protocol}://{proxy_ip}:{proxy_port}"}
            proxies_list.append(proxies)

    return proxies_list

def proxy_test(proxies, event, return_dict):
    global PROXIES

    url = "https://www.myip.com/"
    print(f"Testing: {proxies}")
    try:
        ip_with_proxy = get_my_ip(url, proxies)
        print(f'IP with proxy:{ip_with_proxy}')

        ip_without_proxy = get_my_ip(url)
        print(f'IP without proxy:{ip_without_proxy}')

        if ip_with_proxy != ip_without_proxy:
            PROXIES = proxies
            return_dict["value"] = proxies
            event.set()
            print(f"IP test successful. PROXIES set to {PROXIES}")
            return True
        else:
            print("IP test failed")
            return False
    except Exception as e:
        print(e)
        return False

def find_proxies():
    final_proxies_list = []
    event = Event()
    manager = Manager()
    return_dict = manager.dict()

    for find_proxies_method in [find_proxies_spys, find_proxies_nova]:
        if proxies:=find_proxies_method():
            final_proxies_list.extend(proxies)

    process_list = [Process(target=proxy_test, args=(proxies, event, return_dict), daemon=True) for proxies in final_proxies_list]
    print(f"Starting Processes. Got {len(process_list)} of processes")
    for index, process in enumerate(process_list):
        if not event.is_set():
            process.start()
        else:
            print(f"Found Proxies: {return_dict['value']}")
            break
    else:
        print(f"All processes started")
        print("Executing else")
        while not event.is_set():
            # print(f"Proxies is still not set")
            continue
        print(f"Found Proxies: {return_dict['value']}")
        for process in process_list:
            process.terminate()
        print("All processes terminated")
        for process in process_list:
            process.join()
        print("All processes joined")

        return return_dict['value']


def get_my_ip(url, proxies=None):
    r = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(r.content, features="lxml")
    els = soup.find_all(id="ip")
    ip = els[0].text

    print(f'Response Time: {r.elapsed}')

    return ip



if __name__ == "__main__":
    proxies = find_proxies()
    print(f"Final proxies: {proxies}")