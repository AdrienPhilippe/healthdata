#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

structure = {
    "01-info":{
        "version": 1,
        "collection_name": "projet",
        "collection_URI": "https://www.gaalactic.fr/~menchit_SEV5204/ws/projet",
        "title": "Project Web Service",
        "host": "www.gaalactic.fr",
        "description": "App allowing doctors to monitor patients.",
        "base_path": "/~menchit_SEV5204/ws",
        "more_info": "https://www.gaalactic.fr/~menchit_SEV5204/ws/doc.json"
    },
    "02-methods":{
        "POST": "yes",
        "DELETE": "yes",
        "PUT": "yes",
        "GET": "yes"
    },
    "03-headers":{
        "consume":{
            "Content type": ["application/x-www-form-urlencoded"],
            "Accept": ["application/json"],
            "X-Auth": ["mailadresse:password"]
        },
        "produce":{
            "Content type": ["application/json"]
        }
    }
}

print("Content-type: application/json\n")
print(json.dumps(structure, indent=1))
