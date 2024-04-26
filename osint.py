import os
import json
import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests

# Your API keys
reddit_client_id = '4z_KwqzRkB6dONXu-8N7nQ'
reddit_client_secret = 'J7ig8Ox1AKNdEYNiBUI_f-IbXAAdIw'
newsapi_key = 'b7d3b7e0a24d43c499f3f1e8571ac42f'
gnews_key = 'a1e61ddfc3ec12127cc45a777c2f7b1d'
bing_search_api_key = '52b11238dfcc497bbc768d260a0349f6'

# The APIs
apis = {
    'Reddit': {
        'url': 'https://www.reddit.com/search.json',
        'auth': requests.auth.HTTPBasicAuth(reddit_client_id, reddit_client_secret),
        'headers': {'User-Agent': 'SearchReddit/0.1'},
        'params': {}
    },
    'NewsAPI': {
        'url': 'https://newsapi.org/v2/everything',
        'params': {'apiKey': newsapi_key}
    },
    'GNews': {
        'url': 'https://gnews.io/api/v4/search',
        'params': {'token': gnews_key}
    },
    'Bing': {
        'url': 'https://api.bing.microsoft.com/v7.0/search',
        'headers': {'Ocp-Apim-Subscription-Key': bing_search_api_key},
        'params': {}
    }
}

def search():
    keyword = keyword_entry.get()
    api_name = api_combobox.get()
    api = apis[api_name]
    api['params']['q'] = keyword
    response = requests.get(api['url'], headers=api.get('headers', {}), params=api['params'])
    data = response.json()
    result_text.insert(tk.END, json.dumps(data, indent=4, sort_keys=True))
    df = pd.json_normalize(data)
    df.to_csv(f'{api_name}_search_results.csv')

# Create the main window
root = tk.Tk()
root.title("API Search Engine")

# Create a 'keyword' label and entry
keyword_label = tk.Label(root, text="Keyword:")
keyword_label.grid(row=0, column=0, sticky="w")
keyword_entry = tk.Entry(root)
keyword_entry.grid(row=0, column=1)

# Create an 'API' label and combobox
api_label = tk.Label(root, text="API:")
api_label.grid(row=1, column=0, sticky="w")
api_combobox = ttk.Combobox(root, values=list(apis.keys()))
api_combobox.grid(row=1, column=1)

# Create a 'search' button
search_button = tk.Button(root, text="Search", command=search)
search_button.grid(row=2, column=0, columnspan=2)

# Create a text widget to display the results
result_text = tk.Text(root)
result_text.grid(row=3, column=0, columnspan=2)

# Start the main loop
root.mainloop()



