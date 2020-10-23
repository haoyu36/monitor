# -*- coding: utf-8 -*-
'''
通过 HTTP API 获取 Prometheus 监控数据，保存为 json 文件
目前只获取 CPU 和内存的平均值和峰值
'''


import sys
import time
import json
import requests

import numpy as np
from loguru import logger


class Config:
    prometheus_url = 'http://192.168.1.98:9090'

    # 打压机 cpu、内存使用百分比
    pressure_node_cpu_promql = '(1-((sum(increase(node_cpu_seconds_total{mode="idle",job="pressure-node"}[2m])) by (instance)) / (sum(increase(node_cpu_seconds_total[2m])) by (instance)))) * 100'
    pressure_node_mem_promql = 'instance:node_memory_utilisation:ratio{job="pressure-node"}'

    # 压测集群 cpu、内存使用百分比
    cluster_node_cpu_promql = '(1-((sum(increase(node_cpu_seconds_total{mode="idle",job="node-exporter"}[2m])) by (instance)) / (sum(increase(node_cpu_seconds_total[2m])) by (instance)))) * 100'
    cluster_node_mem_promql = 'instance:node_memory_utilisation:ratio{job="node-exporter"}'

    # k8s 集群 default 命名空间 pod 的cpu、内存
    cluster_pod_cpu_promql = 'node_namespace_pod_container:container_cpu_usage_seconds_total:sum_rate{namespace="default",pod=~"tl.*(service|gateway).*"}'
    cluster_pod_mem_promql = 'container_memory_working_set_bytes{namespace="default",pod=~"tl.*(service|gateway).*"}'


class RequestsError(Exception):
    pass


def get_response(url, num_retries=2, timeout=1000, **kwargs):
    '''
    请求一个 url 并返回成功时的响应，如果失败则重复请求 3 次
    :param num_retries: 请求的 url
    :param num_retries: 限定的重试次数
    '''
    try:
        r = requests.get(url, timeout=timeout, **kwargs)
        if r.status_code == 200:
            logger.info(f'>>>>>> 请求成功: {url}')
            return r
        else:
            logger.error('请求失败，正在尝试重试，{r}')
            raise RequestsError
    except:
        if num_retries > 0:
            logger.error('请求错误，5 秒后重新请求')
            time.sleep(5)
            return get_response(url, num_retries - 1)
        else:
            logger.error('请求 {} 重复次数用完，请检测后重试')
            sys.exit(-1)


def get_monitor_data(promql, job_name, start_time, end_time, step_time=15):
    '''
    获取监控的数据
    :param promql: 查询 prometheus 数据的语句
    :param job_name: 查询 prometheus 数据的名字
    '''
    url = f'{Config.prometheus_url}/api/v1/query_range?query={promql}&start={start_time}&end={end_time}&step={step_time}'
    res = get_response(url)
    data = res.json()
    logger.info(f'{promql}请求状态 {data["status"]}')
    monitor_data = []
    for item in data['data']['result']:
        value_lst = [float(i[1]) for i in item['values']]
        if job_name == 'pod':
            instance = item['metric'][job_name].rsplit('-', 2)[0]
        else:
            instance = item['metric'][job_name]
        monitor_data.append({
            'instance': instance,
            'max_value': np.max(value_lst),
            'avg_vaule': np.mean(value_lst),
        })
    return monitor_data


def main(start_time, end_time, step_time=15):
    '''
    主函数，生成数据并写入 json 文件
    :param start_time: 获取监控数据开始的时间，时间戳
    :param end_time: 获取监控数据结束的时间，时间戳
    :param step_time: 每隔多少秒抓取数据，默认 15s
    '''
    data = {
        'CPU': {
            'pressure-node': get_monitor_data(Config.pressure_node_cpu_promql, 'instance', start_time, end_time, step_time),
            'cluster-node': get_monitor_data(Config.cluster_node_cpu_promql, 'instance', start_time, end_time, step_time),
            'cluster-pod': get_monitor_data(Config.cluster_pod_cpu_promql, 'container', start_time, end_time, step_time),
        },
        'MEM': {
            'pressure-node': get_monitor_data(Config.pressure_node_mem_promql, 'instance', start_time, end_time, step_time),
            'cluster-node': get_monitor_data(Config.cluster_node_mem_promql, 'instance', start_time, end_time, step_time),
            'cluster-pod': get_monitor_data(Config.cluster_pod_mem_promql, 'pod', start_time, end_time, step_time),
        },
    }
    with open('record.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    main(1587449530, 1587499530)
