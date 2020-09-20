import sys
import os
import sqlite3
import json
from datetime import datetime
import ftfy


def activate_hyperlinks(post):

    post_length = len(post)
    post_slice = post
    slice_length = post_length
    i = 0
    url_count = 0

    while i < post_length:
        url = ""
        http = post_slice.find("http")

        if http == -1:
            break

        for i in range(http, slice_length):
            url += post_slice[i]
            if i == slice_length - 1:
                break
            if post_slice[i + 1] == " ":
                break

        post = post.replace(url, "<a href='" + url + "'>" + url + "</a>")
        url_count += 1

        post_slice = post_slice[slice(i + 1, post_length)]
        slice_length = len(post_slice)

    return(post, url_count)


def clean_nametags(post):

    post_length = len(post)
    post_slice = post
    slice_length = post_length
    i = 0
    colon_count = 0

    while i < post_length:
        tagged_name = ""
        nametag = post_slice.find("@[")

        if nametag == -1:
            break

        for i in range(nametag, slice_length):
            tagged_name += post_slice[i]
            if i == slice_length - 1:
                break
            if post_slice[i + 1] == ":":
                colon_count += 1
                if colon_count == 2:
                    tagged_name += post_slice[i + 1]
                    break

        post = post.replace(tagged_name, "")

        post_slice = post_slice[slice(i + 2, post_length)]
        name_end = post_slice.find("]")

        name = post_slice[slice(0, name_end)]

        post = post.replace(
            name + "]", "<span class='name'>" + name + "</span>")

        post_slice = post_slice[slice(name_end + 1, post_length)]
        slice_length = len(post_slice)
        colon_count = 0

    return(post)
