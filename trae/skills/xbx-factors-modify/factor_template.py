"""
[AI-GENERATED] 本文件由 AI 辅助创建，非框架原始文件。
创建目的：作为 COIN（币圈）因子模板，用于 position-mgmt_v2.1.0/factors 的 signal 接口。
"""
import pandas as pd
import numpy as np

FA_INTRO = {
    "因子说明": """ 
    [因子名称]：[因子的详细技术说明，解释因子如何计算]
    因子值越大：[在币圈里通常代表什么]
    因子值越小：[在币圈里通常代表什么]
    """,
    "选币案例": ("MyFactor", False, 24, 1.0),
}

extra_data_dict = {}


def signal(*args):
    df = args[0]
    param = args[1]
    factor_name = args[2]
    n = int(param) if param else 24
    df[factor_name] = df["close"].pct_change(n)
    return df


def signal_multi_params(df: pd.DataFrame, param_list) -> dict:
    ret = {}
    for param in param_list:
        n = int(param)
        ret[str(param)] = df["close"].pct_change(n)
    return ret
