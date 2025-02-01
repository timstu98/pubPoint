import requests

class ApiClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def call_api(self, endpoint, method, headers, data):
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}
        response = requests.request(method, url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            try:
                print(f"Error: {response.json()['error']['message']}")
            except:
                print(f"Error: status-code:{response.status_code}, reason:{response.reason}")
                print(response.text)
            return None
        
    def get(self, endpoint, headers=None, data=None):
        return self.call_api(endpoint, "GET", headers, data)
    
    def post(self, endpoint, headers=None, data=None):
        return self.call_api(endpoint, "POST", headers, data)
    
    def put(self, endpoint, headers=None, data=None):
        return self.call_api(endpoint, "PUT", headers, data)
    
    def delete(self, endpoint, headers=None, data=None):
        return self.call_api(endpoint, "DELETE", headers, data)
