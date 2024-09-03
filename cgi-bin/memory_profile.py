#!/usr/bin/env python3

import cgi
import cgitb
import os
import psutil

cgitb.enable()  # Enable CGI traceback for debugging

print("Content-Type: text/html\n")

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        return f"{func.__name__}: consumed memory: {mem_after - mem_before:,} bytes"
    return wrapper

@profile
def func():
    x = [1] * (10 ** 7)  # Adjusted size for demonstration purposes
    y = [2] * (10 ** 7)  # Adjusted size for demonstration purposes
    del x
    return y

result = func()
print(f"<html><body><h1>{result}</h1></body></html>")

