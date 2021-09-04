#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:24:51 2020

@author: youngsuk
"""
import pandas as pd


def bollinger_band(s: pd.Series, w=20, multiplier=2):
    kw={}
    kw[s.name] = s
    kw['MA'] = s.rolling(window=w).mean()
    kw['STD'] = s.rolling(window=w).std()
    kw['BU'] = kw['MA'] + multiplier*kw['STD']
    kw['BD'] = kw['MA'] - multiplier*kw['STD']
    
    df = pd.DataFrame(kw)
    return df

def top_bottom(s: pd.Series, w = 120):
    
    kw={}
    kw[s.name] = s
    kw['H'] = s.rolling(window=w).max()
    kw['L'] = s.rolling(window=w).min()
    kw['FH'] = (s - kw['H'])/kw['H']
    kw['FL'] = (s - kw['L'])/kw['L']
    
    df = pd.DataFrame(kw)
    return df

